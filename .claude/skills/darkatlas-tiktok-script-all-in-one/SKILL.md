---
name: darkatlas-tiktok-script-all-in-one
description: "Skill 2/3 của bộ TikTok Dark Atlas (DA1, cá nhân hoá từ BASE_RAW v4.0 cho profile darkatlas-us-states-en). Nhận TT_TOPIC_PACKET_V1 và viết kịch bản truyền thuyết bang Mỹ theo khuôn 10 nhịp Dark Atlas (165–180 từ, Milo ~146 từ/phút, 68–78 s), CẤM VIẾT 1 HƠI: soạn 3–5 hook chấm ≥16/20, viết tuần tự P01..P04 qua scripts/tiktok_script_assembler.py (verify-part, opening-audit, stitch-draft, beat-audit, cổng khuôn 10 nhịp), QA 8 trục P0/P1/P2, lock-export 01-TT-SCRIPT + 02-TT-VOICE + 03-TT-TIMELINE.csv + 04-TT-MANIFEST.json, rồi kit-bridge xuất script.txt cho sonic_tts.py và 05-TT-SHOTLIST (30± cảnh gắn T(word,n), jumpscare 0,8–1,7 s, thẻ hook 5–9 s) khớp render_ep05.py. Dừng trước TTS/render. Dùng khi viết kịch bản TikTok TT-00x hoặc tập mới Dark Atlas từ packet."
---

# Dark Atlas TikTok Script All-in-One (`v4.0-DA1`, 22/11/2026)

- **Đầu vào:** `TT_TOPIC_PACKET_V1` từ [darkatlas-tiktok-topic-studio](../darkatlas-tiktok-topic-studio/SKILL.md) (profile, Sổ Giả Thuyết và bảng tập đã có nằm ở mục 0 của skill đó — đọc trước).
- **Đầu ra dừng ở kịch bản:** 4 file + bảng cảnh + `script.txt`. Giọng (sonic_tts), SFX, render, mix, QA video là việc của [dark-atlas-tales-production](../dark-atlas-tales-production/SKILL.md) và **chỉ chạy khi người dùng duyệt kịch bản**.
- Công cụ: `scripts/tiktok_script_assembler.py` (`v4.0-DA1`, không thư viện ngoài). Viết tắt `A=.claude/skills/darkatlas-tiktok-script-all-in-one/scripts/tiktok_script_assembler.py`.

---

## 0) Hồ sơ cấp kênh (khoá, đồng bộ với Skill 1)
- `profile_id = darkatlas-us-states-en`, revision 1 · track `creator_rewards` · mode `clean_voiceover` · `count_unit = words` · rate `MEASURED_SAMPLE` 146 / 138 / 152 · tổng **165–180 từ** · thời lượng QA **68–78 s** (fast ≥ 62 s tự đạt).
- **Shortform DNA (đo trên V01–V03 + EP01–EP05):** giọng vào 0,00 s; 27–34 cắt/72 s; cảnh TB 2,1–2,7 s; ≤5 s/cảnh (thẻ tiêu đề ≤7 s); phụ đề Oswald Bold in hoa 84 px, từ khoá đỏ (206,50,46), tâm ~67,5 % chiều cao; thẻ hook nền đen chữ đỏ ~150 px; kết ~0,75 s sau chữ cuối.
- **Voice Guide 5 thành tố (Milo):** (1) câu ngắn, 6–14 từ; (2) động từ cụ thể, danh từ chạm được (porch light, crossroads, swing chain); (3) không tính từ cảm xúc chung chung ("terrifying" chỉ được 1 lần trong câu nhịp 7); (4) "..." **đúng 2 lần**: trước mệnh lệnh hook và trước câu thoại/cao trào; (5) không thẻ TTS `[whisper]`, không `—`, không `→`, không "Did you know…?".
- **Thẻ dọc của kênh (thay "14 Thẻ Dữ liệu"):** kit vẽ vector, không có biểu đồ. Dùng **thẻ trong-thế-giới** tràn khung 9:16, mục tiêu **20–30 % số cảnh** (giả thuyết H6): ① thẻ hook đen chữ đỏ · ② thẻ tiêu đề (nhãn `<STATE> · LEGEND`) · ③ con dấu năm/số lớn (1822, 14 INCHES) · ④ biển báo/biển đường thật của bang · ⑤ trang báo cũ / trang sổ tay (như EP02, EP04) · ⑥ lá cờ nước xuất xứ khi lời kể nhắc nước khác · ⑦ đồng hồ/giờ (12:00) · ⑧ dòng chữ quy tắc (DON'T…) · ⑨ chân dung + nhãn dân tộc (`TOLD BY THE PAIUTE`). Mọi con số/giờ đọc trong 0–30 s phải hiện đúng lúc đọc ("nói gì hình hiện nấy").

## 1) Kỷ luật CẤM VIẾT 1 HƠI (`AGENT_AUTONOMOUS_STEP_LOOP`, 1 lượt tool = 1 phần)
1. **Blueprint (1 lượt):** đọc packet → soạn **3–5 hook** cho nhịp 1–2, chấm 5 tiêu chí × 0–4 (*Mute Test Frame-0 · độ sắc What+Why · nguy cơ cá nhân "you" · câu hỏi kéo sang 15–30 s · tự nhiên 0 % mùi AI*), loại 4 Hook Killers (mở bằng năm/"Back in", thuật ngữ khô, rao bán, khoe). Chỉ hook ≥16/20 được chọn; ghi bảng điểm vào `TT/<id>/01b-HOOK-SELECTION.md`.
2. **Init:**
   ```bash
   python -I $A init --workspace dark_atlas/TT/<TT-00x>_<slug> --topic-id TT-00x --slug <slug> \
     --part-budgets "42,50,46,36" --frame0-text "IN <STATE>, IF..."
   ```
   (Mặc định đã là creator_rewards / words / 146-138-152 / MEASURED_SAMPLE / max beat 6 s / strict natural speech.)
3. **Mỗi phần 1 lượt riêng:** viết `PARTS/P0k.txt` (mỗi dòng = 1 beat lời đọc 1–2 câu; không tiêu đề, không ghi chú) → `verify-part`. Sau P01 chạy ngay `opening-audit --p01-only`. Không ghi nhiều phần trong 1 lượt, không sinh cả bài rồi cắt.
4. Đủ 4 phần → `stitch-draft` (tự chạy **cổng khuôn 10 nhịp**: mở "In <STATE>, if", "..." = 2, Because, They call, According to the legend/They say, But here's the terrifying part, So if you, 165–180 từ) → `beat-audit` → QA 8 trục → sửa P0/P1 trên `PARTS/` + `verify-part --revision r+1` → `lock-export` → `kit-bridge`.

### Bản đồ 4 phần ↔ 10 nhịp (mặc định)
| Phần | Nhịp | Ước tính | Nhiệm vụ & Scene-State Delta |
|---|---|---|---|
| P01 (~42 từ) | 1 "In <STATE>, if …" · 2 mệnh lệnh (thẻ hook) · 3 "Because…" · 4 "They call her <NAME>." | 0–17 s | DANGER↑ (tình huống), INFORMATION (lý do sốc), tên = thẻ tiêu đề |
| P02 (~50 từ) | 5 dữ kiện thật (năm, nơi, ai ghi lại) · 6 "According to the legend…" | 17–38 s | TRUST (thật) → SCALE (truyền thuyết) |
| P03 (~46 từ) | 7 "But here's the terrifying part." · 8 quy tắc/điểm yếu "They say only…" | 38–57 s | đỉnh ở ~55–62 %; DANGER/POWER đảo chiều |
| P04 (~36 từ) | 9 "So if you're ever … tonight, …" · 10 câu đảo ngược lặp tiền đề | 57–72 s | TIME (đêm nay, "you") → Loop về câu mở |

## 2) Luật viết riêng của kênh
- Nhịp 1 phải có **vật thể/hành động hữu hình** và địa danh bang; nhịp 2 là mệnh lệnh ≤6 từ đọc, thẻ ≤3 từ (`DON'T LOOK BACK.`).
- Nhịp 5 chỉ chứa dữ kiện **có trong `SOURCES.md`**; năm không chắc thì viết thập niên ("In the 1930s"). Nhịp 6–8 mở bằng *According to the legend / They say / One version says*.
- Truyền thuyết bản địa: nêu tên dân tộc ở nhịp 3 hoặc 5; không mô tả nghi lễ thật như thật; không "savage", không "evil spirits of the Indians".
- Câu cuối **đảo ngược hoặc lặp lại tiền đề** (V03 "Her feet never do", EP04 "It's waiting for you to come find it") để Loop khít.
- Watchlist (assembler cảnh báo): blood, gore, murder, corpse, kill/killed, suicide, self-harm → thay bằng "taken", "never came home", "remains". Kit cấm máu.
- **Không viết thứ kit không dựng được:** đám đông lớn, cảnh quay thật, chữ viết dài trên màn hình, bản đồ chi tiết, hơn 1 giọng.

## 3) QA 8 trục (`/100`, P0 = chặn, P1 = phải sửa trước khoá, P2 = ghi chú)
1. Frame-0 + 3–5 hook ≥16/20 + mở bằng vật thể (20) — P0 nếu không có vật thể/bang trong 2 từ đầu.
2. Sự thật & nguồn, Twin Check, sạch từ bóp FYP (20) — P0 nếu có dữ kiện không nguồn hoặc twin ≥3/5.
3. Đồng bộ hình–lời 9:16 + thẻ dọc 20–30 % (10).
4. 10 nhịp đủ, đỉnh 55–65 %, không khoảng chết >3 s (15) — P0 nếu cổng khuôn báo blocker.
5. Nhân quả, continuity, Scene-State Delta mỗi phần (10).
6. Toán thời lượng 68–78 s @146, fast ≥62 s (15) — P0 nếu ngoài 165–180 từ.
7. Giọng tự nhiên chống văn AI, Safe Zone phụ đề (5).
8. Đóng gói lossless 4 file + 05-SHOTLIST + script.txt khớp token (5).
Ghi kết quả vào `TT/<id>/06-TT-QA-REPORT.md`. Chỉ khoá khi ≥85/100 và 0 lỗi P0/P1.

## 4) kit-bridge: bảng cảnh khớp kit
Viết `TT/<id>/shots.json`:
```json
{"paragraph_starts": ["b001","b004", "..."],
 "shots": [{"id":"s0","role":"open","at_sec":0.0,"visual":"...","camera":"...","motion":"...","card":"","sfx":"...","transition":"cut"},
           {"id":"s0j","role":"jumpscare","at_sec":0.85,"visual":"face fills frame","sfx":"<creature> x3 + sub_boom"},
           {"id":"s1","role":"hook_card","word":"don't","n":1,"card":"HOOK CARD: DON'T ...","transition":"cut"}]}
```
Vai trò: `open, jumpscare, hook_card, title_card, fact, legend, pivot, rule, advice, reveal, scene`. Neo bằng `word`+`n` (lần xuất hiện thứ n trong lời đọc) — chính là `T("word", n)` trong `render_epXX.py`; đếm kỹ từ lặp (in, the, they, her, it).
```bash
python -I $A kit-bridge --workspace <ws> --topic-id TT-00x --shots <ws>/shots.json --out-dir <ws>/EXPORT --episode-dir dark_atlas/EPxx_<name>
```
Cổng: 26–34 cảnh · TB 2,1–2,7 s · ≤5 s (thẻ tiêu đề ≤7 s) · jumpscare 0,8–1,7 s · thẻ hook 4–9,5 s · cảnh cuối = `reveal`. Thời gian là **ước tính theo tốc độ**; sau khi có transcript thật, render dùng `T()` nên tự khớp.

## 5) Gói xuất
`EXPORT/01-TT-SCRIPT-<slug>.txt` · `02-TT-VOICE-<slug>.txt` (lossless, ngăn bằng " | " — **không** đưa file này vào TTS) · `03-TT-TIMELINE-<slug>.csv` (beat_id ↔ dải 00_03s/03_15s/15_30s/30_60s/60s+, dùng cho D+3/D+7) · `04-TT-MANIFEST-<slug>.json` · `05-TT-SHOTLIST-<slug>.csv` + `.summary.json` · `dark_atlas/EPxx_<name>/script.txt` (đoạn văn theo nhịp — file duy nhất đưa vào `sonic_tts.py`).
Kèm `TITLE.txt` nháp ("If … in <State>… DON'T …" + mô tả + hashtag, ≥3 từ khoá Search) và `SOURCES.md`.

## 6) Sửa sau khi khoá (`Edit-Propagation`)
Sửa câu nào thì sửa trong `PARTS/P0k.txt`, chạy `verify-part --revision <r+1>` (tự huỷ khoá, tăng script_version), rồi stitch → lock-export → kit-bridge lại. Không sửa tay file trong `EXPORT/`.
