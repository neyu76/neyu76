# PROJECT_STATE — series "Tyler meets…" (kit v1.0, 21/11/2026)

## Đã xong (đã duyệt)
- HB01, HB02 (series homeboy gốc, Dre; không kèm scene trong kit).
- TM01 Jaylen — `references/videos/TM01_jaylen_v3.mp4`.
- TM02 Marcus — `references/videos/TM02_marcus_v2.mp4`.
- TMG01 Brody GTA 6 (trend) — `references/videos/TMG01_brody.mp4`.

## Đang chờ
- **TM03 Destiny "Friend with an Attitude":** kịch bản v1 ở `episodes/TM03/`. Chờ người dùng chốt, rồi làm giọng, dựng, render. Bối cảnh dự kiến: sân trước trường (khác góc với cổng trường TMG01), lab hóa, phòng máy tính, khán đài sân bóng. Câu "What the fuck is wrong with this dude?" giữ nguyên chữ ("dude" dùng được cho nữ); người dùng có thể đổi thành "this girl".
- Sau TM03: nhân vật 04 Brianna (Drama Queen), theo danh sách trong `docs/homeboy/SERIES_TYLER_MEETS.md`.

- **TM04 (TT-001) Bryce "The Habitual Liar":** kịch bản v1 đã khóa qua tiktok_script_assembler (24 câu, 178 từ, ~74 s, 37 key cảnh, QA 96/100). File duyệt: `episodes/TM04/TM04_script_lienmach.md`, `TM04_script_full.md`; gói TT: `episodes/TM04/TT/out/`; `episodes/TM04/shots.txt` đã sẵn cho bước giọng. **Chờ người dùng chốt.** Bối cảnh: sân bóng rổ ngoài trời, phòng nhạc, cửa hàng trường, hội chợ khoa học. Sau khi chốt: thêm TM04 vào `EPISODE_REGISTRY`, `USED_SETS`, `OWN_PAST_HOOKS` trong assembler và mục 6 của skill sản xuất.

## Môi trường cloud (Linux, 22/11/2026)
- Blender 5.2.4 LTS Linux tại `/opt/blender/blender-5.2.4-linux-x64/blender` (lệnh `blender`). Render Eevee chạy được trên CPU nhờ Mesa (đã thử TMG01: `CU_BRO_HYPE`, `WIDE_PATIO` đúng hình), nhưng chậm hơn nhiều so với RTX 3060. Thư mục ra dùng `$(pwd)/work/...` (không có `pwd -W`).
- Python 3.13 + numpy, opencv-python-headless, Pillow, soundfile, requests, faster-whisper; model Whisper `medium.en` đã tải. ffmpeg 6 có sẵn.
- Chưa có `.env.sonicvoice` (cần khóa SonicVoice trước bước giọng). Font Windows (Arial, Impact) không có trên Linux: script `make_tex_*.py` cần font thay thế khi tạo chữ mới.

## Nhật ký
- 21/11/2026: đóng gói kit (skill + tools + assets + 3 tập mẫu) để mang sang tài khoản Claude khác.
- 22/11/2026: cài kit vào môi trường cloud (Blender 5.2.4 Linux, Whisper, deps); render thử 2 cảnh TMG01 đạt.
- 22/11/2026: ADAPT_SKILLS bộ BASE_RAW v4.0 → `.claude/skills/tiktok-topic-studio`, `tiktok-script-all-in-one` (+ `scripts/tiktok_script_assembler.py` 4.0-tm1, đọc thẳng định dạng shots.txt, xuất thêm 05-KIT-shots.txt + 06-KIT-SCENES.csv), `tiktok-studio-doctor`; sổ giả thuyết `docs/tiktok/HYPOTHESIS_LEDGER.md`.
- 22/11/2026: người dùng CHỐT kịch bản TM04. Giọng: Tyler clone mới `uv_1628_b152bf711a96` (ID cũ uv_1883 không có trong tài khoản SonicVoice hiện tại), Bryce = Chrisva - Animated and Vivacious `wIVKcZbkr7yia2bPb1Hm` (0.12:1.12), Hargrove = Odd Todd - Nerdy, Pompous Professor `SDARFhQygpPvpLh7Ad1B` (0.2:1.08). vo.wav 73.48 s, 1091 ký tự. ASR: "Bro-bro-bro" đúng; "Fweee" kiểm riêng dòng L08 đủ 3 tiếng. Timeline 37 cảnh, 74.02 s, 5.0 cắt/10 s.
- 22/11/2026: Blender TM04: `tools/hb/hb_sets6.py` (sân bóng rổ, phòng nhạc, cửa hàng trường, hội chợ khoa học), `make_tex_tm04.py`, `tm04_scene.py`, `phone_burger_insert.py`. `--check` sạch (chỉ còn tiếp xúc cố ý: bóng trong tay, tay đặt trên quầy). Ảnh thử 37 cảnh: sửa cận quá sát (×1.32 theo khung video mẫu), phiếu bài tập ngược chữ, cô giáo quay lưng, người che máy, đèn cháy sáng, nhãn bị cắt. Render đủ ở nền: 1080×1920, **16 mẫu** (so sánh 16/32/64 không khác nhau, CPU không GPU), `work/tm04/clips`, log `work/tm04/render_log.txt`; chạy lại cùng lệnh sẽ bỏ qua cảnh đã đủ khung. Phụ đề trên Linux dùng Montserrat Black thay Arial Black.
- 22/11/2026: TT-001 chọn #14 Bryce (5-Axis CLEAR 0/5 với TM01/TM02/TMG01/TM03; loại Rodney, Kevin vì gần TM02). Viết tuần tự P01→P04, opening-audit + beat-audit sạch, QA 96/100, lock-export v1. Chưa chạy TTS/render.
- 23/11/2026: TM04 render xong (CPU, 16 mẫu, ~18 h kể cả làm lại). Sửa trong lúc render: đường chỉ bóng rổ (hộp vuông → đĩa mỏng), Bryce cầm sandwich trước miệng (S24, S25), đèn máy phát hiện nói dối phát đúng màu xanh/đỏ (Emission Color mặc định trắng). Ghép: `episodes/TM04/out/TM04_bryce.mp4` 74.02 s, 1080×1920 30 fps, 87 trang phụ đề, −16.9 LUFS, true peak −1.9 dBFS; check_cuts sạch; bảng khung `TM04_sheet.png`. **Chờ người dùng duyệt video.** Sau khi duyệt: thêm TM04 vào EPISODE_REGISTRY/USED_SETS/OWN_PAST_HOOKS và mục 6 skill sản xuất.
