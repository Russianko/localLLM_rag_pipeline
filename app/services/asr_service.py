from __future__ import annotations

import logging
import tempfile
from pathlib import Path

from faster_whisper import WhisperModel

from app.config import ASR_MODEL, ASR_DEVICE, ASR_COMPUTE_TYPE, ASR_LANGUAGE

logger = logging.getLogger(__name__)


class ASRService:
    def __init__(self) -> None:
        self.model_name = ASR_MODEL
        self.device = ASR_DEVICE
        self.compute_type = ASR_COMPUTE_TYPE
        self.language = ASR_LANGUAGE
        self._model: WhisperModel | None = None

    def _get_model(self) -> WhisperModel:
        if self._model is None:
            logger.info(
                "Loading ASR model: model=%s device=%s compute_type=%s",
                self.model_name,
                self.device,
                self.compute_type,
            )
            self._model = WhisperModel(
                self.model_name,
                device=self.device,
                compute_type=self.compute_type,
            )
        return self._model

    def transcribe_bytes(self, audio_bytes: bytes, suffix: str = ".webm") -> dict:
        if not audio_bytes:
            raise ValueError("Audio payload is empty.")

        model = self._get_model()

        with tempfile.NamedTemporaryFile(suffix=suffix, delete=True) as tmp:
            tmp.write(audio_bytes)
            tmp.flush()

            segments, info = model.transcribe(
                tmp.name,
                language=self.language,
                vad_filter=True,
                beam_size=1,
            )

            parts: list[str] = []
            raw_segments: list[dict] = []

            for segment in segments:
                text = segment.text.strip()
                if text:
                    parts.append(text)

                raw_segments.append(
                    {
                        "start": float(segment.start),
                        "end": float(segment.end),
                        "text": text,
                    }
                )

        transcript = " ".join(parts).strip()

        return {
            "text": transcript,
            "language": getattr(info, "language", self.language),
            "duration": getattr(info, "duration", None),
            "segments": raw_segments,
        }