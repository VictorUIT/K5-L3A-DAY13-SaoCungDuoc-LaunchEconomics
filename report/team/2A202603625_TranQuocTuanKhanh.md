# Báo cáo cá nhân — TranQuocTuanKhanh-2A202603625

## 1. Thông tin thành viên

- Họ tên: Trần Quốc Tuấn Khanh
- MSSV: 2A202603625
- Email: 26ai.khanhtqt@vinuni.edu.vn
- GitHub: VictorUIT
- Vai trong nhóm: Người gắn nhãn 2 kiêm giữ hồ sơ (P4 – Pilot & Launch)

## 2. Phần việc phụ trách

- CP4: kế hoạch pilot `report/team/pilot_plan.yaml` (D1, D2, luật dừng, ngày quyết định).
- CP5: hồ sơ launch `report/team/ho_so_launch_v0.md`, đặc tả chỉ số và rủi ro `report/team/chi_so.md`, phiếu chấm hội đồng `report/team/phieu_cham.md`.
- CP3: gắn nhãn độc lập 20 ca lỗi (bộ nhãn người 2).
- Giữ repo: ghép nhánh, sửa lỗi chạy trên Windows, commit và push bản hồ sơ.

## 3. Đóng góp cụ thể

- **Pilot plan (CP4):** chia theo nhân viên 20 + 20, ngẫu nhiên phân tầng theo depot. Năm câu D1: 1.251 · 3.103 (42 người/nhóm, tổng 84 > 40) · tối đa 1.000 · tối đa 300 · m ≥ 299. Chấp nhận mức chênh 6 điểm (n = 859, DE 6,96) và ghi rõ power còn 0,64 nếu tác động thật là 5 điểm. Bốn luật dừng NẾU – TRONG – THÌ – KHÔNG THÌ (an toàn, sổ cái, chi phí, mức độ dùng). Ngày quyết định 2027-01-12, chừa 7 ngày theo dõi mở lại sau ngày đo cuối.
- **Hai con số bất lợi tự phát hiện từ dữ liệu:** (1) `hang_nang` mở lại 8,23% (13/158), vượt trần 6% nên luật an toàn so riêng với đối chứng cùng loại; (2) luật chi phí 8.000 đ/việc trong hướng dẫn mẫu sẽ kích ngay khi xem lại 100% (11.743 đ, B4) nên đổi sang 9.600 đ/yêu cầu = 0,8× của 12.000 đ, chừa 2.370 đ cố định khi khối lượng còn một nửa [simulated].
- **Hồ sơ launch (CP5):** bảy mục đều có con số, trạng thái, vai phụ trách; đề xuất Go có điều kiện cho noi_dia + hang_nang (cả hệ thống 4.131 đ/yêu cầu = 0,34× [simulated]) với 5 điều kiện có người phụ trách và ngày kiểm tra.
- **Chỉ số (E1, E2):** ba chỉ số trong đợt chạy thử 82,83% · 27,12% · 4,25%, kèm số trong phạm vi pilot; đề xuất thêm chỉ số dùng theo `arm` (phát hiện tràn tác động) và chỉ số an toàn qua kiểm tra mẫu hoàn sai tiền; 11 event có `trace_id`, nối với các ca trong bảng lỗi; 5 dòng rủi ro kinh tế lấy số từ bảng độ nhạy.
- **Duyệt chéo:** chấm nhóm 04552 (commit `92e0a70`), 30/30, Go có điều kiện; câu hỏi về việc bước 0.50 kéo dài 1 tuần chỉ cho khoảng 215 < 299 yêu cầu mỗi nhân viên.
- **CP3:** bộ nhãn người 2, trùng 18/20 = 90% với người 1; hai ca lệch 13, 17.
- **Kỹ thuật repo:** ghép nhánh `p1/cost-model` vào `main`; sửa lỗi in tiếng Việt trên console Windows ở `src/lab13.py` và `tools/p2_verify.py`; đổi `p2_verify.py` để chỉ ghi đè báo cáo khi có `--write` (bản cũ đã ghi đè lập luận A1–A4 của P1 khi chạy mặc định).

## 4. Bằng chứng

- Commit `05deb26`: `pilot_plan.yaml`, `ho_so_launch_v0.md`, `chi_so.md`, `phieu_cham.md`.
- Commit `a8abdd7` (ghép nhánh P1) và `f913894` (sửa UTF-8, cờ `--write`).
- Cột "Nhãn người 2" trong `report/team/bang_loi.md`.
- Tự kiểm tra: `python lab13.py` chạy hết, ba phép thử ĐẠT; `pilot_plan.yaml` đọc được bằng `yaml.safe_load` và không còn dấu `?` ngoài chú thích; không có từ "production" trong `report/team/`.

## 5. Công cụ AI đã dùng

- Claude Code (trong VS Code): đánh giá phần P1, P2; ghép nhánh và sửa lỗi encoding; tính lại D1, tỉ lệ mở lại theo loại và các chỉ số E1 từ CSV; soạn bản nháp `pilot_plan.yaml`, `ho_so_launch_v0.md`, `chi_so.md`, `phieu_cham.md`; tạo phiếu gắn nhãn 20 ca (không kèm đáp án).
- Bộ nhãn 20 ca lỗi do tôi tự gắn trên phiếu trống, không dùng AI và không xem đáp án trong hướng dẫn.
- Kiểm tra kết quả: mọi con số trong hồ sơ được tính lại từ `logix_requests.csv`, `logix_runs.csv` và đối chiếu với `bang_chi_phi.md`, `p2_doi_chieu_so.md` (31/31 số khớp tham chiếu trong ngưỡng 2%).

## 6. Tự đánh giá

- Làm được: CP4 và CP5 đủ yêu cầu "Xong khi"; hồ sơ nêu cả con số bất lợi (power 0,64; xem lại 100% là 0,98–1,03×; hang_nang mở lại 8,23%) kèm cách xử lý thay vì chỉ nêu số thuận lợi.
- Rút ra: ngưỡng dừng phải đặt sau khi nhìn tỉ lệ hiện tại và kịch bản xấu nhất của chính nhóm, nếu không luật dừng sẽ kích ngay tuần đầu; một kế hoạch đủ cỡ mẫu trên giấy vẫn cần lịch đủ dài để mỗi cụm đạt số yêu cầu tối thiểu.
- Cần cải thiện: luật dừng chi phí 9.600 đ/yêu cầu sẽ kích hết tuần 2 nếu vẫn xem lại 100% (11.764 đ/yêu cầu [simulated]), trước mốc giảm xem lại theo bậc; hội đồng đã hỏi đúng điểm này (xem `tra_loi_hoi_dong.md`).
