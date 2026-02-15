from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, Text, text, Enum, UUID
from sqlalchemy.types import Enum, UUID
import uuid
from datetime import datetime
from nexus.repository.schemas.job_applications import JobStatus

class Base(DeclarativeBase):
    pass


class WorkLog(Base):
    __tablename__ = "work_logs"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()")
    )
    content: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )

class JobApplication(Base):
    __tablename__ = "job_applications"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()")
    )
    company_name: Mapped[str] = mapped_column(String(100))
    position: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(Enum(JobStatus, name="job_status"), default=JobStatus.APPLIED)
    applied_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )
    notes: Mapped[str] = mapped_column(Text, nullable=True)