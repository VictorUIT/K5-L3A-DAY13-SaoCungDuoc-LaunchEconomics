"""Unit tests of independent checking logic (synthetic data, NOT lab source CSV)."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path
import pandas as pd

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import p2_verify as p2


def fixture():
    reqs=pd.DataFrame([
        dict(request_id='q1',loai='noi_dia',ket_qua='thanh_cong',so_lan_chay=2,
             phut_xem_lai_simulated=2.,phut_lam_lai_simulated=0.,duoc_xem_lai=1,
             quyet_dinh_xem_lai='giu',dong_trong_24h=1,mo_lai_trong_7_ngay=0),
        dict(request_id='q2',loai='hang_nang',ket_qua='lam_lai',so_lan_chay=1,
             phut_xem_lai_simulated=0.,phut_lam_lai_simulated=3.,duoc_xem_lai=0,
             quyet_dinh_xem_lai='',dong_trong_24h=0,mo_lai_trong_7_ngay=1),
        dict(request_id='q3',loai='noi_dia',ket_qua='thanh_cong',so_lan_chay=1,
             phut_xem_lai_simulated=1.,phut_lam_lai_simulated=0.,duoc_xem_lai=1,
             quyet_dinh_xem_lai='sua',dong_trong_24h=1,mo_lai_trong_7_ngay=0),
    ])
    runs=pd.DataFrame([
        dict(request_id='q1',attempt=1,tokens_in=1000,tokens_out=1000,tool_calls=1,status='loi'),
        dict(request_id='q1',attempt=2,tokens_in=1000,tokens_out=1000,tool_calls=1,status='ok'),
        dict(request_id='q2',attempt=1,tokens_in=1000,tokens_out=1000,tool_calls=1,status='loi'),
        dict(request_id='q3',attempt=1,tokens_in=1000,tokens_out=1000,tool_calls=1,status='ok'),
    ])
    return runs,reqs


class P2CheckTests(unittest.TestCase):
    def test_a1_known_answers(self):
        p=.8
        self.assertAlmostEqual((1-(1-p)**2)/p,1.2)
        self.assertAlmostEqual(1/p,1.25)
        self.assertAlmostEqual(((1-(1-p)**3)/p)/(1-(1-p)**3),1.25)

    def test_model_includes_failed_runs(self):
        r,q=fixture(); x=p2.model(r,q)
        self.assertEqual(x['runs'],4)
        self.assertEqual(x['success'],2)
        self.assertAlmostEqual(x['token'],4*(26+130))
        self.assertAlmostEqual(x['tool'],60)
        self.assertAlmostEqual(x['review'],6000)
        self.assertAlmostEqual(x['rework'],6000)
        self.assertAlmostEqual(x['total'],4*156+60+12000)
        self.assertAlmostEqual(x['cps'],(4*156+60+12000)/2)

    def test_retry_cost_is_subset_not_extra(self):
        r,q=fixture(); x=p2.model(r,q)
        self.assertAlmostEqual(x['retry_cost'],156+15)
        self.assertAlmostEqual(x['total'],x['token']+x['tool']+x['review']+x['rework'])

    def test_cap1_handoff_and_zero_review(self):
        r,q=fixture(); before=q.copy(deep=True)
        x=p2.model(r,q,max_lan_chay=1)
        self.assertEqual(x['success'],1)
        self.assertEqual(x['runs'],3)
        self.assertEqual(x['review'],2000)  # q1 handed off -> zero; q3 remains
        self.assertEqual(x['unsuccessful'],2)
        pd.testing.assert_frame_equal(q,before)  # original data unchanged

    def test_subtype_filters_runs(self):
        r,q=fixture()
        x=p2.model(r,q[q.loai.eq('noi_dia')])
        self.assertEqual(x['runs'],3)
        self.assertEqual(x['requests'],2)
        self.assertEqual(x['success'],2)
        with self.assertRaises(ZeroDivisionError):
            p2.model(r,q[q.loai.eq('hang_nang')])

    def test_linear_sensitivity(self):
        r,q=fixture(); origin=p2.model(r,q)
        doubled=p2.model(r,q,he_so_xem_lai=2)
        halved=p2.model(r,q,he_so_xem_lai=.5)
        self.assertAlmostEqual(doubled['total']-origin['total'],origin['review'])
        self.assertAlmostEqual(origin['total']-halved['total'],origin['review']/2)

    def test_d1_exact(self):
        x=p2.d1_numbers()
        self.assertEqual(x['n_5pt'],1251)
        self.assertEqual(x['n_6pt'],859)
        self.assertEqual(x['raw_req_per_arm'],3103)
        self.assertEqual(x['staff_total'],84)
        self.assertEqual(x['m_for_6pt'],299)

    def test_e1(self):
        r,q=fixture(); x=p2.e1_numbers(q)
        self.assertAlmostEqual(x['primary_pct'],200/3)
        self.assertAlmostEqual(x['ignore_pct'],50)
        self.assertAlmostEqual(x['reopen_pct'],100/3)

    def test_report_has_all_sections(self):
        r,q=fixture()
        # Add successful requests for two other types to exercise the whole pipeline.
        for name,typ in [('q4','quoc_te'),('q5','doi_tac'),('q6','hang_nang')]:
            row=q.iloc[2].copy()
            row['request_id']=name
            row['loai']=typ
            q=pd.concat([q,pd.DataFrame([row])],ignore_index=True)
            run=r.iloc[3].copy()
            run['request_id']=name
            r=pd.concat([r,pd.DataFrame([run])],ignore_index=True)
        x=p2.calculate(r,q)
        report=p2.make_official_report(x)
        for heading in ('## A1','## A2','## A3','## A4','## B1','## B2','## B3','## B4'):
            self.assertIn(heading,report)
        self.assertEqual(len(x['b1']),9)
        self.assertEqual(len(x['b3']),3)

    def test_missing_csv_is_clear(self):
        with self.assertRaises(FileNotFoundError) as e:
            p2.read_data(Path('/does-not-exist'))
        self.assertIn('THIẾU DỮ LIỆU',str(e.exception))

if __name__=='__main__':unittest.main()
