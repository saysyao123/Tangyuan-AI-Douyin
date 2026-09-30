"""Compatibility S0 gate: direction eligibility only; audible truth is owned by S1."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from s0_s1_repair.candidate_intake import evaluate_direction

def qualify(candidate, allow_supplemental_test=False):
    result = evaluate_direction(candidate, allow_supplemental_test)
    return result | {
        'qualification': 'ELIGIBLE_DIRECTION' if result['direction_status'] == 'ELIGIBLE' else 'NOT_ELIGIBLE_DIRECTION',
        'blockers': result['reasons'], 's0_sealed': False, 'audio_gate_passed': False
    }
