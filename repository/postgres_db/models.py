from sqlalchemy import String, DateTime, Float, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from repository.postgres_db.base import Base
from sqlalchemy.types import Enum, UUID
from repository.schemas.users import RelationshipType
import uuid

class User(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(100), primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(100), nullable=True)
    relationship_type: Mapped[str] = mapped_column(Enum(RelationshipType, name="relationship_type"), nullable=True)
    company: Mapped[str] = mapped_column(String(100), nullable=True)
    college: Mapped[str] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    
class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()")
    )
    amount: Mapped[float] = mapped_column(Float)
    from_user: Mapped[str] = mapped_column(
        ForeignKey("users.name"),
        index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="transactions"
    )


