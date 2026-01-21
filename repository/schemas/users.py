from pydantic import BaseModel
from typing import Optional
from enum import Enum

class RelationshipType(str, Enum):
    FAMILY = "family"
    FRIEND = "friend"
    COLLEAGUE = "colleague"
    OTHER = "other"

class User(BaseModel):
    name: str
    email: Optional[str] = None
    relationship_type: Optional[RelationshipType] = None
    company: Optional[str] = None
    college: Optional[str] = None
