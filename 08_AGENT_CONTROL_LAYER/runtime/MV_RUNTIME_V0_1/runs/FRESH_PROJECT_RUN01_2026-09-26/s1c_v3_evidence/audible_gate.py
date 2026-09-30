"""Run-local audible lyric gate. Recognition/alignment never seal a stage."""
def evaluate(evidence):
    human=evidence['human_audio_review']
    if human == 'FAIL':
        return {'route':'REVISE','gate':'FAIL','allow_final_cut':False,'allow_seal':False}
    required=('actual_source_verified','lyric_order_verified','phrase_boundaries_clean','production_duration_practical')
    ready=(human=='PASS' and evidence['concrete_words_audible']=='TRUE' and all(evidence[k]=='TRUE' for k in required))
    return {'route':'PASS' if ready else 'REVISE','gate':'PASS' if ready else 'INSUFFICIENT_EVIDENCE','allow_final_cut':ready,'allow_seal':ready}

def regression_checks():
    ready=dict(human_audio_review='PASS',concrete_words_audible='TRUE',actual_source_verified='TRUE',lyric_order_verified='TRUE',phrase_boundaries_clean='TRUE',production_duration_practical='TRUE',asr_support='UNAVAILABLE',forced_alignment_support='WEAK')
    assert evaluate(ready)['gate']=='PASS'
    for human in ('FAIL','PENDING','NOT_RUN'):
        trial=ready|{'human_audio_review':human,'asr_support':'SUPPORTS','forced_alignment_support':'SUPPORTS'}
        assert not evaluate(trial)['allow_seal']
    for key in ('concrete_words_audible','actual_source_verified','lyric_order_verified','phrase_boundaries_clean','production_duration_practical'):
        for value in ('FALSE','INSUFFICIENT'):
            assert not evaluate(ready|{key:value})['allow_final_cut']
    return {'regression_checks':14,'status':'PASS'}
