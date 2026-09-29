from datetime import datetime, timedelta

from database import SessionLocal
from models import Candidate, StageHistory


db = SessionLocal()


def add_candidate(name, email, history):
    existing = (
        db.query(Candidate)
        .filter(Candidate.name == name)
        .first()
    )

    if existing:
        print(f"{name} already exists - skipping")
        return

    candidate = Candidate(
        name=name,
        email=email,
        current_stage=history[-1][0],
        created_at=history[0][1],
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    for i, (stage, timestamp) in enumerate(history):

        previous_stage = (
            history[i - 1][0]
            if i > 0
            else None
        )

        record = StageHistory(
            candidate_id=candidate.id,
            from_stage=previous_stage,
            to_stage=stage,
            timestamp=timestamp,
        )

        db.add(record)

    db.commit()

    print(
        f"Created: {name} -> {candidate.current_stage}"
    )


now = datetime.utcnow()


# Monday of the current week
monday = (
    now - timedelta(days=now.weekday())
).replace(
    hour=10,
    minute=0,
    second=0,
    microsecond=0,
)


# Rahul - currently in Interview
add_candidate(
    "Rahul Das",
    "rahul@gmail.com",
    [
        (
            "Applied",
            monday - timedelta(days=2),
        ),
        (
            "Screening",
            monday - timedelta(days=1),
        ),
        (
            "Interview",
            monday + timedelta(hours=1),
        ),
    ],
)


# Ananya - stuck in Screening
add_candidate(
    "Ananya Roy",
    "ananya@gmail.com",
    [
        (
            "Applied",
            now - timedelta(days=12),
        ),
        (
            "Screening",
            now - timedelta(days=10),
        ),
    ],
)


# Arjun - reached Offer but not Hired
add_candidate(
    "Arjun Patel",
    "arjun@gmail.com",
    [
        (
            "Applied",
            now - timedelta(days=8),
        ),
        (
            "Screening",
            now - timedelta(days=7),
        ),
        (
            "Interview",
            now - timedelta(days=5),
        ),
        (
            "Offer",
            now - timedelta(days=3),
        ),
    ],
)


# Neha - Hired
add_candidate(
    "Neha Singh",
    "neha@gmail.com",
    [
        (
            "Applied",
            now - timedelta(days=10),
        ),
        (
            "Screening",
            now - timedelta(days=8),
        ),
        (
            "Interview",
            now - timedelta(days=6),
        ),
        (
            "Offer",
            now - timedelta(days=4),
        ),
        (
            "Hired",
            now - timedelta(days=2),
        ),
    ],
)


# Riya - currently Applied
add_candidate(
    "Riya Sen",
    "riya@gmail.com",
    [
        (
            "Applied",
            now - timedelta(days=1),
        ),
    ],
)


db.close()

print()
print("Test data creation completed.")