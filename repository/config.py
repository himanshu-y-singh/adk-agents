from pydantic import BaseModel
import os

class DatabaseConfig(BaseModel):
    url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://himanshu@localhost:5432/chat_history"
    )

db_config = DatabaseConfig()
