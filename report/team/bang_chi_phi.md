# Bảng chi phí · Nhiệm vụ A và B

Phần A tính bằng `src/lab13.py` của P1 và được P2 kiểm độc lập; phần B tính bằng `tools/p2_verify.py`, các kịch bản B1–B3 đã đối chiếu với `mo_hinh()` của P1. Mọi con số tính từ cột `_simulated` ghi nhãn `simulated`. Mỗi câu trả lời không quá ba dòng, có ít nhất một con số.

## A1 · Ba phép thử đáp án biết trước

| Phép thử (p = 0,8) | Kết quả của nhóm |
| --- | --- |
| Số lần chạy trung bình, tối đa 2 lần | 1,20 (= (1 − 0,2²) ÷ 0,8) · ĐẠT |
| Số lần chạy trung bình, chạy đến khi đúng | 1,25 (= 1 ÷ 0,8) · ĐẠT |
| Hệ số chi phí mỗi việc thành công, tối đa 3 lần | 1,25 (= 1,24 ÷ 0,992 = 1/p, k triệt tiêu) · ĐẠT |

`python lab13.py` in `Ba phép thử đáp án biết trước: ĐẠT` và `Phép thử biên A1: ĐẠT` (p = 0, p = 1, k = 1, k lớn; tham số sai: p ngoài [0, 1], nan, inf, k ≤ 0, k không nguyên, bool).

## A2 · Mô hình chi phí từ trace

| Khoản | Số tiền (đ) | Nguồn | Nhãn |
| --- | ---: | --- | --- |
| Token | 245.585 | `logix_runs.csv` | đo từ trace |
| Tool | 84.000 | `logix_runs.csv` | đo từ trace |
| Trong đó, phần của lần chạy thứ 2 và 3 | 93.804 | attempt lớn hơn 1 | đo từ trace |
| Xem lại | 1.780.000 | `phut_xem_lai_simulated` | simulated |
| Làm lại | 2.264.000 | `phut_lam_lai_simulated` | simulated |
| Tổng chi phí | 4.373.585 | token + tool + xem lại + làm lại (93.804 đã nằm trong token + tool) | simulated |
| Số việc thành công | 978 | `ket_qua` | đo từ dữ liệu |
| Chi phí mỗi việc thành công | 4.472 | 4.373.585 ÷ 978 | simulated |
| Hoá đơn token và tool chia cho số yêu cầu | 274,7 | (245.585 + 84.000) ÷ 1.200 | đo từ trace |

- Chi phí mỗi việc thành công gấp bao nhiêu lần "hoá đơn chia số yêu cầu"? 4.472 ÷ 274,7 = **16,3 lần** [simulated], vì hoá đơn token + tool không gồm chi phí nhân viên (simulated) và chia cho cả 1.200 yêu cầu, còn chi phí mỗi việc thành công chia tổng chi phí cho 978 việc thành công; token + tool vẫn tính cả các lần chạy lỗi.
- Khoản nào chiếm tỉ trọng lớn nhất trong tổng chi phí, bao nhiêu phần trăm? **Làm lại, 51,8%** [simulated], tiếp theo là xem lại 40,7% [simulated]; giờ nhân viên chiếm 92,5%, token + tool chỉ 7,5% tổng chi phí [simulated].
- So với 12.000 đ: 4.472 đ chưa gồm 222 ca không thành công (148 `chuyen_nhan_vien` + 74 `lam_lai`). Chi phí cả hệ thống = (4.373.585 + 222 × 12.000) ÷ 1.200 = **5.865 đ/yêu cầu = 0,49×** [simulated].

## A3 · Tách theo loại yêu cầu

| Loại | Số yêu cầu | Tỉ lệ thành công | Số lần chạy mỗi yêu cầu | Chi phí mỗi việc thành công | So với 12.000 đ |
| --- | ---: | ---: | ---: | ---: | ---: |
| noi_dia | 824 | 95,0% (783) | 1,11 | 2.696 đ [simulated] | 0,22× [simulated] |
| hang_nang | 158 | 74,1% (117) | 1,47 | 8.221 đ [simulated] | 0,69× [simulated] |
| quoc_te | 150 | 27,3% (41) | 2,32 | 22.515 đ [simulated] | 1,88× [simulated] |
| doi_tac | 68 | 54,4% (37) | 1,88 | 10.215 đ [simulated] | 0,85× [simulated] |

- Loại nào không đáng để trợ lý xử lý? Với loại đó, cho chạy lại tới 3 lần có giúp không? **quoc_te**: 1,88× [simulated], chỉ 27,3% thành công, 91/150 ca chuyển nhân viên. Chạy lại có lợi ích biên rất thấp và không hiệu quả kinh tế: tỉ lệ ok 30,0% → 11,4% → 2,2% (lần 1 → 2 → 3); 198 lần chạy lại chỉ thêm 14 lần ok, 9 việc thành công, nhưng chiếm 58% tiền token + tool của loại này.
- doi_tac cũng loại khỏi pilot dù 0,85× [simulated]: chỉ 54,4% thành công, cộng 31 ca nhân viên làm thay thì cả hệ thống là 11.029 đ/yêu cầu = 0,92× [simulated], sát ngưỡng và có điều khoản riêng.
- Phạm vi pilot đề xuất: **noi_dia + hang_nang** (0,22× và 0,69× [simulated]; cả hệ thống 0,26× và 0,77× [simulated]). Ở noi_dia, lần chạy 2 vẫn ok 75,7%: 92 lần chạy lại thêm 60 việc thành công, nên chạy lại còn có ích ở loại này.

## A4 · Chi phí cố định (phạm vi noi_dia + hang_nang)

| Khối lượng | Việc thành công mỗi tháng | Chi phí cố định mỗi việc | Chi phí mỗi việc thành công + cố định | So với 12.000 đ |
| --- | ---: | ---: | ---: | ---: |
| 45.000 yêu cầu/tháng | 33.750 (= 45.000 × 900 ÷ 1.200) | 1.185 đ (= 40.000.000 ÷ 33.750) | 3.414 + 1.185 = 4.599 đ [simulated] | 0,38× [simulated] |
| Một nửa khối lượng | 16.875 (= 22.500 × 900 ÷ 1.200) | 2.370 đ (= 40.000.000 ÷ 16.875) | 3.414 + 2.370 = 5.784 đ [simulated] | 0,48× [simulated] |

Chi phí biến đổi trong phạm vi = 3.072.513 đ ÷ 900 việc thành công = 3.414 đ/việc [simulated]; 900/1.200 là tỉ lệ việc thành công trong phạm vi trên toàn mẫu.

- Chi phí cố định có đổi kết luận không? Ở khối lượng nào? Không đổi ở cả hai mức: 0,38× (45.000 yc/tháng) và 0,48× (22.500 yc/tháng) [simulated], vẫn dưới 12.000 đ. Cố định tỉ lệ nghịch với khối lượng: tổng chỉ chạm 12.000 đ khi còn 40.000.000 ÷ (12.000 − 3.414) = 4.659 việc thành công/tháng ≈ 6.212 yc/tháng [simulated].

## B1 · Độ nhạy: chín kịch bản

| Kịch bản | CPS (simulated) | Thay đổi so với gốc |
|---|---:|---:|
| Giá token gấp đôi | 4.723 đ | +5.6% |
| Giá token giảm một nửa | 4.346 đ | -2.8% |
| Tỉ lệ xem lại gấp đôi | 6.292 đ | +40.7% |
| Tỉ lệ xem lại giảm một nửa | 3.562 đ | -20.3% |
| Số ca làm lại gấp đôi | 6.787 đ | +51.8% |
| Số ca làm lại giảm một nửa | 3.315 đ | -25.9% |
| Lương nhân viên tăng 25% | 5.506 đ | +23.1% |
| Tối đa 2 lần chạy | 4.237 đ | -5.2% |
| Chỉ 1 lần chạy | 4.111 đ | -8.1% |

## B2 · Đổi đồng thời hai tham số

- Token gấp đôi **và** xem lại gấp đôi: **6.543 đ/việc** (+46.3%, simulated).
- Ba yếu tố nhạy nhất: **1. Làm lại → 2. Xem lại → 3. Chi phí nhân viên**.

## B3 · Giới hạn số lần chạy

| Giới hạn | Tổng Agent (simulated) | Không thành công | Cả hệ thống (simulated) | CPS Agent (simulated) |
|---|---:|---:|---:|---:|
| 1 lần | 3.621.781 đ | 319 | 7.449.781 đ | 4.111 đ |
| 2 lần | 4.093.220 đ | 234 | 6.901.220 đ | 4.237 đ |
| 3 lần | 4.373.585 đ | 222 | 7.037.585 đ | 4.472 đ |

- **2 lần** có tổng chi phí hệ thống thấp nhất (6.901.220 đ), khác với giới hạn có CPS thấp nhất (simulated).

## B4 · Xem lại 100% trong phạm vi

- 948 yêu cầu cần xem lại, 5 phút/yêu cầu; 48 ca làm lại, 9 phút/ca → CPS **11.743 đ**, bằng 0.98× baseline (simulated).
- Nếu làm lại mất 15,3 phút/ca → CPS **12.415 đ**, bằng 1.03× baseline (simulated).
- Để hòa vốn, thời gian xem lại phải không quá **5.1 phút** (làm lại 9 phút) hoặc **4.8 phút** (làm lại 15,3 phút).

---
### Trạng thái xác minh
- **ĐÃ ĐỐI CHIẾU P1/P2** tại commit `25bb25e`: 20/20 kịch bản A2/A3/A4/B1/B2/B3, 222/222 giá trị khớp, sai lệch bằng 0. B4 và D1 chưa có phần tương ứng trong P1 để so.
- Chi tiết sai lệch với tham chiếu: `report/team/p2_doi_chieu_so.md`.
