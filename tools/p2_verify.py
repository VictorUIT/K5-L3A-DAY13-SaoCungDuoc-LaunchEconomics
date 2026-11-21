#!/usr/bin/env python3
"""Lab 13 — auxiliary, independent numerical verification for P2 (người kiểm số).

Never imports or changes P1's src/lab13.py unless --compare-p1 is explicitly set.
Never modifies source CSV data. Calculated evidence comes from CSV at execution.

Run at repo root:
    python tools/p2_verify.py --src src --out report/team
    python tools/p2_verify.py --src src --out report/team --compare-p1
"""
from __future__ import annotations
import argparse
import importlib.util
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from statistics import NormalDist
import pandas as pd

GIA_VAO=26.0
GIA_RA=130.0
GIA_TOOL=15.0
LUONG_PHUT=2000.0
BASELINE=12000.0
FIXED_MONTH=40_000_000.0
REQUIRED_RUN_COLUMNS={'request_id','attempt','tokens_in','tokens_out','tool_calls','status'}
REQUIRED_REQ_COLUMNS={'request_id','loai','ket_qua','so_lan_chay','phut_xem_lai_simulated','phut_lam_lai_simulated','duoc_xem_lai','quyet_dinh_xem_lai','dong_trong_24h','mo_lai_trong_7_ngay'}

REFERENCES={
    'A2.token':245585.0,'A2.tool':84000.0,'A2.retry_cost':93804.0,
    'A2.review':1780000.0,'A2.rework':2264000.0,'A2.total':4373585.0,
    'A2.success':978.0,'A2.cps':4472.0,'A2.invoice_per_req':274.7,
    'A4.full_cps_with_fixed':4599.0,'A4.half_cps_with_fixed':5784.0,
    'B1.token_double':4723.0,'B1.token_half':4346.0,
    'B1.review_double':6292.0,'B1.review_half':3562.0,
    'B1.rework_double':6787.0,'B1.rework_half':3315.0,
    'B1.salary_plus25':5506.0,'B1.cap2':4237.0,'B1.cap1':4111.0,
    'B2.both':6543.0,
    'B3.system_cap1':7449781.0,'B3.system_cap2':6901220.0,'B3.system_cap3':7037585.0,
    'B4.cps_9m':11743.0,'B4.cps_15_3m':12414.0,
    'D1.n_5pt':1251.0,'D1.n_6pt':859.0,
    'E1.primary_pct':82.83,'E1.ignore_pct':27.12,'E1.reopen_pct':4.25,
}
B1_SCENARIOS=[
    ('Giá token gấp đôi','token_double',dict(gia_vao=52,gia_ra=260)),
    ('Giá token giảm một nửa','token_half',dict(gia_vao=13,gia_ra=65)),
    ('Tỉ lệ xem lại gấp đôi','review_double',dict(he_so_xem_lai=2)),
    ('Tỉ lệ xem lại giảm một nửa','review_half',dict(he_so_xem_lai=0.5)),
    ('Số ca làm lại gấp đôi','rework_double',dict(he_so_lam_lai=2)),
    ('Số ca làm lại giảm một nửa','rework_half',dict(he_so_lam_lai=0.5)),
    ('Lương nhân viên tăng 25%','salary_plus25',dict(luong_phut=2500)),
    ('Tối đa 2 lần chạy','cap2',dict(max_lan_chay=2)),
    ('Chỉ 1 lần chạy','cap1',dict(max_lan_chay=1)),
]

def read_data(src: Path):
    rp,qp=src/'logix_runs.csv',src/'logix_requests.csv'
    if not rp.is_file() or not qp.is_file():
        raise FileNotFoundError(f'THIẾU DỮ LIỆU: cần {rp} và {qp} từ repo Lab 13. Không phải đợi P1; hãy clone/fork repo nhóm.')
    runs=pd.read_csv(rp)
    reqs=pd.read_csv(qp,keep_default_na=False)
    for name,df,required in [('runs',runs,REQUIRED_RUN_COLUMNS),('requests',reqs,REQUIRED_REQ_COLUMNS)]:
        missing=required-set(df.columns)
        if missing:
            raise ValueError(f'{name} thiếu các cột: {sorted(missing)}')
    if reqs.request_id.duplicated().any():
        raise ValueError('logix_requests.csv có request_id trùng, không thể tính đúng mẫu số')
    if not runs.request_id.isin(reqs.request_id).all():
        raise ValueError('Một số lần chạy không có request_id trong file requests')
    for c in ('tokens_in','tokens_out','tool_calls','attempt'):
        runs[c]=pd.to_numeric(runs[c],errors='raise')
    for c in ('phut_xem_lai_simulated','phut_lam_lai_simulated','so_lan_chay','duoc_xem_lai','dong_trong_24h','mo_lai_trong_7_ngay'):
        reqs[c]=pd.to_numeric(reqs[c],errors='raise')
    if len(runs)!=1624 or len(reqs)!=1200:
        print(f'CHÚ Ý: số hàng ({len(runs)} runs, {len(reqs)} requests) khác mô tả 1.624/1.200. Kiểm tra nguồn dữ liệu.')
    return runs,reqs


def model(runs,reqs,*,gia_vao=GIA_VAO,gia_ra=GIA_RA,gia_tool=GIA_TOOL,
          luong_phut=LUONG_PHUT,he_so_xem_lai=1.0,he_so_lam_lai=1.0,max_lan_chay=None):
    """A2, A3 and B. Counting failures in cost numerator is mandatory."""
    if reqs.empty: raise ValueError('reqs rỗng')
    q=reqs.copy()
    r=runs.loc[runs.request_id.isin(q.request_id)].copy()
    if max_lan_chay is not None:
        if int(max_lan_chay)!=max_lan_chay or max_lan_chay<1: raise ValueError('max_lan_chay >= 1')
        r=r.loc[r.attempt<=max_lan_chay]
        handoff=q.so_lan_chay>max_lan_chay
        q.loc[handoff,'ket_qua']='chuyen_nhan_vien'
        q.loc[handoff,['phut_xem_lai_simulated','phut_lam_lai_simulated']]=0
    money_token=r.tokens_in.div(1000).mul(gia_vao)+r.tokens_out.div(1000).mul(gia_ra)
    money_tool=r.tool_calls.mul(gia_tool)
    token=float(money_token.sum());tool=float(money_tool.sum())
    retry_cost=float((money_token+money_tool)[r.attempt>1].sum())
    review=float(q.phut_xem_lai_simulated.sum()*luong_phut*he_so_xem_lai)
    rework=float(q.phut_lam_lai_simulated.sum()*luong_phut*he_so_lam_lai)
    total=token+tool+review+rework
    success=int(q.ket_qua.eq('thanh_cong').sum())
    if not success: raise ZeroDivisionError('Không có ca thành công; CPS không xác định')
    return dict(token=token,tool=tool,retry_cost=retry_cost,review=review,rework=rework,
                total=total,success=success,unsuccessful=len(q)-success,requests=len(q),
                runs=len(r),cps=total/success,invoice_per_req=(token+tool)/len(q),
                review_minutes=float(q.phut_xem_lai_simulated.sum()),
                rework_minutes=float(q.phut_lam_lai_simulated.sum()),
                token_in=int(r.tokens_in.sum()),token_out=int(r.tokens_out.sum()),
                tool_calls=int(r.tool_calls.sum()))


def a1_numbers(p=.8):
    if not 0<p<=1: raise ValueError('0 < p <= 1')
    k2=(1-(1-p)**2)/p
    unbounded=1/p
    k3=(1-(1-p)**3)/p
    success3=1-(1-p)**3
    return dict(expected_2=k2,expected_unbounded=unbounded,
                cost_factor_3=k3/success3)


def n_per_arm(p1,p2,alpha=.05,power=.8):
    if not 0<p1<1 or not 0<p2<1 or p1==p2:raise ValueError('p1,p2 không hợp lệ')
    z_alpha=NormalDist().inv_cdf(1-alpha/2); z_power=NormalDist().inv_cdf(power)
    pbar=(p1+p2)/2
    numerator=(z_alpha*math.sqrt(2*pbar*(1-pbar))+
               z_power*math.sqrt(p1*(1-p1)+p2*(1-p2)))**2
    return math.ceil(numerator/(p2-p1)**2)


def d1_numbers():
    n5=n_per_arm(.70,.75)
    n6=n_per_arm(.70,.76)
    de75=1+(75-1)*.02
    needed=math.ceil(n5*de75)
    staff=math.ceil(needed/75)
    # Solve c*m/(1+(m-1)*icc) >= n6, with c=20.
    c,icc=20,.02
    min_m=math.ceil(n6*(1-icc)/(c-n6*icc))
    return dict(n_5pt=n5,n_6pt=n6,de_75=de75,raw_req_per_arm=needed,
                staff_per_arm=staff,staff_total=2*staff,max_staff_eff=20/.02,
                max_depot_eff=6/.02,m_for_6pt=min_m,de_at_m=1+(min_m-1)*icc)


def b4_numbers(runs,reqs):
    scoped=reqs[reqs.loai.isin(['noi_dia','hang_nang'])]
    subset=runs[runs.request_id.isin(scoped.request_id)]
    token_tool=float((subset.tokens_in.div(1000).mul(GIA_VAO)+subset.tokens_out.div(1000).mul(GIA_RA)+subset.tool_calls.mul(GIA_TOOL)).sum())
    n_review=int(subset.loc[subset.status.eq('ok'),'request_id'].nunique())
    rework_count=int(scoped.ket_qua.eq('lam_lai').sum())
    success=int(scoped.ket_qua.eq('thanh_cong').sum())
    if not success: raise ValueError('Không có việc thành công trong phạm vi')
    review_cost=n_review*5*LUONG_PHUT
    rework_9=rework_count*9*LUONG_PHUT
    rework_15_3=rework_count*15.3*LUONG_PHUT
    total9=token_tool+review_cost+rework_9
    total15=token_tool+review_cost+rework_15_3
    threshold9=(BASELINE*success-token_tool-rework_9)/(n_review*LUONG_PHUT)
    threshold15=(BASELINE*success-token_tool-rework_15_3)/(n_review*LUONG_PHUT)
    all_rework=reqs.loc[reqs.ket_qua.eq('lam_lai'),'phut_lam_lai_simulated']
    mean_rework=float(all_rework.mean()) if len(all_rework) else None
    return dict(scoped_requests=len(scoped),success=success,ok_requests=n_review,
                rework_count=rework_count,token_tool=token_tool,review_cost=review_cost,
                rework_9=rework_9,rework_15_3=rework_15_3,total9=total9,total15_3=total15,
                cps_9m=total9/success,cps_15_3m=total15/success,
                break_even_review_minutes_9m=threshold9,break_even_review_minutes_15_3m=threshold15,
                observed_mean_rework_minutes_simulated=mean_rework)


def e1_numbers(reqs):
    primary=100*float((reqs.dong_trong_24h.eq(1)&reqs.mo_lai_trong_7_ngay.eq(0)).mean())
    review_subset=reqs[reqs.duoc_xem_lai.eq(1)]
    ignored=100*float(review_subset.quyet_dinh_xem_lai.isin(['sua','bo']).mean()) if len(review_subset) else None
    reopened=100*float(reqs.mo_lai_trong_7_ngay.eq(1).mean())
    return dict(primary_pct=primary,ignore_pct=ignored,reopen_pct=reopened,
                reviewed=len(review_subset),ignored_count=int(review_subset.quyet_dinh_xem_lai.isin(['sua','bo']).sum()))


def calculate(runs,reqs):
    a2=model(runs,reqs)
    a3={category:model(runs,reqs[reqs.loai.eq(category)]) for category in ['noi_dia','hang_nang','quoc_te','doi_tac']}
    scoped=reqs[reqs.loai.isin(['noi_dia','hang_nang'])]
    a4_base=model(runs,scoped)
    monthly_success=45000*a4_base['success']/len(reqs)
    a4=dict(scoped_success=a4_base['success'],scoped_requests=len(scoped),scoped_cps=a4_base['cps'],monthly_success=monthly_success,
            full_fixed_per_success=FIXED_MONTH/monthly_success,
            full_cps_with_fixed=a4_base['cps']+FIXED_MONTH/monthly_success,
            half_fixed_per_success=FIXED_MONTH/(monthly_success/2),
            half_cps_with_fixed=a4_base['cps']+FIXED_MONTH/(monthly_success/2))
    b1=[]
    for label,key,kw in B1_SCENARIOS:
        m=model(runs,reqs,**kw)
        b1.append(dict(label=label,key=key,cps=m['cps'],delta_pct=(m['cps']/a2['cps']-1)*100,scenario=kw))
    both=model(runs,reqs,gia_vao=52,gia_ra=260,he_so_xem_lai=2)
    b2=dict(both=both['cps'],delta_pct=(both['cps']/a2['cps']-1)*100)
    b3=[]
    for cap in (1,2,3):
        m=model(runs,reqs,max_lan_chay=cap)
        b3.append(dict(cap=cap,agent_total=m['total'],unsuccessful=m['unsuccessful'],
                       system_total=m['total']+BASELINE*m['unsuccessful'],cps=m['cps']))
    qt_runs=runs[runs.request_id.isin(reqs.loc[reqs.loai.eq('quoc_te'),'request_id'])]
    qt_attempts={int(attempt):float(part.status.eq('ok').mean()*100)
                 for attempt,part in qt_runs.groupby('attempt')}
    return dict(a1=a1_numbers(),a2=a2,a3=a3,a4=a4,b1=b1,b2=b2,b3=b3,
                b4=b4_numbers(runs,reqs),d1=d1_numbers(),e1=e1_numbers(reqs),
                qt_attempts=qt_attempts)


def computed_reference_pairs(x):
    pairs={
       'A2.token':x['a2']['token'],'A2.tool':x['a2']['tool'],'A2.retry_cost':x['a2']['retry_cost'],
       'A2.review':x['a2']['review'],'A2.rework':x['a2']['rework'],'A2.total':x['a2']['total'],
       'A2.success':x['a2']['success'],'A2.cps':x['a2']['cps'],
       'A2.invoice_per_req':x['a2']['invoice_per_req'],
       'A4.full_cps_with_fixed':x['a4']['full_cps_with_fixed'],
       'A4.half_cps_with_fixed':x['a4']['half_cps_with_fixed'],
       'B2.both':x['b2']['both'],
       'B4.cps_9m':x['b4']['cps_9m'],'B4.cps_15_3m':x['b4']['cps_15_3m'],
       'D1.n_5pt':x['d1']['n_5pt'],'D1.n_6pt':x['d1']['n_6pt'],
       'E1.primary_pct':x['e1']['primary_pct'], 'E1.ignore_pct':x['e1']['ignore_pct'],
       'E1.reopen_pct':x['e1']['reopen_pct'],
    }
    for row in x['b1']:
        pairs['B1.'+row['key']]=row['cps']
    for row in x['b3']:
        pairs['B3.system_cap'+str(row['cap'])]=row['system_total']
    return pairs


def compare_reference(x,tolerance=.02):
    computed=computed_reference_pairs(x)
    lines=[]
    for key,ref in REFERENCES.items():
        value=computed[key]
        delta=abs(value-ref)/abs(ref) if ref else abs(value-ref)
        lines.append(dict(metric=key,calculated=value,reference=ref,relative_error_pct=100*delta,
                          status='PASS' if delta<=tolerance else 'FAIL'))
    return lines


def compare_p1(src,x,runs,reqs):
    path=src/'lab13.py'
    if not path.exists(): return {'status':'WAIT_P1','message':f'Không thấy {path}'}
    try:
        spec=importlib.util.spec_from_file_location('lab13_p1',path)
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not hasattr(module,'mo_hinh'):
            return {'status':'WAIT_P1','message':'P1 chưa có hàm mo_hinh()'}
        p1=module.mo_hinh(runs,reqs)
        mappings={'token':'token','tool':'tool','xem_lai':'review','lam_lai':'rework',
                  'tong':'total','thanh_cong':'success','cps':'cps'}
        comparisons={}
        for theirs,ours in mappings.items():
            if theirs not in p1:
                comparisons[theirs]={'status':'MISSING'}
            else:
                v1=float(p1[theirs]);v2=float(x['a2'][ours]);delta=abs(v1-v2)
                err=(delta/abs(v2)*100) if v2 else delta*100
                comparisons[theirs]={'p1':v1,'p2':v2,'diff':v1-v2,
                    'relative_error_pct':err,'status':'PASS' if err<=2 else 'FAIL'}
        status='MATCHED' if all(z['status']=='PASS' for z in comparisons.values()) else 'MISMATCH'
        return {'status':status,'details':comparisons}
    except Exception as exc:
        return {'status':'WAIT_P1','message':f'P1 chưa hoàn tất / chưa import được: {type(exc).__name__}: {exc}'}


def num(value,digits=0):
    return f'{value:,.{digits}f}'.replace(',','.') if digits==0 else f'{value:,.{digits}f}'


def make_official_report(x):
    a2,a3,a4,b1,b2,b3,b4=x['a2'],x['a3'],x['a4'],x['b1'],x['b2'],x['b3'],x['b4']
    a1=x['a1']
    s=['# Bảng chi phí · Nhiệm vụ A và B',
       '', '> **Nguồn:** `src/logix_runs.csv`, `src/logix_requests.csv`; P2 tính độc lập từ CSV bằng `tools/p2_verify.py`.',
       '> **Lưu ý:** mọi số sử dụng cột `_simulated` đều là **simulated**; chỉ số toàn mẫu chưa gồm chi phí cố định nếu chưa ghi rõ.',
       '', '## A1 · Ba phép thử đáp án biết trước',
       '', '| Phép thử (p = 0,8) | Kết quả |','|---|---:|',
       f"| Số lần chạy kỳ vọng, tối đa 2 lần | {a1['expected_2']:.2f} |",
       f"| Số lần chạy kỳ vọng, chạy đến khi đúng | {a1['expected_unbounded']:.2f} |",
       f"| Hệ số chi phí/việc thành công, tối đa 3 lần | {a1['cost_factor_3']:.2f} |",
       '', '## A2 · Mô hình chi phí từ trace',
       '', '| Khoản | Số lượng / Số tiền | Nguồn, nhãn |','|---|---:|---|',
       f"| Token | {num(a2['token'])} đ | Trace |",
       f"| Tool ({a2['tool_calls']} lần gọi) | {num(a2['tool'])} đ | Trace |",
       f"| Trong đó, lần chạy 2 và 3 | {num(a2['retry_cost'])} đ | Trace, đã bao gồm trong token + tool |",
       f"| Xem lại ({num(a2['review_minutes'])} phút) | {num(a2['review'])} đ | **simulated** |",
       f"| Làm lại ({num(a2['rework_minutes'])} phút) | {num(a2['rework'])} đ | **simulated** |",
       f"| Tổng | {num(a2['total'])} đ | Có thành phần **simulated** |",
       f"| Việc thành công | {a2['success']} | requests.ket_qua |",
       f"| Chi phí mỗi việc thành công | {num(a2['cps'])} đ | **simulated** |",
       f"| Hoá đơn token + tool chia tổng yêu cầu | {a2['invoice_per_req']:.1f} đ | Trace |",
       '',f"- CPS gấp **{a2['cps']/a2['invoice_per_req']:.1f} lần** hóa đơn token + tool chia số yêu cầu (simulated).",
       f"- Làm lại chiếm **{a2['rework']/a2['total']*100:.1f}%** tổng chi phí, lớn hơn xem lại ({a2['review']/a2['total']*100:.1f}%, simulated).",
       '', '## A3 · Tách theo loại yêu cầu',
       '', '| Loại | Yêu cầu | Thành công | Lần chạy/yêu cầu | CPS (simulated) | So 12.000 đ |',
       '|---|---:|---:|---:|---:|---:|']
    for typ,t in a3.items():
        s.append(f"| `{typ}` | {t['requests']} | {t['success']/t['requests']*100:.1f}% | {t['runs']/t['requests']:.2f} | {num(t['cps'])} đ | {t['cps']/BASELINE:.2f}× |")
    qt_attempts=x['qt_attempts']
    attempt_detail=', '.join(f'lần {i}: {v:.1f}%' for i,v in sorted(qt_attempts.items()))
    s+=['',f"- `quoc_te`: {a3['quoc_te']['cps']/BASELINE:.2f}× chi phí nhân viên và tỉ lệ thành công {a3['quoc_te']['success']/a3['quoc_te']['requests']*100:.1f}%; chưa nên đưa vào pilot (simulated).",
        f"- Tỉ lệ chạy `ok` riêng `quoc_te` theo attempt: {attempt_detail} (đo trace). Chạy lại không bảo đảm xử lý được lỗi lặp.",
        '', '## A4 · Chi phí cố định (noi_dia + hang_nang)',
        '', '| Khối lượng | Việc thành công/tháng | Cố định/việc | CPS + cố định (simulated) | So 12.000 đ |',
        '|---|---:|---:|---:|---:|',
        f"| 45.000 yc/tháng | {num(a4['monthly_success'])} | {num(a4['full_fixed_per_success'])} đ | {num(a4['full_cps_with_fixed'])} đ | {a4['full_cps_with_fixed']/BASELINE:.2f}× |",
        f"| Một nửa khối lượng | {num(a4['monthly_success']/2)} | {num(a4['half_fixed_per_success'])} đ | {num(a4['half_cps_with_fixed'])} đ | {a4['half_cps_with_fixed']/BASELINE:.2f}× |",
        '', '- Chi phí cố định tăng khi khối lượng giảm; chỉ áp dụng phép quy đổi giả định cho phạm vi `noi_dia + hang_nang` (simulated).',
        '', '## B1 · Độ nhạy: chín kịch bản',
        '', '| Kịch bản | CPS (simulated) | Thay đổi so với gốc |',
        '|---|---:|---:|']
    for b in b1:
        s.append(f"| {b['label']} | {num(b['cps'])} đ | {b['delta_pct']:+.1f}% |")
    s += ['', '## B2 · Đổi đồng thời hai tham số',
          '',f"- Token gấp đôi **và** xem lại gấp đôi: **{num(b2['both'])} đ/việc** ({b2['delta_pct']:+.1f}%, simulated).",
          '- Ba yếu tố nhạy nhất: **1. Làm lại → 2. Xem lại → 3. Chi phí nhân viên**.',
          '', '## B3 · Giới hạn số lần chạy',
          '', '| Giới hạn | Tổng Agent (simulated) | Không thành công | Cả hệ thống (simulated) | CPS Agent (simulated) |',
          '|---|---:|---:|---:|---:|']
    for b in b3:
        s.append(f"| {b['cap']} lần | {num(b['agent_total'])} đ | {b['unsuccessful']} | {num(b['system_total'])} đ | {num(b['cps'])} đ |")
    cheapest=min(b3,key=lambda z:z['system_total'])
    s += ['', f"- **{cheapest['cap']} lần** có tổng chi phí hệ thống thấp nhất ({num(cheapest['system_total'])} đ), khác với giới hạn có CPS thấp nhất (simulated).",
          '', '## B4 · Xem lại 100% trong phạm vi',
          '',f"- {b4['ok_requests']} yêu cầu cần xem lại, 5 phút/yêu cầu; {b4['rework_count']} ca làm lại, 9 phút/ca → CPS **{num(b4['cps_9m'])} đ**, bằng {b4['cps_9m']/BASELINE:.2f}× baseline (simulated).",
          f"- Nếu làm lại mất 15,3 phút/ca → CPS **{num(b4['cps_15_3m'])} đ**, bằng {b4['cps_15_3m']/BASELINE:.2f}× baseline (simulated).",
          f"- Để hòa vốn, thời gian xem lại phải không quá **{b4['break_even_review_minutes_9m']:.1f} phút** (làm lại 9 phút) hoặc **{b4['break_even_review_minutes_15_3m']:.1f} phút** (làm lại 15,3 phút).",
          '', '---',
          '### Trạng thái xác minh',
          '- **ĐÃ TÍNH TỪ CSV** bằng script độc lập P2. Đối chiếu với `src/lab13.py` của P1 chỉ hoàn tất sau khi P1 chạy xong.',
          '- Chi tiết sai lệch với tham chiếu: `report/team/p2_doi_chieu_so.md`.',
          '']
    return '\n'.join(s)


def make_check_report(x,checks,p1_compare=None):
    a2=x['a2'];d=x['d1']
    s=['# P2 · Hồ sơ kiểm số độc lập','',
       '## Trạng thái và nguồn','',
       '- Tính trên CSV trong repo theo công thức đề; **không** lấy đầu ra `src/lab13.py` làm kết quả kiểm độc lập.',
       '- Các khoản review/rework và kết quả suy ra từ chúng phải ghi **simulated**.',
       '- Kết quả bảng dưới đây được kiểm tra với **đáp án tham chiếu trong hướng dẫn** theo ngưỡng 2%; đây KHÔNG phải việc chấm đúng tuyệt đối P1.',
       '', '## Ít nhất một phép tính tay độc lập (bắt buộc P2)',
       '', f"1. Tool: **{a2['tool_calls']} lần × 15 đ/lần = {num(a2['tool'])} đ** (trace).",
       f"2. Xem lại: **{num(a2['review_minutes'])} phút × 2.000 đ/phút = {num(a2['review'])} đ**, simulated.",
       f"3. Làm lại: **{num(a2['rework_minutes'])} phút × 2.000 đ/phút = {num(a2['rework'])} đ**, simulated.",
       f"4. Tổng: {num(a2['token'])} + {num(a2['tool'])} + {num(a2['review'])} + {num(a2['rework'])} = **{num(a2['total'])} đ**, simulated.",
       f"5. CPS: {num(a2['total'])} / {a2['success']} = **{a2['cps']:.2f} đ/việc**, simulated.",
       f"6. B3 giới hạn 2: {num(x['b3'][1]['agent_total'])} + {x['b3'][1]['unsuccessful']} × 12.000 = **{num(x['b3'][1]['system_total'])} đ**, simulated.",
       '', '## D1 · Kiểm số cỡ mẫu và thiết kế pilot',
       '', '| Bài | Phép tính | Kết quả |','|---|---|---:|',
       f"| a | So hai tỉ lệ 0,70 và 0,75, alpha=0,05, power=0,80 | {d['n_5pt']} mỗi nhóm |",
       f"| b | DE = 1 + (75−1)×0,02 = {d['de_75']:.2f}; n=ceil({d['n_5pt']}×{d['de_75']:.2f}) | {d['raw_req_per_arm']} yc / {d['staff_per_arm']} nhân viên mỗi nhóm, {d['staff_total']} tổng |",
       f"| c | 20 nhân viên / ICC=0,02 | ≤ {num(d['max_staff_eff'])} hiệu dụng |",
       f"| d | 6 depot / ICC=0,02 | ≤ {num(d['max_depot_eff'])} hiệu dụng |",
       f"| e | MDE 6 điểm, n={d['n_6pt']}; 20m/(1+(m−1)×0,02) ≥ n | m ≥ {d['m_for_6pt']} yc/nhân viên |",
       '', '## Đối chiếu số với hướng dẫn (sai lệch tối đa 2%)',
       '', '| Mục | P2 tính từ CSV | Tham chiếu | Sai lệch | Kết quả |',
       '|---|---:|---:|---:|---|']
    for r in checks:
        s.append(f"| `{r['metric']}` | {r['calculated']:,.2f} | {r['reference']:,.2f} | {r['relative_error_pct']:.3f}% | {r['status']} |")
    s += ['', '## Đối chiếu với kết quả P1', '']
    if p1_compare is None:
        s.append('**CHỜ P1** — P1 cần hoàn tất `src/lab13.py`; sau đó chạy thêm `--compare-p1` để xác nhận các khóa kết quả chi phí.')
    else:
        s.append(f"**{p1_compare['status']}** — {p1_compare.get('message','')}")
        for k,v in p1_compare.get('details',{}).items():
            s.append(f"- `{k}`: {v}")
    s += ['', '## Phần P2 cần chốt sau khi các thành viên bàn giao',
          '', '- [ ] P1: in ba phép thử A1 ĐẠT; so `mo_hinh` với số P2, xử lý sai khác và ghi dấu vết kiểm.',
          '- [ ] P3/P4: dùng số đã xác nhận để hoàn thiện chỉ số và hồ sơ quyết định.',
          '- [ ] Nhóm trưởng: chốt báo cáo, duyệt chéo, merge và push; P2 dẫn commit bằng chứng trong báo cáo cá nhân.',
          '']
    return '\n'.join(s)


def main(argv=None):
    p=argparse.ArgumentParser(description='P2 - Người kiểm số, Lab13 LogiX-VN')
    p.add_argument('--src',type=Path,default=Path('src'),help='Thư mục có 2 CSV gốc')
    p.add_argument('--out',type=Path,default=Path('report/team'),help='Thư mục report/team')
    p.add_argument('--compare-p1',action='store_true',help='Chỉ bật sau khi P1 hoàn thành src/lab13.py')
    p.add_argument('--no-write',action='store_true',help='Chỉ in bảng kiểm mà không ghi file')
    p.add_argument('--strict',action='store_true',help='Exit code 2 nếu bất kỳ số tham chiếu nào lệch quá 2%')
    args=p.parse_args(argv)
    runs,reqs=read_data(args.src)
    x=calculate(runs,reqs)
    checks=compare_reference(x)
    passed=sum(v['status']=='PASS' for v in checks)
    print(f'CSV: {len(reqs)} requests, {len(runs)} runs')
    print(f'A2 CPS simulated: {x["a2"]["cps"]:,.2f} VND; tổng: {x["a2"]["total"]:,.0f} VND')
    print(f'B3 chi phí hệ thống, giới hạn 2 lần: {x["b3"][1]["system_total"]:,.0f} VND')
    print(f'D1 n(5 điểm): {x["d1"]["n_5pt"]} /nhóm')
    print(f'Tham chiếu: {passed}/{len(checks)} PASS (ngưỡng <=2%)')
    p1=None
    if args.compare_p1:
        p1=compare_p1(args.src,x,runs,reqs)
        print('So P1:',p1['status'])
        if 'message' in p1:print('  ',p1['message'])
    if not args.no_write:
        args.out.mkdir(parents=True,exist_ok=True)
        (args.out/'bang_chi_phi.md').write_text(make_official_report(x),encoding='utf-8')
        (args.out/'p2_doi_chieu_so.md').write_text(make_check_report(x,checks,p1),encoding='utf-8')
        payload=dict(timestamp_utc=datetime.now(timezone.utc).isoformat(),inputs=dict(requests=len(reqs),runs=len(runs)),results=x,
                     reference_checks=checks,p1_comparison=p1,note='Time-derived quantities are simulated')
        (args.out/'p2_ket_qua.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
        print(f'Đã ghi bang_chi_phi.md, p2_doi_chieu_so.md, p2_ket_qua.json tại {args.out}')
    if args.strict and passed!=len(checks):
        print('Có chỉ số lệch quá 2%; kiểm tra CSV, logic và tham chiếu.')
        return 2
    if args.compare_p1 and args.strict and p1['status']!='MATCHED':
        print('P1 chưa sẵn sàng hoặc số P1/P2 chưa khớp; cần đối chiếu trước khi chốt.')
        return 3
    return 0

if __name__=='__main__':
    raise SystemExit(main())
