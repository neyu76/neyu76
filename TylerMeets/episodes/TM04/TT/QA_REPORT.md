# TT-001 / TM04 "Bryce — The Habitual Liar" · QA 8 trục (script v1, R2 các phần)

| # | Trục | Điểm | P0 | P1 | P2 (để lại) |
|---|---|---|---|---|---|
| 1 | Frame-0 + hook | 20/20 | 0 | 0 | — · H1 19/20; beat 1 = 1.75 s, cold open hết 2.81 s, WTF hết 6.06 s, "This is Bryce." 6.51 s |
| 2 | Sạch nội dung, twin, từ bóp FYP | 18/20 | 0 | 0 | Câu WTF có chửi (OWNER_LOCKED; theo dõi H-02). Bóng đập mặt: hài cartoon, không máu |
| 3 | Hình–lời trong thế giới 3D | 10/10 | 0 | **2 đã sửa** | "Twice" → Bryce giơ 2 ngón (MS_BRY_BALL); "Second period" → bảng 'PERIOD 2 - MUSIC' (WIDE_MUSIC_ROOM). Không đồ họa ngoài phụ đề |
| 4 | 6 mốc, đỉnh 55–65 %, 0 khoảng chết | 15/15 | 0 | 0 | Đỉnh 40.7–48.1 s = L12–L14 (sandwich bị lấy bằng lời nói dối); cú lật ở L19–L22 |
| 5 | Nhân quả & continuity | 9/10 | 0 | **1 đã sửa** | Cuối bài Tyler cầm vụn bánh (vô lý vì sandwich đã bị ăn) → đổi thành giấy gói rỗng. P2: thì quá khứ/hiện tại trộn lẫn như các tập mẫu |
| 6 | Toán thời lượng | 15/15 | 0 | 0 | 178 từ, 24 dòng, ước tính 74.0 s (nhanh 72.2 / chậm 78.7); T_fast ≥ 62 s |
| 7 | Giọng tự nhiên | 4/5 | 0 | 0 | P2: "Bro-bro-bro" và "Fweee! Fweee! FWEEEE!" phải kiểm ASR ở bước giọng; sai thì viết gạch nối và tạo lại riêng dòng đó |
| 8 | Gói xuất | 5/5 | 0 | 0 | Lossless 01 ↔ 02 ↔ 05 PASS |
| | **Tổng** | **96/100** | **0** | **0 còn lại** | |

## Continuity (Scene-State Delta)
- P01 sân bóng rổ: INFORMATION — khán giả biết Bryce bịa (phiếu Toán hôm qua). Bryce: phiếu bài tập → bóng rổ.
- P02 phòng nhạc: POWER — cả lớp thấy Bryce không biết thổi sáo. Recorder do cô giáo đưa, ở lại phòng nhạc.
- P03 cửa hàng trường: OWNERSHIP — sandwich của Tyler sang tay Bryce. Tyler giữ giấy gói.
- P04 hội chợ khoa học: TRUST — máy và hiệu trưởng tin Bryce. Bryce nhận ruy băng; Tyler nhận phiếu detention, vẫn cầm giấy gói.

## Rủi ro dựng (kiểm ở bước Blender)
- Cảnh bóng đập mặt: quỹ đạo bóng phải khớp, không xuyên đầu.
- Máy phát hiện nói dối: đèn xanh/đỏ dùng `flash()`, chữ "LIE DETECTOR" viết tay bằng `tex_quad`.
- Chỉ 1 người lớn có thoại (Hargrove). Cô giáo nhạc không thoại.
