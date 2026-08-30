from __future__ import annotations


class BrowserCaptureNotImplemented(RuntimeError):
    """Raised because authenticated browser capture is intentionally P1."""


def capture(*_args, **_kwargs):
    raise BrowserCaptureNotImplemented(
        "browser-capture is P1; P0 accepts sanitized metadata JSON via --metadata"
    )
