from enum import Enum


class DocumentStatus(str, Enum):
    NOT_PROCESSED = "not_processed"
    PARTIAL = "partial"
    PROCESSED = "processed"
    FAILED = "failed"