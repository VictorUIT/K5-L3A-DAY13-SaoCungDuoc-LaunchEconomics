# P2 · Hồ sơ kiểm số độc lập

## Trạng thái và nguồn

- Tính trên CSV trong repo theo công thức đề; **không** lấy đầu ra `src/lab13.py` làm kết quả kiểm độc lập.
- Các khoản review/rework và kết quả suy ra từ chúng phải ghi **simulated**.
- Kết quả bảng dưới đây được kiểm tra với **đáp án tham chiếu trong hướng dẫn** theo ngưỡng 2%; đây KHÔNG phải việc chấm đúng tuyệt đối P1.

## Ít nhất một phép tính tay độc lập (bắt buộc P2)

1. Tool: **5600 lần × 15 đ/lần = 84.000 đ** (trace).
2. Xem lại: **890 phút × 2.000 đ/phút = 1.780.000 đ**, simulated.
3. Làm lại: **1.132 phút × 2.000 đ/phút = 2.264.000 đ**, simulated.
4. Tổng: 245.585 + 84.000 + 1.780.000 + 2.264.000 = **4.373.585 đ**, simulated.
5. CPS: 4.373.585 / 978 = **4471.97 đ/việc**, simulated.
6. B3 giới hạn 2: 4.093.220 + 234 × 12.000 = **6.901.220 đ**, simulated.

## D1 · Kiểm số cỡ mẫu và thiết kế pilot

| Bài | Phép tính | Kết quả |
|---|---|---:|
| a | So hai tỉ lệ 0,70 và 0,75, alpha=0,05, power=0,80 | 1251 mỗi nhóm |
| b | DE = 1 + (75−1)×0,02 = 2.48; n=ceil(1251×2.48) | 3103 yc / 42 nhân viên mỗi nhóm, 84 tổng |
| c | 20 nhân viên / ICC=0,02 | ≤ 1.000 hiệu dụng |
| d | 6 depot / ICC=0,02 | ≤ 300 hiệu dụng |
| e | MDE 6 điểm, n=859; 20m/(1+(m−1)×0,02) ≥ n | m ≥ 299 yc/nhân viên |

## Đối chiếu số với hướng dẫn (sai lệch tối đa 2%)

| Mục | P2 tính từ CSV | Tham chiếu | Sai lệch | Kết quả |
|---|---:|---:|---:|---|
| `A2.token` | 245,585.13 | 245,585.00 | 0.000% | PASS |
| `A2.tool` | 84,000.00 | 84,000.00 | 0.000% | PASS |
| `A2.retry_cost` | 93,804.49 | 93,804.00 | 0.001% | PASS |
| `A2.review` | 1,780,000.00 | 1,780,000.00 | 0.000% | PASS |
| `A2.rework` | 2,264,000.00 | 2,264,000.00 | 0.000% | PASS |
| `A2.total` | 4,373,585.13 | 4,373,585.00 | 0.000% | PASS |
| `A2.success` | 978.00 | 978.00 | 0.000% | PASS |
| `A2.cps` | 4,471.97 | 4,472.00 | 0.001% | PASS |
| `A2.invoice_per_req` | 274.65 | 274.70 | 0.017% | PASS |
| `A4.full_cps_with_fixed` | 4,599.09 | 4,599.00 | 0.002% | PASS |
| `A4.half_cps_with_fixed` | 5,784.27 | 5,784.00 | 0.005% | PASS |
| `B1.token_double` | 4,723.08 | 4,723.00 | 0.002% | PASS |
| `B1.token_half` | 4,346.41 | 4,346.00 | 0.010% | PASS |
| `B1.review_double` | 6,292.01 | 6,292.00 | 0.000% | PASS |
| `B1.review_half` | 3,561.95 | 3,562.00 | 0.001% | PASS |
| `B1.rework_double` | 6,786.90 | 6,787.00 | 0.002% | PASS |
| `B1.rework_half` | 3,314.50 | 3,315.00 | 0.015% | PASS |
| `B1.salary_plus25` | 5,505.71 | 5,506.00 | 0.005% | PASS |
| `B1.cap2` | 4,237.29 | 4,237.00 | 0.007% | PASS |
| `B1.cap1` | 4,110.99 | 4,111.00 | 0.000% | PASS |
| `B2.both` | 6,543.12 | 6,543.00 | 0.002% | PASS |
| `B3.system_cap1` | 7,449,780.64 | 7,449,781.00 | 0.000% | PASS |
| `B3.system_cap2` | 6,901,220.23 | 6,901,220.00 | 0.000% | PASS |
| `B3.system_cap3` | 7,037,585.13 | 7,037,585.00 | 0.000% | PASS |
| `B4.cps_9m` | 11,742.79 | 11,743.00 | 0.002% | PASS |
| `B4.cps_15_3m` | 12,414.79 | 12,414.00 | 0.006% | PASS |
| `D1.n_5pt` | 1,251.00 | 1,251.00 | 0.000% | PASS |
| `D1.n_6pt` | 859.00 | 859.00 | 0.000% | PASS |
| `E1.primary_pct` | 82.83 | 82.83 | 0.004% | PASS |
| `E1.ignore_pct` | 27.12 | 27.12 | 0.005% | PASS |
| `E1.reopen_pct` | 4.25 | 4.25 | 0.000% | PASS |

## Đối chiếu với kết quả P1

**MATCHED** — 7 khóa A2 khớp kết quả P1.
- `token`: {'p1': 245585.13199999998, 'p2': 245585.13199999998, 'diff': 0.0, 'relative_error_pct': 0.0, 'status': 'PASS'}
- `tool`: {'p1': 84000.0, 'p2': 84000.0, 'diff': 0.0, 'relative_error_pct': 0.0, 'status': 'PASS'}
- `xem_lai`: {'p1': 1780000.0, 'p2': 1780000.0, 'diff': 0.0, 'relative_error_pct': 0.0, 'status': 'PASS'}
- `lam_lai`: {'p1': 2264000.0, 'p2': 2264000.0, 'diff': 0.0, 'relative_error_pct': 0.0, 'status': 'PASS'}
- `tong`: {'p1': 4373585.132, 'p2': 4373585.132, 'diff': 0.0, 'relative_error_pct': 0.0, 'status': 'PASS'}
- `thanh_cong`: {'p1': 978.0, 'p2': 978.0, 'diff': 0.0, 'relative_error_pct': 0.0, 'status': 'PASS'}
- `cps`: {'p1': 4471.968437627812, 'p2': 4471.968437627812, 'diff': 0.0, 'relative_error_pct': 0.0, 'status': 'PASS'}

## Phần P2 cần chốt sau khi các thành viên bàn giao

- [x] P1: A1 và tests biên ĐẠT; `mo_hinh` khớp P2 tại commit `25bb25e`; xem đối chiếu mở rộng bên dưới.
- [ ] P3/P4: dùng số đã xác nhận để hoàn thiện chỉ số và hồ sơ quyết định.
- [ ] Nhóm trưởng: chốt báo cáo, duyệt chéo, merge và push; P2 dẫn commit bằng chứng trong báo cáo cá nhân.

## Đối chiếu mở rộng với P1 — commit `25bb25e`

20/20 kịch bản, 222/222 giá trị khớp; sai lệch tuyệt đối lớn nhất bằng 0 (kiểm tra bằng `math.isclose`, rel_tol=1e-12, abs_tol=1e-8).

| Kịch bản | Số giá trị so | Sai lệch lớn nhất | Kết quả |
|---|---:|---:|---|
| `A2` | 12 | 0 | PASS |
| `A3.noi_dia` | 12 | 0 | PASS |
| `A3.hang_nang` | 12 | 0 | PASS |
| `A3.quoc_te` | 12 | 0 | PASS |
| `A3.doi_tac` | 12 | 0 | PASS |
| `B1.token_double` | 12 | 0 | PASS |
| `B1.token_half` | 12 | 0 | PASS |
| `B1.review_double` | 12 | 0 | PASS |
| `B1.review_half` | 12 | 0 | PASS |
| `B1.rework_double` | 12 | 0 | PASS |
| `B1.rework_half` | 12 | 0 | PASS |
| `B1.salary_plus25` | 12 | 0 | PASS |
| `B1.cap2` | 12 | 0 | PASS |
| `B1.cap1` | 12 | 0 | PASS |
| `B2` | 12 | 0 | PASS |
| `B3.cap1` | 12 | 0 | PASS |
| `B3.cap2` | 12 | 0 | PASS |
| `B3.cap3` | 12 | 0 | PASS |
| `A4.full` | 3 | 0 | PASS |
| `A4.half` | 3 | 0 | PASS |

- `python lab13.py` chạy từ `src/` thành công, ba phép thử A1 và tests biên đều ĐẠT.
- CLI P1 hiện in A1–A4; bảng B được kiểm bằng cách gọi `mo_hinh()` với từng bộ tham số, chưa phải bảng được CLI P1 in ra.
- B4 và D1 vẫn chỉ có kết quả độc lập P2; chưa có phần tương ứng trong P1 để so. Ba chỉ số E1 cũng là kết quả độc lập P2.
