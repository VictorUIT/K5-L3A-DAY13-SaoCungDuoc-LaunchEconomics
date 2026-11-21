# Team

## Thông tin nhóm

- Tên nhóm:
- Lớp: L3A hoặc L3B
- Repo nhóm: `K5-L3A-DAY13-TenNhom-LaunchEconomics` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 |        |      |       |        |         |
|   2 | Nguyễn Bình An | 2A202603606 | 26ai.annb@vinuni.edu.vn | An041003 | Người kiểm số (P2) |
|   3 | Đỗ Phương Nam | 2A202603621 | donam02zx@gmail.com | donam02zx | Người gắn nhãn 1 |
|   4 |        |      |       |        |         |

Bốn vai của lab:

- **Người viết code:** viết và chạy `src/lab13.py`.
- **Người kiểm số:** tính tay một con số để đối chiếu, điền bảng.
- **Người gắn nhãn 1:** đọc đề, theo dõi điều kiện "Xong khi"; gắn nhãn 20 ca độc lập ở CP3.
- **Người gắn nhãn 2, kiêm giữ hồ sơ:** điền `report/team/ho_so_launch_v0.md` từ đầu buổi; gắn nhãn 20 ca độc lập ở CP3.

Đổi người viết code sau giờ giải lao, để ít nhất hai người trong nhóm tự tay tính được chi phí.

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## NguyenBinhAn-2A202603606

### Phần việc phụ trách

- Người kiểm số (P2): kiểm độc lập A1–A4, B1–B4, D1 và ba chỉ số E1 từ hai CSV gốc; điền bảng chi phí và ghi phép tính đối chiếu.
- Đã đối chiếu P1 tại commit `25bb25e`: A1 ĐẠT; 20/20 kịch bản A2/A3/A4/B1/B2/B3 và 222/222 giá trị khớp, sai lệch bằng 0. B4, D1 và E1 hiện là kết quả độc lập P2.

### Đóng góp cụ thể

- Tích hợp công cụ `tools/p2_verify.py` và bộ 10 unit tests; kiểm số trên 1.200 yêu cầu, 1.624 lần chạy, đạt 31/31 phép đối chiếu với tham chiếu trong ngưỡng sai lệch ≤2%.
- Đối chiếu tiền tool: 5.600 × 15 = 84.000 đ; tổng chi phí 4.373.585,13 đ / 978 việc thành công = 4.471,97 đ/việc (simulated).
- Hoàn thiện bảng A/B và kiểm D1: 1.251 yêu cầu/nhóm cho chênh lệch 5 điểm phần trăm; cần tổng 84 nhân viên nếu mỗi người có 75 yêu cầu, ICC=0,02.
- Phân biệt CPS và chi phí cả hệ thống: giới hạn 2 lần chạy cho tổng chi phí thấp nhất, 6.901.220 đ (simulated).

### Bằng chứng

- [Báo cáo cá nhân](report/team/2A202603606_NguyenBinhAn.md).
- [Bảng chi phí A/B](report/team/bang_chi_phi.md), [phiếu kiểm số và trạng thái đối chiếu P1](report/team/p2_doi_chieu_so.md), [kết quả chi tiết](report/team/p2_ket_qua.json).
- [Công cụ kiểm số](tools/p2_verify.py), [unit tests](tests/test_p2_verify.py): 10/10 tests đạt trong lần kiểm chứng tích hợp.

## DoPhuongNam-2A202603621

### Phần việc phụ trách

- Người gắn nhãn 1: đọc đề, theo dõi điều kiện "Xong khi" của CP1–CP5; gắn nhãn độc lập 20 ca lỗi ở CP3.

### Đóng góp cụ thể

- Soát CP1, CP2 theo "Xong khi": số A2, A3, A4, B1–B4 khớp số đối chiếu; báo nhóm `TODO CP2` trong `src/lab13.py` chưa viết và B4 thiếu câu "pilot cần học được gì".
- Bộ nhãn người 1 cho 20 ca lỗi (ND 4 · HT 5 · NC 4 · GH 4 · NG 3), gắn bằng agent AI theo cho phép của giảng viên.

### Bằng chứng

- [Báo cáo cá nhân](report/team/2A202603621_DoPhuongNam.md), cột "Nhãn người 1" trong [bảng lỗi](report/team/bang_loi.md).

## HoVaTen-MSSV

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-
