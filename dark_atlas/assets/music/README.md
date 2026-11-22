# Nhạc nền dùng chung — Dark Atlas Tales

| File | Mô tả |
|---|---|
| `dark_bed_master_5min.wav` / `.mp3` | **Nhạc nền chính dùng cho mọi tập.** Dài 5 phút, ghép từ một vòng 63 s lặp liền mạch (nối chéo 4 s, không có tiếng click). |
| `dark_bed_loop_cycle.wav` | Một vòng 63 s, dùng khi cần lặp trong phần mềm dựng. |
| `bed_master_source_ep01.mp3` | Bản gốc 82 s tạo bằng Magnific (ElevenLabs Music v2, 1.640 credit, 17/11/2026), dùng làm nguồn. |
| `bed_alt_40s.mp3` | Bản 40 s dùng cho bản thử V03 (800 credit), giữ làm phương án dự phòng. |

## Cách dùng (không tốn thêm credit)
```bash
python -I tools/mix_episode.py EPxx/voice_milo.mp3 EPxx/mix.wav <thời_lượng_giây> [--sfx EPxx/sfx.wav] [--offset 0-200]
```
- Mỗi tập tự bắt đầu ở một điểm khác nhau trong 5 phút nhạc (tính theo tên file giọng), nên các tập không nghe giống hệt nhau. Có thể chọn điểm bắt đầu bằng `--offset`.
- Mức âm lượng: nhạc nhỏ hơn giọng khoảng 8 dB, tổng −16 LUFS, đỉnh −1,5 dB (đo theo V03).
- Chỉ cần tạo nhạc mới khi muốn đổi không khí hẳn, ví dụ tập có tông khác.

## Nhạc nền series bang Mỹ (19/11/2026)
| File | Mô tả |
|---|---|
| `us_bed_master_5min.wav` / `.mp3` | **Nhạc nền chung cho mọi tập series bang Mỹ.** Kinh dị dân gian Mỹ (fiddle/banjo kéo dài, cello trầm, piano lạc điệu, harmonica xa). Dài 5 phút, đã cân âm lượng, nối chéo 5 s. |
| `bed_us_source.mp3` | Bản gốc 181 s tạo bằng Magnific (Google Lyria 3 Pro, 160 credit). Đã kiểm tra: không có giọng hát. |

Dùng: `python -I tools/mix_episode.py EPxx/voice_milo.mp3 EPxx/mix.wav <giây> --sfx EPxx/sfx.wav --sfx_gain 1.0 --bed us_bed_master_5min.wav`
- Nhạc mặc định ở −25 LUFS trước khi chuẩn hoá (theo yêu cầu "nhạc nhỏ lại"; trước đây −21). Script tự bù để tổng đạt −16 LUFS, đỉnh khoảng −1,7 dB.
- Series các nước dùng `dark_bed_master_5min.wav` (không khí châu Á).
