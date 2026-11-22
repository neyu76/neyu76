# Bộ bàn giao Dark Atlas: series truyền thuyết quái vật các bang Mỹ

Bộ này giúp một tài khoản Claude khác (Claude Code) làm tiếp series với đúng quy trình và chất lượng của 3 tập đã duyệt:

| Tập | Bang | Quái vật | Video mẫu |
|---|---|---|---|
| EP02 | Pennsylvania | Belsnickel | `video_mau/EP02_Belsnickel_DarkAtlas_v2.mp4` |
| EP04 | Alaska | Kushtaka (truyền thuyết Tlingit) | `video_mau/EP04_Kushtaka_DarkAtlas_v2.mp4` |
| EP05 | Wyoming | Nimerigar (truyền thuyết Shoshone) | `video_mau/EP05_Nimerigar_DarkAtlas_v3.mp4` |

Định dạng: video dọc 9:16, dài khoảng 72 giây. Hình minh hoạ vector 2D được vẽ hoàn toàn bằng code Python, không dùng AI tạo ảnh. Có một giọng kể tiếng Anh (Sonic Voice "Milo"), phụ đề Oswald in hoa hiện từng từ, nhạc nền chung và thư viện SFX.

---

## 1. Trong gói có gì

```
DarkAtlas_US_States_Kit/
├── 00_DOC_TRUOC.md              ← file này
├── requirements.txt             ← thư viện Python cần cài
├── skill/dark-atlas-tales-production/   ← SKILL cho Claude (quy trình, quy tắc, bảng dung sai QA, bài học)
│   ├── SKILL.md
│   ├── references/  dac_ta_phong_cach.md · quy_tac_san_xuat.md (luật + bảng biến thể) · qa_checklist.md
│   ├── templates/   script_template.md · style_template.json
│   └── scripts/     bản sao các công cụ
├── dark_atlas/                  ← THƯ MỤC DỰ ÁN (gọi là DA/), mọi lệnh chạy từ đây
│   ├── PROJECT_STATE.md         ← trạng thái, credit đã dùng
│   ├── SERIES_PLAN_US_STATES.md ← danh sách tập tiếp theo (EP06 trở đi)
│   ├── tools/                   ← engine.py, style.py, render_ep02/04/05.py, sonic_tts.py, transcribe.py,
│   │                              check_transcript.py, fit_voice.py, build_sfx.py, mix_episode.py, qa_metrics.py, qa_full.py
│   ├── fonts/                   ← Oswald Bold/Regular (giấy phép OFL)
│   ├── assets/music/            ← us_bed_master_5min.wav (nhạc nền series Mỹ), dark_bed_master_5min.wav (series các nước)
│   ├── assets/sfx/              ← thư viện SFX: horror/ (dùng chung) + ep04_kushtaka/ + ep05_nimerigar/ + README.md
│   └── EP02_belsnickel/ · EP04_kushtaka/ · EP05_nimerigar/
│         script.txt · SOURCES.md · style.json · voice_milo.mp3 · voice_milo_transcript.json · sfx_cues.json · TITLE.txt
└── video_mau/                   ← 3 video thành phẩm đã duyệt, dùng làm chuẩn so sánh
```

Không có trong gói: 3 video mẫu gốc của kênh @darkatlastales (bản quyền của tác giả kênh), khoá API và mọi thông tin đăng nhập.

---

## 2. Cài đặt trên máy mới (làm một lần)

1. **Python 3.11 trở lên** và **ffmpeg** (có `ffmpeg` và `ffprobe` trong PATH).
2. Cài thư viện Python:
   ```bash
   pip install -r requirements.txt
   ```
   Lần đầu chạy `transcribe.py` sẽ tải model whisper large-v3, khoảng 3 GB. Model chạy bằng CPU nên không cần GPU.
3. **Chép skill cho Claude Code:** chép thư mục `skill/dark-atlas-tales-production` vào `C:\Users\<tên>\.claude\skills\` (macOS/Linux: `~/.claude/skills/`). Claude sẽ tự dùng skill khi bạn nhắc "Dark Atlas" hoặc "làm tập mới".
4. **Đặt thư mục dự án:** chép `dark_atlas/` vào chỗ bạn muốn làm việc rồi mở Claude Code tại thư mục đó.
5. **Khoá giọng Sonic Voice** (bạn tự nhập, không đưa khoá cho Claude):
   ```bash
   setx SONIC_API_KEY "wp_..."
   ```
   Sau khi chạy lệnh trên, mở lại terminal hoặc app. `sonic_tts.py` chỉ đọc khoá từ biến môi trường và không bao giờ in khoá ra.
   Giọng dùng là **Milo – Calm, Soothing and Meditative**, mã `GUDYcgRAONiI1nXDcNQQ`. Nếu tài khoản Sonic mới chưa có giọng này, hãy thêm vào mục yêu thích.
6. **Kết nối Magnific** trong tài khoản Claude mới. Kết nối này chỉ dùng để tạo SFX riêng cho quái vật mới (5 credit mỗi giây) hoặc tạo nhạc. Nếu không có Magnific, có thể lấy SFX miễn phí từ Pixabay Sound Effects hoặc Sonniss GDC; xem `assets/sfx/README.md`.
7. **Font Windows dùng ở một số cảnh:** `georgiab.ttf` (tờ báo EP02), `segoesc.ttf` (sổ tay EP04). Trên máy không phải Windows, hãy sửa đường dẫn font trong `render_epXX.py`.

**Kiểm tra cài đặt:** trong `dark_atlas/`, chạy:
```bash
python -I tools/render_ep05.py . "0.9,15,70.8" test.jpg
```
Lệnh tạo ra `EP05_nimerigar/test.jpg` gồm 3 khung: cú jumpscare, thẻ tiêu đề và cảnh lộ mặt.

---

## 3. Quy trình làm 1 tập (đúng như EP04 và EP05)

> Câu lệnh mẫu để giao cho Claude ở tài khoản mới:
> *"Đọc `00_DOC_TRUOC.md`, skill `dark-atlas-tales-production`, `dark_atlas/PROJECT_STATE.md` và `SERIES_PLAN_US_STATES.md`. Làm EP06 Water Babies hồ Pyramid (Nevada) theo đúng quy trình. Viết kịch bản và báo giá SFX trước, chờ tôi duyệt."*

### Bước 1. PLAN (kết thúc bằng việc người dùng duyệt)
- Lấy tập tiếp theo trong `SERIES_PLAN_US_STATES.md`. Tra nguồn để có 1–2 dữ kiện thật (năm, nơi chốn) và ghi vào `SOURCES.md`.
- Kịch bản 165–180 từ theo khuôn 10 nhịp, xem `skill/.../templates/script_template.md`:
  `In <BANG>, if…... don't…` → **thẻ hook đen chữ đỏ** → `Because…` → `They call it <TÊN>.` (thẻ tiêu đề) → dữ kiện thật → `According to the legend…` → `But here's the terrifying part.` → quy tắc → `So if you're ever… tonight, don't…` → câu đảo ngược và lộ mặt.
- Tạo `style.json` với bảng màu riêng của tập và ít nhất 4 dấu hiệu nhận ra bang đó ngay.
- Chọn **biến thể** cho tập trong bảng `references/quy_tac_san_xuat.md`: thẻ tiêu đề, chuyển cảnh, camera, màu, cách lộ mặt, điểm nhấn thẻ hook, SFX đặc trưng. Không dùng lại lựa chọn của 2 tập gần nhất.
- **Báo giá SFX riêng**: 2–3 âm thanh, mỗi âm thanh 2–3 giây, tức khoảng 40 credit.
- **Dừng lại gửi kịch bản cho người dùng duyệt. Chưa duyệt thì không tạo giọng hay dựng hình.**

### Bước 2. Giọng đọc
```bash
cd EP06_<ten>
python ../tools/sonic_tts.py speak script.txt voice_milo.mp3 --voice GUDYcgRAONiI1nXDcNQQ --speed 1.05
PYTHONIOENCODING=utf-8 python -I ../tools/transcribe.py . voice_milo.mp3
python -I ../tools/check_transcript.py .
```
- `check_transcript.py` phải ra **OK**. Whisper hay nghe sai tên riêng, bỏ sót hoặc bịa thêm từ. Khi có lỗi: cắt riêng đoạn đó transcribe lại để lấy mốc thời gian thật, rồi sửa `voice_milo_transcript.json`.
- Nếu giọng dài hơn 78 giây hoặc nhanh hơn 152 từ/phút thì **không tạo lại giọng** mà chạy:
  ```bash
  mv voice_milo.mp3 voice_milo_raw.mp3
  python -I ../tools/fit_voice.py voice_milo_raw.mp3 voice_milo.mp3 --keep "4.56:0.6,12.77:0.6" --cap 0.33 --tempo 0.97
  ```
  Tham số `--keep` giữ khoảng nghỉ dài ở các chỗ kịch tính: trước thẻ hook, trước thẻ tiêu đề, trước câu kết. Chạy xong thì transcribe lại và chạy lại `check_transcript.py`.

### Bước 3. SFX riêng của quái vật
- Tạo bằng Magnific `audio_sfx_generate` (ElevenLabs) theo đúng báo giá. Lưu vào `assets/sfx/ep06_<ten>/` và ghi thêm vào `assets/sfx/README.md`.
- Thư viện `assets/sfx/horror/` **đã có sẵn, không tạo lại**. Gồm: tiếng hét, tiếng thở sợ hãi, tiếng hít hơi, tim đập, thì thầm, tiếng rít jumpscare, tiếng dồn căng thẳng, boom trầm, gầm gừ, gió, tiếng chạy.

### Bước 4. Dựng hình
- Chép `tools/render_ep05.py` thành `tools/render_ep06.py`, đổi `EP = ... "EP06_<ten>"`, rồi viết lại cảnh, nhân vật, `CHUNKS` (phụ đề) và `RED` (từ tô đỏ).
- Mốc thời gian lấy bằng `T("word", n)`, trong đó `n` là lần xuất hiện thứ mấy của từ. **Đếm kỹ từ lặp** như "in", "they", "it", "for", "the". Lỗi hay gặp nhất là đếm sai ở đây.
- Soi ảnh tĩnh trước khi render: `python -I tools/render_ep06.py . "t1,t2,...,t32"` cho ra `stills.jpg`. Những lỗi cần tìm:
  - vật màu trắng nằm sau vùng phụ đề (60–75 % chiều cao);
  - mép đen do camera ra ngoài khung vẽ;
  - hoạ tiết trông như chấm bi;
  - nhân vật trông dễ thương thay vì đáng sợ;
  - sương hoặc bụi che mất nhân vật;
  - cảnh dài quá 5 giây (dùng `split()` để tách).
- Render toàn bộ mất 12–15 phút: `python -I tools/render_ep06.py .` cho ra `EP06_<ten>/ep06_noaudio.mp4`.

### Bước 5. Âm thanh và ghép
- Viết `EP06_<ten>/sfx_cues.json` theo mẫu `EP05_nimerigar/sfx_cues.json`:
  - **Cú hù mở đầu:** đúng tiếng của quái vật, chồng 3 lớp (gốc, `pitch` −4, `pitch` +5) cộng `horror/sub_boom.mp3`. **Không dùng tiếng hét người ở cú hù đầu.**
  - Thêm khoảng 10–25 cue khác: thẻ hook, thẻ tiêu đề, cảnh hành động, tiếng thở ở cảnh chân dung, lộ mặt cuối. Đặt `duck` để SFX tự hạ nhỏ khi giọng đang đọc.
```bash
python -I tools/build_sfx.py EP06_<ten> EP06_<ten>/sfx_cues.json EP06_<ten>/sfx.wav
python -I tools/mix_episode.py EP06_<ten>/voice_milo.mp3 EP06_<ten>/mix.wav <thoi_luong> --sfx EP06_<ten>/sfx.wav --sfx_gain 1.0 --bed us_bed_master_5min.wav
ffmpeg -i EP06_<ten>/ep06_noaudio.mp4 -i EP06_<ten>/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart EP06_<ten>/EP06_<Ten>_DarkAtlas.mp4
```
`<thoi_luong>` bằng mốc kết thúc của từ cuối cộng 0,75 giây. Nhạc nền mặc định ở −25 LUFS, script tự bù tổng về −16 LUFS.

### Bước 6. QA, rồi gửi người dùng
```bash
python -I tools/qa_full.py EP06_<ten>/EP06_<Ten>_DarkAtlas.mp4
```
- Phải **ĐẠT cả 11 chỉ số**: thời lượng 68–78 s, 26–34 lần cắt, cảnh trung bình 2,1–2,7 s, 138–152 từ/phút, −16 ± 0,5 LUFS, không có đoạn lặng… Xem kỹ `qa_sheet.jpg` (1 khung mỗi giây).
- Viết `TITLE.txt` gồm tiêu đề kiểu "If … in <Bang>… DON'T …", mô tả và hashtag. Gửi video cho người dùng.
- Người dùng nói **"Đạt"** thì mới ghi vào `PROJECT_STATE.md` và `SERIES_PLAN_US_STATES.md`.

---

## 4. Những yêu cầu người dùng đã chốt (bắt buộc giữ)

1. **Duyệt kịch bản trước.** Chưa chốt thì không tạo giọng hay video. Không đăng lên mạng khi chưa được yêu cầu.
2. **Jumpscare trong 0,8–1,7 giây đầu:** mặt quái vật lao thẳng vào ống kính, chiếm trọn khung, chớp màu, rung khung, ẩn phụ đề, dùng **tiếng của chính quái vật đó**. Không chỉ hé lộ mờ mờ, vì người xem sẽ lướt qua.
3. **Mỗi tập phải khác nhau** về thẻ tiêu đề, chuyển cảnh, camera, màu, cách lộ mặt, điểm nhấn thẻ hook và SFX. Chỉ giữ cố định khuôn 10 nhịp, thẻ hook đen chữ đỏ, phụ đề, giọng Milo và nhạc nền.
4. **Nhạc nhỏ:** nhạc nền đặt ở −25 LUFS. Series Mỹ dùng `us_bed_master_5min.wav`, không dùng nhạc mang không khí Nhật.
5. **SFX:** thư viện chung chỉ tạo một lần. Mỗi quái vật mới tạo thêm 2–3 âm thanh riêng, **báo giá trước**.
6. **Bối cảnh đúng bang:** ít nhất 4 dấu hiệu nhận diện. Khi lời kể nhắc đến nước khác thì gắn cờ nước đó vào cảnh, như cờ Đức trên con tàu ở EP02.
7. **Dữ kiện thật phải có nguồn.** Phần truyền thuyết mở bằng "According to the legend" hoặc "They say". Không bịa trích dẫn hay năm tháng.
8. **Truyền thuyết của người bản địa** phải ghi rõ tên dân tộc và vẽ đúng mực. Quái vật vẽ cách điệu, không có máu.
9. **Walking Sam (South Dakota):** không nhắc các vụ tự tử có thật, cuối video có dòng số đường dây hỗ trợ 988. **El Sombrerón (Texas):** nói rõ đây là truyền thuyết từ Guatemala và Mexico được kể ở biên giới Texas.

---

## 5. Chi phí tham khảo
| Hạng mục | Mức |
|---|---|
| Giọng Sonic (Milo, eleven_v4) | khoảng 1.400 ký tự mỗi tập |
| SFX riêng (Magnific, ElevenLabs SFX) | 5 credit mỗi giây, khoảng 40–100 credit mỗi tập |
| Nhạc mới (nếu cần): Google Lyria 3 Pro | 160 credit mỗi bản dài tối đa 180 giây. ElevenLabs Music tốn khoảng 1.600 credit cho 80 giây |
| Render | 12–15 phút CPU mỗi lần |

## 6. Tập tiếp theo
Xem `dark_atlas/SERIES_PLAN_US_STATES.md`. Tập kế tiếp là **EP06 Water Babies, hồ Pyramid (Nevada, truyền thuyết Paiute)**, sau đó lần lượt La Mala Hora (New Mexico), Dead Children's Playground (Alabama), Pukwudgie (Massachusetts), Ircenrraat (Alaska), Qallupilluit, Walking Sam, El Sombrerón.
