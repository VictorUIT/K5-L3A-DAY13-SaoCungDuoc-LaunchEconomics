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
- **D · Pilot** ([pilot_plan.yaml](pilot_plan.yaml)): tính năm câu D1 trong `lab13.py` trước, rồi chọn chia theo nhân viên 20 + 20, ngẫu nhiên, phân tầng theo depot. Có 4 luật dừng NẾU – TRONG – THÌ – KHÔNG THÌ. Sau phản biện hội đồng, luật chi phí 9.600 đ chỉ áp từ bước 0.50 (lý do ghi trong chú thích đầu `pilot_plan.yaml`).
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
- Kết quả duyệt chéo nhóm nhận được từ hội đồng:
  - Câu hỏi nhận được: "Nếu tuần đầu phải xem lại 100%, chi phí mỗi việc thành công là bao nhiêu, và luật dừng chi phí 8.000 đ trong `pilot_plan.yaml` có tự kích hoạt ngay không?" Nhóm trả lời: xem lại 100% cho 11.743 đ/việc = 0,98× (12.415 đ = 1,03× nếu làm lại 15,3 phút) [simulated]; mốc 8.000 đ của hướng dẫn mẫu sẽ bị vượt ngay nên nhóm không dùng; luật 9.600 đ/yêu cầu cần 2 tuần liên tiếp và nay chỉ áp từ bước 0.50.
  - Nhóm hội đồng: **04552** (L3A), theo phiếu chấm của nhóm 04552. Lần 1 (commit `1d25587`, hồ sơ và pilot còn mẫu): 0 + 10 + 0 = 10/30, No-go. Lần 2 (commit `b7586bd`): 10 + 10 + 5 = 25/30, Go có điều kiện. **Lần 3 (commit `d8a7723`): 10 + 10 + 10 = 30/30, Go có điều kiện** cho noi_dia + hang_nang. Hai nhóm đã thảo luận trực tiếp và xác nhận điểm chấm chính xác, đúng quy trình; 30/30 là chất lượng hồ sơ theo rubric, các điều kiện triển khai trong `ho_so_launch_v0.md` vẫn phải thực hiện.
  - Lần 2, tiêu chí "Pilot ra được quyết định" chỉ được 5/10 vì luật chi phí chưa nhất quán: `pilot_plan.yaml` cộng 12.000 đ cho mọi ca không thành công, còn `chi_so.md` chỉ cộng theo `handoff_to_staff`; ngưỡng 9.600 đ/yêu cầu lại được giải thích bằng 2.370 đ/việc thành công (khác mẫu số). Hội đồng hỏi: ca `lam_lai` được cộng chi phí thế nào để không bỏ sót hoặc cộng trùng, và cố định đã quy đổi cùng mẫu số chưa?
  - Nhóm trả lời bằng commit `d8a7723` (xem mục 7): một định nghĩa chi phí C chung cho `pilot_plan.yaml`, `chi_so.md` và `lab13.py`; cố định quy đổi 2.172 đ/yêu cầu; thêm `data_lock` (khoá dữ liệu 12/01, thiếu mẫu thì lùi) và `operational_monitoring` (chi phí, mức dùng, hoàn trùng theo dõi hằng tuần, tách khỏi `interim_looks`). Hội đồng nâng tiêu chí này lên 10/10. Hội đồng cũng tính lại cỡ mẫu: 14 ngày ở bước 0.50 cho m ≈ 430, DE 9,57, khoảng 898 hiệu dụng mỗi nhánh > 859.

## 5. Khó khăn và cách xử lý

- `src/lab13.py` ban đầu chưa có phần B và D1. Số B được tính bằng `tools/p2_verify.py` và người gắn nhãn 1 đã báo nhóm. Đã viết B1–B4, D1 vào `lab13.py` và đối chiếu lại: trùng `p2_verify.py`, 31/31 số tham chiếu trong ngưỡng 2%.
- Console Windows (cp1252) không in được tiếng Việt: thêm `reconfigure(encoding='utf-8')` (commit `f913894`). Python hệ thống trên macOS (3.9) không có pandas: tạo `.venv` Python 3.12 rồi cài `requirements.txt`.
- Số làm tròn lệch giữa các file (B4: 12.414 và 12.415): thống nhất theo output `lab13.py`, 11.173.313 ÷ 900 = 12.414,8 → 12.415 đ.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong `TEAM.md`.

## 7. Hạn chế và hướng cải thiện

- Phút xem lại, làm lại là giả lập. Phải thay bằng phút đo thật qua `staff_review_decision`, `staff_rework_completed` sau tuần 1 của pilot.
- Chi phí cả hệ thống cộng 12.000 đ cho mọi ca không thành công, kể cả 74 ca `lam_lai` đã có phút làm lại, nên có thể tính trùng một phần. Hội đồng 04552 chỉ ra cùng điểm này: nếu 48 ca `lam_lai` trong phạm vi không phát `handoff_to_staff`, hai cách tính lệch 48 × 12.000 ÷ 982 ≈ 587 đ/yêu cầu [simulated]. Đã thống nhất định nghĩa C cho luật dừng trong `pilot_plan.yaml`, `chi_so.md` và `lab13.py`: ca `lam_lai` chỉ tính phút làm lại đo thật (`staff_rework_completed`), 12.000 đ chỉ cho ca chuyển nhân viên (`handoff_to_staff`); C trên dữ liệu chạy thử là 3.544 đ/yêu cầu [simulated]. Các bảng A3, B3 vẫn dùng cách cộng 12.000 đ cho mọi ca không thành công theo đề.
- Ngưỡng 9.600 đ là **mỗi yêu cầu**, còn chi phí cố định 2.370 đ là **mỗi việc thành công**; không cộng thẳng hai số. Quy đổi về mỗi yêu cầu trong phạm vi: khối lượng một nửa 22.500 yêu cầu/tháng × 982/1.200 = 18.413 yêu cầu noi_dia + hang_nang; 40.000.000 ÷ 18.413 ≈ 2.172 đ/yêu cầu, nên 9.600 + 2.172 = 11.772 đ = 0,98× của 12.000 đ [simulated]. Ngưỡng vẫn dưới mức hoà vốn nhưng chỉ còn khoảng 2% dư địa; `pilot_plan.yaml` đã ghi lại lý do theo cùng mẫu số.
- Mức chênh 6 điểm là đánh đổi. Nếu tác động thật chỉ 5 điểm, pilot có 36% khả năng không phát hiện được.
- hang_nang có tỉ lệ mở lại 8,23% (13/158), gấp 2,6 lần noi_dia, nên phải theo dõi riêng với đối chứng cùng loại.

## 8. Tài liệu tham khảo

- `docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md`, `docs/du_lieu_va_cong_thuc.md`, `docs/Ngay13_Lab13_De_bai_hoc_vien.docx` (công thức, số tham chiếu, 20 ca lỗi).
- Google PAIR, *People + AI Guidebook*, chương Errors + Graceful Failure (năm loại lỗi).
- pandas và statsmodels (`NormalIndPower`, `proportion_effectsize` để tính power); `statistics.NormalDist` của Python để tính cỡ mẫu.
