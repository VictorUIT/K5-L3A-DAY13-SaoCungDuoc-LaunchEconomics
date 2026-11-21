# Báo cáo nhóm

Báo cáo ngắn, tối đa 2 trang. Số liệu chi tiết nằm trong các file hồ sơ; ở đây chỉ dẫn lại con số chính.

## 1. Thông tin nhóm

- Tên nhóm: SaoCungDuoc
- Lớp: L3A
- Thành viên: xem `TEAM.md`

## 2. Mục tiêu và cách tiếp cận

Quyết định ở Gate 2a có nên cho trợ lý hoàn phí LogiX-VN chạy pilot hay không, và chạy trong phạm vi nào. Mọi con số do `src/lab13.py` tính từ hai CSV giả lập (1.200 yêu cầu, 1.624 lần chạy). Người kiểm số tính lại độc lập bằng `tools/p2_verify.py` và đối chiếu với số tham chiếu (ngưỡng 2%). Số tính từ cột `_simulated` đều ghi nhãn simulated.

## 3. Giải pháp

- **A · Chi phí mỗi việc thành công** ([bang_chi_phi.md](bang_chi_phi.md)): `mo_hinh` cộng token + tool của mọi lần chạy (kể cả lần lỗi) với tiền xem lại, làm lại, rồi chia cho số việc `thanh_cong`. Tách theo 4 loại; cộng chi phí cố định 40 triệu đ/tháng cho noi_dia + hang_nang.
- **B · Độ nhạy** ([bang_chi_phi.md](bang_chi_phi.md)): gọi lại `mo_hinh` cho 9 kịch bản đổi từng yếu tố, 1 cặp, giới hạn 1/2/3 lần chạy (tính cả chi phí hệ thống), xem lại 100%.
- **C · Bảng lỗi** ([bang_loi.md](bang_loi.md)): hai bộ nhãn cho 20 ca theo 5 loại của Google PAIR, quy tắc cho ca lệch, bảng khắc phục 5 ca có ngưỡng đo được và một vai trò phụ trách.
- **D · Pilot** ([pilot_plan.yaml](pilot_plan.yaml)): tính năm câu D1 trong `lab13.py` trước, rồi chọn chia theo nhân viên 20 + 20, ngẫu nhiên, phân tầng theo depot. Có 4 luật dừng NẾU – TRONG – THÌ – KHÔNG THÌ.
- **E · Chỉ số và hồ sơ** ([chi_so.md](chi_so.md), [ho_so_launch_v0.md](ho_so_launch_v0.md)): ba chỉ số tính thử, 11 event có `trace_id`, 5 rủi ro kinh tế lấy số từ B, hồ sơ 7 mục.

## 4. Kết quả

- Chi phí mỗi việc thành công **4.472 đ** = 16,3× hoá đơn token + tool mỗi yêu cầu (274,7 đ); giờ nhân viên chiếm 92,5% [simulated]. Cả hệ thống 5.865 đ/yêu cầu = 0,49× của 12.000 đ [simulated].
- quoc_te 22.515 đ/việc = 1,88× với 27,3% thành công; chạy lại lần 3 chỉ ok 2,2% → loại. doi_tac 54,4% thành công, cả hệ thống 0,92× → loại [simulated].
- Phạm vi noi_dia + hang_nang: 3.414 đ + cố định 1.185 đ = 4.599 đ = 0,38× (5.784 đ = 0,48× nếu khối lượng còn một nửa) [simulated].
- Ba yếu tố nhạy nhất: số ca làm lại +51,8% · tỉ lệ xem lại +40,7% · lương +23,1% [simulated]. Giới hạn 2 lần chạy rẻ nhất cho công ty (6.901.220 đ), khác giới hạn có chi phí mỗi việc thấp nhất (1 lần) [simulated].
- **Con số bất lợi:**
  - Xem lại 100% cho 11.743 đ = 0,98× (12.415 đ = 1,03× nếu làm lại 15,3 phút) [simulated].
  - 20 nhân viên mỗi nhóm chỉ đạt tối đa 1.000 mẫu hiệu dụng, dưới mức 1.251 cần cho chênh 5 điểm. Nhóm chấp nhận mức chênh 6 điểm, nên power chỉ còn 0,64 nếu tác động thật là 5 điểm.
- Chỉ số trong đợt chạy thử: chính 82,83%, bỏ qua gợi ý 27,12%, mở lại 7 ngày 4,25%. Đợt chạy thử không có đối chứng nên các số này chưa nói lên tác động của trợ lý.
- **Đề xuất: Go có điều kiện**, chỉ cho noi_dia + hang_nang. Các điều kiện kèm người phụ trách và ngày kiểm tra nằm trong `ho_so_launch_v0.md`.
- Kết quả duyệt chéo nhóm nhận được từ hội đồng: [CẦN ĐIỀN: tên nhóm hội đồng, điểm, quyết định, câu hỏi].

## 5. Khó khăn và cách xử lý

- `src/lab13.py` ban đầu chưa có phần B và D1. Số B được tính bằng `tools/p2_verify.py` và người gắn nhãn 1 đã báo nhóm. Đã viết B1–B4, D1 vào `lab13.py` và đối chiếu lại: trùng `p2_verify.py`, 31/31 số tham chiếu trong ngưỡng 2%.
- Console Windows (cp1252) không in được tiếng Việt: thêm `reconfigure(encoding='utf-8')` (commit `f913894`). Python hệ thống trên macOS (3.9) không có pandas: tạo `.venv` Python 3.12 rồi cài `requirements.txt`.
- Số làm tròn lệch giữa các file (B4: 12.414 và 12.415): thống nhất theo output `lab13.py`, 11.173.313 ÷ 900 = 12.414,8 → 12.415 đ.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong `TEAM.md`.

## 7. Hạn chế và hướng cải thiện

- Phút xem lại, làm lại là giả lập. Phải thay bằng phút đo thật qua `staff_review_decision`, `staff_rework_completed` sau tuần 1 của pilot.
- Chi phí cả hệ thống cộng 12.000 đ cho mọi ca không thành công, kể cả 74 ca `lam_lai` đã có phút làm lại, nên có thể tính trùng một phần. Cần tách hai khoản khi có dữ liệu thật.
- Mức chênh 6 điểm là đánh đổi. Nếu tác động thật chỉ 5 điểm, pilot có 36% khả năng không phát hiện được.
- hang_nang có tỉ lệ mở lại 8,23% (13/158), gấp 2,6 lần noi_dia, nên phải theo dõi riêng với đối chứng cùng loại.

## 8. Tài liệu tham khảo

- `docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md`, `docs/du_lieu_va_cong_thuc.md`, `docs/Ngay13_Lab13_De_bai_hoc_vien.docx` (công thức, số tham chiếu, 20 ca lỗi).
- Google PAIR, *People + AI Guidebook*, chương Errors + Graceful Failure (năm loại lỗi).
- pandas và statsmodels (`NormalIndPower`, `proportion_effectsize` để tính power); `statistics.NormalDist` của Python để tính cỡ mẫu.
