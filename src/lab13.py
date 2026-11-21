"""Lab 13 · Định giá agent và lập kế hoạch pilot (Gate 2a) — bài làm của nhóm (file nộp).
Chạy trong thư mục src/: python3 lab13.py   (cần pandas; Nhiệm vụ D cần thêm statsmodels)
Không cần khoá API. Đã viết CP1 (A1–A4), CP2 (B1–B4), CP4 (D1). Dữ liệu trong hai file CSV là giả lập.
Bản gốc chưa sửa nằm ở lab13_starter.py.
"""
import math
import numbers
import sys
from statistics import NormalDist
import pandas as pd

# Bảng giá GIẢ ĐỊNH của lab (không phải giá thật của nhà cung cấp nào)
GIA_VAO = 26        # đồng cho 1.000 token đầu vào
GIA_RA = 130        # đồng cho 1.000 token đầu ra
GIA_TOOL = 15       # đồng cho 1 lần gọi tool
LUONG_PHUT = 2000   # đồng cho 1 phút của nhân viên (đã gồm bảo hiểm, văn phòng)
BASELINE = 12000    # đồng cho 1 yêu cầu khi nhân viên tự làm (6 phút)


# ---------- Nhiệm vụ A1 · Kinh tế của việc chạy lại ----------
# CP1: ba hàm dưới đây đã viết xong, kiem_tra_dap_an_biet_truoc() in ĐẠT.
def _kiem_tra_p_k(p, k):
    """Miền hợp lệ: 0 ≤ p ≤ 1; k là số nguyên ≥ 1 hoặc None (chạy đến khi đúng)."""
    if isinstance(p, bool) or not isinstance(p, numbers.Real) or math.isnan(p) or not 0 <= p <= 1:
        raise ValueError(f'p phải là xác suất trong [0, 1], nhận {p!r}')
    if k is not None and (isinstance(k, bool) or not isinstance(k, numbers.Integral) or k < 1):
        raise ValueError(f'k phải là số nguyên ≥ 1 hoặc None, nhận {k!r}')


def so_lan_chay_ky_vong(p, k=None):
    """Số lần chạy trung bình cho 1 yêu cầu khi mỗi lần đúng với xác suất p.
    k = số lần chạy tối đa; k=None nghĩa là chạy lại đến khi đúng."""
    _kiem_tra_p_k(p, k)
    if p == 0:  # không lần nào đúng: chạy đủ k lần, hoặc chạy mãi nếu không giới hạn
        return math.inf if k is None else float(k)
    if k is None:
        return 1 / p
    return (1 - (1 - p) ** k) / p


def ti_le_thanh_cong(p, k=None):
    """Xác suất yêu cầu thành công sau tối đa k lần chạy."""
    _kiem_tra_p_k(p, k)
    if k is None:
        return 1.0 if p > 0 else 0.0
    return 1 - (1 - p) ** k


def he_so_chi_phi_moi_viec_thanh_cong(p, k=None):
    """Chi phí mỗi việc thành công, tính bằng bội số của giá một lần chạy."""
    p_thanh_cong = ti_le_thanh_cong(p, k)
    if p_thanh_cong == 0:  # không có việc thành công nào để chia
        return math.inf
    return so_lan_chay_ky_vong(p, k) / p_thanh_cong


def kiem_tra_dap_an_biet_truoc():
    """Ba phép thử bắt buộc đạt 100% trước khi tính trên dữ liệu."""
    assert abs(so_lan_chay_ky_vong(0.8, 2) - 1.20) < 1e-9, 'p=0,8, tối đa 2 lần → 1,20 lần chạy'
    assert abs(so_lan_chay_ky_vong(0.8) - 1.25) < 1e-9, 'p=0,8, chạy đến khi đúng → 1,25 lần chạy'
    assert abs(he_so_chi_phi_moi_viec_thanh_cong(0.8, 3) - 1.25) < 1e-9, 'p=0,8, tối đa 3 lần → 1,25 lần giá một lần chạy'
    print('Ba phép thử đáp án biết trước: ĐẠT')


def kiem_tra_bien_a1():
    """Phép thử biên bổ sung (không thay ba phép thử bắt buộc ở trên)."""
    assert ti_le_thanh_cong(0.8, 2) == 1 - 0.2 ** 2                      # 0,96
    assert so_lan_chay_ky_vong(1.0, 3) == 1 and ti_le_thanh_cong(1.0) == 1  # luôn đúng ngay lần đầu
    assert so_lan_chay_ky_vong(0.8, 1) == 1                              # k = 1: đúng 1 lần chạy
    assert so_lan_chay_ky_vong(0.0, 3) == 3 and ti_le_thanh_cong(0.0, 3) == 0
    assert math.isinf(so_lan_chay_ky_vong(0.0)) and math.isinf(he_so_chi_phi_moi_viec_thanh_cong(0.0, 3))
    for p in (0.1, 0.3, 0.5, 0.8, 0.95):                                 # hệ số = 1/p với mọi k
        for k in (1, 2, 3, 10, None):
            assert abs(he_so_chi_phi_moi_viec_thanh_cong(p, k) - 1 / p) < 1e-9
        assert abs(so_lan_chay_ky_vong(p, 1000) - so_lan_chay_ky_vong(p)) < 1e-9  # k lớn → 1/p
    for p_sai, k_sai in ((-0.1, 2), (1.1, 2), (0.5, 0), (0.5, -1), (0.5, 2.5), (float('nan'), 2),
                         (float('inf'), 2), (True, 2), (0.5, True)):
        try:
            so_lan_chay_ky_vong(p_sai, k_sai)
        except ValueError:
            continue
        raise AssertionError(f'phải báo lỗi với p={p_sai}, k={k_sai}')
    print('Phép thử biên A1: ĐẠT')


def in_bang_a1():
    """In giá trị của ba phép thử để chép vào bảng A1 (phép thử nằm ở kiem_tra_dap_an_biet_truoc)."""
    print(f'  A1 (p = 0,8): tối đa 2 lần → {vn(so_lan_chay_ky_vong(0.8, 2), 2)} lần chạy · '
          f'đến khi đúng → {vn(so_lan_chay_ky_vong(0.8), 2)} lần chạy · '
          f'hệ số chi phí, tối đa 3 lần → {vn(he_so_chi_phi_moi_viec_thanh_cong(0.8, 3), 2)}')


# ---------- Nhiệm vụ A2 · Mô hình chi phí từ trace ----------
# CP1: mo_hinh đã viết xong; CP2 gọi lại hàm này với tham số giá và hệ số đã đổi.
COT_RUNS = ('run_id', 'request_id', 'attempt', 'tokens_in', 'tokens_out', 'tool_calls', 'status')
COT_REQS = ('request_id', 'loai', 'so_lan_chay', 'ket_qua',
            'phut_xem_lai_simulated', 'phut_lam_lai_simulated')


def kiem_tra_du_lieu(runs, reqs):
    """Kiểm tra cấu trúc hai bảng trước khi tính. Không sửa dữ liệu."""
    thieu = [c for c in COT_RUNS if c not in runs.columns] + [c for c in COT_REQS if c not in reqs.columns]
    assert not thieu, f'Thiếu cột: {thieu}'
    assert reqs['request_id'].is_unique, 'request_id trong logix_requests.csv bị trùng'
    assert runs['run_id'].is_unique, 'run_id trong logix_runs.csv bị trùng'
    assert not runs.duplicated(['request_id', 'attempt']).any(), 'một (request_id, attempt) xuất hiện hai lần'
    assert runs['request_id'].isin(reqs['request_id']).all(), 'có lần chạy không thuộc yêu cầu nào'
    so_run = runs.groupby('request_id').size()
    assert (reqs.set_index('request_id')['so_lan_chay'] == so_run.reindex(reqs['request_id']).fillna(0)).all(), \
        'so_lan_chay không khớp số dòng trong logix_runs.csv'
    assert reqs['ket_qua'].isin(['thanh_cong', 'lam_lai', 'chuyen_nhan_vien']).all(), 'ket_qua lạ'
    assert reqs['loai'].isin(LOAI).all(), 'loai lạ'
    assert runs['status'].isin(['ok', 'loi']).all(), 'status lạ'
    assert runs['attempt'].ge(1).all() and (runs.groupby('request_id')['attempt'].max() == so_run).all(), \
        'attempt không chạy liên tục từ 1'
    assert (runs[['tokens_in', 'tokens_out', 'tool_calls']] >= 0).all().all() and \
        (reqs[['phut_xem_lai_simulated', 'phut_lam_lai_simulated']] >= 0).all().all(), 'có giá trị âm'
    print(f'Dữ liệu: {vn(len(reqs))} yêu cầu, {vn(len(runs))} lần chạy, khoá và số lần chạy khớp nhau')


def mo_hinh(runs, reqs, gia_vao=26, gia_ra=130, gia_tool=15, luong_phut=2000,
            he_so_xem_lai=1.0, he_so_lam_lai=1.0, max_lan_chay=None):
    """Trả về dict gồm: token, tool, xem_lai, lam_lai, tong, thanh_cong, cps (chi phí mỗi việc thành công).
    - token, tool: cộng trên MỌI lần chạy trong runs, kể cả lần lỗi.
    - xem_lai, lam_lai: số phút (cột *_simulated) × LUONG_PHUT. Đây là số GIẢ LẬP, phải ghi nhãn simulated khi báo cáo.
    - thanh_cong: số yêu cầu có ket_qua == 'thanh_cong'.
    - Các tham số giá/hệ số/max_lan_chay dùng cho Nhiệm vụ B (độ nhạy, giới hạn số lần chạy); giữ mặc định ở A2.
    Thêm: chay_lai (token + tool của lần chạy attempt > 1, ĐÃ nằm trong token + tool, không cộng lại vào tong),
    hoa_don_moi_yc (token + tool chia số yêu cầu), so_yeu_cau, khong_thanh_cong, so_run.
    """
    if max_lan_chay is not None and (isinstance(max_lan_chay, bool)
                                     or not isinstance(max_lan_chay, numbers.Integral) or max_lan_chay < 1):
        raise ValueError(f'max_lan_chay phải là số nguyên ≥ 1 hoặc None, nhận {max_lan_chay!r}')
    reqs = reqs.copy()                                        # không sửa DataFrame của người gọi
    runs = runs[runs['request_id'].isin(reqs['request_id'])]  # chỉ giữ lần chạy của các yêu cầu đang xét
    if max_lan_chay is not None:  # B1, B3: bỏ lần chạy vượt giới hạn; yêu cầu cần nhiều lần hơn → chuyển nhân viên
        runs = runs[runs['attempt'] <= max_lan_chay]
        vuot = reqs['so_lan_chay'] > max_lan_chay
        reqs.loc[vuot, 'ket_qua'] = 'chuyen_nhan_vien'
        reqs.loc[vuot, ['phut_xem_lai_simulated', 'phut_lam_lai_simulated']] = 0
    tien_token = runs['tokens_in'] / 1000 * gia_vao + runs['tokens_out'] / 1000 * gia_ra  # giá cho 1.000 token
    tien_tool = runs['tool_calls'] * gia_tool
    token, tool = float(tien_token.sum()), float(tien_tool.sum())
    chay_lai = float((tien_token + tien_tool)[runs['attempt'] > 1].sum())
    xem_lai = float(reqs['phut_xem_lai_simulated'].sum() * luong_phut * he_so_xem_lai)  # simulated
    lam_lai = float(reqs['phut_lam_lai_simulated'].sum() * luong_phut * he_so_lam_lai)  # simulated
    tong = token + tool + xem_lai + lam_lai                  # tử số: mọi lần chạy, kể cả lần lỗi
    thanh_cong = int((reqs['ket_qua'] == 'thanh_cong').sum())  # mẫu số: chỉ việc thành công
    so_yeu_cau = len(reqs)
    return dict(token=token, tool=tool, chay_lai=chay_lai, xem_lai=xem_lai, lam_lai=lam_lai, tong=tong,
                thanh_cong=thanh_cong,
                cps=tong / thanh_cong if thanh_cong else math.inf,
                hoa_don_moi_yc=(token + tool) / so_yeu_cau if so_yeu_cau else math.nan,
                so_yeu_cau=so_yeu_cau, khong_thanh_cong=so_yeu_cau - thanh_cong, so_run=len(runs))


def vn(x, so_le=0):
    """Định dạng số kiểu Việt Nam: 4.373.585 · 274,7."""
    return f'{x:,.{so_le}f}'.replace(',', '_').replace('.', ',').replace('_', '.')


def in_bang_a2(kq, baseline=BASELINE):
    nv = kq['xem_lai'] + kq['lam_lai']
    ca_he_thong = (kq['tong'] + kq['khong_thanh_cong'] * baseline) / kq['so_yeu_cau']
    print('\nA2 · Mô hình chi phí từ trace (toàn bộ mẫu)')
    for nhan, khoa, so_le, ghi_chu in (
            ('Token (mọi lần chạy)', 'token', 0, 'đo từ trace'),
            ('Tool', 'tool', 0, 'đo từ trace'),
            ('  trong đó lần chạy 2 và 3', 'chay_lai', 0, 'đo từ trace, đã nằm trong token + tool'),
            ('Xem lại', 'xem_lai', 0, 'simulated'),
            ('Làm lại', 'lam_lai', 0, 'simulated'),
            ('Tổng chi phí trợ lý', 'tong', 0, 'simulated'),
            ('Số việc thành công', 'thanh_cong', 0, f"trên {vn(kq['so_yeu_cau'])} yêu cầu"),
            ('Chi phí mỗi việc thành công', 'cps', 0, 'simulated'),
            ('Hoá đơn token + tool / yêu cầu', 'hoa_don_moi_yc', 1, 'đo từ trace')):
        print(f'  {nhan:32s} {vn(kq[khoa], so_le):>12s}  {ghi_chu}')
    print(f"  Chi phí mỗi việc thành công / hoá đơn mỗi yêu cầu = {vn(kq['cps'] / kq['hoa_don_moi_yc'], 1)} lần")
    print(f"  Tỉ trọng: làm lại {vn(kq['lam_lai'] / kq['tong'] * 100, 1)}%, xem lại {vn(kq['xem_lai'] / kq['tong'] * 100, 1)}%, "
          f"token {vn(kq['token'] / kq['tong'] * 100, 1)}%, tool {vn(kq['tool'] / kq['tong'] * 100, 1)}% "
          f"(token + tool {vn((kq['token'] + kq['tool']) / kq['tong'] * 100, 1)}%); "
          f"giờ nhân viên {vn(nv / kq['tong'] * 100, 1)}% (simulated)")
    print(f"  Cả hệ thống / yêu cầu = (tổng + {kq['khong_thanh_cong']} ca không thành công × {vn(baseline)}) / "
          f"{vn(kq['so_yeu_cau'])} = {vn(ca_he_thong)} đ = {vn(ca_he_thong / baseline, 2)}× baseline (simulated)")


# ---------- Nhiệm vụ A3 · Tách theo loại yêu cầu ----------
LOAI = ('noi_dia', 'hang_nang', 'quoc_te', 'doi_tac')


def tach_theo_loai(runs, reqs, baseline=BASELINE):
    """Gọi lại mo_hinh cho từng loại; mo_hinh tự lọc runs theo request_id."""
    hang = []
    for loai in LOAI:
        kq = mo_hinh(runs, reqs[reqs['loai'] == loai])
        n = kq['so_yeu_cau'] or math.nan  # loại vắng mặt trong tập con → nan, không chia cho 0
        hang.append(dict(loai=loai, so_yeu_cau=kq['so_yeu_cau'], thanh_cong=kq['thanh_cong'],
                         ti_le_thanh_cong=kq['thanh_cong'] / n,
                         lan_chay_moi_yc=kq['so_run'] / n,
                         tong=kq['tong'], cps=kq['cps'], so_voi_baseline=kq['cps'] / baseline,
                         chay_lai=kq['chay_lai'], token_tool=kq['token'] + kq['tool'],
                         # cả hệ thống: cộng 12.000 đ cho mỗi yêu cầu không thành công vì nhân viên làm thay
                         ca_he_thong_moi_yc=(kq['tong'] + kq['khong_thanh_cong'] * baseline) / n))
    return pd.DataFrame(hang).set_index('loai')


def ti_le_ok_theo_lan_thu(runs, reqs):
    """Tỉ lệ status == 'ok' của từng lần thử (attempt 1, 2, 3) theo loại, kèm số lần chạy."""
    m = runs.merge(reqs[['request_id', 'loai']], on='request_id', validate='many_to_one')
    m = m.assign(ok=m['status'].eq('ok'))
    ti_le = m.pivot_table(index='loai', columns='attempt', values='ok', aggfunc='mean').reindex(list(LOAI))
    so_run = m.pivot_table(index='loai', columns='attempt', values='ok', aggfunc='size').reindex(list(LOAI))
    return ti_le, so_run


def in_bang_a3(runs, reqs):
    bang = tach_theo_loai(runs, reqs)
    print('\nA3 · Tách theo loại yêu cầu (chi phí mỗi việc thành công: simulated)')
    print(f"  {'loai':10s} {'yêu cầu':>8s} {'thành công':>14s} {'lần chạy/yc':>12s} {'CPS (đ)':>9s} {'so 12.000':>10s}"
          f" {'cả hệ thống/yc':>15s} {'chạy lại/(token+tool)':>22s}")
    for loai, h in bang.iterrows():
        print(f"  {loai:10s} {h['so_yeu_cau']:>8.0f} {h['thanh_cong']:>5.0f} = {vn(h['ti_le_thanh_cong'] * 100, 1):>5s}% "
              f"{vn(h['lan_chay_moi_yc'], 2):>12s} {vn(h['cps']):>9s} {vn(h['so_voi_baseline'], 2):>9s}×"
              f" {vn(h['ca_he_thong_moi_yc']):>9s} = {vn(h['ca_he_thong_moi_yc'] / BASELINE, 2)}×"
              f" {vn(h['chay_lai'])}/{vn(h['token_tool'])} = {vn(h['chay_lai'] / h['token_tool'] * 100, 0)}%")
    print('  Kết quả theo loại (số yêu cầu)')
    kq_loai = pd.crosstab(reqs['loai'], reqs['ket_qua']).reindex(list(LOAI)).fillna(0)
    kq_loai.loc['tổng'] = kq_loai.sum()
    for loai, h in kq_loai.iterrows():
        print(f"  {loai:10s} " + '  '.join(f'{c}: {h.get(c, 0):.0f}' for c in ('thanh_cong', 'lam_lai', 'chuyen_nhan_vien'))
              + f"  → không thành công: {h.get('lam_lai', 0) + h.get('chuyen_nhan_vien', 0):.0f}")
    ti_le, so_run = ti_le_ok_theo_lan_thu(runs, reqs)
    print('  Tỉ lệ lần chạy ok theo lần thử (số lần ok / số lần chạy trong ngoặc)')
    for loai in LOAI:
        o = '  '.join(f'lần {a}: {vn(ti_le.loc[loai, a] * 100, 1):>5s}% '
                      f'({ti_le.loc[loai, a] * so_run.loc[loai, a]:.0f}/{so_run.loc[loai, a]:.0f})'
                      for a in ti_le.columns)
        print(f'  {loai:10s} {o}')
    # Lợi ích biên của chạy lại: run ok ở attempt > 1 là lần ok đầu tiên (agent dừng khi ok)
    chay_lai = runs.merge(reqs[['request_id', 'loai', 'ket_qua']], on='request_id', validate='many_to_one')
    chay_lai = chay_lai[chay_lai['attempt'] > 1]
    print('  Chạy lại (attempt > 1): số lần chạy lại → số lần ok → số việc thành công thêm')
    for loai in LOAI:
        r = chay_lai[chay_lai['loai'] == loai]
        ok = r[r['status'] == 'ok']
        print(f"  {loai:10s} {len(r)} → {len(ok)} ok → {(ok['ket_qua'] == 'thanh_cong').sum()} thành công")
    return bang


# ---------- Nhiệm vụ A4 · Chi phí cố định ----------
CO_DINH_THANG = 40_000_000             # đồng / tháng
KHOI_LUONG_THANG = 45_000              # yêu cầu / tháng ở quy mô đầy đủ
PHAM_VI_PILOT = ('noi_dia', 'hang_nang')


def chi_phi_co_dinh(runs, reqs, khoi_luong=KHOI_LUONG_THANG, co_dinh=CO_DINH_THANG,
                    pham_vi=PHAM_VI_PILOT, baseline=BASELINE):
    """Cộng chi phí cố định vào chi phí mỗi việc thành công trong phạm vi pilot.
    Ngoại suy: việc thành công/tháng = khối lượng × (thành công trong phạm vi ÷ TOÀN BỘ mẫu)."""
    kq = mo_hinh(runs, reqs[reqs['loai'].isin(pham_vi)])
    ti_le = kq['thanh_cong'] / len(reqs) if len(reqs) else 0.0  # mẫu rỗng → 0 việc/tháng → cố định = inf
    viec_thang = khoi_luong * ti_le
    co_dinh_moi_viec = co_dinh / viec_thang if viec_thang else math.inf
    tong_moi_viec = kq['cps'] + co_dinh_moi_viec
    return dict(khoi_luong=khoi_luong, so_yeu_cau_pham_vi=kq['so_yeu_cau'], thanh_cong_pham_vi=kq['thanh_cong'],
                tong_pham_vi=kq['tong'], ti_le_tren_mau=ti_le, viec_thanh_cong_thang=viec_thang,
                co_dinh_moi_viec=co_dinh_moi_viec, bien_doi_moi_viec=kq['cps'],
                tong_moi_viec=tong_moi_viec, so_voi_baseline=tong_moi_viec / baseline)


def in_bang_a4(runs, reqs):
    print(f"\nA4 · Chi phí cố định {vn(CO_DINH_THANG)} đ/tháng, phạm vi {' + '.join(PHAM_VI_PILOT)} (simulated)")
    kq_a4 = []
    for khoi_luong in (KHOI_LUONG_THANG, KHOI_LUONG_THANG // 2):
        a = chi_phi_co_dinh(runs, reqs, khoi_luong=khoi_luong)
        kq_a4.append(a)
        print(f"  {vn(khoi_luong):>6s} yc/tháng: {a['thanh_cong_pham_vi']}/{vn(len(reqs))} = {vn(a['ti_le_tren_mau'] * 100, 1)}% "
              f"→ {vn(a['viec_thanh_cong_thang'])} việc/tháng; cố định {vn(a['co_dinh_moi_viec'])} đ + "
              f"biến đổi {vn(a['tong_pham_vi'])}/{a['thanh_cong_pham_vi']} = {vn(a['bien_doi_moi_viec'])} đ "
              f"= {vn(a['tong_moi_viec'])} đ = {vn(a['so_voi_baseline'], 2)}×")
    a = kq_a4[0]
    viec_hoa_von = CO_DINH_THANG / (BASELINE - a['bien_doi_moi_viec'])  # cố định + biến đổi = 12.000 đ
    print(f"  Hoà vốn với 12.000 đ: {vn(CO_DINH_THANG)} / (12.000 − {vn(a['bien_doi_moi_viec'])}) = "
          f"{vn(viec_hoa_von)} việc thành công/tháng ≈ {vn(viec_hoa_von / a['ti_le_tren_mau'])} yêu cầu/tháng")
    pv = mo_hinh(runs, reqs[reqs['loai'].isin(PHAM_VI_PILOT)])
    ca_he_thong = (pv['tong'] + pv['khong_thanh_cong'] * BASELINE) / pv['so_yeu_cau']
    print(f"  Cả hệ thống trong phạm vi (chưa gồm cố định) = ({vn(pv['tong'])} + {pv['khong_thanh_cong']} × 12.000) / "
          f"{pv['so_yeu_cau']} = {vn(ca_he_thong)} đ/yêu cầu = {vn(ca_he_thong / BASELINE, 2)}×")
    return kq_a4


# ---------- Nhiệm vụ B · Bảng độ nhạy ----------
# CP2: mỗi kịch bản là một lần gọi lại mo_hinh với một tham số đã đổi; không có con số nào viết tay.
KICH_BAN_B1 = {
    'Giá token gấp đôi': dict(gia_vao=GIA_VAO * 2, gia_ra=GIA_RA * 2),   # giá tool giữ nguyên
    'Giá token giảm một nửa': dict(gia_vao=GIA_VAO / 2, gia_ra=GIA_RA / 2),
    'Tỉ lệ xem lại gấp đôi': dict(he_so_xem_lai=2),
    'Tỉ lệ xem lại giảm một nửa': dict(he_so_xem_lai=0.5),
    'Số ca làm lại gấp đôi': dict(he_so_lam_lai=2),
    'Số ca làm lại giảm một nửa': dict(he_so_lam_lai=0.5),
    'Lương nhân viên tăng 25%': dict(luong_phut=LUONG_PHUT * 1.25),
    'Chỉ cho chạy tối đa 2 lần': dict(max_lan_chay=2),
    'Chỉ cho chạy 1 lần': dict(max_lan_chay=1),
}
YEU_TO_B1 = {  # gom kịch bản theo yếu tố để xếp hạng (B2)
    'số ca làm lại': ('Số ca làm lại gấp đôi', 'Số ca làm lại giảm một nửa'),
    'tỉ lệ xem lại': ('Tỉ lệ xem lại gấp đôi', 'Tỉ lệ xem lại giảm một nửa'),
    'lương nhân viên': ('Lương nhân viên tăng 25%',),
    'giới hạn số lần chạy': ('Chỉ cho chạy tối đa 2 lần', 'Chỉ cho chạy 1 lần'),
    'giá token': ('Giá token gấp đôi', 'Giá token giảm một nửa'),
}
CAP_B2 = dict(gia_vao=GIA_VAO * 2, gia_ra=GIA_RA * 2, he_so_xem_lai=2)  # giá token gấp đôi + xem lại gấp đôi


def _dau(x, so_le=1):
    """Số có dấu kiểu Việt Nam: +5,6 · −2,8."""
    return ('+' if x >= 0 else '−') + vn(abs(x), so_le)


def do_nhay(runs, reqs, kich_ban=KICH_BAN_B1):
    """B1: chi phí mỗi việc thành công của từng kịch bản và mức thay đổi so với gốc (tỉ lệ, 0,056 = +5,6%)."""
    goc = mo_hinh(runs, reqs)['cps']
    bang = {}
    for ten, kw in kich_ban.items():
        cps = mo_hinh(runs, reqs, **kw)['cps']
        bang[ten] = dict(cps=cps, thay_doi=cps / goc - 1)
    return goc, bang


def gioi_han_lan_chay(runs, reqs, cac_muc=(1, 2, 3), baseline=BASELINE):
    """B3: cả hệ thống = tổng chi phí trợ lý + 12.000 đ × số yêu cầu không thành công (nhân viên làm thay)."""
    bang = {}
    for m in cac_muc:
        kq = mo_hinh(runs, reqs, max_lan_chay=m)
        bang[m] = dict(tong=kq['tong'], khong_thanh_cong=kq['khong_thanh_cong'],
                       ca_he_thong=kq['tong'] + kq['khong_thanh_cong'] * baseline, cps=kq['cps'])
    return bang


def xem_lai_toan_bo(runs, reqs, phut_xem=5, phut_lam=9, pham_vi=PHAM_VI_PILOT,
                    luong_phut=LUONG_PHUT, baseline=BASELINE):
    """B4: trong phạm vi, mọi yêu cầu có ít nhất một lần chạy ok được xem lại phut_xem phút; mỗi ca lam_lai mất
    phut_lam phút; token + tool tính trên mọi lần chạy của phạm vi. Số phút là giả định → kết quả simulated."""
    pv = reqs[reqs['loai'].isin(pham_vi)]
    kq = mo_hinh(runs, pv)                                   # token + tool và số việc thành công của phạm vi
    r = runs[runs['request_id'].isin(pv['request_id'])]
    so_xem = int(r.loc[r['status'] == 'ok', 'request_id'].nunique())
    so_lam = int((pv['ket_qua'] == 'lam_lai').sum())
    token_tool = kq['token'] + kq['tool']
    tien_xem, tien_lam = so_xem * phut_xem * luong_phut, so_lam * phut_lam * luong_phut
    tong, tc = token_tool + tien_xem + tien_lam, kq['thanh_cong']
    # phút xem lại tối đa để chi phí mỗi việc thành công không vượt 12.000 đ
    phut_hoa_von = (baseline * tc - token_tool - tien_lam) / (so_xem * luong_phut) if so_xem else math.inf
    return dict(so_yeu_cau=len(pv), so_xem=so_xem, so_lam=so_lam, phut_lam=phut_lam, token_tool=token_tool,
                tien_xem=tien_xem, tien_lam=tien_lam, tong=tong, thanh_cong=tc,
                cps=tong / tc if tc else math.inf, phut_xem_hoa_von=phut_hoa_von)


def in_bang_b(runs, reqs):
    goc, b1 = do_nhay(runs, reqs)
    print('\nB1 · Độ nhạy, đổi từng yếu tố (chi phí mỗi việc thành công: simulated)')
    print(f"  {'Gốc (A2)':28s} {vn(goc):>7s} đ")
    for ten, h in b1.items():
        print(f"  {ten:28s} {vn(h['cps']):>7s} đ {_dau(h['thay_doi'] * 100):>7s}%")
    # Tự kiểm tra của CP2: mô hình cộng tuyến tính nên "giảm một nửa" = −½ mức thay đổi của "gấp đôi"
    for yt in ('giá token', 'tỉ lệ xem lại', 'số ca làm lại'):
        gap_doi, nua = YEU_TO_B1[yt]
        assert math.isclose(b1[nua]['thay_doi'], -b1[gap_doi]['thay_doi'] / 2, rel_tol=1e-9), yt
    print('  Tự kiểm tra: mỗi kịch bản "giảm một nửa" thay đổi đúng −½ kịch bản "gấp đôi": ĐẠT')

    cap = mo_hinh(runs, reqs, **CAP_B2)['cps']
    rieng = (b1['Giá token gấp đôi']['thay_doi'], b1['Tỉ lệ xem lại gấp đôi']['thay_doi'])
    assert math.isclose(cap / goc - 1, sum(rieng), rel_tol=1e-9), 'B2 phải bằng tổng hai tác động riêng'
    print('\nB2 · Đổi một cặp và xếp hạng (simulated)')
    print(f'  Giá token gấp đôi + xem lại gấp đôi: {vn(cap)} đ ({_dau((cap / goc - 1) * 100)}%) '
          f'= {_dau(rieng[0] * 100)}% {_dau(rieng[1] * 100)}% (cộng tuyến tính)')
    anh_huong = {yt: max(abs(b1[t]['thay_doi']) for t in ts) for yt, ts in YEU_TO_B1.items()}
    xep_hang = sorted(anh_huong, key=anh_huong.get, reverse=True)
    print('  Xếp hạng theo |thay đổi| lớn nhất của mỗi yếu tố: '
          + ' · '.join(f'{i}. {yt} {vn(anh_huong[yt] * 100, 1)}%' for i, yt in enumerate(xep_hang, 1)))

    b3 = gioi_han_lan_chay(runs, reqs)
    print('\nB3 · Giới hạn số lần chạy (simulated; cả hệ thống = tổng trợ lý + không thành công × 12.000 đ)')
    print(f"  {'giới hạn':8s} {'tổng trợ lý':>12s} {'không TC':>9s} {'cả hệ thống':>12s} {'CPS':>7s}")
    for m, h in b3.items():
        print(f"  {m} lần     {vn(h['tong']):>12s} {h['khong_thanh_cong']:>9d} {vn(h['ca_he_thong']):>12s} {vn(h['cps']):>7s}")
    re_nhat = min(b3, key=lambda m: b3[m]['ca_he_thong'])
    cps_thap = min(b3, key=lambda m: b3[m]['cps'])
    print(f"  Rẻ nhất cho công ty: {re_nhat} lần ({vn(b3[re_nhat]['ca_he_thong'])} đ); CPS thấp nhất: {cps_thap} lần "
          f"({vn(b3[cps_thap]['cps'])} đ) → {'trùng' if re_nhat == cps_thap else 'KHÔNG trùng'}; giới hạn {cps_thap} lần "
          f"đẩy thêm {b3[cps_thap]['khong_thanh_cong'] - b3[re_nhat]['khong_thanh_cong']} yêu cầu sang nhân viên")

    lam_lai = reqs.loc[reqs['ket_qua'] == 'lam_lai', 'phut_lam_lai_simulated']
    phut_lam_du_lieu = round(float(lam_lai.mean()), 1)
    print(f"\nB4 · Xem lại 100%, phạm vi {' + '.join(PHAM_VI_PILOT)} (simulated)")
    print(f'  phut_lam_lai_simulated trên {len(lam_lai)} ca lam_lai: trung bình {vn(lam_lai.mean(), 2)}, '
          f'trung vị {vn(lam_lai.median(), 1)} phút (simulated)')
    b4 = []
    for phut_lam in (9, phut_lam_du_lieu):
        h = xem_lai_toan_bo(runs, reqs, phut_lam=phut_lam)
        b4.append(h)
        print(f"  Làm lại {vn(phut_lam, 1)} phút: {h['so_xem']}/{h['so_yeu_cau']} yêu cầu có lần chạy ok × 5 phút = "
              f"{vn(h['tien_xem'])} đ; {h['so_lam']} ca làm lại = {vn(h['tien_lam'])} đ; token + tool "
              f"{vn(h['token_tool'])} đ → {vn(h['tong'])} / {h['thanh_cong']} = {vn(h['cps'])} đ "
              f"= {vn(h['cps'] / BASELINE, 2)}×; xem lại chiếm {vn(h['tien_xem'] / h['tong'] * 100, 1)}%; "
              f"hoà vốn khi mỗi lần xem lại ≤ {vn(h['phut_xem_hoa_von'], 1)} phút")
    return dict(goc=goc, b1=b1, b2=cap, xep_hang=xep_hang, b3=b3, b4=b4)


# ---------- Nhiệm vụ D1 · Cỡ mẫu ----------
# CP4: cho sẵn baseline 0,70; mục tiêu +5 điểm; alpha 0,05; power 0,8; ICC 0,02.
P_HIEN_TAI, ALPHA, POWER, ICC = 0.70, 0.05, 0.80, 0.02
SO_NHAN_VIEN, YC_MOI_NGAY = 40, 1500  # 40 nhân viên CSKH; khoảng 1.500 yêu cầu/ngày


def co_mau(p1, p2, alpha=ALPHA, power=POWER):
    """Cỡ mẫu mỗi nhóm khi so hai tỉ lệ (công thức trong docs/du_lieu_va_cong_thuc.md), làm tròn lên."""
    za, zb = NormalDist().inv_cdf(1 - alpha / 2), NormalDist().inv_cdf(power)
    pb = (p1 + p2) / 2
    return math.ceil((za * math.sqrt(2 * pb * (1 - pb)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
                     / (p2 - p1) ** 2)


def he_so_thiet_ke(m, icc=ICC):
    return 1 + (m - 1) * icc


def m_toi_thieu(n_can, so_cum, icc=ICC):
    """m nhỏ nhất để c·m / (1 + (m − 1)·ICC) ≥ n_can; None nếu không đạt dù m lớn đến đâu (n_can ≥ c ÷ ICC)."""
    if n_can * icc >= so_cum:
        return None
    return math.ceil(n_can * (1 - icc) / (so_cum - n_can * icc))


def power_hai_ti_le(p1, p2, n, alpha=ALPHA):
    """Power của phép so hai tỉ lệ với n mỗi nhóm (statsmodels, như hướng dẫn D1).
    Máy chưa cài statsmodels: tính cùng công thức (Cohen's h, kiểm định hai phía) bằng NormalDist."""
    try:
        from statsmodels.stats.power import NormalIndPower
        from statsmodels.stats.proportion import proportion_effectsize
    except ImportError:
        from statistics import NormalDist
        h = abs(2 * math.asin(math.sqrt(p2)) - 2 * math.asin(math.sqrt(p1)))
        z, d = NormalDist().inv_cdf(1 - alpha / 2), h * math.sqrt(n / 2)
        return NormalDist().cdf(d - z) + NormalDist().cdf(-d - z)
    return float(NormalIndPower().power(proportion_effectsize(p2, p1), nobs1=n, alpha=alpha, ratio=1.0))


def in_bang_d1(reqs):
    p5, p6 = round(P_HIEN_TAI + 0.05, 4), round(P_HIEN_TAI + 0.06, 4)
    n5 = co_mau(P_HIEN_TAI, p5)
    print(f'\nD1 · Cỡ mẫu (baseline {vn(P_HIEN_TAI, 2)}, alpha {vn(ALPHA, 2)}, power {vn(POWER, 1)}, ICC {vn(ICC, 2)})')
    print(f'  a) Chia theo yêu cầu, {vn(P_HIEN_TAI, 2)} → {vn(p5, 2)}: {vn(n5)} yêu cầu mỗi nhóm')
    m, de = 75, he_so_thiet_ke(75)
    n_b = math.ceil(n5 * de)
    nv_b = math.ceil(n_b / m)
    print(f'  b) Theo nhân viên, m = {m}: DE = 1 + {m - 1} × {vn(ICC, 2)} = {vn(de, 2)} → {vn(n5)} × {vn(de, 2)} = '
          f'{vn(n_b)} yêu cầu mỗi nhóm = {nv_b} nhân viên mỗi nhóm, tổng {2 * nv_b} '
          f"{'>' if 2 * nv_b > SO_NHAN_VIEN else '≤'} {SO_NHAN_VIEN}: {'KHÔNG ĐỦ NGƯỜI' if 2 * nv_b > SO_NHAN_VIEN else 'đủ'}")
    tran_c = 20 / ICC
    print(f"  c) 20 nhân viên mỗi nhóm: hiệu dụng < 20 ÷ {vn(ICC, 2)} = {vn(tran_c)} "
          f"{'<' if tran_c < n5 else '≥'} {vn(n5)}: {'KHÔNG ĐẠT dù m lớn đến đâu' if tran_c < n5 else 'đạt'}")
    tran_d = 6 / ICC
    print(f'  d) 6 depot mỗi nhóm: hiệu dụng < 6 ÷ {vn(ICC, 2)} = {vn(tran_d)} < {vn(n5)}; chỉ 6 cụm (< 20)')
    n6 = co_mau(P_HIEN_TAI, p6)
    m6 = m_toi_thieu(n6, 20)
    de6 = he_so_thiet_ke(m6)
    pw = power_hai_ti_le(P_HIEN_TAI, p5, n6)
    print(f'  e) Mức chênh 6 điểm: {vn(n6)} mỗi nhóm; 20 nhân viên mỗi nhóm cần m ≥ {m6} yêu cầu/người '
          f'(DE = {vn(de6, 2)}, hiệu dụng = {vn(20 * m6 / de6, 1)})')
    print(f'     Con số bất lợi: nếu tác động thật chỉ 5 điểm thì power với n = {vn(n6)} chỉ còn {vn(pw, 2)}')
    ti_le_pham_vi = reqs['loai'].isin(PHAM_VI_PILOT).mean()
    yc_nv_ngay = YC_MOI_NGAY / SO_NHAN_VIEN * ti_le_pham_vi
    print(f'     Đủ m ≥ {m6}: {vn(YC_MOI_NGAY)} yc/ngày ÷ {SO_NHAN_VIEN} nhân viên × {vn(ti_le_pham_vi * 100, 1)}% trong phạm vi '
          f'= {vn(yc_nv_ngay, 1)} yc/nhân viên/ngày → cần ≥ {math.ceil(m6 / yc_nv_ngay)} ngày; 14 ngày ≈ {vn(14 * yc_nv_ngay)} yc')
    return dict(n5=n5, de75=de, n_b=n_b, nv_b=nv_b, tran_c=tran_c, tran_d=tran_d, n6=n6, m6=m6, de6=de6, power_5=pw)


def in_ti_le_hien_tai(reqs):
    """Tỉ lệ trong đợt chạy thử (không có đối chứng: chỉ mô tả hiện trạng, không phải tác động của trợ lý).
    Dùng cho luật an toàn của CP4 và ba chỉ số E1 của CP5."""
    print('\nTỉ lệ hiện tại trong đợt chạy thử (cho luật dừng CP4 và chỉ số E1; không phải tác động của trợ lý)')
    pv = reqs['loai'].isin(PHAM_VI_PILOT)
    for ten, tap in (('toàn mẫu', reqs), (' + '.join(PHAM_VI_PILOT), reqs[pv])):
        chinh = ((tap['dong_trong_24h'] == 1) & (tap['mo_lai_trong_7_ngay'] == 0)).sum()
        xem = tap[tap['duoc_xem_lai'] == 1]
        bo_qua = xem['quyet_dinh_xem_lai'].isin(['sua', 'bo']).sum()
        mo_lai = (tap['mo_lai_trong_7_ngay'] == 1).sum()
        lam_lai = (tap['ket_qua'] == 'lam_lai').sum()
        n = len(tap)
        print(f'  {ten:20s} chính {chinh}/{vn(n)} = {vn(chinh / n * 100, 2)}% · bỏ qua gợi ý {bo_qua}/{len(xem)} = '
              f'{vn(bo_qua / len(xem) * 100, 2)}% · mở lại 7 ngày {mo_lai}/{vn(n)} = {vn(mo_lai / n * 100, 2)}% · '
              f'làm lại {lam_lai}/{vn(n)} = {vn(lam_lai / n * 100, 1)}%')
    print('  Mở lại 7 ngày theo loại: ' + ' · '.join(
        f"{loai} {vn(reqs.loc[reqs['loai'] == loai, 'mo_lai_trong_7_ngay'].mean() * 100, 2)}%" for loai in LOAI))


if __name__ == '__main__':
    for _s in (sys.stdout, sys.stderr):  # console Windows (cp1252) không in được tiếng Việt
        if hasattr(_s, 'reconfigure'):
            _s.reconfigure(encoding='utf-8')
    runs = pd.read_csv('logix_runs.csv')
    reqs = pd.read_csv('logix_requests.csv', keep_default_na=False)
    kiem_tra_dap_an_biet_truoc()
    in_bang_a1()
    kiem_tra_bien_a1()
    kiem_tra_du_lieu(runs, reqs)
    ket_qua = mo_hinh(runs, reqs)
    in_bang_a2(ket_qua)
    # CP1 · Nhiệm vụ A3: tính lại theo từng giá trị của cột loai.
    bang_a3 = in_bang_a3(runs, reqs)
    # CP1 · Nhiệm vụ A4: cộng chi phí cố định cho phạm vi noi_dia + hang_nang.
    kq_a4 = in_bang_a4(runs, reqs)
    # CP2 · Nhiệm vụ B: đổi từng yếu tố (B1), một cặp (B2), giới hạn số lần chạy (B3), xem lại 100% (B4).
    kq_b = in_bang_b(runs, reqs)
    # CP4 · Nhiệm vụ D1: cỡ mẫu theo yêu cầu, nhân viên, depot và mức chênh 6 điểm (power dùng statsmodels).
    kq_d1 = in_bang_d1(reqs)
    in_ti_le_hien_tai(reqs)
