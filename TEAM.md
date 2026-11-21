# Team

## Thông tin nhóm

- Tên nhóm: SaoCungDuoc
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY13-SaoCungDuoc-LaunchEconomics` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: https://github.com/VictorUIT/K5-L3A-DAY13-SaoCungDuoc-LaunchEconomics · nhánh `main` · commit chốt: [CẦN ĐIỀN sau khi push bản cuối]

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Văn Ngọc Sơn | 2A202603600 | kidoamdice@gmail.com | kynnnS | Người viết code (P1) |
|   2 | Nguyễn Bình An | 2A202603606 | 26ai.annb@vinuni.edu.vn | An041003 | Người kiểm số (P2) |
|   3 | Đỗ Phương Nam | 2A202603621 | donam02zx@gmail.com | donam02zx | Người gắn nhãn 1 |
|   4 | Trần Quốc Tuấn Khanh | 2A202603625 | 26ai.khanhtqt@vinuni.edu.vn | VictorUIT | Người gắn nhãn 2, kiêm giữ hồ sơ (P4) |

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
- Bộ nhãn người 1 cho 20 ca lỗi (ND 4 · HT 5 · NC 4 · GH 4 · NG 3).
### Bằng chứng

- [Báo cáo cá nhân](report/team/2A202603621_DoPhuongNam.md), cột "Nhãn người 1" trong [bảng lỗi](report/team/bang_loi.md).

## NguyenVanNgocSon-2A202603600

### Phần việc phụ trách

- Người viết code (P1): viết và chạy `src/lab13.py`, gồm CP1 (A1–A4), CP2 (B1–B4) và D1 của CP4; điền A1–A4 trong `report/team/bang_chi_phi.md`.

### Đóng góp cụ thể

- A1: ba hàm kinh tế chạy lại, ba phép thử đáp án biết trước ĐẠT (1,20 · 1,25 · 1,25) và phép thử biên.
- A2–A4: `mo_hinh` tính mọi lần chạy kể cả lần lỗi, mẫu số chỉ `thanh_cong`: 4.472 đ/việc = 16,3× hoá đơn token + tool mỗi yêu cầu [simulated]; tách 4 loại; cố định 40 triệu đ/tháng cho noi_dia + hang_nang (4.599 đ [simulated]).
- B1–B4 và D1 trong `lab13.py`: gọi lại `mo_hinh` cho 9 + 1 kịch bản, giới hạn 1/2/3 lần chạy, xem lại 100%; cỡ mẫu năm câu D1 (1.251 · 3.103/42 người · 1.000 · 300 · m ≥ 299, power 0,64).

### Bằng chứng

- [Báo cáo cá nhân](report/team/2A202603600_NguyenVanNgocSon.md).
- Commit `25bb25e`, `a5e97e5`, `972733f` (CP1) và commit thêm CP2 + D1 vào `src/lab13.py`; output `python lab13.py` khớp số tham chiếu trong ngưỡng 2% và khớp `tools/p2_verify.py` của P2.

## TranQuocTuanKhanh-2A202603625

### Phần việc phụ trách

- Người gắn nhãn 2 kiêm giữ hồ sơ (P4 – Pilot & Launch): CP4 `pilot_plan.yaml`; CP5 `ho_so_launch_v0.md`, `chi_so.md`, `phieu_cham.md`; bộ nhãn người 2 ở CP3.

### Đóng góp cụ thể

- Pilot chia theo nhân viên 20 + 20, ngẫu nhiên phân tầng theo depot; D1 đủ năm câu (1.251 · 3.103 · 1.000 · 300 · m ≥ 299); mức chênh 6 điểm (n = 859, DE 6,96), ghi rõ power 0,64 nếu tác động thật 5 điểm; 4 luật dừng đủ bốn vế; quyết định 2027-01-12.
- Hồ sơ launch bảy mục, đề xuất Go có điều kiện (5 điều kiện có người phụ trách, ngày kiểm tra); nêu con số bất lợi hang_nang mở lại 8,23% và xem lại 100% là 0,98–1,03× [simulated].
- `chi_so.md`: ba chỉ số 82,83% · 27,12% · 4,25%; hai chỉ số tự đề xuất; 11 event có `trace_id`; 5 rủi ro kinh tế.
- Chấm hội đồng nhóm 04552: 30/30, Go có điều kiện.
- Ghép nhánh P1 vào `main`; sửa lỗi in tiếng Việt trên Windows; `p2_verify.py` chỉ ghi đè báo cáo khi có `--write`.

### Bằng chứng

- [Báo cáo cá nhân](report/team/2A202603625_TranQuocTuanKhanh.md); commit `05deb26`, `a8abdd7`, `f913894`; cột "Nhãn người 2" trong [bảng lỗi](report/team/bang_loi.md).
