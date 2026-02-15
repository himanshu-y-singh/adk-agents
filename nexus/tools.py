from typing import List, Dict, Any, Optional
from nexus.repository.crud import add_work_log as crud_add_work, get_work_logs as crud_get_work, add_job_application as crud_add_job, get_job_applications as crud_get_jobs, update_job_status as crud_update_job
from nexus.repository.session import get_db
from nexus.repository.models import WorkLog, JobApplication
from google.adk.tools import ToolContext

async def add_work_log(
    content: str,
    category: str
) -> str:
    """Logs a work item for tracking.
    
    Args:
        content: Description of the work done.
        category: Category of work (e.g., coding, meeting, research).
    """
    work_data = WorkLog(content=content, category=category)
    async with get_db() as session:
        result = await crud_add_work(session, work_data)
        return f"Work log added: {result.id}"

async def get_work_logs() -> List[Dict[str, Any]]:
    """Retrieves work logs (e.g., for daily standup)."""
    async with AsyncSessionLocal() as session:
        logs = await crud_get_work(session)
        return [l.__dict__ for l in logs]

async def add_job_app(
    company_name: str,
    position: str,
    notes: Optional[str] = None
) -> str:
    """Logs a new job application.
    
    Args:
        company_name: Name of the company.
        position: Position applied for.
        notes: Optional notes about the application.
    """
    job_data = JobApplication(
        company_name=company_name, 
        position=position, 
        notes=notes,
        status=JobStatus.APPLIED
    )
    async with get_db() as session:
        result = await crud_add_job(session, job_data)
        return f"Job application added: {result.id}"

async def get_job_apps() -> List[Dict[str, Any]]:
    """Retrieves job applications."""
    async with AsyncSessionLocal() as session:
        apps = await crud_get_jobs(session)
        # Convert Enum to string for JSON serialization if needed
        return [a.__dict__ for a in apps]

async def update_job_status(
    job_id: str,
    status: str
) -> str:
    """Updates the status of a job application.
    
    Args:
        job_id: ID of the job application.
        status: New status (applied, interviewing, rejected, offer).
    """
    async with get_db() as session:
        result = await crud_update_job(session, job_id, status)
        if result:
            return f"Job status updated to {status}"
        return "Job not found"
