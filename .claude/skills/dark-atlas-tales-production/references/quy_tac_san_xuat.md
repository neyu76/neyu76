# Quy tắc sản xuất + bài học từ góp ý của người dùng

## Kỹ thuật dựng (engine.py)
- Cảnh = nhiều sprite RGBA vẽ bằng `Painter` (vẽ ở độ phân giải ×2 rồi thu nhỏ để khử răng cưa). Camera `(cx, cy, zoom)` có keyframe và easing cubic.
- Mỗi khung chỉ warp vùng bao của từng sprite. Sprite bị thu nhỏ dưới 0,75 dùng mip một nửa để tránh nhiễu.
- **Motion blur:** số lần lấy mẫu phụ = độ dịch chuyển trên màn hình / 2,5 px (tối đa 10), màn trập 0,5 khung.
- **Dissolve:** đặt `dissolve=0.27` cho cảnh vào thẻ tiêu đề, cảnh hồi tưởng hoặc chuyển thời gian.
- **Cắt thêm (`split`):** cảnh dài hơn ~3,5 s thì tách thành 2 khung khác nhau (đẩy vào hoặc đổi khung) gắn vào một từ.
- Nhiễu hạt **tĩnh** (`grain(img, 0, …)`), không đổi theo khung.

## Bẫy kỹ thuật đã gặp
- PIL vẽ màu có alpha < 255 lên ảnh RGBA thì **ghi đè** kênh alpha, gây ra lỗ đen. Phải vẽ lên lớp riêng rồi `alpha_composite`.
- `Painter.box` phải tự sắp xếp toạ độ (lỗi x1 < x0 khi vẽ đối xứng).
- Vẽ chi từ vai/hông: trục Y của Painter hướng lên, nên điểm cuối là `y0 + cos(góc) * L`.
- Từ lặp trong transcript ("in", "they", "her", "say", "because"…): đếm đúng lần xuất hiện cho `T()`. Thêm `assert` để số token phụ đề khớp số từ.
- faster-whisper trên GPU lỗi thiếu cublas: chạy CPU int8, đọc âm thanh bằng ffmpeg.
- Tên tiêu đề dài: giới hạn bề ngang ≤ 980 px (KUCHISAKE-ONNA dùng cỡ 132).

## Bài học từ góp ý (theo thời gian)
1. "Demo phải giống nhau mới so sánh được" → khi thử độ trung thành, dựng lại **đúng nội dung mẫu** (lời, thứ tự cảnh, thời gian căn theo từng từ), chỉ dùng để so sánh nội bộ.
2. "Font sai, nhân vật sai, camera chưa mượt, cắt thô, mọi thứ phải chuyển động" → Oswald, nhân vật đo theo mẫu, camera easing + motion blur, dissolve đúng chỗ, mỗi cảnh có chuyển động.
3. "Bóng tiêu đề như cột, chân đơn giản, trăng/núi phẳng, nhạc tự tổng hợp" → bóng có tay thõng, eo, váy xoè, 2 dải tóc lưỡi liềm; chân nhìn nghiêng có mu, gót, ngón; trăng có quầng; núi nhiều lớp có sương; nhạc thật (Magnific/ElevenLabs).
4. "Trăng chưa toả sáng, chân sai, tài xế sai, góc rộng hẹp, xe sai" → **đo toạ độ trên khung hình mẫu** (khung 720 nhân 1,5) cho từng cảnh thay vì ước lượng.
5. "Vách núi trái và nhân vật bên phải quá tệ" → vách là khối tròn có 2 đường cong; người phụ nữ chính diện có tóc ôm mặt, váy xoè gấp đôi vai.
6. "Nhạc tạo mỗi tập quá tốn" → **dùng nhạc nền chung** `dark_bed_master_5min.wav` (vòng 63 s nối liền mạch), mỗi tập bắt đầu ở một điểm khác.
7. "Kịch bản nói Nhật Bản mà bối cảnh và trang phục không phải Nhật, màu lặp nhàm chán" → **mỗi tập một `style.json`** và ≥ 4 dấu hiệu văn hoá. EP01 dùng: mái kawara, biển 止まれ, chữ sơn trên đường, máy bán hàng, gương cầu lồi, đèn lồng chōchin, shoji, núi Kinka + thành Gifu, torii, gakuran, mũ vàng + cặp randoseru.
8. Đổi sang áo đỏ làm chữ đỏ chìm vào nền → phụ đề có viền tối 3 px; vai áo ở cảnh chân dung dùng tông sẫm; không để khẩu trang hay vật trắng nằm sau vùng phụ đề (~60–75 % chiều cao).
9. QA EP01 (đo số): cắt ít, cảnh dài, nhiễu hạt động, nghỉ quá nhiều, nhạc nhỏ hơn mẫu 5 dB → thêm `split`, nhiễu tĩnh, bỏ "..." thừa, tốc độ 1,05, nhạc ở −21 LUFS trước khi chuẩn hoá.
10. EP02 Belsnickel (series các bang Mỹ):
   - Whisper có thể "bịa" từ rất ngắn (ví dụ "Santa." dài 0,08 s thay cho "he"). Từ nào dài dưới 0,1 s thì cắt đoạn đó transcript lại, rồi sửa JSON trước khi dựng.
   - Mọi tập đều đặt tên giọng là `voice_milo.mp3`, nên offset nhạc nền trước đây trùng nhau. `mix_episode.py` nay băm theo **tên thư mục tập**.
   - Lông thú: tuft ít và tương phản thấp, độ dày ≤ 6. Ở cỡ nhân vật lớn, tuft nhiều trông như vệt mưa.
   - Cái bao vác vai nhìn từ chính diện thành "cái đầu thứ hai" hoặc vầng hào quang, chỉ dùng ở góc nghiêng.
   - Cảnh cận chân (ủng) phải đặt bàn chân phía trên vùng tối đáy khung (y ≤ 1800).
   - Dấu hiệu Pennsylvania Dutch đã dùng: nhà trại đá có nến cửa sổ, kho thóc đỏ có hex sign, cầu có mái che, Fraktur, bếp lò gang, cây thông có nến, tháp State House Philadelphia, tàu di dân.
11. "Đoạn nhắc đến Đức có con thuyền thì thêm cờ Đức để nhận diện" → **khi lời kể nhắc tên một nước khác (nơi xuất xứ, di cư), thêm lá cờ nước đó vào cảnh**. Cờ phải bay, có viền sáng để dải màu tối vẫn đọc được trên nền đêm, và camera trôi về phía cờ. Tên nước đó tô đỏ trong phụ đề. Lưu ý: cờ hiện đại có thể lệch niên đại (cờ đen-đỏ-vàng có từ 1848). Ưu tiên nhận diện, nhưng phải báo cho người dùng.
12. "Đừng làm tập nào cũng rập khuôn một mẫu edit giống nhau, mỗi kịch bản xử lí khác và hay hơn" (19/11/2026) → **chỉ giữ cố định phần nhận diện kênh**: khuôn 10 nhịp, thẻ hook đen chữ đỏ, kiểu phụ đề, giọng Milo, nhạc nền chung. **Mọi thứ khác phải đổi mỗi tập**, chọn trong bảng biến thể bên dưới. Không dùng lại lựa chọn của 2 tập gần nhất.

## Bảng biến thể mỗi tập (ghi lại để không lặp)
| Hạng mục | EP01 Kuchisake | EP02 Belsnickel | EP04 Kushtaka | EP05 Nimerigar | Ý tưởng cho tập sau |
|---|---|---|---|---|---|
| Thẻ tiêu đề | Trăng lớn + bóng người | Trăng lớn + bóng người | Bóng in ngược trên nước gợn sóng, chữ trồi lên | Vách đá nổ, mảnh đá bay, bụi tan lộ chữ | khói/sương tan lộ chữ; ngọn lửa; khung cửa sổ; bản đồ bang; dấu chân trên tuyết |
| Chuyển cảnh mềm | Dissolve thường | Dissolve thường | Dissolve qua làn sương | Lia nhanh theo mũi tên (whip-pan) | wipe bằng bóng đi ngang; chớp đèn; mực loang; lật trang |
| Ngôn ngữ camera | Đẩy/kéo đều | Đẩy/kéo đều | Dập dềnh như trên thuyền | Góc thấp sát đất, tiền cảnh cây ngải trượt nhanh | rung cầm tay; trượt ngang dài; góc thấp; nhìn từ trên xuống |
| Màu | Gốc | Gốc, cam nến đối lập xanh tuyết | Lạnh, xanh rêu, giảm bão hoà | Ấm, đất đỏ/nâu đất | đỏ đất sa mạc; sepia ảnh cũ; xanh lục đầm lầy; đơn sắc |
| Cách lộ mặt | Chớp sáng nhấp nháy | Chớp sáng nhấp nháy | Trồi lên từ mặt nước, mắt sáng trước | Đèn quét miệng hang đầy mắt, rồi một khuôn mặt | bước ra từ bóng tối; hiện trong gương/kính xe; tia chớp; quay đầu chậm |
| Thẻ hook | Chữ đỏ + glow | Chữ đỏ + glow | + vòng sóng âm phía sau | + mũi tên cắm phập, rung khung | + vết cào; + hơi thở mờ kính; + bóng đi qua |
| SFX đặc trưng | 3 tiếng boom | boom + roi quất | tiếng khóc than vọng + nước té + boom | bước chân nhỏ trên sỏi, tên rít/cắm, ríu rít the thé | tiếng gõ cửa; tiếng xích đu; tiếng chuông; tiếng bước chân |
13. Giọng Milo dài quá 78 s → **không tạo lại giọng**: rút các khoảng nghỉ (chỗ kịch tính giữ 0,5–0,6 s, còn lại 0,33 s) rồi giãn tốc độ bằng `atempo` 0,97–1,03 để tốc độ đọc về 140–150 từ/phút. Sau đó luôn đối chiếu transcript với kịch bản (difflib) để bắt từ whisper bỏ sót hoặc bịa ra.

## Gợi ý dấu hiệu văn hoá theo nước (ĐX, phải kiểm lại khi làm)
- Nhật: như mục 7. Philippines: nhà sàn nipa, cây dừa/chuối, jeepney, xe ba bánh, rèm capiz.
- Ấn Độ: cửa gỗ chạm, chữ Kannada/Hindi, đèn dầu diya, bàn thờ có vòng hoa cúc vạn thọ, xe tuk-tuk.
- Pakistan: mũ pakol, khăn choàng, xe jeep trên đèo, núi phủ tuyết phía Bắc.
- Mexico: nhà adobe, nhà thờ có tháp chuông, nến, cúc vạn thọ, sông (La Llorona).
- Malaysia/Indonesia: nhà sàn Mã Lai, cây chuối, cây đa, kampung, đèn dầu (Pontianak, Kuntilanak).
- Hàn Quốc: hanok mái cong, đèn đường hẻm, cửa trượt; dùng chữ Hangul khi cần.
- Mỗi nước một bảng màu nhân vật riêng, ví dụ váy trắng (Pontianak), áo đỏ (Kuchisake-onna), sari đỏ hoặc vàng nghệ.
