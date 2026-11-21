# Bảng lỗi và cách khắc phục · Nhiệm vụ C

20 ca lỗi nằm trong `docs/Ngay13_Lab13_De_bai_hoc_vien.docx`. Năm loại theo Google PAIR: **Do người dùng · Hệ thống · Ngữ cảnh · Giới hạn hệ thống · Ngầm**. Gắn nhãn theo nguyên nhân gốc, không theo chỗ cần sửa.

## Hai bộ nhãn độc lập

Người gắn nhãn 1: Đỗ Phương Nam (gắn bằng agent AI theo cho phép của giảng viên) · Người gắn nhãn 2: Trần Quốc Tuấn Khanh (gắn trong 8 phút, không trao đổi)

Mã nhãn: ND = Do người dùng · HT = Hệ thống · NC = Ngữ cảnh · GH = Giới hạn hệ thống · NG = Ngầm.

| Ca | Nhãn người 1 | Nhãn người 2 | Trùng? | Nhãn thống nhất |
| --: | --- | --- | --- | --- |
| 1 | ND | ND | Có | Do người dùng |
| 2 | HT | HT | Có | Hệ thống |
| 3 | NC | NC | Có | Ngữ cảnh |
| 4 | GH | GH | Có | Giới hạn hệ thống |
| 5 | NG | NG | Có | Ngầm |
| 6 | ND | ND | Có | Do người dùng |
| 7 | HT | HT | Có | Hệ thống |
| 8 | HT | HT | Có | Hệ thống |
| 9 | ND | ND | Có | Do người dùng |
| 10 | NC | NC | Có | Ngữ cảnh |
| 11 | GH | GH | Có | Giới hạn hệ thống |
| 12 | NG | NG | Có | Ngầm |
| 13 | GH | HT | Không | Giới hạn hệ thống |
| 14 | ND | ND | Có | Do người dùng |
| 15 | HT | HT | Có | Hệ thống |
| 16 | NC | NC | Có | Ngữ cảnh |
| 17 | NG | HT | Không | Ngầm |
| 18 | NC | NC | Có | Ngữ cảnh |
| 19 | GH | GH | Có | Giới hạn hệ thống |
| 20 | HT | HT | Có | Hệ thống |

**Tỉ lệ đồng thuận:** 18 / 20 = 90% (đạt ngưỡng 80%). Hai ca không trùng: 13, 17.

Phân bố nhãn thống nhất: Do người dùng 4 (1, 6, 9, 14) · Hệ thống 5 (2, 7, 8, 15, 20) · Ngữ cảnh 4 (3, 10, 16, 18) · Giới hạn hệ thống 4 (4, 11, 13, 19) · Ngầm 3 (5, 12, 17).

## Quy tắc phân biệt cho các ca không trùng

Mỗi ca không trùng một câu. Đồng thuận dưới 80% thì ghi định nghĩa đã viết lại.

- **Ca 13 → Giới hạn hệ thống, không phải Hệ thống:** bảo hiểm hàng hoá nằm ngoài phạm vi trợ lý, nên gốc lỗi là giới hạn; việc trợ lý không nói rõ "không xử lý được" là chỗ cần sửa, không đổi nguyên nhân gốc.
- **Ca 17 → Ngầm, không phải Hệ thống:** 212 đơn lệch trong 9 ngày mà không khách nào mở lại, không cảnh báo nào kích; chỉ gắn Hệ thống khi cái sai đã lộ ra (khách báo hoặc nhân viên bắt được như ca 2, 15).

## Bảng khắc phục cho 5 ca, mỗi loại một ca

Cách phát hiện phải đo được (event, ngưỡng, tần suất). Người phụ trách là một vai trò, không ghi "cả đội".

| Ca | Loại lỗi | Phát hiện bằng gì | Khắc phục thế nào | Ai phụ trách |
| --: | --- | --- | --- | --- |
| 1 | Do người dùng | Event `bank_transfer_failed` với `reason = sai_so_tai_khoan`; cảnh báo khi vượt 1% số lệnh hoàn/ngày | Kiểm tra độ dài và checksum số tài khoản ngay khi khách nhập; hỏi lại tên chủ tài khoản trước khi tạo lệnh | PM trợ lý hoàn phí |
| 20 | Hệ thống | Đối soát mỗi giờ: hai lệnh hoàn cùng mã vận đơn trong 24 giờ; ngưỡng 0 ca | Thêm khoá chống trùng (idempotency key = mã vận đơn + loại hoàn) cho lệnh ghi sổ cái; yêu cầu gửi lại thì trả trạng thái lệnh cũ | Kỹ sư trưởng agent |
| 16 | Ngữ cảnh | Tỉ lệ phản ánh "làm phiền" trên số tin gửi trong khung 22:00–07:00, theo tuần; ngưỡng 0,5% | Tin gửi trong khung 22:00–07:00 được xếp hàng tới 07:00; tiền vẫn hoàn ngay, chỉ hoãn thông báo | Trưởng nhóm CSKH |
| 11 | Giới hạn hệ thống | Event `input_unsupported` với `type = audio`, đếm theo ngày; cảnh báo khi vượt 2% số yêu cầu | Trả lời rõ "chưa nghe được tin thoại", đưa mẫu nhập 3 trường; quá 1 lần thì chuyển nhân viên kèm file âm thanh | PM trợ lý hoàn phí |
| 12 | Ngầm | Chi phí token + tool mỗi yêu cầu theo depot, tính hằng ngày; cảnh báo khi một depot vượt 1,5× trung vị các depot 2 ngày liên tiếp | Kiểm tra schema đầu ra của tool tra đơn, thiếu trường thì báo lỗi ngay thay vì gọi lại; sửa tool của D05 | Kỹ sư trưởng agent |
