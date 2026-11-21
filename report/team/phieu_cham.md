# Phiếu chấm hội đồng Gate 2a

Nhóm số n chấm nhóm số n + 1; nhóm cuối chấm nhóm 1. Chấm theo bằng chứng trong hồ sơ, không theo cách trình bày: một đề xuất No-go có lý do bằng số được điểm cao hơn một đề xuất Go bỏ qua con số bất lợi.

- Nhóm chấm (hội đồng): SaoCungDuoc · L3A
- Nhóm được chấm: 04552 · L3A · repo `ducminhnwork/K5-L3A-DAY13-04552-LaunchEconomics`, commit `92e0a70`

| Tiêu chí | 0 điểm | 5 điểm | 10 điểm | Điểm | Lý do (có số) |
| --- | --- | --- | --- | ---: | --- |
| Đề xuất khớp bằng chứng | Mâu thuẫn với số của chính nhóm | Khớp nhưng bỏ qua một con số bất lợi | Khớp, nêu cả con số bất lợi và cách xử lý | 10 | "Go có điều kiện" khớp số của nhóm: cả hệ thống 5.865 đ = 0,49×; phạm vi cộng cố định 4.599 đ = 0,38× [simulated]. Mục "Con số bất lợi" nêu đủ 5 con số kèm cách xử lý: power 0,64 nếu tác động thật 5 điểm (Giám đốc vận hành ký); xem lại 100% 0,98×–1,03× (giảm theo bậc); mở lại 4,25% (so đối chứng +2 điểm, trần 6%); quoc_te 1,88× (loại); phút simulated (đo thật sau tuần 1). Hội đồng tự tính thêm: riêng hang_nang mở lại 8,23% (13/158), đã vượt trần 6% của chính nhóm, nhưng hồ sơ không nhắc |
| Số giả lập và phạm vi | Không nhãn; phạm vi "mọi yêu cầu" | Có nhãn hoặc có thu hẹp phạm vi | Nhãn ở mọi số giả lập; phạm vi thu hẹp có lý do bằng số | 10 | Phạm vi thu hẹp về noi_dia + hang_nang, có lý do bằng số: 0,22× và 0,69×; loại quoc_te 1,88× với 27,3% thành công, loại doi_tac 0,85× [simulated]. Mọi chi phí trong hồ sơ, bảng chi phí và pilot_plan đều có nhãn [simulated]; `simulated_inputs` liệt kê 6 nguồn. Góp ý nhỏ: cột "So với 12.000 đ" ở A3, A4 trong `bang_chi_phi.md` chưa gắn nhãn riêng |
| Pilot ra được quyết định | Không đối chứng hoặc thiếu cỡ mẫu | Đủ cỡ mẫu, luật dừng chung chung | Tách được tác động, đủ mẫu, luật dừng có ngưỡng, thời hạn, người có quyền dừng | 10 | Chia ngẫu nhiên theo nhân viên 20 + 20, phân tầng theo depot, đối chứng chạy cùng thời gian. D1 đúng cả năm câu (1.251 · 3.103/42 người · 1.000 · 300 · m ≥ 299, DE 6,96). Ba luật dừng đủ bốn vế, có ngưỡng, thời hạn, người dừng; rollback 30 phút. Hai điểm yếu: (1) bước 0.50 chỉ 1 tuần ≈ 30,7 yc/nhân viên/ngày × 7 ≈ 215 < 299 nên có thể thiếu mẫu (xem câu hỏi); (2) luật chi phí 8.000 đ/việc sẽ bị kích ngay nếu xem lại 100% (11.743 đ theo B4 của chính nhóm) |
| **Tổng** | | | | **30 / 30** | |

**Quyết định của hội đồng:** Go có điều kiện

**Lý do:** Phạm vi noi_dia + hang_nang rẻ hơn nhân viên tự làm ngay cả khi cộng chi phí cố định ở một nửa khối lượng (5.784 đ = 0,48× [simulated]). Pilot tách được tác động và đã ghi rõ đánh đổi mức chênh 6 điểm, power 0,64. Hội đồng đồng ý bốn điều kiện của nhóm và đề nghị thêm ba điều kiện: (a) kéo dài bước 0.50 hoặc ghi rõ số ngày đo để mỗi nhân viên đạt m ≥ 299 yêu cầu; (b) luật an toàn tách riêng hang_nang (mở lại 8,23% trong đợt chạy thử) và so với đối chứng cùng loại; (c) sửa ngưỡng chi phí 8.000 đ cho khớp kế hoạch giảm xem lại theo bậc, vì xem lại 100% đã là 11.743 đ [simulated]. Ngoài ra, mục 5 (bảng lỗi) còn "Chưa": `bang_loi.md` có bảng khắc phục 5 ca nhưng chưa có hai bộ nhãn và tỉ lệ đồng thuận.

**Một câu hỏi cho đội trình:** Bước 0.50 kéo dài 1 tuần (khoảng 2026-12-28 đến 2027-01-03). Với khoảng 1.500 × 82% ÷ 40 ≈ 30,7 yêu cầu trong phạm vi mỗi nhân viên mỗi ngày, mỗi người chỉ có khoảng 215 yêu cầu, ít hơn 299 mà D1 câu e yêu cầu. Nhóm đo chỉ số chính trong bao nhiêu ngày để đủ 859 hiệu dụng mỗi nhóm, mà vẫn chừa đủ 7 ngày theo dõi mở lại trước ngày quyết định 2027-01-15?

**Câu trả lời của đội trình (ghi lại tại buổi):** ...
