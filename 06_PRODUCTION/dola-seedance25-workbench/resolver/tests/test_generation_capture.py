from __future__ import annotations

import json
from pathlib import Path

from app.capture.generation_time import resolve_generation_bundle, scan_generation_identity


VID = "v186a3gm000cda9gbpfog65jfpbu9q50"


def test_generation_identity_requires_real_media_evidence() -> None:
    only_model = scan_generation_identity([{"video_model": "seedance"}])
    assert only_model["identity_pass"] is False
    assert only_model["values"]["vids"] == []

    node = scan_generation_identity(
        [{"node_id": "node-123", "key": "media-key-123", "node_type": 6, "video_list": []}]
    )
    assert node["identity_pass"] is True
    assert node["values"]["node_ids"] == ["node-123"]
    assert node["values"]["media_keys"] == ["media-key-123"]


def test_resolve_generation_bundle_writes_derived_artifacts(tmp_path: Path) -> None:
    bundle = tmp_path / "captures" / "generation" / "20260830_120000"
    bundle.mkdir(parents=True)
    (bundle / "network-index.json").write_text(
        json.dumps(
            {
                "full_cdp": True,
                "capture_armed_before_generation": True,
                "events": [{"method": "POST", "path": "/samantha/video/get_play_info"}],
            }
        ),
        encoding="utf-8",
    )
    response = {
        "task_id": "task-123",
        "message_id": "message-123",
        "conversation_id": "conversation-123",
        "vid": VID,
        "video_list": [
            {
                "main_url": "https://cdn.example/video.mp4?sig=secret",
                "logo_type": "unwatermarked",
                "original": True,
                "width": 720,
                "height": 1280,
                "bitrate": 800000,
            }
        ],
    }
    (bundle / "fetch-events.jsonl").write_text(
        json.dumps(
            {
                "method": "POST",
                "path": "/samantha/chat/async/stream",
                "status": 200,
                "mime_type": "application/json",
                "body": json.dumps(response),
            }
        )
        + "\n",
        encoding="utf-8",
    )

    report = resolve_generation_bundle(bundle)

    assert report["FULL_CDP"] == "PASS"
    assert report["CAPTURE_ARMED_BEFORE_GENERATION"] == "PASS"
    assert report["GENERATION_REQUEST_CAPTURED"] == "YES"
    assert report["STREAMING_PROTOCOL"] == "FETCH"
    assert report["TASK_ID_FOUND"] == "YES"
    assert report["VID_FOUND"] == "YES"
    assert report["VIDEO_LIST_FOUND"] == "YES"
    assert report["GET_PLAY_INFO_CALLED"] == "PASS"
    assert report["GENERATION_MEDIA_IDENTITY_CAPTURE"] == "PASS"
    assert report["FOUND_CLEAN_CANDIDATE"] == "YES"
    assert report["HIGHEST_NATIVE_RESOLUTION"] == "720x1280"
    assert report["FFPROBE"] == "NOT_RUN"
    assert "sig=secret" not in json.dumps(report, ensure_ascii=False)
    assert (bundle / "identity-chain.json").is_file()
    assert (bundle / "media-hits.json").is_file()
    assert (bundle / "resolver-input.json").is_file()
    assert (bundle / "generation-report.json").is_file()


def test_protocol_does_not_promote_unrelated_cdp_websocket_events(tmp_path: Path) -> None:
    bundle = tmp_path / "generation"
    bundle.mkdir()
    (bundle / "network-index.json").write_text(
        json.dumps(
            {
                "full_cdp": True,
                "capture_armed_before_generation": True,
                "events": [{"method": "Network.webSocketFrameReceived", "path": ""}],
            }
        ),
        encoding="utf-8",
    )
    (bundle / "xhr-events.jsonl").write_text(
        json.dumps({"path": "/im/chain/single", "status": 200, "body": json.dumps({"vid": VID})})
        + "\n",
        encoding="utf-8",
    )
    report = resolve_generation_bundle(bundle)
    assert report["STREAMING_PROTOCOL"] == "XHR"
