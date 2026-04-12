import logging
import time

from app.assistants.factory import build_assistant
from app.config import ASSISTANT_TYPE
from app.job_queue import dequeue_process_job
from app.job_status import update_job_status


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


def run_worker():
    logger.info("Worker started. Waiting for jobs...")

    assistant = build_assistant(ASSISTANT_TYPE)

    while True:
        job = dequeue_process_job(block_timeout=5)

        if job is None:
            continue

        if "job_id" not in job:
            logger.error("Invalid job payload: %s", job)
            continue

        job_id = job["job_id"]
        logger.info("Picked job %s for file %s", job_id, job.get("filename"))

        update_job_status(job_id, status="running")

        try:
            result = assistant.process_document(
                filename=job["filename"],
                summary_limit=job.get("summary_limit"),
                chunk_size=job.get("chunk_size"),
                overlap=job.get("overlap"),
                force_rebuild=job.get("force_rebuild", False),
            )

            update_job_status(
                job_id,
                status="done",
                result=result,
            )

            logger.info("Job %s completed", job_id)

        except Exception as e:
            logger.exception("Job %s failed", job_id)

            update_job_status(
                job_id,
                status="failed",
                error=str(e),
            )

            time.sleep(1)


if __name__ == "__main__":
    run_worker()