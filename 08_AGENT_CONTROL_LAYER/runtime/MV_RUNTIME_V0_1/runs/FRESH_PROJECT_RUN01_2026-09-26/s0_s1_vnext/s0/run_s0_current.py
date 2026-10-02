import json
from pathlib import Path

from s0_stage import evaluate_s0

ROOT = Path(__file__).resolve().parent
payload = json.loads((ROOT / "ACTUAL_INPUT_2026-10-02.json").read_text(encoding="utf-8"))
result = evaluate_s0(payload)
(ROOT / "S0_ACTUAL_TEST_RESULT_2026-10-02.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(result, ensure_ascii=False, indent=2))

