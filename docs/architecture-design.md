\# Mini Hiring Pipeline — Architecture \& Design



\## 1. Overview



Mini Hiring Pipeline is a lightweight recruiter application for managing candidates through a fixed hiring workflow.



The pipeline is:



Applied → Screening → Interview → Offer → Hired



Candidates can also be rejected at any stage before Hired.



The application provides candidate management, stage validation, audit history, current-stage duration, and recruiter search.



\---



\## 2. Architecture



```text

+----------------------+

|    React Frontend    |

|      Vite + Axios    |

+----------+-----------+

&#x20;          |

&#x20;          | HTTP / REST API

&#x20;          v

+----------------------+

|    FastAPI Backend   |

|                      |

| Candidate Management |

| Stage Validation     |

| Search Logic         |

| History Handling     |

+----------+-----------+

&#x20;          |

&#x20;          v

+----------------------+

|      SQLAlchemy      |

|         ORM          |

+----------+-----------+

&#x20;          |

&#x20;          v

+----------------------+

|       SQLite         |

|                      |

| Candidates           |

| Stage History        |

+----------------------+

