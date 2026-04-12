import json
from datetime import datetime, timezone

from app.config import REDIS_JOB_TTL_SECONDS
from app.redis_client import get_redis_client


def _job_key(job_id: str) -> str:
    return f"job:{job_id}"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_job_status(job_id: str, payload: dict) -> dict:
    data = {
        "job_id": job_id,
        "status": "queued",
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
        "payload": payload,
        "result": None,
        "error": None,
    }

    redis_client = get_redis_client()
    redis_client.set(
        _job_key(job_id),
        json.dumps(data, ensure_ascii=False),
        ex=REDIS_JOB_TTL_SECONDS,
    )
    return data


def update_job_status(
    job_id: str,
    status: str,
    result: dict | None = None,
    error: str | None = None,
) -> dict | None:
    redis_client = get_redis_client()
    raw = redis_client.get(_job_key(job_id))

    if raw is None:
        return None

    data = json.loads(raw)
    data["status"] = status
    data["updated_at"] = _now_iso()

    if result is not None:
        data["result"] = result

    if error is not None:
        data["error"] = error

    redis_client.set(
        _job_key(job_id),
        json.dumps(data, ensure_ascii=False),
        ex=REDIS_JOB_TTL_SECONDS,
    )
    return data


def get_job_status(job_id: str) -> dict | None:
    redis_client = get_redis_client()
    raw = redis_client.get(_job_key(job_id))

    if raw is None:
        return None

    return json.loads(raw)