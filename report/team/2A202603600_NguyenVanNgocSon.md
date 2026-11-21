# Báo cáo cá nhân — NguyenVanNgocSon-2A202603600

## 1. Thông tin thành viên

- Họ tên: Nguyễn Văn Ngọc Sơn
- MSSV: 2A202603600
- GitHub: kynnnS
- Vai trong nhóm: Người viết code (P1)

## 2. Phần việc phụ trách

- Viết và chạy `src/lab13.py`: CP1 (A1–A4), CP2 (B1–B4), D1 của CP4. Điền A1–A4 trong `report/team/bang_chi_phi.md`.

## 3. Đóng góp cụ thể

- A1: `so_lan_chay_ky_vong`, `ti_le_thanh_cong`, `he_so_chi_phi_moi_viec_thanh_cong`, có kiểm tra miền p ∈ [0, 1] và k ≥ 1. Ba phép thử ĐẠT (1,20 · 1,25 · 1,25).
- A2: `mo_hinh` lấy token + tool trên mọi lần chạy, kể cả lần lỗi, vì công ty trả tiền cho mọi lần chạy. Mẫu số chỉ đếm `ket_qua == 'thanh_cong'`, vì chỉ việc thành công mới tạo giá trị. Kết quả 4.472 đ/việc = 16,3× hoá đơn token + tool mỗi yêu cầu [simulated].
- A3, A4:
  - quoc_te 1,88×, chạy lại lần 3 chỉ ok 2,2% [simulated];
  - phạm vi noi_dia + hang_nang cộng cố định ra 4.599 đ = 0,38× [simulated];
  - hoà vốn ở 4.659 việc thành công/tháng.
- B1–B4 và D1:
  - 9 kịch bản cộng 1 cặp, giới hạn 1/2/3 lần chạy (giới hạn 2 lần rẻ nhất cho công ty);
  - xem lại 100% ra 11.743 đ = 0,98× [simulated];
  - năm câu D1: 1.251 · 3.103 = 42 người mỗi nhóm · 1.000 · 300 · m ≥ 299, power 0,64.

## 4. Bằng chứng

- Commit `25bb25e`, `a5e97e5`, `972733f` (CP1) và commit thêm CP2 + D1 vào `src/lab13.py`.
- Output `cd src && python lab13.py`: exit 0, in A1 ĐẠT, A2, A3, A4, B1–B4, D1.

## 5. Công cụ AI đã dùng

- Claude Code (Claude Opus 5.5): gợi ý code, soát lỗi, viết script kiểm thử.
- Cách tôi tự kiểm tra:
  - Tính lại A2 bằng cách khác: gộp theo yêu cầu rồi mới nhân giá.
  - Tính B1 không qua `mo_hinh`.
  - Kiểm tra A1 theo tổng Σ(1 − p)^(i−1).
  - Kiểm tra power bằng hai cách: statsmodels và công thức arcsine.
  - So từng số với bảng tham chiếu trong hướng dẫn (ngưỡng 2%) và với `tools/p2_verify.py` do người kiểm số viết độc lập.
  - Kiểm tra hàm không sửa DataFrame đầu vào và không sửa hai CSV (hash).
- Không dùng AI để tạo số. Mọi số trong hồ sơ là output của `lab13.py`.

## 6. Tự đánh giá

- Làm được: `lab13.py` chạy hết và in đủ A, B, D1; mọi số khớp tham chiếu và khớp phần kiểm độc lập của P2.
- Hạn chế:
  - Chi phí cả hệ thống cộng 12.000 đ cho cả 74 ca `lam_lai` nên có thể tính trùng một phần.
  - Chưa chạy thử trên máy Windows của thành viên khác.
