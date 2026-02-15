from nexus.repository.models import WorkLog, JobApplication
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def add_work_log(
    db: AsyncSession,
    work_log: any
):
    db_work_log = WorkLog(**work_log.model_dump())
    db.add(db_work_log)
    await db.commit()
    await db.refresh(db_work_log)
    return db_work_log

async def get_work_logs(
    db: AsyncSession,
):
    stmt = (
        select(WorkLog)
        .order_by(WorkLog.created_at.desc())
    )
    result = await db.execute(stmt)
    return result.scalars().all()

async def add_job_application(
    db: AsyncSession,
    job_application: any
):
    db_job_app = JobApplication(**job_application.model_dump())
    db.add(db_job_app)
    await db.commit()
    await db.refresh(db_job_app)
    return db_job_app

async def get_job_applications(
    db: AsyncSession,
):
    stmt = (
        select(JobApplication)
        .order_by(JobApplication.applied_date.desc())
    )
    result = await db.execute(stmt)
    return result.scalars().all()

async def update_job_status(
    db: AsyncSession,
    job_id: str,
    status: str
):
    stmt = (
        select(JobApplication)
        .where(JobApplication.id == job_id)
    )
    result = await db.execute(stmt)
    job_app = result.scalars().first()
    if job_app:
        job_app.status = status
        await db.commit()
        await db.refresh(job_app)
    return job_app

