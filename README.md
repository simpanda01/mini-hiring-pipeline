# Mini Hiring Pipeline



A lightweight recruiter workflow application for managing candidates through a fixed hiring pipeline.



## Project Overview



The application allows a recruiter to manage candidates for a single job through these stages:



\*\*Applied → Screening → Interview → Offer → Hired\*\*



A candidate can also be rejected at any stage before being hired.



The system prevents invalid stage transitions and maintains a complete history of every stage change.



## Features



\- Add new candidates

\- View candidates by hiring stage

\- Move candidates through the hiring pipeline

\- Reject candidates before hiring

\- Prevent skipping stages

\- Prevent changes after Hired or Rejected

\- View complete candidate history

\- Show time spent in the current stage

\- Search candidates using natural-language-style queries

\- Typo-tolerant candidate name search

\- Clear explanation for unsupported searches



## Supported Search Queries



Examples:



\- `Find Priya Sharma`

\- `Find Priya Sharam`

\- `Who's in Interview right now?`

\- `Who has been stuck in Screening for more than a week?`

\- `Who moved to Interview since Monday?`

\- `Who reached the Offer stage but didn't get hired?`

\- `Everyone except rejected candidates.`



The search API explains how the query was interpreted. Unsupported queries return a clear explanation instead of an empty result.



## Tech Stack



### Frontend

\- React

\- Vite

\- JavaScript

\- Axios



### Backend

\- Python

\- FastAPI

\- SQLAlchemy

\- Pydantic



### Database

\- SQLite



## Architecture



```text

React Frontend

&#x20;     |

&#x20;     | HTTP / REST API

&#x20;     v

FastAPI Backend

&#x20;     |

&#x20;     v

SQLAlchemy

&#x20;     |

&#x20;     v

SQLite Database


