# Báo cáo cá nhân — Nguyễn Bình An — 2A202603606

## 1. Thông tin thành viên

- Họ tên: Nguyễn Bình An
- MSSV: 2A202603606
- Email: 26ai.annb@vinuni.edu.vn
- Vai trong nhóm: Người kiểm số (P2).
- Nhóm: SaoCungDuoc · Lớp: L3A.
- Repo: https://github.com/VictorUIT/K5-L3A-DAY13-SaoCungDuoc-LaunchEconomics

## 2. Phần việc phụ trách

Kiểm số độc lập A1–A4, B1–B4, D1 và ba chỉ số E1 từ hai CSV gốc; ghi phép tính đối chiếu và bảng chi phí. Đã đối chiếu P1 tại commit `25bb25e`: 20/20 kịch bản A2/A3/A4/B1/B2/B3 và 222/222 giá trị khớp; B4, D1 và E1 hiện là kết quả độc lập P2.

## 3. Đóng góp cụ thể

- Tích hợp `tools/p2_verify.py` và 10 unit tests có sẵn từ gói bài làm P2; giữ nguyên code P1 và dữ liệu gốc.
- Tính lại bảng A/B từ 1.200 yêu cầu, 1.624 lần chạy; 31/31 phép đối chiếu với hướng dẫn đạt ngưỡng sai lệch ≤2%.
- Phép tính đối chiếu: 5.600 lượt tool × 15 đ = 84.000 đ; tổng chi phí 4.373.585,13 đ / 978 việc thành công = 4.471,97 đ/việc (simulated).
- Kiểm D1: 1.251 yêu cầu/nhóm cho chênh lệch 5 điểm phần trăm; cần 84 nhân viên tổng khi mỗi người có 75 yêu cầu, ICC=0,02.

## 4. Bằng chứng

- `report/team/bang_chi_phi.md`: bảng A1–A4 và B1–B4 tính từ CSV.
- `report/team/p2_doi_chieu_so.md`: công thức, D1, 31 dòng PASS tham chiếu, trạng thái `MATCHED` và 20 kịch bản đối chiếu P1.
- `report/team/p2_ket_qua.json`: số chưa làm tròn, thời điểm chạy UTC và kết quả đối chiếu.
- Chạy từ `src/`: `.venv/Scripts/python.exe -m unittest discover -s ../tests -p test_p2_verify.py -v` → 10/10 tests đạt; tests dùng dữ liệu tổng hợp, báo cáo dùng CSV gốc.
- Chạy từ `src/`: `.venv/Scripts/python.exe ../tools/p2_verify.py --src . --out ../report/team --strict --no-write` → 31/31 PASS, exit code 0.
- Chạy `--compare-p1 --strict` với commit P1 `25bb25e` → `MATCHED`, exit code 0; 7 khóa A2 khớp. Đối chiếu mở rộng đạt 222/222 giá trị, sai lệch bằng 0; chi tiết trong phiếu kiểm số và JSON.
- Commit P1 được đối chiếu: `25bb25e`; bằng chứng phần P2 nằm trong các file báo cáo và công cụ đi kèm.

## 5. Công cụ AI đã dùng

ChatGPT hỗ trợ cấu trúc công cụ và bản dự thảo; Codex hỗ trợ tích hợp, chạy tests và kiểm chứng trên CSV. Kết quả được kiểm bằng 10 tests, công thức đối chiếu và 31 số tham chiếu; các mục A2/A3/A4/B1/B2/B3 đã khớp P1. B4, D1 và E1 chưa có phần tương ứng trong P1 để so.

## 6. Tự đánh giá

Phần kiểm độc lập và đối chiếu P1 đã có bằng chứng cho các mục nêu trên; bàn giao và chốt hồ sơ nhóm còn chờ. CPS thấp nhất ở giới hạn 1 lần (4.111 đ/việc), nhưng giới hạn 2 lần cho tổng chi phí hệ thống thấp nhất (6.901.220 đ, simulated); khi chọn pilot cần tính cả chi phí xử lý các ca không thành công.
