"""S0 direction selection + S1 early source screen. No implicit audio seal."""
CORE_TIERS={'VERIFIED_CORE','HISTORICAL_CORE_VERIFIED','HISTORICAL_VERIFIED_CORE','CURRENT_CORE_DIRECT'}
CHINESE_SUPPORT={'TRUSTED_CHINESE_LYRICS','HISTORICAL_CHINESE_REFERENCE'}

def evaluate_direction(candidate,allow_supplemental_test=False):
    reasons=[]
    if candidate.get('history_policy') not in {'ELIGIBLE','NO_EXCLUSION_IN_CURRENT_LEDGER'}:
        reasons.append('HISTORY_NOT_ELIGIBLE')
    if candidate.get('human_rejected_for_run'):
        reasons.append('HUMAN_REJECTED_FOR_THIS_RUN')
    if candidate.get('language_support') not in CHINESE_SUPPORT:
        reasons.append('CHINESE_LANGUAGE_EVIDENCE_INSUFFICIENT')
    if not candidate.get('reference_leads') or not all(u.startswith('https://') for u in candidate['reference_leads']):
        reasons.append('REFERENCE_LEAD_REQUIRED')
    tier=candidate.get('source_tier')
    group='CORE' if tier in CORE_TIERS else 'SUPPLEMENTAL_TEST' if tier=='SUPPLEMENTAL' and allow_supplemental_test else 'WATCH'
    if group=='WATCH':reasons.append('NOT_ENABLED_FOR_SELECTION_LANE')
    return {'direction_status':'ELIGIBLE' if not reasons else 'HOLD','source_group':group,'reasons':reasons,'audio_truth':'UNLOCKED','requires_audio_before_s0_direction':False}

def rank_directions(candidates,allow_supplemental_test=False):
    ranked=[]
    for c in candidates:
        assessment=evaluate_direction(c,allow_supplemental_test)
        if assessment['direction_status']=='ELIGIBLE':ranked.append(c|{'assessment':assessment})
    ranked.sort(key=lambda c:(c['assessment']['source_group']!='CORE',-c.get('semantic_priority',0)))
    unique=[];seen=set()
    for c in ranked:
        if c['song_family'] not in seen:
            unique.append(c);seen.add(c['song_family'])
    return unique[:3]

def screen_source(evidence):
    # Technical support can authorize analysis, never audible truth or stage seal.
    if evidence.get('sha256') and evidence['sha256'] in evidence.get('rejected_source_hashes',[]):
        route='SKIP_PREVIOUSLY_REJECTED_SOURCE'
    elif evidence.get('human_audio_review')=='FAIL':
        route='REJECT_CURRENT_SOURCE'
    elif not evidence.get('actual_media_exists'):
        route='RECOVER_SOURCE'
    elif not evidence.get('identity_verified'):
        route='VERIFY_SOURCE_IDENTITY'
    elif evidence.get('supporting_windows',0)>=2 and evidence.get('best_contiguous_match_chars',0)>=6:
        route='FULL_ANALYSIS_ELIGIBLE'
    else:
        route='TRY_ALTERNATE_SOURCE_OR_CANDIDATE'
    return {'route':route,'allow_full_analysis':route=='FULL_ANALYSIS_ELIGIBLE','audible_lyric_gate':'NOT_PASSED','allow_final_cut':False,'allow_s1_seal':False,'allow_s2':False}

def failure_route(source_attempt_count,family_attempt_count):
    if family_attempt_count>=3:return 'STOP_WITH_EVIDENCE_SUMMARY'
    return 'RECOVER_SAME_FAMILY_SOURCE' if source_attempt_count<2 else 'NEXT_CANDIDATE'

def can_seal_audio(evidence):
    digest=evidence.get('sha256')
    source_verified=bool(evidence.get('actual_media_exists') is True and evidence.get('identity_verified') is True and isinstance(digest,str) and len(digest)==64 and all(c in '0123456789abcdef' for c in digest))
    return bool(source_verified and evidence.get('human_audio_review')=='PASS' and evidence.get('audible_concrete_lyrics') is True and evidence.get('version_locked') is True and evidence.get('timeline_verified') is True and evidence.get('phrase_boundaries_verified') is True)

def validate_current_state(state):
    errors=[]
    if state.get('s0') not in {'REOPENED','SHORTLIST_READY','SEALED'}:errors.append('UNKNOWN_OR_MISSING_S0_STATE')
    if state.get('s1') not in {'NOT_SEALED','NOT_SEALED_REJECTED_CURRENT_SELECTION','SEALED'}:errors.append('UNKNOWN_OR_MISSING_S1_STATE')
    if state.get('s2') not in {'BLOCKED','ALLOWED'}:errors.append('UNKNOWN_OR_MISSING_S2_STATE')
    if state.get('s0')=='SEALED' and state.get('selected_song_family') is None:errors.append('S0_SEAL_WITHOUT_SELECTED_SONG')
    if state.get('s1')=='SEALED' and state.get('s0')!='SEALED':errors.append('S1_SEAL_WITHOUT_S0_SEAL')
    if state.get('s1')!='SEALED' and state.get('s2')!='BLOCKED':errors.append('S2_OPEN_WITHOUT_S1_SEAL')
    if state.get('s1')=='SEALED' and not can_seal_audio(state.get('audio_lock_evidence',{})):
        errors.append('S1_SEAL_WITHOUT_REQUIRED_AUDIO_EVIDENCE')
    if state.get('selected_song_family') is None and state.get('s1')=='SEALED':errors.append('SEALED_AUDIO_WITHOUT_SELECTED_SONG')
    if state.get('selected_song_family') in state.get('rejected_song_families',[]) and state.get('selected_song_family') is not None:errors.append('REJECTED_SONG_RESELECTED')
    branch=state.get('validation_branch')
    if branch and branch.get('purpose')!='VALIDATION_ONLY_NOT_PRODUCTION_LOCK':errors.append('TEST_SCOPE_UNDECLARED')
    if branch and (branch.get('allow_s1_seal') or branch.get('allow_s2')):errors.append('TEST_BRANCH_PROMOTED_WITHOUT_HUMAN_LOCK')
    return {'validator':'CURRENT_RUN_STATE_VALIDATOR_V0_5','status':'PASS' if not errors else 'FAIL','meaning':'State consistency only; PASS is not an audio review or stage seal.','errors':errors,'production_s1_sealed':state.get('s1')=='SEALED','source_screen_is_audio_lock':False}
