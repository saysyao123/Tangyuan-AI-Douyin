from __future__ import annotations

import json
import sys
from urllib.error import URLError
from urllib.request import urlopen


ENDPOINT = "http://127.0.0.1:9222/json/version"


def read_cdp_version(endpoint: str = ENDPOINT) -> dict[str, object]:
    with urlopen(endpoint, timeout=3) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("CDP version response must be an object")
    return payload


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    endpoint = args[0] if args else ENDPOINT
    if endpoint.endswith("/json/version") is False:
        endpoint = endpoint.rstrip("/") + "/json/version"
    try:
        payload = read_cdp_version(endpoint)
        browser = str(payload.get("Browser", "UNKNOWN"))
        protocol = str(payload.get("Protocol-Version", "UNKNOWN"))
        websocket_present = bool(payload.get("webSocketDebuggerUrl"))
        print(f"CDP_READY: YES")
        print(f"Browser: {browser[:120]}")
        print(f"Protocol-Version: {protocol[:40]}")
        print(f"webSocketDebuggerUrl: {'PRESENT' if websocket_present else 'MISSING'}")
        return 0 if websocket_present else 2
    except (OSError, URLError, ValueError, json.JSONDecodeError) as exc:
        print("CDP_READY: NO")
        print(f"Error: {type(exc).__name__}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
