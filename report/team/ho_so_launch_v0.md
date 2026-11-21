# Hồ sơ launch v0 · Trợ lý hoàn phí LogiX-VN · Gate 2a

Một trang. Cột trạng thái chỉ nhận: **Xong, có bằng chứng · Chưa · Giả lập**. Mục nào dựa trên cột `_simulated` ghi Giả lập. Người phụ trách là một vai trò, không ghi "cả đội". Gate 2a chỉ duyệt kế hoạch pilot: không viết như thể trợ lý đã được duyệt chạy chính thức (xem quy tắc 5 trong `README.md`).

Nhóm: SaoCungDuoc · Lớp: L3A

| Mục | Con số chính | Trạng thái | Người phụ trách |
| --- | --- | --- | --- |
| 1 · Chi phí mỗi việc thành công | Toàn mẫu **4.472 đ** = 16,3× hoá đơn token + tool mỗi yêu cầu (274,7 đ); làm lại 51,8%, xem lại 40,7% tổng chi phí. Phạm vi pilot noi_dia + hang_nang: 3.414 đ, cộng cố định 40 triệu đ/tháng → **4.599 đ** [simulated] · [bang_chi_phi.md](bang_chi_phi.md) A2, A4 | Giả lập | PM trợ lý hoàn phí |
| 2 · Ba yếu tố nhạy nhất | 1. Số ca làm lại gấp đôi **+51,8%** (6.787 đ) · 2. Xem lại gấp đôi **+40,7%** (6.292 đ) · 3. Lương +25% **+23,1%** (5.506 đ); giá token gấp đôi chỉ +5,6% [simulated] · B1, B2 | Giả lập | PM trợ lý hoàn phí |
| 3 · So với nhân viên tự làm | Cả hệ thống (cộng 12.000 đ mỗi ca không thành công): toàn mẫu 5.865 đ = **0,49×**; phạm vi pilot 4.131 đ = **0,34×**; quoc_te 22.515 đ/việc = **1,88×** nên loại. **Bất lợi:** nếu xem lại 100% thì 11.743 đ = 0,98× (12.414 đ = 1,03× với 15,3 phút làm lại/ca như dữ liệu) [simulated] · A3, B4 | Giả lập | Giám đốc vận hành |
| 4 · Chỉ số chính, chỉ số dùng, chỉ số an toàn | Chỉ số trong đợt chạy thử là: chính (đóng trong 24 giờ, không mở lại 7 ngày) **82,83%** (994/1.200); dùng (bỏ qua gợi ý) **27,12%** (48/177); an toàn (mở lại 7 ngày) **4,25%** (51/1.200). Đợt chạy thử không có đối chứng nên chưa kết luận tác động. Thêm 1 chỉ số dùng, 1 chỉ số an toàn (kiểm tra mẫu hoàn sai tiền); 11 event có `trace_id`, mọi chỉ số và luật dừng đều tính được từ event · [chi_so.md](chi_so.md) | Xong, có bằng chứng | PM trợ lý hoàn phí |
| 5 · Bảng lỗi và cách khắc phục | Hai bộ nhãn độc lập, đồng thuận **18/20 = 90%** (lệch ca 13, 17, đã có quy tắc phân biệt). Bảng khắc phục 5 ca đủ năm loại (ca 1, 20, 16, 11, 12), mỗi dòng có ngưỡng phát hiện; lỗi nặng nhất là hoàn trùng (ca 20, ngưỡng 0 ca) · [bang_loi.md](bang_loi.md) | Xong, có bằng chứng | Trưởng nhóm CSKH |
| 6 · Pilot plan | Chia theo nhân viên **20 + 20**, ngẫu nhiên phân tầng theo depot; mức chênh tối thiểu **6 điểm**, n = 859/nhóm, DE 6,96, m ≥ 299 yc/nhân viên. **Bất lợi:** power chỉ **0,64** nếu tác động thật là 5 điểm; 20 cụm tối đa 1.000 hiệu dụng < 1.251. 4 luật dừng có ngưỡng, thời hạn, người dừng; quyết định 2027-01-12 · [pilot_plan.yaml](pilot_plan.yaml) | Xong, có bằng chứng | Giám đốc vận hành |
| 7 · Rủi ro kinh tế | Làm lại gấp đôi → 6.787 đ (+51,8%); khối lượng còn một nửa → cố định 2.370 đ/việc, tổng 5.784 đ = 0,48×; hoà vốn khi còn 4.659 việc thành công/tháng ≈ 6.212 yc/tháng; xem lại 100% → 0,98–1,03× [simulated] · A4, B1, B4 | Giả lập | PM trợ lý hoàn phí |

**Đề xuất:** **Go có điều kiện**, chỉ cho pilot noi_dia + hang_nang (82% số yêu cầu: 982/1.200). Bắt đầu 2026-12-07 nếu đủ các điều kiện sau:

- Giám đốc vận hành ký chấp nhận mức chênh tối thiểu 6 điểm và power 0,64 nếu tác động thật là 5 điểm. **Kiểm tra: 2026-12-04.**
- Khoá chống hoàn trùng (ca 20 trong `bang_loi.md`) và đối soát sổ cái mỗi giờ chạy trước ngày bắt đầu. Người phụ trách: Kế toán trưởng. **Kiểm tra: 2026-12-04.**
- Bật đủ event có `trace_id`. Đo phút xem lại, làm lại thật để thay số simulated sau tuần 1. Người phụ trách: PM trợ lý hoàn phí. **Kiểm tra: 2026-12-14.**
- Giảm tỉ lệ xem lại theo bậc trước bước 0.50, vì xem lại 100% gần như không tiết kiệm (0,98–1,03×, simulated). Người phụ trách: Trưởng nhóm CSKH. **Kiểm tra: 2026-12-21.**
- hang_nang có tỉ lệ mở lại 8,23% trong đợt chạy thử, cao gấp 2,6 lần noi_dia (3,16%). Theo dõi riêng so với đối chứng cùng loại; cao hơn ≥ 2 điểm thì thu hẹp về noi_dia. Người phụ trách: Giám đốc vận hành. **Kiểm tra: hằng tuần, mốc đầu 2026-12-14.**
