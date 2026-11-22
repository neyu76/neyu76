# TT-001 La Mala Hora — QA 8 trục (script v1, khoá 22/11/2026)

Kết quả máy: 176 từ · 20 beat · center 72,3 s (fast 69,5 / slow 76,5) · `creator_rewards_60s_safe = true` · lossless roundtrip PASS · cổng khuôn 10 nhịp 0 blocker / 0 cảnh báo · opening-audit `--strict` PASS (beat 1 = 4,11 s, câu dài nhất 0–15 s = 18/20, Frame-0 PASS) · beat-audit `--strict` PASS (max 5,34 s) · kit-bridge PASS (31 cảnh, TB 2,36 s, max 4,52 s, thẻ dọc 22,6 %).

| # | Trục | Điểm | Nhận xét |
|---|---|---|---|
| 1 | Frame-0 + hook 3–5 bản (≥16/20) + vật thể | 19/20 | H1 19/20 thắng 4 bản khác; mở bằng vật thể chạm được (đống len đen ở ngã tư); bang ở từ 2–3. Trừ 1: âm 0,0 s chỉ là giọng + len kéo lê, cú nhấn mạnh nằm ở 0,85 s (đúng luật kit). |
| 2 | Sự thật, Sổ chống bịa, Twin, từ bóp FYP | 18/20 | 1910 + "spirit at dark crossroads, terrorizing people alone" + "lock of wool / whole sheep's fleece" khớp trích Espinosa; "someone you love will die soon" đóng khung "They say"; "woman in black" đóng khung "According to the legend". Twin CLEAR (max 2/5 với V03, Jaccard ≤ 0,261). Trừ 2: chưa tự đọc toàn văn JSTOR (dựa trên trích dẫn chương Springer); "She doesn't chase you / watches you walk home / which door you open" là **diễn giải sáng tạo** của người kể dựa trên niềm tin điềm báo, không phải trích nguồn (ghi CREATIVE). |
| 3 | Đồng bộ hình–lời 9:16 + thẻ dọc | 9/10 | "1910" hiện con dấu đúng lúc đọc (s7); "New Mexico" có tem bang (s8); "lock of wool"/"fleece" hiện đúng vật; thẻ 22,6 % (mục tiêu 20–30 %). Trừ 1: "The Evil Hour" chỉ có trên thẻ tiêu đề, không có thẻ riêng. |
| 4 | 10 nhịp, đỉnh 55–65 %, không khoảng chết >3 s | 15/15 | Đủ 10 nhịp; pivot "But here's the terrifying part" ở từ 99/176 = 56 % (40,7 s/73,1 s = 56 %); beat dài nhất 5,34 s nhưng mỗi cảnh ≤4,52 s nên hình luôn đổi. |
| 5 | Nhân quả, continuity, Scene-State Delta | 9/10 | P01 DANGER+INFO → P02 TRUST+SCALE → P03 POWER đảo (không vì bạn, vì người thân) → P04 TIME/"tonight" + loop. Trừ 1: đại từ đổi "it" (len) → "she" (người đàn bà) có chủ đích theo hình dạng, người xem có thể khựng nhẹ; hình s14 (len đứng dậy thành người) phải làm rõ chuyển đổi này. |
| 6 | Toán thời lượng & vách 60 s | 15/15 | 176 từ trong 165–180; 69,5–76,5 s nằm trong QA kit 68–78 s; fast ≥ 62 s. Hiệu chỉnh: EP05 179 từ → thực đo 72,5 s, nên ước 72,3 s là đáng tin. |
| 7 | Giọng tự nhiên, Safe Zone | 5/5 | Không "—"/"→", không thẻ TTS, "..." đúng 2 lần, câu 5–13 từ; caption ở y≈1296 trong Safe Zone; walker mặc hoodie xanh xám (không trắng sau phụ đề). |
| 8 | Đóng gói lossless + kit | 5/5 | 01-SCRIPT / 02-VOICE / 03-TIMELINE / 04-MANIFEST + 05-SHOTLIST + `EP06_la_mala_hora/script.txt` (token khớp 100 %), `style.json`, `SOURCES.md`, `TITLE.txt`. |
| | **Tổng** | **95/100** | 0 lỗi P0, 0 lỗi P1 còn mở. |

## Lỗi đã sửa trước khi khoá (Edit-Propagation)
- P1 · b005 dài 6,16 s > 6 s → rút "collecting old Spanish folk tales" thành "recording Spanish folklore" (P02 R2).
- P1 · trung thực nguồn: "hunting people who travel alone" → "terrorizing people who walk alone" (sát nguyên văn Espinosa "terrorizes the unfortunate ones who wander alone at night").

## P2 (ghi chú, không chặn)
- Chưa có quy tắc "bảo vệ" trong nguồn → nhịp 8 dùng điềm báo + lời khuyên của người kể "don't cross alone" (suy từ dữ kiện "săn người đi một mình"). Không bịa nghi lễ.
- Nhịp 4 "They call her La Mala Hora. The Evil Hour." — Milo đọc tiếng Tây Ban Nha: khi tạo giọng nên nghe kiểm "Mala Hora" (MAH-lah OH-rah); whisper có thể ghi sai "Mala Hora" → sửa JSON theo `check_transcript.py`.
- Bước tiếp theo (chưa chạy, chờ duyệt): báo giá SFX riêng 3 âm × 7,5 s (`custom_sfx_quote` trong packet), tạo giọng Milo từ `EP06_la_mala_hora/script.txt`, render từ `render_ep05.py`.
