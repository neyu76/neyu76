# PROJECT_STATE — Dark Atlas Tales (cập nhật 17/11/2026)

## Đã hoàn thành
- Phân tích 3 mẫu V01–V03 có số đo (`PHAN_TICH_MAU.md`, `analysis/`). Mẫu chính: **V03**.
- Bản thử độ trung thành V03 0–32,7 s: v1 → v5, người dùng duyệt "Đạt" (`test_v03/TEST_V03_milo_v5.mp4`). Chỉ dùng nội bộ, không đăng.
- **EP01 Kuchisake-onna (Nhật Bản)**: v1 → v3. Bản v3 qua QA đo số (`EP01_kuchisake/EP01_Kuchisake-onna_DarkAtlas_v3.mp4`).
- **EP02 Belsnickel (Pennsylvania, series các bang Mỹ)**: qua QA đo số (`EP02_belsnickel/EP02_Belsnickel_DarkAtlas_v2.mp4`, v2 có cờ Đức ở cảnh tàu, người dùng duyệt "Đạt" 18/11/2026). Nguồn ở `EP02_belsnickel/SOURCES.md`.
- **EP04 Kushtaka (Alaska, Tlingit)**: qua QA đo số (`EP04_kushtaka/EP04_Kushtaka_DarkAtlas_v2.mp4`; v2 thêm cú chèn quái vật ở đầu, 18 cue SFX thư viện, nhạc nền Mỹ mới nhỏ hơn 4 dB). Người dùng duyệt "Đạt" 19/11/2026. Tập đầu tiên áp dụng quy tắc "mỗi tập khác nhau": tiêu đề phản chiếu trên nước, dissolve qua sương, camera dập dềnh, màu lạnh, mặt trồi lên từ nước.
- **EP05 Nimerigar (Wyoming, Shoshone)**: qua QA đo số (`EP05_nimerigar/EP05_Nimerigar_DarkAtlas_v3.mp4`; v2 thêm jumpscare ở giây 0,85, v3 dùng tiếng của chính Nimerigar thay tiếng hét). Người dùng duyệt "Đạt" 19/11/2026., 27 cue SFX, 3 SFX riêng (40 credit).
- EP03 Black-Eyed Children: người dùng bỏ (19/11). Kế hoạch series ở `SERIES_PLAN_US_STATES.md`.
- Thư viện SFX `assets/sfx/` (395 credit) và nhạc nền series Mỹ `assets/music/us_bed_master_5min.wav` (160 credit), tạo ngày 19/11.
- Nhạc nền dùng chung `assets/music/dark_bed_master_5min.wav`.
- Skill `dark-atlas-tales-production` v1.0 tại `C:\Users\ADMIN\.claude\skills\dark-atlas-tales-production\`.

## Thông số đã chốt
- Giọng: Sonic Voice — Milo (`GUDYcgRAONiI1nXDcNQQ`), eleven_v4, speed 1.05 → ~145 từ/phút.
- Font: Oswald Bold/Regular (`fonts/`); chữ Nhật dùng YuGothB.
- Âm thanh: nhạc −21 LUFS trước khi trộn, tổng −16 LUFS, đỉnh −1,5 dB; SFX là 3 tiếng boom.
- Nhịp: ~30 lần cắt / 72 s; dissolve 0,27 s ở thẻ tiêu đề và đoạn chuyển thời gian; nhiễu hạt tĩnh.
- Mỗi tập một `style.json` (màu nhân vật, dấu hiệu văn hoá).

## Credit đã dùng
- Magnific (nhạc): 800 + 1.640 = 2.440 / 42.810.
- Sonic: khoảng 2.500 ký tự (EP01) + khoảng 1.400 (EP02) + khoảng 1.400 (EP03, không dùng) + khoảng 1.400 (EP04).

## Tồn đọng
- Giọng Milo nghỉ nhiều hơn mẫu (17 lần so với 6–10) vì ngắt ở cuối mỗi câu; vẫn trong khoảng cho phép đã đặt.
- Kho SFX EDITORNGHIEPDU chưa kết nối (cần agent token), hiện dùng SFX tự tổng hợp.

- `EP02_black_eyed_children/` là bản dở từ lệnh bị ngắt, không dùng.
- `EP02_belsnickel_DRAFT/` là bản nháp kịch bản cũ.

## Bước tiếp theo
- Chờ người dùng giao chủ đề hoặc yêu cầu tập mới, rồi chạy skill ở chế độ PLAN → PRODUCE → QA.
