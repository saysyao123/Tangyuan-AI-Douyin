"""Run-local S0 lyric-MV qualification; metadata cannot establish audibility."""
def qualify(candidate):
    reasons=[]
    for key,required in [('history_policy','ELIGIBLE'),('source_tier','VERIFIED_CORE'),('reference_media','VERIFIED'),('audible_chinese','PASS'),('continuous_meaningful_lyrics','PASS'),('semantic_visual_fit','PASS')]:
        if candidate.get(key)!=required:reasons.append(key.upper()+'_NOT_PASSED')
    if candidate.get('lyric_review_basis') not in ('HUMAN_LISTENING','INDEPENDENT_AUDIO_LISTENING'):
        reasons.append('ACTUAL_LISTENING_REVIEW_REQUIRED')
    if candidate.get('human_rejected'):
        reasons.insert(0,'HUMAN_REJECTED_CURRENT_REFERENCE')
    return {'qualification':'QUALIFIED_FOR_CHOICE' if not reasons else 'NOT_QUALIFIED','blockers':reasons,'s0_sealed':False}

def regression_checks():
    ok={'history_policy':'ELIGIBLE','source_tier':'VERIFIED_CORE','reference_media':'VERIFIED','audible_chinese':'PASS','continuous_meaningful_lyrics':'PASS','semantic_visual_fit':'PASS','lyric_review_basis':'INDEPENDENT_AUDIO_LISTENING','human_rejected':False}
    assert qualify(ok)['qualification']=='QUALIFIED_FOR_CHOICE'
    n=1
    for key,value in [('history_policy','HARD_EXCLUDE'),('history_policy','REGRESSION_ONLY'),('source_tier','SUPPLEMENTAL'),('reference_media','PAGE_200_ONLY'),('audible_chinese','METADATA_CHINESE'),('continuous_meaningful_lyrics','LYRICS_PAGE_PRESENT'),('semantic_visual_fit','INSUFFICIENT'),('lyric_review_basis','ASR_ONLY'),('lyric_review_basis','FORCED_ALIGNMENT_ONLY'),('human_rejected',True)]:
        assert qualify(ok|{key:value})['qualification']=='NOT_QUALIFIED';n+=1
    assert not qualify(ok)['s0_sealed'];n+=1
    return {'status':'PASS','case_count':n,'meaning':'Qualification is separate from human song lock and stage seal.'}
