# Mini Hiring Pipeline

A lightweight recruiter workflow application for managing candidates through a fixed hiring pipeline.

## Project Overview

The application allows a recruiter to manage candidates for a single job through these stages:

**Applied → Screening → Interview → Offer → Hired**

A candidate can also be rejected at any stage before being hired.

The system prevents invalid stage transitions and maintains a complete history of every stage change.

## Features

- Add new candidates
- View candidates by hiring stage
- Move candidates through the hiring pipeline
- Reject candidates before hiring
- Prevent skipping stages
- Prevent changes after Hired or Rejected
- View complete candidate history
- Show time spent in the current stage
- Search candidates using natural-language-style queries
- Typo-tolerant candidate name search
- Clear explanation for unsupported searches

## Supported Search Queries

Examples:

- `Find Priya Sharma`
- `Find Priya Sharam`
- `Who's in Interview right now?`
- `Who has been stuck in Screening for more than a week?`
- `Who moved to Interview since Monday?`
- `Who reached the Offer stage but didn't get hired?`
- `Everyone except rejected candidates.`

The search API explains how the query was interpreted. Unsupported queries return a clear explanation instead of an empty result.

## Tech Stack

### Frontend

- React
- Vite
- JavaScript
- Axios

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic

### Database

- SQLite

## Architecture

```text
React Frontend
      |
      | HTTP / REST API
      v
FastAPI Backend
      |
      v
SQLAlchemy
      |
      v
SQLite Database
```

## How to Run

### Backend

```bash
cd backend
python -m venv venv
```

Activate the virtual environment.

On Windows:

```powershell
.\venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the backend:

```bash
uvicorn main:app --reload
```

Backend runs at:

`http://127.0.0.1:8000`

### Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

`http://localhost:5173`

## Key Design Decisions

- FastAPI handles workflow rules and stage validation on the backend.
- SQLite was chosen for simple local persistence.
- SQLAlchemy is used for database interaction.
- StageHistory stores every stage transition instead of overwriting previous states.
- Hired and Rejected are treated as terminal states.
- Candidates can only move one stage forward.
- Name matching supports small spelling mistakes.
- Search parsing is deterministic for predictable recruiter queries.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API health check |
| GET | `/candidates` | Get all candidates |
| POST | `/candidates` | Create candidate |
| GET | `/candidates/{id}` | Get candidate details and history |
| POST | `/candidates/{id}/move` | Move candidate to next stage |
| GET | `/search` | Search candidates |

## API Testing

The REST APIs were tested using Postman and FastAPI Swagger.

## Documentation

Architecture and design documentation:

`docs/architecture-design.md`

Design PDF:

`docs/mini-hiring-pipeline-design.pdf`

## AI Development Log

The AI-assisted development process is documented in:

`ai-logs/development-log.md`

The log includes development decisions and an example where an AI suggestion was reviewed and changed based on the assignment requirements.

## What I Would Add With More Time

- Automated backend and frontend tests
- A dedicated search-results view with better ranking
- More flexible combined search queries
- Timezone-aware timestamps
- Authentication and role-based recruiter access
- PostgreSQL for production deployment
- Docker-based local setup