from worker.celery_app import celery
from app.core.database import SessionLocal
from app.models.job import Job
from app.services.fetcher import fetch_url_content
from app.services.summarizer import summarize
from app.services.cache import set_cache
import time

@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=5)
def process_job(self, job_id):
    db = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        return

    try:
        job.status = "processing"
        db.commit()

        start_time = time.time()

        if job.input_type == "url":
            content = fetch_url_content(job.input_data)
        else:
            content = job.input_data

        print("Content length:", len(content))

        summary = summarize(content)

        print("Summary:", summary[:200])

        end_time = time.time()
        job.processing_time_ms = int((end_time - start_time) * 1000)

        if summary.startswith("Error"):
            job.status = "failed"
            job.error = summary
        else:
            job.summary = summary
            job.status = "completed"
            set_cache(job.input_data, summary)

        db.commit()

    except Exception as e:
        job.status = "failed"
        job.error = str(e)
        db.commit()

    finally:
        db.close()