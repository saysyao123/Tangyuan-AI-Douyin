import unittest
from candidate_intake import evaluate_direction,rank_directions,screen_source,can_seal_audio,validate_current_state,failure_route

class RepairTests(unittest.TestCase):
    def direction(self,**changes):
        return dict(song_family='测试中文歌',history_policy='ELIGIBLE',source_tier='HISTORICAL_CORE_VERIFIED',language_support='HISTORICAL_CHINESE_REFERENCE',reference_leads=['https://example.org/song'],semantic_priority=1,**changes)
    def test_s0_does_not_require_audio_first(self):
        self.assertEqual(evaluate_direction(self.direction())['direction_status'],'ELIGIBLE')
    def test_all_declared_core_labels_normalize(self):
        for tier in ('HISTORICAL_CORE_VERIFIED','VERIFIED_CORE','HISTORICAL_VERIFIED_CORE','CURRENT_CORE_DIRECT'):
            c=self.direction();c['source_tier']=tier
            self.assertEqual(evaluate_direction(c)['source_group'],'CORE')
    def test_supplemental_lane_explicit_and_not_core(self):
        c=self.direction();c['source_tier']='SUPPLEMENTAL'
        self.assertEqual(evaluate_direction(c)['direction_status'],'HOLD')
        self.assertEqual(evaluate_direction(c,True)['source_group'],'SUPPLEMENTAL_TEST')
    def test_title_alone_fails_chinese_filter(self):
        c=self.direction();c['language_support']='TITLE_CHINESE'
        self.assertEqual(evaluate_direction(c)['direction_status'],'HOLD')
    def test_used_or_human_rejected_song_fails(self):
        for policy in ('HARD_EXCLUDE','REGRESSION_ONLY'):
            c=self.direction();c['history_policy']=policy
            self.assertEqual(evaluate_direction(c)['direction_status'],'HOLD')
        self.assertEqual(evaluate_direction(self.direction(human_rejected_for_run=True))['direction_status'],'HOLD')
    def test_unique_max_three_and_core_first(self):
        cs=[]
        for i in range(5):
            c=self.direction();c['song_family']=str(i);cs.append(c)
        cs.append(cs[0]);sup=self.direction();sup['song_family']='补充';sup['source_tier']='SUPPLEMENTAL';sup['semantic_priority']=100;cs.insert(0,sup)
        ranked=rank_directions(cs,True)
        self.assertEqual(len(ranked),3);self.assertEqual(len({c['song_family'] for c in ranked}),3)
        self.assertTrue(all(c['assessment']['source_group']=='CORE' for c in ranked))
    def test_page_only_recovers_source_without_rejecting_family(self):
        self.assertEqual(screen_source({'actual_media_exists':False})['route'],'RECOVER_SOURCE')
    def test_metadata_does_not_pass_lexical_screen(self):
        self.assertEqual(screen_source({'actual_media_exists':True,'identity_verified':True})['route'],'TRY_ALTERNATE_SOURCE_OR_CANDIDATE')
    def test_lexical_support_advances_analysis_but_never_seals(self):
        r=screen_source({'actual_media_exists':True,'identity_verified':True,'supporting_windows':2,'best_contiguous_match_chars':11})
        self.assertTrue(r['allow_full_analysis']);self.assertFalse(r['allow_s1_seal']);self.assertFalse(r['allow_final_cut']);self.assertFalse(r['allow_s2'])
    def test_human_failure_overrides_machine_support(self):
        r=screen_source({'actual_media_exists':True,'identity_verified':True,'supporting_windows':9,'best_contiguous_match_chars':100,'human_audio_review':'FAIL'})
        self.assertEqual(r['route'],'REJECT_CURRENT_SOURCE')
    def test_screen_threshold_is_for_analysis_not_truth(self):
        base={'actual_media_exists':True,'identity_verified':True}
        self.assertEqual(screen_source(base|{'supporting_windows':1,'best_contiguous_match_chars':50})['route'],'TRY_ALTERNATE_SOURCE_OR_CANDIDATE')
        self.assertEqual(screen_source(base|{'supporting_windows':2,'best_contiguous_match_chars':5})['route'],'TRY_ALTERNATE_SOURCE_OR_CANDIDATE')
        r=screen_source(base|{'supporting_windows':2,'best_contiguous_match_chars':6})
        self.assertTrue(r['allow_full_analysis']);self.assertFalse(r['allow_s1_seal'])
    def test_identity_check_precedes_content(self):
        self.assertEqual(screen_source({'actual_media_exists':True})['route'],'VERIFY_SOURCE_IDENTITY')
    def test_human_rejected_source_cannot_retry_by_new_window(self):
        r=screen_source({'sha256':'old','rejected_source_hashes':['old'],'actual_media_exists':True,'identity_verified':True,'supporting_windows':9,'best_contiguous_match_chars':50})
        self.assertEqual(r['route'],'SKIP_PREVIOUSLY_REJECTED_SOURCE')
    def test_failure_budget_has_exit(self):
        self.assertEqual(failure_route(1,1),'RECOVER_SAME_FAMILY_SOURCE')
        self.assertEqual(failure_route(2,1),'NEXT_CANDIDATE')
        self.assertEqual(failure_route(1,3),'STOP_WITH_EVIDENCE_SUMMARY')
    def test_final_audio_gate_requires_all_real_evidence(self):
        e=dict(actual_media_exists=True,identity_verified=True,sha256='a'*64,human_audio_review='PASS',audible_concrete_lyrics=True,version_locked=True,timeline_verified=True,phrase_boundaries_verified=True)
        self.assertTrue(can_seal_audio(e))
        for key in e:
            c=dict(e);c[key]='PENDING' if key=='human_audio_review' else False
            self.assertFalse(can_seal_audio(c))
    def test_current_state_accepts_honest_reopened_run(self):
        self.assertEqual(validate_current_state({'s0':'REOPENED','selected_song_family':None,'s1':'NOT_SEALED','s2':'BLOCKED'})['status'],'PASS')
    def test_missing_state_is_not_a_pass(self):
        self.assertEqual(validate_current_state({})['status'],'FAIL')
    def test_rejected_family_cannot_be_reselected(self):
        self.assertEqual(validate_current_state({'s0':'SEALED','s1':'NOT_SEALED','s2':'BLOCKED','selected_song_family':'告别','rejected_song_families':['告别']})['status'],'FAIL')
    def test_current_state_rejects_stale_seal_and_test_promotion(self):
        self.assertEqual(validate_current_state({'selected_song_family':'歌','s1':'SEALED','s2':'ALLOWED'})['status'],'FAIL')
        self.assertEqual(validate_current_state({'s1':'NOT_SEALED','s2':'ALLOWED'})['status'],'FAIL')
        self.assertEqual(validate_current_state({'s1':'NOT_SEALED','s2':'BLOCKED','validation_branch':{'purpose':'UNDECLARED','allow_s1_seal':True}})['status'],'FAIL')

if __name__=='__main__':unittest.main()
