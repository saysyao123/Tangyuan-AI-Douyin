#!/usr/bin/env python3
"""Current run consistency validation. Historical deliveries cannot supply a seal."""
import json
import sys
import subprocess
from pathlib import Path
from s0_s1_repair.candidate_intake import validate_current_state

ROOT = Path(__file__).resolve().parent
def validate():
    try:
        state = json.loads((ROOT / 'RUN_CURRENT_STATE.yaml').read_text(encoding='utf-8'))
        delivery = json.loads((ROOT / 'S0_DELIVERY.yaml').read_text(encoding='utf-8'))['s0']
        result = validate_current_state(state)
        errors = result['errors']
        if delivery.get('status') != state.get('s0'):
            errors.append('S0_DELIVERY_STATE_MISMATCH')
        if delivery.get('selected_song_family') != state.get('selected_song_family'):
            errors.append('S0_SELECTED_FAMILY_MISMATCH')
        if state.get('s0') == 'SEALED' and delivery.get('human_song_family_lock', {}).get('status') != 'PASS':
            errors.append('S0_SEAL_WITHOUT_HUMAN_FAMILY_LOCK')
        regression = subprocess.run(
            [sys.executable, '-m', 'unittest', 'discover', '-s', str(ROOT / 's0_s1_repair'), '-p', 'test_*.py'],
            capture_output=True, text=True, check=False)
        result['unit_regressions_passed'] = regression.returncode == 0
        result['unit_regression_summary'] = regression.stderr.strip()
        if regression.returncode != 0:
            errors.append('UNIT_REGRESSION_FAILED')
        result['status'] = 'FAIL' if errors else 'PASS'
        result['authority'] = 'RUN_CURRENT_STATE.yaml + S0_DELIVERY.yaml'
        result['historical_s1_delivery_used'] = False
        return result
    except (OSError, ValueError, KeyError, TypeError) as error:
        return {'status': 'FAIL', 'errors': ['CURRENT_STATE_LOAD_FAILED'], 'detail': str(error)}
if __name__ == '__main__':
    result = validate()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result['status'] == 'PASS' else 1)
