import json
import uuid

from app.config import REDIS_QUEUE_PROCESS
from app.redis_client import get_redis_client
from app.job_status import create_job_status


def enqueue_process_job(
    filename: str,
    summary_limit: int | None,
    chunk_size: int | None,
    overlap: int | None,
    force_rebuild: bool = False,
) -> dict:
    job_id = str(uuid.uuid4())

    payload = {
        "job_id": job_id,
        "type": "process_document",
        "filename": filename,
        "summary_limit": summary_limit,
        "chunk_size": chunk_size,
        "overlap": overlap,
        "force_rebuild": force_rebuild,
    }

    create_job_status(job_id, payload)

    redis_client = get_redis_client()
    redis_client.rpush(REDIS_QUEUE_PROCESS, json.dumps(payload, ensure_ascii=False))

    return {
        "job_id": job_id,
        "status": "queued",
        "queue": REDIS_QUEUE_PROCESS,
    }


def dequeue_process_job(block_timeout: int = 5) -> dict | None:
    redis_client = get_redis_client()
    item = redis_client.blpop(REDIS_QUEUE_PROCESS, timeout=block_timeout)

    if not item:
        return None

    _, raw_payload = item
    return json.loads(raw_payload)