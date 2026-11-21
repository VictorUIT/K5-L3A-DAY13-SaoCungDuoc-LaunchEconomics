# Báo cáo cá nhân — DoPhuongNam-2A202603621

## 1. Thông tin thành viên

- Họ tên: Đỗ Phương Nam
- MSSV: 2A202603621
- Email: donam02zx@gmail.com
- GitHub: donam02zx
- Vai trong nhóm: Người gắn nhãn 1

## 2. Phần việc phụ trách

- Đọc đề, theo dõi điều kiện "Xong khi" của CP1–CP5 cho cả nhóm.
- Gắn nhãn độc lập 20 ca lỗi ở CP3; cùng người gắn nhãn 2 so nhãn, thống nhất ca lệch và lập bảng khắc phục 5 ca.

## 3. Đóng góp cụ thể

- Lập checklist "Xong khi" cho CP1–CP5 và phần nộp bài, gom từ đề bài, `CHECKPOINTS.md`, `RUBRIC.md`, `RULES.md`.
- Soát CP1: ba phép thử A1 ĐẠT; A2 (4.472 đ/việc thành công, 16,3 lần hoá đơn), A3, A4 khớp số đối chiếu, lệch 0%; hai dòng giả lập có nhãn simulated.
- Soát CP2: số B1–B4 khớp số đối chiếu (ví dụ làm lại gấp đôi +51,8%, B3 giới hạn 2 lần rẻ nhất 6.901.220 đ [simulated]). Phát hiện và báo nhóm: `TODO CP2` trong `src/lab13.py` chưa viết (số B đang tính bằng `tools/p2_verify.py`), B4 thiếu câu "pilot cần học được gì", định dạng số thập phân phần B chưa thống nhất.
- CP3: bộ nhãn người 1 cho 20 ca (ND 4 · HT 5 · NC 4 · GH 4 · NG 3). Tỉ lệ đồng thuận với người gắn nhãn 2: 18/20 = 90%; hai ca lệch 13 và 17 đã thống nhất (Giới hạn hệ thống, Ngầm) kèm quy tắc phân biệt. Soạn bảng khắc phục 5 ca (1, 20, 16, 11, 12), đủ năm loại.
- CP4, CP5: [điền kết quả soát "Xong khi"]

## 4. Bằng chứng

- `report/team/bang_loi.md`: cột "Nhãn người 1" (bộ nhãn độc lập của tôi).
- Danh sách lỗi đã báo nhóm ở CP2 (mục 3).

## 5. Công cụ AI đã dùng

- Claude Code: tóm tắt đề; trích 20 ca lỗi từ file docx ra phiếu gắn nhãn không kèm đáp án; lập checklist "Xong khi"; chạy `src/lab13.py` và đối chiếu số A, B với số trong hướng dẫn chi tiết.
- Gắn nhãn 20 ca lỗi (bộ nhãn người 1): dùng một agent Claude mới, chỉ nhận định nghĩa năm loại và 20 ca, không đọc file nào trong repo, theo cho phép của giảng viên. Bộ nhãn được giữ riêng, không chia sẻ cho người gắn nhãn 2 trước khi so.
- Tự kiểm tra: đối chiếu từng số trong `bang_chi_phi.md` với output `python lab13.py` và bảng số đối chiếu trong `docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md`.

## 6. Tự đánh giá

- Làm được: soát CP1, CP2 theo "Xong khi" và phát hiện hai chỗ thiếu trước khi nộp (`TODO CP2` chưa viết trong `src/lab13.py`, B4 thiếu câu "pilot cần học được gì"); CP3 đạt đồng thuận 18/20 = 90%, bảng khắc phục đủ năm loại, mỗi dòng có ngưỡng đo được và một vai trò phụ trách.
- Rút ra: gắn nhãn theo nguyên nhân gốc, không theo chỗ cần sửa.