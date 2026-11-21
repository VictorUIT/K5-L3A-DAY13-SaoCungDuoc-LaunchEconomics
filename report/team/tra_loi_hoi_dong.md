# Trả lời câu hỏi của hội đồng Gate 2a · Nhóm SaoCungDuoc (L3A)

**Câu hỏi:** Nếu tuần đầu phải xem lại 100%, chi phí mỗi việc thành công là bao nhiêu, và luật dừng chi phí 8.000 đ trong `pilot_plan.yaml` có tự kích hoạt ngay không?

## 1. Chi phí khi xem lại 100%

Phạm vi pilot noi_dia + hang_nang (982 yêu cầu, 900 việc thành công), theo B4 trong `bang_chi_phi.md` [simulated]:

- Xem lại: 948 yêu cầu × 5 phút × 2.000 đ = 9.480.000 đ
- Token + tool của mọi lần chạy: 224.513 đ
- Làm lại: 48 ca × phút làm lại × 2.000 đ

| Phút làm lại mỗi ca | Chi phí mỗi việc thành công | Chi phí cả hệ thống mỗi yêu cầu (cộng 82 ca không thành công × 12.000 đ) |
| --- | ---: | ---: |
| 9 phút (theo đề) | 10.568.513 ÷ 900 = **11.743 đ = 0,98×** | 11.764 đ = 0,98× |
| 15,3 phút (trung bình trong dữ liệu) | 11.173.313 ÷ 900 = **12.415 đ = 1,03×** | 12.380 đ = 1,03× |

Xem lại 100% thì trợ lý gần như không tiết kiệm được so với nhân viên tự làm (12.000 đ) [simulated].

## 2. Luật dừng chi phí có tự kích hoạt không

- **Mốc 8.000 đ/việc thành công** (hướng dẫn mẫu): có, sẽ kích ngay tuần đầu vì 11.743 đ > 8.000 đ. Vì vậy `pilot_plan.yaml` của nhóm **không dùng mốc này**.
- **Luật nhóm đang dùng:** NẾU chi phí biến đổi cả hệ thống mỗi yêu cầu > **9.600 đ** (= 0,8 × 12.000 đ, chừa 2.370 đ cố định mỗi việc khi khối lượng còn một nửa, A4) TRONG **2 tuần liên tiếp** THÌ PM trợ lý hoàn phí giảm xem lại theo bậc, thu hẹp về noi_dia và giới hạn 2 lần chạy.
  - Tuần đầu: **không kích**, vì luật cần 2 tuần liên tiếp.
  - Hết tuần 2 (20/12, bước 0.25): **có kích** nếu vẫn xem lại 100% (11.764 đ > 9.600 đ). Mốc kiểm tra "giảm xem lại theo bậc" trong hồ sơ là 21/12, muộn hơn một ngày. Luật có thể thu hẹp pilot về noi_dia trước khi kế hoạch giảm xem lại kịp áp dụng. Nhóm thừa nhận đây là điểm chưa khớp.

## 3. Cách xử lý

1. Bước 0.10 và 0.25 (07/12–20/12): chi phí khi xem lại 100% đã biết trước (0,98–1,03× [simulated]); chỉ theo dõi, không áp luật dừng chi phí.
2. Luật 9.600 đ tính **từ bước 0.50 (21/12)**. Trước mốc này, tỉ lệ xem lại phải đã giảm theo bậc khi tỉ lệ sửa + bỏ < 15% trong 1 tuần (đợt chạy thử: 21,1% trong phạm vi, 27/128).
3. Mục tiêu thời gian: mỗi lần xem lại ≤ 5,1 phút (làm lại 9 phút) hoặc ≤ 4,8 phút (làm lại 15,3 phút) để hoà vốn; đo phút thật bằng event `staff_review_decision` từ tuần 1, thay số simulated.
4. Luật an toàn (mở lại 7 ngày) vẫn áp dụng ngay từ tuần đầu, không thay đổi.

Đã cập nhật `pilot_plan.yaml`: luật chi phí ghi "TRONG 2 tuần liên tiếp tính từ bước 0.50 (2026-12-21 đến 2027-01-03)", kèm chú thích "Thay đổi thiết kế sau phản biện hội đồng". Đã cập nhật điều kiện tương ứng trong `ho_so_launch_v0.md`. Ngưỡng 9.600 đ, thời hạn 2 tuần, hành động và người phụ trách giữ nguyên. Đây là thay đổi thiết kế trước ngày bắt đầu 2026-12-07, khi chưa có dữ liệu pilot, nên không phải đổi luật sau khi xem kết quả.
