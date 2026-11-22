---
name: dark-atlas-tales-production
description: Phân tích mẫu, lên kế hoạch, sản xuất và QA video dọc 9:16 (~72 s) kể truyền thuyết kinh dị dân gian theo từng quốc gia, theo phong cách quan sát được ở kênh TikTok @darkatlastales — minh hoạ vector phẳng 2D vẽ bằng code, đêm xanh đen, trăng tròn có quầng, khuôn kể 10 nhịp "In <NƯỚC>, if… → thẻ đen chữ đỏ → Because… → They call her <TÊN> (thẻ tiêu đề) → bối cảnh → According to the legend → But here's the terrifying part → quy tắc/điểm yếu → So if you ever… → câu đảo ngược + lộ mặt quái vật", phụ đề Oswald in hoa hiện từng từ có từ khoá đỏ, một giọng kể (Sonic Voice "Milo"), nhạc nền u ám dùng chung. Dùng khi người dùng nhắc darkatlastales, "Dark Atlas", "Truyện ma các nước", truyền thuyết đô thị/quỷ dân gian của một nước, yêu cầu làm tập mới, viết kịch bản, bảng cảnh, bản thử, QA hoặc bổ sung video mẫu. Chế độ ANALYZE, PLAN, PRODUCE, QA. v1.2 — dựng từ 3 mẫu (V01–V03), EP01 Kuchisake-onna (series các nước) và 3 tập series bang Mỹ đã duyệt: EP02 Belsnickel, EP04 Kushtaka, EP05 Nimerigar.
---

# dark-atlas-tales-production (v1.2 — 21/11/2026)

Skill này là **quy trình + số đo** rút từ 3 video mẫu và các vòng góp ý của người dùng. Nó không phải mô hình đã được huấn luyện.
- Giải thích và báo cáo cho người dùng bằng **tiếng Việt**. Kịch bản, prompt tạo ảnh, nhạc, giọng viết bằng **tiếng Anh**.
- Không hứa "giống 100 %", không đưa ra phần trăm giống. Chấm riêng từng hạng mục: kể chuyện, hình, camera, chữ, giọng, nhạc/SFX, nhịp dựng.
- **Trước khi làm tập mới, đọc theo thứ tự:** `references/dac_ta_phong_cach.md` (số đo), `references/quy_tac_san_xuat.md` (luật dựng + bài học từ góp ý), `references/qa_checklist.md`.

## Thư mục dự án
`DA/` = thư mục `dark_atlas/` của dự án. Trên máy gốc là `F:\Truyện ma các nước\dark_atlas\`; trong gói bàn giao là `DarkAtlas_US_States_Kit/dark_atlas/`. Mọi lệnh chạy từ `DA/`. Đọc `DA/PROJECT_STATE.md` và `DA/SERIES_PLAN_US_STATES.md` trước, cập nhật sau mỗi bước.
- `DA/refs/` — V01_mother_calls, V02_ticking_roof, **V03_look_at_feet (mẫu chính)**.
- `DA/analysis/` — transcript có mốc từng từ, stems demucs, khung hình đo.
- `DA/tools/` — `engine.py`, `style.py` (engine vẽ), `render_ep02/04/05.py` (khuôn tập series Mỹ), `sonic_tts.py` (giọng), `transcribe.py`, `check_transcript.py`, `fit_voice.py`, `build_sfx.py`, `mix_episode.py`, `qa_metrics.py`, `qa_full.py`.
- `DA/assets/music/dark_bed_master_5min.wav` — **nhạc nền dùng chung cho mọi tập.** Không tạo nhạc mới cho từng tập trừ khi người dùng yêu cầu.
- `DA/fonts/` — Oswald-Bold/Regular (phụ đề, tiêu đề). Chữ Nhật: `C:/Windows/Fonts/YuGothB.ttc`.
- `DA/EPxx_<tên>/` — mỗi tập: `script.txt`, `style.json`, `voice_milo.mp3` + transcript, `sfx.wav`, `mix.wav`, MP4.
- Bản đóng gói script nằm ở `scripts/` của skill; bản làm việc ở `DA/tools/`. Khi sửa thì sửa ở `DA/tools/` rồi chép sang `scripts/`.

## Thứ bậc mẫu
1. **V03 "If She Asks You for Help on the Road… LOOK AT HER FEET" (Pichal Peri, Pakistan)** là mẫu chính, chọn ngày 17/11/2026. Bản thử dựng lại V03 0–32,7 s (`DA/test_v03/TEST_V03_milo_v5.mp4`) được người dùng duyệt "Đạt".
2. V01 (Naale Baa, Bangalore) và V02 (Manananggal, Philippines) cùng định dạng: cùng khuôn 10 nhịp, cùng kiểu hình và phụ đề.
3. **Chuẩn tập đã qua QA: `DA/EP01_kuchisake/EP01_Kuchisake-onna_DarkAtlas_v3.mp4` và `DA/EP02_belsnickel/EP02_Belsnickel_DarkAtlas_v2.mp4`** (tập bang Mỹ: chép `render_ep02.py`; có sẵn nhà trại, kho thóc hex sign, cầu có mái, nội thất, kẹo bay, tay với, nhân vật áo lông). Tập mới bắt đầu bằng cách chép `render_ep01.py` rồi thay cảnh, giữ nguyên engine và style.

## Chế độ
### ANALYZE (khi có video mẫu mới)
Đặt ID V04+, chép vào `DA/refs/`. Đo bằng `scripts/qa_metrics.py`, transcript bằng faster-whisper (CPU int8, đọc âm thanh qua ffmpeg), tách giọng bằng demucs. Ghi các nhận xét dưới dạng QS / ĐO / SL / CHƯA RÕ. Chỉ cập nhật `dac_ta_phong_cach.md` khi có số đo.

### PLAN (khi người dùng đưa chủ đề hoặc nói "làm tập mới")
1. **Chọn truyền thuyết** của một nước chưa làm. Kiểm tra nguồn bằng WebSearch: lấy 1–2 dữ kiện thật (năm, địa danh, sự kiện) và tách rõ phần truyền thuyết.
2. **Viết kịch bản** theo khuôn 10 nhịp (`templates/script_template.md`): 165–180 từ. Chỉ dùng "..." ở 2 chỗ (trước thẻ hook và trước câu hỏi cao trào). Phần truyền thuyết luôn mở bằng "they say / according to the legend".
3. **Tạo `style.json` riêng** theo `templates/style_template.json`: màu nhân vật chính, nạn nhân, điểm nhấn văn hoá. Mỗi tập một bảng màu, không dùng lại màu be/trắng chung chung. Bối cảnh phải có ít nhất 4 dấu hiệu nhận ra ngay nước đó (kiến trúc, biển báo, chữ viết, đồ vật, trang phục).
4. **Bảng cảnh:** 30–33 cảnh, mỗi cảnh trung bình 2,2–2,6 s, dài nhất ≤ 5 s (trừ thẻ tiêu đề). Gắn mỗi lần cắt vào một từ của transcript.

### MỞ ĐẦU JUMPSCARE (bắt buộc, người dùng yêu cầu 19/11/2026)
"Đoạn đầu cần kinh dị hơn, hiện thẳng mặt kinh dị ra hù luôn, không thì người xem lướt đi." Trong **0,8–1,7 s đầu**:
- Cắt thẳng vào **mặt quái vật chiếm trọn khung**. Mặt lao vào ống kính (zoom từ khoảng 3,2 xuống 1,45 trong 0,16 s), chớp màu 2 khung, rung mạnh rồi tắt dần.
- Ánh sáng kiểu phim kinh dị: bóng tối từ trên xuống, ánh đỏ hắt từ dưới lên. Mắt có điểm sáng, răng nanh. Không có máu.
- SFX cùng lúc: **chỉ dùng tiếng của chính quái vật đó** (người dùng: "đừng dùng tiếng hú, dùng đúng tiếng của quái vật"), chồng 3 lớp (gốc, hạ 4 nửa cung, nâng 5 nửa cung) + `sub_boom`. Không dùng tiếng hét người hay `stinger_jumpscare` ở cú hù mở đầu.
- Ẩn phụ đề trong cú jumpscare. Sau đó quay lại cảnh mở đầu như bình thường.
- Màu chớp và cách lao vào đổi theo từng tập (đỏ, xanh, trắng; lao vào, trồi lên, quay đầu).

### KHÁC BIỆT MỖI TẬP (bắt buộc)
Trước khi dựng, chọn và ghi vào bảng biến thể trong `references/quy_tac_san_xuat.md`: thẻ tiêu đề, chuyển cảnh, ngôn ngữ camera, màu, cách lộ mặt, điểm nhấn thẻ hook, SFX đặc trưng. Không dùng lại lựa chọn của 2 tập gần nhất. Chỉ khuôn 10 nhịp, thẻ hook đen chữ đỏ, phụ đề, giọng và nhạc nền là cố định.

### PRODUCE
1. **Giọng:** Sonic Voice, Milo – Calm, Soothing and Meditative (`GUDYcgRAONiI1nXDcNQQ`), model eleven_v4, **speed 1.05**. Cần biến môi trường `SONIC_API_KEY`. Lệnh (trong `DA/EPxx/`): `python ../tools/sonic_tts.py speak script.txt voice_milo.mp3 --voice GUDYcgRAONiI1nXDcNQQ --speed 1.05`. Mục tiêu: 140–150 từ/phút, 68–78 s.
   - Transcript: `PYTHONIOENCODING=utf-8 python -I ../tools/transcribe.py . voice_milo.mp3`, rồi **luôn** chạy `python -I ../tools/check_transcript.py .` và sửa JSON đến khi "OK" (whisper hay nghe sai tên riêng, bỏ sót hoặc bịa từ).
   - Nếu dài quá 78 s hoặc đọc nhanh quá 152 từ/phút: `python -I ../tools/fit_voice.py voice_raw.mp3 voice_milo.mp3 --keep "<giây>:0.6,..." --cap 0.33 --tempo 0.97`, không tạo lại giọng.
2. **Dựng hình:** chép `render_ep05.py` (mới nhất, có jumpscare, chuyển cảnh whip, màu theo tập) → `render_epXX.py`, đổi tên thư mục tập, thay cảnh và nhân vật. Dùng `T("word", n)` để lấy mốc từ; với từ lặp lại, đếm đúng lần xuất hiện. Mỗi cảnh phải có chuyển động camera và ít nhất một chuyển động nhỏ trong cảnh.
3. **Kiểm tra ảnh tĩnh trước:** `python -I render_epXX.py DA "t1,t2,…"` → `stills.jpg`. Soi kỹ tạo hình và phụ đề trước khi render toàn bộ (mất khoảng 12–15 phút).
4. **SFX:** dùng thư viện `DA/assets/sfx/horror/` (tạo một lần bằng Magnific · ElevenLabs SFX, **không tạo lại**). Chỉ tạo thêm 2–3 âm thanh đặc trưng khi tập có quái vật mới (5 credit mỗi giây, báo giá cho người dùng trước khi tạo), lưu vào `DA/assets/sfx/epXX_<tên>/`. Mỗi video 8–10 điểm SFX, 3 giây đầu phải hé lộ quái vật kèm âm thanh đặc trưng của nó. Xem `DA/assets/sfx/README.md`.
5. **SFX theo cue:** viết `EPxx/sfx_cues.json` (file thư viện, thời điểm, dB, mức duck dưới giọng), rồi chạy `python -I tools/build_sfx.py EPxx EPxx/sfx_cues.json EPxx/sfx.wav`. Mẫu: `EP04_kushtaka/sfx_cues.json`.
6. **Trộn âm:** `python -I tools/mix_episode.py voice_milo.mp3 mix.wav <dur> --sfx sfx.wav --sfx_gain 1.0 --bed us_bed_master_5min.wav` (series bang Mỹ; series các nước bỏ `--bed`). Nhạc mặc định −25 LUFS (người dùng muốn nhạc nhỏ); script tự bù tổng về −16 LUFS. Ghép: `ffmpeg -i EPxx/epXX_noaudio.mp4 -i EPxx/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart EPxx/EPxx_<Tên>_DarkAtlas.mp4`.

### QA (bắt buộc trước khi giao)
Chạy `python -I tools/qa_full.py EPxx/EPxx_<Tên>_DarkAtlas.mp4`: đo đủ 11 chỉ số, in PASS/FAIL theo bảng trong `references/qa_checklist.md` và xuất `qa_sheet.jpg` (1 khung mỗi giây). Xem kỹ bảng khung bằng mắt. Ghi lỗi vào nhật ký lỗi và sửa tận gốc. Chỉ báo "đạt" khi mọi chỉ số nằm trong khoảng cho phép.

## Series bang Mỹ — quy trình đã chốt (EP02, EP04, EP05)
1. **PLAN:** lấy truyền thuyết tiếp theo trong `DA/SERIES_PLAN_US_STATES.md`; tra nguồn; viết kịch bản 165–180 từ; tạo `SOURCES.md`, `style.json`; chọn biến thể (bảng trong `quy_tac_san_xuat.md`); **báo giá SFX riêng** (5 credit/giây). **Dừng, gửi kịch bản cho người dùng duyệt.** Chưa duyệt thì không tạo giọng hay dựng hình.
2. **Giọng → transcript → check_transcript → (fit_voice)** như mục PRODUCE.
3. **SFX riêng:** 2–3 âm thanh của quái vật mới qua Magnific `audio_sfx_generate` (ElevenLabs), lưu `DA/assets/sfx/epXX_<tên>/`, ghi vào README. Không tạo lại thư viện chung.
4. **Dựng:** `render_epXX.py` → ảnh tĩnh 30+ mốc → soi lỗi (vật trắng sau phụ đề, mép đen khi camera ra ngoài khung vẽ, nhân vật bị cắt, hoạ tiết chấm bi, nhân vật trông dễ thương thay vì đáng sợ) → sửa → render toàn bộ (12–15 phút, chạy nền).
5. **Âm thanh:** `sfx_cues.json` (mở đầu jumpscare bằng tiếng quái vật 3 lớp + sub_boom; 10–25 cue; SFX hạ dưới giọng) → `build_sfx.py` → `mix_episode.py --bed us_bed_master_5min.wav --sfx_gain 1.0`.
6. **QA:** `qa_full.py` phải ĐẠT cả 11 chỉ số, rồi viết `TITLE.txt` (tiêu đề "If …… DON'T …", mô tả, hashtag) và gửi video. Người dùng duyệt "Đạt" mới ghi vào PROJECT_STATE và SERIES_PLAN.
- Mức tốn kém tham khảo: giọng Sonic khoảng 1.400 ký tự/tập; SFX riêng 40–100 credit/tập; render 12–15 phút/lần.

## Quyền và an toàn
- Bản thử dựng lại V03 dùng lời của tác giả nên **chỉ để so sánh nội bộ, không đăng**.
- Tập mới: kịch bản gốc; dữ kiện thật phải có nguồn; truyền thuyết nói rõ là truyền thuyết. Không bịa trích dẫn hay nhân chứng.
- Quái vật vẽ cách điệu (răng, mắt chết), không có máu hay vết thương ghê rợn.
- Không đăng công khai khi người dùng chưa yêu cầu.
- Truyền thuyết của người bản địa (Tlingit, Shoshone, Paiute, Yup'ik, Wampanoag, Lakota...): ghi rõ tên dân tộc, vẽ đúng mực, không chế giễu, không thêm chi tiết bịa về tập tục có thật. Walking Sam: không nhắc các vụ tự tử có thật, cuối video có dòng hỗ trợ 988.
