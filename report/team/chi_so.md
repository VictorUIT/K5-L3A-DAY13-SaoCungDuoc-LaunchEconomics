# Đặc tả chỉ số, event và rủi ro kinh tế · Nhiệm vụ E1, E2

Ba chỉ số E1 tính từ `src/logix_requests.csv` (1.200 yêu cầu), đã đối chiếu với [p2_doi_chieu_so.md](p2_doi_chieu_so.md). Số ở E2 lấy từ [bang_chi_phi.md](bang_chi_phi.md); mọi số tính từ cột `_simulated` ghi nhãn `simulated`.

## E1 · Đặc tả chỉ số

| Loại | Chỉ số | Công thức | Tính thử trên 1.200 yêu cầu |
| --- | --- | --- | --- |
| Chính (kết quả) | % yêu cầu đóng trong 24 giờ và không mở lại trong 7 ngày | `dong_trong_24h` bằng 1 và `mo_lai_trong_7_ngay` bằng 0, chia tổng số yêu cầu | **82,83%** (994/1.200); trong phạm vi noi_dia + hang_nang 92,26% (906/982) |
| Dùng | Tỉ lệ bỏ qua gợi ý | `quyet_dinh_xem_lai` là `sua` hoặc `bo`, chia số yêu cầu được xem lại | **27,12%** (48/177); trong phạm vi 21,09% (27/128) |
| An toàn | Tỉ lệ lỗi lọt đến khách | `mo_lai_trong_7_ngay` bằng 1, chia tổng số yêu cầu | **4,25%** (51/1.200); trong phạm vi 3,97% (39/982); riêng hang_nang 8,23% (13/158) |
| Dùng | Nhóm tự đề xuất: % yêu cầu trong phạm vi được mở bằng trợ lý, tính riêng cho nhóm trợ lý và nhóm đối chứng | số `agent_suggestion_shown` chia số `refund_request_created` trong phạm vi, theo `arm` và theo tuần. Nhóm trợ lý thấp cho biết nhân viên không dùng; nhóm đối chứng > 5% là tràn tác động (vi phạm thiết kế trong `pilot_plan.yaml`) | Không cần tính |
| An toàn | Nhóm tự đề xuất: % đơn hoàn sai tiền qua kiểm tra mẫu hằng tuần | số đơn có `so_tien_da_hoan` khác `so_tien_dung` trong `audit_sample_checked`, chia số đơn được kiểm (100 đơn ngẫu nhiên mỗi tuần). Bắt lỗi ngầm mà khách không mở lại, như ca 5 (14 đơn thừa 12.000 đ) và ca 17 (212 đơn lệch trong 9 ngày) | Không cần tính |

Chỉ số chính trong đợt chạy thử là 82,83%. Không viết "trợ lý đã nâng chỉ số từ 0,70": đợt chạy thử không có nhóm đối chứng, và 0,70 là số cho sẵn của giai đoạn chỉ có nhân viên, không đo trên cùng mẫu.

## Danh sách event

Mười một event, mỗi event có `trace_id` để nối với trace của agent; event nào gắn với yêu cầu đều có thêm `request_id` và `arm` (tro_ly / doi_chung).

| Event | Ai tạo | Thuộc tính chính | Thời điểm |
| --- | --- | --- | --- |
| `refund_request_created` | Ứng dụng của khách | request_id, loai, depot, staff_id, arm, so_tien_yeu_cau, trace_id | Khi khách gửi yêu cầu |
| `agent_run_completed` | Agent | request_id, attempt, tokens_in, tokens_out, tool_calls, status (ok / loi), depot, trace_id | Sau mỗi lần chạy, kể cả lần lỗi |
| `agent_suggestion_shown` | Giao diện nhân viên | request_id, staff_id, arm, so_tien_de_xuat, trace_id | Khi gợi ý của trợ lý hiện ra |
| `staff_review_decision` | Nhân viên | request_id, staff_id, quyet_dinh (giu / sua / bo), phut_xem_lai đo thật, trace_id | Khi nhân viên bấm giữ, sửa hoặc bỏ |
| `staff_rework_completed` | Nhân viên | request_id, staff_id, phut_lam_lai đo thật, ly_do, trace_id | Khi làm lại xong |
| `handoff_to_staff` | Agent | request_id, reason (het_lan_chay / ngoai_pham_vi / thieu_du_lieu), tom_tat, trace_id | Khi chuyển yêu cầu cho nhân viên |
| `input_unsupported` | Agent | request_id, type (audio / image / khac), trace_id | Khi nhận đầu vào không xử lý được (ca 11) |
| `refund_ledger_write` | Dịch vụ sổ cái | request_id, ma_van_don, idempotency_key, so_tien, ket_qua (ok / loi / trung), trace_id | Mỗi lần ghi sổ hoàn tiền (ca 7, 20) |
| `bank_transfer_failed` | Cổng ngân hàng | request_id, reason (sai_so_tai_khoan / khac), trace_id | Khi ngân hàng trả lỗi chuyển tiền (ca 1) |
| `ticket_closed` / `ticket_reopened` | Hệ thống ticket | request_id, closed_at hoặc reopened_at, reason, trace_id | Khi đóng; khi khách mở lại |
| `audit_sample_checked` | Kế toán | request_id, so_tien_da_hoan, so_tien_dung, phien_ban_bang_gia, trace_id | Hằng tuần, 100 đơn ngẫu nhiên |

**Kiểm tra chéo:** với mỗi chỉ số ở bảng E1, ghi event dùng để tính. Chỉ số nào không tính được từ danh sách event thì chưa đo được.

- **Chính:** `ticket_closed` có closed_at trong 24 giờ kể từ `refund_request_created`, và không có `ticket_reopened` trong 7 ngày sau đó; mẫu số là `refund_request_created`. So hai nhóm bằng trường `arm`.
- **Dùng (bỏ qua gợi ý):** `staff_review_decision` có quyet_dinh là sua hoặc bo, chia tổng số `staff_review_decision`.
- **An toàn (lỗi lọt đến khách):** số `ticket_reopened` trong 7 ngày chia số `refund_request_created`.
- **Dùng tự đề xuất:** `agent_suggestion_shown` chia `refund_request_created` trong phạm vi, tách theo `arm`.
- **An toàn tự đề xuất:** `audit_sample_checked` có so_tien_da_hoan khác so_tien_dung, chia số đơn được kiểm.
- **Luật dừng chi phí tính được từ event, cùng định nghĩa C với `pilot_plan.yaml`:**

  | Thành phần của C (mỗi tuần, nhóm trợ lý, phạm vi noi_dia + hang_nang) | Event | Quy tắc tránh bỏ sót, cộng trùng |
  | --- | --- | --- |
  | Token + tool | `agent_run_completed` | Mọi lần chạy, kể cả status = loi |
  | Xem lại | `staff_review_decision` (phut_xem_lai × 2.000 đ) | Không tính cho yêu cầu đã có `handoff_to_staff` |
  | Làm lại (ca lam_lai) | `staff_rework_completed` (phut_lam_lai × 2.000 đ) | Chỉ tính phút đo thật, **không** cộng 12.000 đ |
  | Nhân viên làm thay (ca chuyển nhân viên) | `handoff_to_staff` | 12.000 đ, mỗi request_id tối đa một lần; không cộng phút xem lại, làm lại |
  | Mẫu số | `refund_request_created` có arm = tro_ly, loai thuộc phạm vi | Mỗi request_id đếm một lần |

  Ngưỡng 9.600 đ chỉ gồm chi phí biến đổi; cố định quy đổi cùng mẫu số là 2.172 đ/yêu cầu ở một nửa khối lượng (40.000.000 ÷ 18.412), tổng 11.772 đ = 0,98× [simulated]. Trên dữ liệu chạy thử, C = (3.072.513 + 34 × 12.000) ÷ 982 = 3.544 đ/yêu cầu [simulated] (`python lab13.py`, mục B4).
- **Hoàn trùng:** `refund_ledger_write` có ket_qua = trung, hoặc hai lệnh cùng ma_van_don trong 24 giờ.

## E2 · Rủi ro kinh tế

Số lấy từ bảng độ nhạy và chi phí cố định trong `bang_chi_phi.md`, đều là số [simulated]. Ngưỡng theo dõi khớp với luật dừng trong `pilot_plan.yaml`.

| Rủi ro | Tác động đã tính | Dấu hiệu theo dõi | Hành động | Người phụ trách |
| --- | --- | --- | --- | --- |
| Số ca làm lại tăng gấp đôi | Chi phí mỗi việc thành công +51,8%, từ 4.472 đ lên 6.787 đ [simulated]; yếu tố nhạy nhất (B1) | Tỉ lệ `staff_rework_completed` trên số yêu cầu của nhóm trợ lý, theo tuần, vượt 7% (đợt chạy thử: 4,9% trong phạm vi, 48/982) | Thu hẹp về noi_dia, rà 20 trace làm lại gần nhất trong 3 ngày | PM trợ lý hoàn phí |
| Phải xem lại 100% kéo dài | 11.743 đ = 0,98× của 12.000 đ với 9 phút làm lại/ca; 12.415 đ = 1,03× với 15,3 phút như dữ liệu (B4) [simulated]: gần như không tiết kiệm | Tỉ lệ yêu cầu có `staff_review_decision` còn > 50% khi hết bước 0.25; phút xem lại trung vị > 5,1 phút (mức hoà vốn) | Giảm xem lại theo bậc khi tỉ lệ sửa + bỏ < 15% trong 1 tuần (đợt chạy thử 21,1% trong phạm vi) | Trưởng nhóm CSKH |
| Khối lượng thấp hơn dự kiến | Cố định 40 triệu đ/tháng: +1.185 đ/việc ở 45.000 yc/tháng; +2.370 đ/việc nếu còn một nửa, tổng 5.784 đ = 0,48×. Hoà vốn khi còn 4.659 việc thành công/tháng ≈ 6.212 yc/tháng (A4) [simulated] | Số việc thành công theo tuần < 50% kế hoạch (dưới khoảng 3.900 việc/tuần ở quy mô đầy đủ) | Không mở rộng pilot; xem lại hợp đồng chi phí cố định | Giám đốc vận hành |
| Cắt giới hạn chạy lại xuống 1 lần để giảm chi phí mỗi việc | Chi phí mỗi việc thấp nhất (4.111 đ) nhưng đẩy thêm 85 yêu cầu sang nhân viên (319 so với 234); cả hệ thống 7.449.781 đ so với 6.901.220 đ ở giới hạn 2 lần (B3) [simulated] | Số `handoff_to_staff` có reason = het_lan_chay theo tuần | Giữ giới hạn 2 lần chạy; không tối ưu riêng chi phí mỗi việc thành công | Kỹ sư trưởng agent |
| Lương nhân viên tăng | Lương +25%: 5.506 đ (+23,1%) vì giờ nhân viên chiếm 92,5% tổng chi phí (B1) [simulated] | Đơn giá phút nhân viên trong kỳ điều chỉnh lương | Tính lại cả chi phí trợ lý lẫn mốc nhân viên tự làm (6 phút × 2.500 đ = 15.000 đ) với đơn giá mới trước khi mở rộng; so sánh luôn dùng cùng một đơn giá | Giám đốc vận hành |
