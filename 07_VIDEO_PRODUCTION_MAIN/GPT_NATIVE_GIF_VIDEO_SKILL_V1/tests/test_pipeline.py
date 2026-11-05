"""Regression cases for failures that matter to actual GIF/video production."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(ROOT/'tests'))
import gif_to_video as g
from fixtures import background, motion_frames, make_all, save_gif


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        cls.base=make_all(Path(cls.tmp.name))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def dest(self,name):
        return self.base/name

    def test_real_gif_signature_required(self):
        p=self.dest('fake.gif');Image.fromarray(background()).save(p,format='PNG')
        with self.assertRaisesRegex(ValueError,'genuine GIF'):g.decode_gif(p)

    def test_single_frame_rejected(self):
        with self.assertRaisesRegex(ValueError,'two decoded'):g.decode_gif(self.dest('static.gif'))

    def test_zero_delays_require_explicit_policy(self):
        p=self.dest('no_delay.gif');ims=[Image.fromarray(f) for f in motion_frames(3)]
        ims[0].save(p,save_all=True,append_images=ims[1:])
        with self.assertRaisesRegex(ValueError,'duration'):g.decode_gif(p)
        _,ds,m=g.decode_gif(p,default_duration_ms=100)
        self.assertEqual(ds,[100]*3);self.assertEqual(m['timing_override_frames'],[0,1,2])

    def test_variable_delays_read_without_flattening(self):
        _,ds,_=g.decode_gif(self.dest('variable.gif'));self.assertEqual(ds,[100,700,200])

    def test_disposal_restore_background_local_patch(self):
        f,ds,m=g.decode_gif(self.dest('disposal2.gif'))
        np.testing.assert_array_equal(f[1][22,12],[0,255,0])
        np.testing.assert_array_equal(f[2][22,12],[255,255,255])
        np.testing.assert_array_equal(f[2][62,42],[0,0,255])
        self.assertEqual(ds,[100,200,300]);self.assertEqual(m['disposal'][1],2)
        self.assertEqual(f[2].shape,(96,64,3))

    def test_disposal_restore_previous_local_patch(self):
        f,_,m=g.decode_gif(self.dest('disposal3.gif'))
        np.testing.assert_array_equal(f[1][22,12],[0,255,0])
        np.testing.assert_array_equal(f[2][22,12],[255,255,255])
        self.assertEqual(m['disposal'][1],3)

    def test_transparency_explicit_matte(self):
        f,_,m=g.decode_gif(self.dest('transparent.gif'),matte=(17,29,41))
        np.testing.assert_array_equal(f[0][0,0],[17,29,41])
        self.assertTrue(m['transparency_composited'])

    def test_time_map_respects_long_second_frame(self):
        records=g.timeline_map([100,700,200],10)
        self.assertEqual([r['source_index'] for r in records],[0,1,1,1,1,1,1,1,2,2])
        self.assertAlmostEqual(records[4]['alpha'],3/7)

    def test_30_to_120_provenance_not_subtraction(self):
        records=g.timeline_map([170]*30,120)
        from collections import Counter
        self.assertEqual(Counter(x['kind'] for x in records),
                         {'source_sample':30,'interpolated':87,'terminal_hold':3})

    def test_unaligned_timing_does_not_claim_all_native_samples(self):
        records=g.timeline_map([90,710,200],12)
        self.assertEqual(sum(x['kind']=='source_sample' for x in records),1)
        self.assertGreaterEqual(min(x['source_index'] for x in records),0)
        self.assertLessEqual(max(x['source_index'] for x in records),2)

    def test_original_onset_pixels_are_exactly_preserved(self):
        source=motion_frames();out,records,_=g.render_frames(source,120,[170]*30)
        for k in range(30):np.testing.assert_array_equal(out[k*4],source[k])

    def test_pair_flow_is_cached(self):
        source=motion_frames(4)
        original=g.pair_flow
        with patch.object(g,'pair_flow',wraps=original) as spy:
            _,_,calls=g.render_frames(source,16,[100]*4)
            self.assertEqual(spy.call_count,3);self.assertEqual(calls,6)

    def test_cached_warp_matches_original_pair_formula(self):
        a,b=motion_frames(2)
        np.testing.assert_array_equal(g.optical_between(a,b,.25),g.optical_between(a,b,.25,fields=g.pair_flow(a,b)))

    def test_blend_requires_no_flow(self):
        with patch.object(g,'pair_flow',side_effect=AssertionError('must not run')):
            _,_,calls=g.render_frames(motion_frames(3),12,[100]*3,method='blend')
            self.assertEqual(calls,0)

    def test_fixed_background_guard_accepts(self):
        f,_,_=g.decode_gif(self.dest('fixed.gif'));self.assertEqual(g.source_risks(f)['flags'],[])

    def test_scroll_guard_rejects(self):
        f,_,_=g.decode_gif(self.dest('scroll.gif'))
        self.assertIn('GLOBAL_DRIFT_OR_SCROLL',g.source_risks(f)['flags'])

    def test_grid_slip_guard_rejects(self):
        f,_,_=g.decode_gif(self.dest('grid_slip.gif'))
        self.assertIn('ABRUPT_CHANGE_OR_GRID_SLIP',g.source_risks(f)['flags'])

    def test_identical_animation_rejected_by_guard(self):
        f=motion_frames(2)[0]
        self.assertIn('STATIC_SOURCE',g.source_risks([f,f.copy()])['flags'])

    def test_centisecond_distribution_exact(self):
        ds=g.gif_delays(120,5)
        self.assertEqual(sum(ds),500);self.assertEqual(set(ds),{4,5})

    def test_unrepresentable_gif_timing_rejected(self):
        for count,sec in [(120,.5),(24,1.005)]:
            with self.assertRaises(ValueError):g.gif_delays(count,sec)

    def test_global_palette_keeps_fixed_background_losslessly_in_time(self):
        f=motion_frames(8);p=self.dest('palette.gif');g.encode_gif(f,p,1.)
        decoded,_,_=g.decode_gif(p)
        for a in decoded[1:]:np.testing.assert_array_equal(a[:40],decoded[0][:40])

    def test_gif_preserves_holds_without_faking_pixels(self):
        f=motion_frames(2);f=[f[0]]*4+[f[1]]*4
        p=self.dest('holds.gif');g.encode_gif(f,p,1.)
        d,ds,m=g.decode_gif(p)
        self.assertEqual(len(d),8);self.assertEqual(sum(ds),1000);self.assertEqual(m['version'],'GIF89a')
        np.testing.assert_array_equal(d[0],d[3]);self.assertIsNone(m['loop'])

    def test_loop_requires_explicit_request(self):
        p=self.dest('loop.gif');g.encode_gif(motion_frames(3),p,1.,loop=True)
        self.assertEqual(g.decode_gif(p)[2]['loop'],0)

    def test_full_9_16_encode_and_decode(self):
        f,ds,_=g.decode_gif(self.dest('fixed.gif'));out,_,_=g.render_frames(f,120,ds)
        gif,mp4=self.dest('full.gif'),self.dest('full.mp4')
        g.encode_gif(out,gif,5.);g.encode_mp4(out,mp4,24)
        v=g.verify_outputs(gif,mp4,120,24,5.,(90,160))
        self.assertEqual(v['full_decode'],'PASS');self.assertEqual(v['mp4']['width']*16,v['mp4']['height']*9)

    def test_odd_dimensions_pad_without_stretch(self):
        f=motion_frames(3,width=91,height=161);p=self.dest('odd.mp4')
        g.encode_mp4(f,p,24);v=g.probe_mp4(p)['streams'][0]
        self.assertEqual((v['width'],v['height']),(92,162))

    def test_audio_is_padded_to_video_duration(self):
        f=motion_frames(3);out,_,_=g.render_frames(f,120,[100]*3,method='blend')
        gif,mp4=self.dest('audio.gif'),self.dest('audio.mp4')
        g.encode_gif(out,gif,5.);g.encode_mp4(out,mp4,24,self.dest('tone.wav'))
        v=g.verify_outputs(gif,mp4,120,24,5.,(90,160),audio=True)
        self.assertEqual(v['audio_tracks'][0]['codec_name'],'aac')

    def test_truncated_mp4_fails_probe(self):
        p=self.dest('broken.mp4');p.write_bytes(b'\0\0\0\x20ftypisom')
        with self.assertRaises(subprocess.CalledProcessError):g.probe_mp4(p)

    def test_cli_source_review_gate_and_risk_rejection(self):
        def run(name,extra=()):
            return subprocess.run([sys.executable,str(ROOT/'scripts/gif_to_video.py'),
                '--input',str(self.dest(name+'.gif')),'--out',str(self.dest('cli_'+name)),*extra],capture_output=True,text=True)
        self.assertEqual(run('fixed').returncode,2)
        r=run('scroll',['--source-reviewed']);self.assertEqual(r.returncode,2)
        self.assertIn('SOURCE_REJECTED',r.stderr)
        self.assertFalse((self.dest('cli_scroll')/'animation.mp4').exists())

    def test_source_selection_preserves_original_frame_lineage(self):
        f,ds,m=g.decode_gif(self.dest('fixed.gif'))
        selected,delays,meta=g.select_source_range(f,ds,m,'0:15')
        self.assertEqual(len(selected),15);self.assertEqual(sum(delays),2550)
        self.assertEqual(meta['input_total_frames'],30)
        self.assertEqual(meta['selected_input_frame_indices'],list(range(15)))
        np.testing.assert_array_equal(selected[-1],f[14])

    def test_invalid_source_selection_rejected(self):
        f,ds,m=g.decode_gif(self.dest('fixed.gif'))
        for selection in ['0:1','-1:10','0:31','abc','0:2:3']:
            with self.assertRaises(ValueError):g.select_source_range(f,ds,m,selection)

    def test_ambiguous_midwarp_region_is_flagged_for_review(self):
        a=np.zeros((100,100,3),np.uint8);b=a.copy()
        a[20:60,20:40]=220;b[20:60,45:65]=220
        zero=np.zeros((100,100,2),np.float32)
        risk=g.flow_pair_risk(a,b,(zero,zero))
        self.assertEqual(risk['flag'],'OCCLUSION_OR_GHOST_RISK')
        self.assertGreater(risk['largest_disagreement_component_pixels'],64)

    def test_matching_midwarps_do_not_raise_ghost_signal(self):
        a=background();zero=np.zeros((*a.shape[:2],2),np.float32)
        self.assertIsNone(g.flow_pair_risk(a,a,(zero,zero))['flag'])

    def test_existing_output_directory_rejected(self):
        out=self.dest('existing');out.mkdir();(out/'qa_report.json').write_text('{}')
        r=subprocess.run([sys.executable,str(ROOT/'scripts/gif_to_video.py'),'--input',str(self.dest('fixed.gif')),
            '--out',str(out),'--source-reviewed'],capture_output=True,text=True)
        self.assertEqual(r.returncode,2);self.assertIn('empty',r.stderr)


if __name__=='__main__':unittest.main(verbosity=2)
