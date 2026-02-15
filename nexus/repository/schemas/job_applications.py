from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum
from uuid import UUID

class JobStatus(str, Enum):
    APPLIED = "applied"
    INTERVIEWING = "interviewing"
    REJECTED = "rejected"
    OFFER = "offer"

class JobApplication(BaseModel):
    company_name: str
    position: str
    status: JobStatus = JobStatus.APPLIED
    applied_date: Optional[datetime] = None
    notes: Optional[str] = None
