from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class MediaCandidate:
    source: str
    url: str
    width: int | None = None
    height: int | None = None
    bitrate: int | None = None
    real_bitrate: int | None = None
    codec: str | None = None
    definition: str | None = None
    gear_name: str | None = None
    is_original: bool = False
    is_unwatermarked: bool = False
    raw: dict[str, Any] | None = None

    @property
    def pixel_area(self) -> int:
        if self.width and self.height:
            return self.width * self.height
        return 0

    @property
    def effective_bitrate(self) -> int:
        return self.real_bitrate or self.bitrate or 0

    def public_dict(self, *, redacted_url: str | None = None) -> dict[str, Any]:
        data = asdict(self)
        data.pop("raw", None)
        data["url"] = redacted_url if redacted_url is not None else self.url
        data["pixel_area"] = self.pixel_area
        data["effective_bitrate"] = self.effective_bitrate
        return data


@dataclass(slots=True)
class ResolveResult:
    vid: str | None
    candidates: list[MediaCandidate] = field(default_factory=list)
    selected: MediaCandidate | None = None
    source_metadata: dict[str, Any] = field(default_factory=dict)
    status: str = "clean_source_not_available"

    @property
    def clean_candidates(self) -> list[MediaCandidate]:
        return [candidate for candidate in self.candidates if candidate.is_unwatermarked]
