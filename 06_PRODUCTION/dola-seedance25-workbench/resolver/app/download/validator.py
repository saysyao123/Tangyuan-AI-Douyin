from __future__ import annotations

from pathlib import Path

from app.download.authenticated import sha256_file


def validate_ftyp(path: str | Path, *, probe_bytes: int = 64) -> bool:
    data = Path(path).read_bytes()[:probe_bytes]
    if b"ftyp" not in data:
        raise ValueError("file does not contain an MP4 ftyp box in its first 64 bytes")
    return True


def validate_download(path: str | Path) -> dict[str, int | str | bool]:
    media_path = Path(path)
    if not media_path.is_file():
        raise FileNotFoundError(media_path)
    if media_path.stat().st_size <= 0:
        raise ValueError("downloaded file is empty")
    validate_ftyp(media_path)
    return {
        "path": str(media_path),
        "size": media_path.stat().st_size,
        "sha256": sha256_file(media_path),
        "ftyp_valid": True,
    }
