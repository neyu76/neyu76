# QA checklist — chạy trước khi giao bất kỳ tập nào

Đo bằng `scripts/qa_metrics.py` cho tập mới và cả 3 mẫu. Bảng số:

| Chỉ số | Mẫu V01–V03 | Khoảng cho phép |
|---|---|---|
| Thời lượng | 72,5–73,3 s | 68–78 s |
| Số lần cắt cứng | 27–31 | 26–34 |
| Cảnh trung bình | 2,27–2,62 s | 2,1–2,7 s |
| Cảnh dài nhất | 5,0–7,1 s | ≤ 7 s (thẻ tiêu đề có thể dài hơn) |
| Khung đứng yên | 13–22 % | > 0 % (không dùng nhiễu hạt động) |
| Tốc độ đọc | 140–150 từ/phút | 138–152 |
| Khoảng nghỉ > 0,35 s | 6–10 | ≤ 18 (Milo nghỉ ở cuối câu; không thêm "..." ngoài 2 chỗ quy định) |
| Âm lượng tổng | −16,1 LUFS | −16 ± 0,5 |
| Lúc nói − lúc nghỉ | 1,0–3,8 dB | 1–5 dB |
| Đoạn lặng < −45 dB | 0 | 0 |

## Kiểm bằng mắt (bảng khung 1 fps + ảnh tĩnh độ phân giải đầy đủ)
- [ ] Khuôn 10 nhịp đủ: thẻ hook đen chữ đỏ ở 5–9 s, thẻ tiêu đề có dissolve vào, "But here's the terrifying part", kết bằng lộ mặt.
- [ ] Có ≥ 4 dấu hiệu văn hoá của nước trong kịch bản; trang phục và bảng màu lấy từ `style.json` của tập.
- [ ] Mỗi cảnh có chuyển động camera và ít nhất một chuyển động nhỏ trong cảnh.
- [ ] Phụ đề không đè lên vật trắng hay đỏ; tên tiêu đề không bị cắt mép; từ khoá đỏ đúng chỗ.
- [ ] Không có lỗ đen hay vùng trong suốt sai, không chi thể bị ngược, không vật thể nổi lạc chỗ.
- [ ] Trăng có quầng, núi nhiều lớp, có vignette.
- [ ] Màn đen duy nhất là thẻ hook; video kết thúc ~0,7 s sau chữ cuối, không bị cụt.
- [ ] Dữ kiện thật khớp nguồn; truyền thuyết có "they say / according to the legend"; quái vật không có máu.

## Nhật ký lỗi
Ghi theo dạng: mốc giờ · lỗi · bằng chứng · mức độ · nguyên nhân · cách sửa · kiểm lại. Sửa tận gốc, không che lỗi bằng cắt nhanh.

## Kết quả QA của chuẩn tập EP01 v3 (17/11/2026), tất cả nằm trong khoảng cho phép
| Thời lượng | Cắt | Cảnh TB | Dài nhất | Khung đứng yên | Từ/phút | Nghỉ | LUFS | Nói − nghỉ | Lặng |
|---|---|---|---|---|---|---|---|---|---|
| 72,9 s | 32 | 2,21 s | 4,07 s | 14,5 % | 146 | 17 | −16,2 | 4,3 dB | 0 |

## Kết quả QA EP02 Belsnickel (Pennsylvania, 17/11/2026), tất cả nằm trong khoảng cho phép
| Thời lượng | Cắt | Cảnh TB | Dài nhất | Khung đứng yên | Từ/phút | Nghỉ | LUFS | Nói − nghỉ | Lặng |
|---|---|---|---|---|---|---|---|---|---|
| 75,2 s | 32 | 2,28 s | 5,3 s | 4,1 % | 142 | 16 | −16,4 | 3,9 dB | 0 |

## Kết quả QA EP04 Kushtaka (Alaska, 19/11/2026), tất cả nằm trong khoảng cho phép
| Thời lượng | Cắt | Cảnh TB | Dài nhất | Khung đứng yên | Từ/phút | Nghỉ | LUFS | Nói − nghỉ | Lặng |
|---|---|---|---|---|---|---|---|---|---|
| 73,4 s | 32 | 2,22 s | 3,9 s | 4,9 % | 144 | 15 | −16,1 | 3,9 dB | 0 |
| EP04 v2 (SFX thư viện, nhạc nền Mỹ −25 LUFS, cú chèn quái vật ở giây 1,25) | 73,4 s | 33 | 2,16 s | 3,9 s | 4,9 % | 144 | 15 | −16,0 | 4,8 dB | 0 |

## Kết quả QA EP05 Nimerigar (Wyoming, 19/11/2026), tất cả nằm trong khoảng cho phép
| Thời lượng | Cắt | Cảnh TB | Dài nhất | Khung đứng yên | Từ/phút | Nghỉ | LUFS | Nói − nghỉ | Lặng |
|---|---|---|---|---|---|---|---|---|---|
| 72,5 s | 30 | 2,34 s | 3,9 s | 9,3 % | 150 | 8 | −16,0 | 1,8 dB | 0 |
Ghi chú: giọng Milo gốc dài 79,7 s (vượt 78 s). Đã rút các khoảng nghỉ (7 chỗ kịch tính giữ 0,5–0,6 s, còn lại 0,33 s) và giãn tốc độ 0,97 (không đổi cao độ); không tạo lại giọng.
| EP05 v2 (jumpscare mở đầu) | 72,5 s | 31 | 2,27 s | 3,9 s | 9,2 % | 150 | 8 | −16,0 | — | 0 |
