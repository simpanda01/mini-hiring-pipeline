\# AI-Assisted Development Log



\## Overview



AI assistance was used during the development of the Mini Hiring Pipeline for implementation support, debugging, UI improvements, search logic, documentation, and testing.



The final implementation was reviewed and tested locally before submission.



\## 1. Backend Development



AI assistance was used to structure and implement the FastAPI backend, including:



\- Candidate creation

\- Candidate listing

\- Candidate details

\- Stage transitions

\- Candidate rejection

\- Stage history

\- Search endpoint

\- Sequential stage validation



The backend was designed to enforce the hiring workflow rules instead of relying only on frontend validation.



\## 2. Frontend Development



AI assistance was used to build and refine the React frontend.



The frontend includes:



\- Six pipeline columns

\- Candidate cards

\- Add candidate form

\- Move candidate actions

\- Reject candidate action

\- Candidate detail modal

\- Stage history

\- Current-stage duration

\- Search interface

\- Search explanations and error messages



The frontend was tested against the FastAPI backend locally.



\## 3. Search Implementation



AI assistance was used to implement the required recruiter search scenarios.



Examples tested:



\- Find Priya Sharma

\- Find Priya Sharam

\- Who's in Interview right now?

\- Who has been stuck in Screening for more than a week?

\- Who moved to Interview since Monday?

\- Who reached the Offer stage but didn't get hired?

\- Everyone except rejected candidates.



The search implementation uses deterministic query parsing and similarity matching for candidate names.



\## 4. Example of Disagreement With AI



\### Problem



The initial fuzzy name-matching implementation was too broad.



When searching:



Find Priya Sharam



the search could return both:



\- Priya Sharma

\- Riya Sen



Although typo-tolerant matching was working, returning an unrelated candidate made the result less precise.



\### Decision



The matching logic was changed to compare individual name parts when the query and candidate have the same number of name parts.



This allowed:



Find Priya Sharam



to match:



Priya Sharma



without incorrectly returning unrelated candidates such as:



Riya Sen.



\### Why This Decision Was Made



The goal was not only to tolerate typos, but also to reduce false-positive candidate matches.



The name-part comparison was preferred over simply changing the global similarity threshold.



\## 5. Testing and Debugging



AI assistance was used while debugging and testing:



\- Backend startup

\- Frontend API connection

\- Candidate data loading

\- Search behavior

\- Rejected candidate display

\- Candidate history

\- Current-stage duration

\- Test data seeding



The application was tested through the browser and FastAPI API.



\## 6. Documentation



AI assistance was used to prepare:



\- README

\- Architecture and design documentation

\- Setup instructions

\- Design decisions

\- Future improvement notes

\- AI development log



The documentation was reviewed against the implemented project functionality.



\## 7. Final Validation



The application was tested with sample candidates covering:



\- Applied

\- Screening

\- Interview

\- Offer

\- Hired

\- Rejected



The required search scenarios were also tested.



The final implementation was kept deterministic and local, without adding an external LLM or search service.

