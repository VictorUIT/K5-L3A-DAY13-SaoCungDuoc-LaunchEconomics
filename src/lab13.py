"""Lab 13 · Định giá agent và lập kế hoạch pilot (Gate 2a) — bài làm của nhóm (file nộp).
Chạy trong thư mục src/: python3 lab13.py   (cần pandas; Nhiệm vụ D cần thêm statsmodels)
Không cần khoá API. Điền các chỗ ghi VIẾT Ở ĐÂY (đánh dấu TODO CP1…CP4). Dữ liệu trong hai file CSV là giả lập.
Bản gốc chưa sửa nằm ở lab13_starter.py.
"""
import math
import numbers
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
    for p_sai, k_sai in ((-0.1, 2), (1.1, 2), (0.5, 0), (0.5, 2.5), (float('nan'), 2)):
        try:
            so_lan_chay_ky_vong(p_sai, k_sai)
        except ValueError:
            continue
        raise AssertionError(f'phải báo lỗi với p={p_sai}, k={k_sai}')
    print('Phép thử biên A1: ĐẠT')


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
          f"token {vn(kq['token'] / kq['tong'] * 100, 1)}%, tool {vn(kq['tool'] / kq['tong'] * 100, 1)}%; "
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
        hang.append(dict(loai=loai, so_yeu_cau=kq['so_yeu_cau'], thanh_cong=kq['thanh_cong'],
                         ti_le_thanh_cong=kq['thanh_cong'] / kq['so_yeu_cau'],
                         lan_chay_moi_yc=kq['so_run'] / kq['so_yeu_cau'],
                         tong=kq['tong'], cps=kq['cps'], so_voi_baseline=kq['cps'] / baseline,
                         chay_lai=kq['chay_lai'], token_tool=kq['token'] + kq['tool'],
                         # cả hệ thống: cộng 12.000 đ cho mỗi yêu cầu không thành công vì nhân viên làm thay
                         ca_he_thong_moi_yc=(kq['tong'] + kq['khong_thanh_cong'] * baseline) / kq['so_yeu_cau']))
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
    for loai, h in kq_loai.iterrows():
        print(f"  {loai:10s} " + '  '.join(f'{c}: {h.get(c, 0):.0f}' for c in ('thanh_cong', 'lam_lai', 'chuyen_nhan_vien')))
    ti_le, so_run = ti_le_ok_theo_lan_thu(runs, reqs)
    print('  Tỉ lệ lần chạy ok theo lần thử (số lần ok / số lần chạy trong ngoặc)')
    for loai in LOAI:
        o = '  '.join(f'lần {a}: {vn(ti_le.loc[loai, a] * 100, 1):>5s}% '
                      f'({ti_le.loc[loai, a] * so_run.loc[loai, a]:.0f}/{so_run.loc[loai, a]:.0f})'
                      for a in ti_le.columns)
        print(f'  {loai:10s} {o}')
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
    ti_le = kq['thanh_cong'] / len(reqs)
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
    return kq_a4


if __name__ == '__main__':
    runs = pd.read_csv('logix_runs.csv')
    reqs = pd.read_csv('logix_requests.csv', keep_default_na=False)
    kiem_tra_dap_an_biet_truoc()
    kiem_tra_bien_a1()
    kiem_tra_du_lieu(runs, reqs)
    ket_qua = mo_hinh(runs, reqs)
    in_bang_a2(ket_qua)
    # CP1 · Nhiệm vụ A3: tính lại theo từng giá trị của cột loai.
    bang_a3 = in_bang_a3(runs, reqs)
    # CP1 · Nhiệm vụ A4: cộng chi phí cố định cho phạm vi noi_dia + hang_nang.
    kq_a4 = in_bang_a4(runs, reqs)
    # TODO CP2 · Nhiệm vụ B: đổi từng yếu tố, ghi vào bảng độ nhạy.
    # TODO CP4 · Nhiệm vụ D: cỡ mẫu.
    #   from statsmodels.stats.proportion import proportion_effectsize
    #   from statsmodels.stats.power import NormalIndPower
