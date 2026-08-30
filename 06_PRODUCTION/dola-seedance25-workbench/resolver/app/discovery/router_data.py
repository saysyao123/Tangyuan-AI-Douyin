from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any


def _parse_json_string(value: str) -> Any | None:
    candidate = value.strip()
    if len(candidate) < 2 or candidate[0] not in "[{":
        return None
    try:
        return json.loads(candidate)
    except (TypeError, ValueError, json.JSONDecodeError):
        return None


def walk_json(value: Any, path: tuple[str | int, ...] = (), *, max_depth: int = 20) -> Iterator[tuple[tuple[str | int, ...], Any]]:
    """Yield every JSON node, including objects encoded inside JSON strings."""
    seen: set[int] = set()

    def visit(node: Any, node_path: tuple[str | int, ...], depth: int) -> Iterator[tuple[tuple[str | int, ...], Any]]:
        yield node_path, node
        if depth >= max_depth:
            return
        if isinstance(node, str):
            parsed = _parse_json_string(node)
            if parsed is not None:
                yield from visit(parsed, node_path + ("<json>",), depth + 1)
            return
        if isinstance(node, dict):
            identity = id(node)
            if identity in seen:
                return
            seen.add(identity)
            for key, child in node.items():
                yield from visit(child, node_path + (str(key),), depth + 1)
            return
        if isinstance(node, list):
            identity = id(node)
            if identity in seen:
                return
            seen.add(identity)
            for index, child in enumerate(node):
                yield from visit(child, node_path + (index,), depth + 1)

    yield from visit(value, path, 0)
