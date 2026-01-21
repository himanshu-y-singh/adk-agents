from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Transaction(BaseModel):
    amount: float
    from_user: str
    created_at: Optional[datetime] = None