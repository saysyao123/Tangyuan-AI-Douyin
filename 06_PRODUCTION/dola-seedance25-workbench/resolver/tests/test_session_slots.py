from __future__ import annotations

import pytest

from app.production.session_slots import safe_slot_manifest, session_slot_for


def test_session_slots_are_isolated_and_deterministic(tmp_path) -> None:
    first = session_slot_for("A01", project_root=tmp_path)
    second = session_slot_for("A02", project_root=tmp_path)
    assert first.session_slot == "S01"
    assert second.session_slot == "S02"
    assert first.port == 9331
    assert second.port == 9332
    assert first.profile_dir != second.profile_dir
    assert "cookies" not in str(first.profile_dir).lower()


def test_session_slot_rejects_ambiguous_account_id() -> None:
    with pytest.raises(ValueError):
        session_slot_for("account-02")


def test_slot_manifest_contains_no_auth_material(tmp_path) -> None:
    manifest = safe_slot_manifest(["A01", "A02"], project_root=tmp_path)
    assert [row["endpoint"] for row in manifest] == ["http://127.0.0.1:9331", "http://127.0.0.1:9332"]
    assert "cookie" not in str(manifest).lower()
    assert "token" not in str(manifest).lower()
