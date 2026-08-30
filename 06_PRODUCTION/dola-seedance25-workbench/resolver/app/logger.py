from __future__ import annotations

import logging
from urllib.parse import urlsplit, urlunsplit


def redact_url(value: str) -> str:
    """Keep enough URL identity for QA without leaking signed query data."""
    try:
        parts = urlsplit(value)
        path = parts.path[:96]
        if len(parts.path) > 96:
            path += "...[TRUNCATED]"
        return urlunsplit((parts.scheme, parts.netloc, path, "REDACTED", ""))
    except ValueError:
        return "<INVALID_URL>"


class RedactingFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        return message.replace("key_seed", "<KEY_SEED>").replace("Cookie", "<COOKIE>")


def configure_logging(level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger("dola_original_resolver")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(RedactingFormatter("%(levelname)s %(message)s"))
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger
