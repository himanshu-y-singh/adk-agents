from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID

class WorkLog(BaseModel):
    content: str
    category: str
    created_at: Optional[datetime] = None
