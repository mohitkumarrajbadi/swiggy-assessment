from fastapi import APIRouter, HTTPException
from app.core.database import SessionLocal
from app.models.job import Job
from worker.tasks import process_job
from app.services.cache import get_cached

router = APIRouter()

@router.post("/submit")
def submit(data: dict):
    db = SessionLocal()

    text = data.get("text")
    url = data.get("url")

    input_data = text or url
    input_type = "text" if text else "url"

    if not input_data:
        raise HTTPException(400, "Either 'text' or 'url' must be provided")

    cached = get_cached(input_data)
    if cached:
        # Create a job record that is already completed
        job = Job(
            input_type=input_type, 
            input_data=input_data, 
            status="completed", 
            summary=cached.decode(),
            is_cached=True,
            processing_time_ms=0 # Instant
        )
        db.add(job)
        db.commit()
        return {"job_id": job.id, "status": "completed"}

    job = Job(input_type=input_type, input_data=input_data)
    db.add(job)
    db.commit()

    process_job.delay(job.id)

    return {"job_id": job.id, "status": "queued"}


@router.get("/status/{job_id}")
def status(job_id: str):
    db = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(404, "Job not found")

    return {
        "job_id": job.id,
        "status": job.status,
        "created_at": job.created_at
    }


@router.get("/result/{job_id}")
def result(job_id: str):
    db = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(404, "Job not found")

    if job.status != "completed":
        return {"status": job.status}

    return {
        "job_id": job.id,
        "original_url": job.input_data if job.input_type == "url" else None,
        "summary": job.summary,
        "cached": job.is_cached,
        "processing_time_ms": job.processing_time_ms
    }