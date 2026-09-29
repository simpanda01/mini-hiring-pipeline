from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CandidateCreate(BaseModel):
    name: str
    email: str


class CandidateResponse(BaseModel):
    id: int
    name: str
    email: str
    current_stage: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StageMove(BaseModel):
    to_stage: str