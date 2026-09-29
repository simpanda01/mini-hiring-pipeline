from datetime import datetime, timedelta
from difflib import SequenceMatcher
import re

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Candidate, StageHistory
from schemas import CandidateCreate, CandidateResponse, StageMove


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Hiring Pipeline")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


STAGES = [
    "Applied",
    "Screening",
    "Interview",
    "Offer",
    "Hired",
]


@app.get("/")
def root():
    return {"message": "Mini Hiring Pipeline API is running"}


@app.get("/candidates")
def get_candidates(db: Session = Depends(get_db)):
    return db.query(Candidate).all()


@app.post("/candidates", response_model=CandidateResponse)
def create_candidate(
    candidate: CandidateCreate,
    db: Session = Depends(get_db)
):
    new_candidate = Candidate(
        name=candidate.name,
        email=candidate.email,
        current_stage="Applied"
    )

    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)

    history = StageHistory(
        candidate_id=new_candidate.id,
        from_stage=None,
        to_stage="Applied"
    )

    db.add(history)
    db.commit()

    return new_candidate


@app.post("/candidates/{candidate_id}/move")
def move_candidate(
    candidate_id: int,
    move: StageMove,
    db: Session = Depends(get_db)
):
    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).first()

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    current_stage = candidate.current_stage
    new_stage = move.to_stage

    if current_stage in ["Hired", "Rejected"]:
        raise HTTPException(
            status_code=400,
            detail=f"Candidate is already {current_stage}."
        )

    # Rejection can happen before hiring
    if new_stage == "Rejected":
        candidate.current_stage = "Rejected"

        history = StageHistory(
            candidate_id=candidate.id,
            from_stage=current_stage,
            to_stage="Rejected"
        )

        db.add(history)
        db.commit()

        return {"message": "Candidate rejected"}

    if new_stage not in STAGES:
        raise HTTPException(
            status_code=400,
            detail="Invalid stage"
        )

    current_index = STAGES.index(current_stage)
    new_index = STAGES.index(new_stage)

    # Only allow one step forward
    if new_index != current_index + 1:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid transition: {current_stage} → {new_stage}. "
                "Only one stage forward is allowed."
            )
        )

    candidate.current_stage = new_stage

    history = StageHistory(
        candidate_id=candidate.id,
        from_stage=current_stage,
        to_stage=new_stage
    )

    db.add(history)
    db.commit()
    db.refresh(candidate)

    return {
        "message": f"Candidate moved to {new_stage}",
        "candidate": candidate
    }


@app.get("/candidates/{candidate_id}")
def get_candidate(
    candidate_id: int,
    db: Session = Depends(get_db)
):
    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).first()

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    history = db.query(StageHistory).filter(
        StageHistory.candidate_id == candidate_id
    ).order_by(StageHistory.timestamp.asc()).all()

    return {
        "candidate": candidate,
        "history": history
    }


# ---------------- SEARCH ----------------


def normalize(text):
    return re.sub(r"[^a-z0-9 ]", "", text.lower()).strip()


def name_similarity(query, name):
    query = normalize(query)
    name = normalize(name)

    # Exact match
    if query == name:
        return 1.0

    # Direct substring match
    if query in name or name in query:
        return 0.95

    query_parts = query.split()
    name_parts = name.split()

    # Compare individual name parts.
    # This prevents unrelated names such as
    # "Riya Sen" from matching "Priya Sharam".
    if len(query_parts) == len(name_parts):
        part_scores = [
            SequenceMatcher(None, q, n).ratio()
            for q, n in zip(query_parts, name_parts)
        ]

        return sum(part_scores) / len(part_scores)

    # Fallback full-string similarity
    return SequenceMatcher(None, query, name).ratio()


def latest_stage_time(history):
    if not history:
        return None

    return max(item.timestamp for item in history)


@app.get("/search")
def search_candidates(
    q: str,
    db: Session = Depends(get_db)
):
    query = normalize(q)

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty."
        )

    candidates = db.query(Candidate).all()

    histories = {}

    for candidate in candidates:
        histories[candidate.id] = (
            db.query(StageHistory)
            .filter(
                StageHistory.candidate_id == candidate.id
            )
            .order_by(StageHistory.timestamp.asc())
            .all()
        )

    results = []
    explanation = ""

    # -----------------------------------------
    # 1. Everyone except rejected candidates
    # -----------------------------------------

    if (
        "everyone" in query
        and "except" in query
        and "rejected" in query
    ):
        results = [
            candidate
            for candidate in candidates
            if candidate.current_stage != "Rejected"
        ]

        explanation = (
            "Showing all candidates except those currently rejected."
        )

        return {
            "query": q,
            "explanation": explanation,
            "results": results
        }

    # -----------------------------------------
    # 2. Candidates currently in a stage
    # -----------------------------------------

    stage_found = None

    for stage in STAGES:
        if normalize(stage) in query:
            stage_found = stage
            break

    if stage_found and (
        "right now" in query
        or "currently" in query
        or "in " in query
    ):
        results = [
            candidate
            for candidate in candidates
            if candidate.current_stage == stage_found
        ]

        explanation = (
            f"Showing candidates currently in {stage_found}."
        )

        return {
            "query": q,
            "explanation": explanation,
            "results": results
        }

    # -----------------------------------------
    # 3. Stuck in a stage for more than 7 days
    # -----------------------------------------

    if (
        ("stuck" in query or "more than a week" in query)
        and stage_found
    ):
        cutoff = datetime.utcnow() - timedelta(days=7)

        for candidate in candidates:
            if candidate.current_stage != stage_found:
                continue

            history = histories[candidate.id]
            latest_time = latest_stage_time(history)

            if latest_time and latest_time < cutoff:
                results.append(candidate)

        explanation = (
            f"Showing candidates currently in {stage_found} "
            "for more than 7 days."
        )

        return {
            "query": q,
            "explanation": explanation,
            "results": results
        }

    # -----------------------------------------
    # 4. Moved to a stage since Monday
    # -----------------------------------------

    if "since monday" in query and stage_found:
        now = datetime.utcnow()

        monday = (
            now - timedelta(days=now.weekday())
        ).replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        for candidate in candidates:
            history = histories[candidate.id]

            for item in history:
                if (
                    item.to_stage == stage_found
                    and item.timestamp >= monday
                ):
                    results.append(candidate)
                    break

        explanation = (
            f"Showing candidates who moved to {stage_found} "
            "since Monday."
        )

        return {
            "query": q,
            "explanation": explanation,
            "results": results
        }

    # -----------------------------------------
    # 5. Reached Offer but did not get hired
    # -----------------------------------------

    if (
        "offer" in query
        and (
            "didn't get hired" in query
            or "didnt get hired" in query
            or "not hired" in query
            or "did not get hired" in query
        )
    ):
        for candidate in candidates:
            history = histories[candidate.id]

            reached_offer = any(
                item.to_stage == "Offer"
                for item in history
            )

            if (
                reached_offer
                and candidate.current_stage != "Hired"
            ):
                results.append(candidate)

        explanation = (
            "Showing candidates who reached Offer but "
            "were not hired."
        )

        return {
            "query": q,
            "explanation": explanation,
            "results": results
        }

    # -----------------------------------------
    # 6. Find candidate by name, including typo
    # -----------------------------------------

    if query.startswith("find "):
        name_query = query.replace("find ", "", 1).strip()

        ranked = []

        for candidate in candidates:
            score = name_similarity(
                name_query,
                candidate.name
            )

            # Higher threshold prevents unrelated candidates
            # from appearing in typo searches.
            if score >= 0.70:
                ranked.append(
                    (score, candidate)
                )

        ranked.sort(
            key=lambda item: item[0],
            reverse=True
        )

        results = [
            candidate
            for score, candidate in ranked
        ]

        explanation = (
            f"Searching candidate names matching '{name_query}'. "
            "Results are ranked by name similarity."
        )

        return {
            "query": q,
            "explanation": explanation,
            "results": results
        }

    # -----------------------------------------
    # 7. Simple stage search
    # -----------------------------------------

    if stage_found:
        results = [
            candidate
            for candidate in candidates
            if candidate.current_stage == stage_found
        ]

        explanation = (
            f"Showing candidates currently in {stage_found}."
        )

        return {
            "query": q,
            "explanation": explanation,
            "results": results
        }

    # -----------------------------------------
    # 8. Invalid / unsupported query
    # -----------------------------------------

    raise HTTPException(
        status_code=400,
        detail=(
            "I couldn't understand that search. Try queries such as: "
            "'Find Priya Sharma', "
            "'Who's in Interview right now?', "
            "'Who has been stuck in Screening for more than a week?', "
            "'Who moved to Interview since Monday?', "
            "'Who reached the Offer stage but didn't get hired?', "
            "or 'Everyone except rejected candidates.'"
        )
    )