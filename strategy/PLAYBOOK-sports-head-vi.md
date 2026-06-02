# 🏀 PLAYBOOK TỔNG HỢP — SPORTS-HEAD DRAMA (Tiếng Việt)

> Tài liệu **một-cửa** gói gọn toàn bộ hệ thống làm video niche "nhân vật đầu là quả
> bóng thể thao" (kiểu `@film.vibe88` & `@aistory.us`): từ phân tích kênh nguồn → công
> thức viral → thiết kế hình ảnh → kịch bản → 2 skill → master prompt → dựng CapCut →
> "bú fame" theo trend. Đọc cái này trước, rồi mở các file chi tiết khi cần.

**Bản đồ tài liệu (mở khi cần đi sâu):**
| Cần gì | Mở file |
|--------|---------|
| Teardown 2 kênh nguồn (hook, visual, công thức) | `reference/sports-head-drama-breakdown.md` |
| Series mẫu 5 part (Thunder Boy) | `reference/thunder-boy-spurs-series-scripts.md` |
| Concept niche map vào engine sẵn có | `strategy/sports-head-drama-concept.md` |
| Sinh ý tưởng (10 topic, 3 luồng) | `.kiro/skills/topic-sports-drama/SKILL.md` |
| Viết kịch bản 1 part | `.kiro/skills/script-sports-drama/SKILL.md` |
| Render prompt (Asset/Image/GROK/KLING/Veo) | `production-prompts/MASTER-PROMPT-sports.md` (V16.3) |

---

## 1. NICHE LÀ GÌ & VÌ SAO VIRAL

**Sports-Head Drama** = phim hoạt hình 3D ngắn (TikTok/Reels/Shorts), nhân vật có **đầu
là quả bóng thể thao** (bóng rổ/bóng bầu dục/bóng chày…) trên thân người thật, mặc **áo
đội thật** (NBA/NFL/MLB/NHL/MLS), **logo đội nổi (embossed) trên trán như vết bớt**. Nội
dung là **drama gia đình + bản sắc fan đội bóng**: bất công → bị sỉ nhục → karma → đoàn tụ/tha thứ.

**Bộ ba "thắng" (vì sao nó nổ view):**
- **CLICK** — đầu-bóng là hình ảnh độc nhất, gần như không ai làm ở chất lượng cao → thumbnail nhận diện ngay.
- **RETENTION** — chạy đúng engine cảm xúc `bất công → chịu đựng → karma → hồi sinh` (giống "Dog Swings Alone"), đã được chứng minh giữ chân.
- **MOAT** — fan thể thao Mỹ (NBA+NFL) cực đông, cực bộ tộc. Sự kình địch giữa 2 đội **chính là xung đột có sẵn** + đội quân khán giả tranh cãi trong comment.

---

## 2. PHÂN TÍCH 2 KÊNH NGUỒN (tóm tắt)

| | FilmVibe `@film.vibe88` | aistory.us `@aistory.us` |
|--|--------------------------|---------------------------|
| Quy mô | 32.1K follow · 496.8K like | 64K follow · 778.8K like |
| View | 49K–684K+ | 779K (Part 2) · ~3.5M (Part 1) |
| Chất | AI 3D cinematic, drama gia đình thể thao | AI 3D, series mồ côi bóng-rổ |
| Hook | nổ xung đột ngay giây 0 | đứa trẻ cô đơn trong bóng tối, **không lời** |
| Hashtag | #aistory #sadstory #basketball #nfl #fyp #brainrot | #fruitdrama #aifruit #brainrot |

**2 kiểu mở đầu (cold-open) đã được chứng minh:**
1. **Nổ xung đột (FilmVibe):** vào thẳng cảnh đối đầu/phản bội — *"VANESSA WHOSE MONEY"*, *"EXPLAIN YOU BROUGHT"*.
2. **Đứa trẻ cô đơn (aistory.us):** một mình trong bóng tối, **nhạc buồn, không thoại**, 1-2 từ caption ở giây 4-6 → đồng cảm tức thì. (Im lặng đập mạnh hơn lời nói.)

**Khung hook 10 giây chung:**
`in medias res (không intro) → visual shock (to vs nhỏ / sáng vs tối) → close-up mặt nhân vật yếu thế → caption 1-2 từ gợi xung đột nhưng KHÔNG giải thích.`

---

## 3. CÔNG THỨC KỊCH BẢN

**Engine 6-beat (xương sống cả series):**
`HOPE & ALLEGIANCE → INJUSTICE → ROCK BOTTOM → THE TURN → KARMA → RESTORATION`
- Cho **kẻ ác tạm thắng** ở "rock bottom" (đuổi ra mưa / clip nhục lan truyền) = đòn bẩy retention mạnh nhất.
- Kết **luôn đoàn tụ / tha thứ** dưới ánh sáng ấm (giống cả 2 kênh nguồn) — vừa đã, vừa dễ share.

**4-ACT trong mỗi part:** `HOOK → BUILD-UP → PEAK → RESOLUTION`, mỗi act gắn 1 **cảm xúc đích**.

**Lời thoại (rất quan trọng — chất "viral"):**
- Ngắn, **thô, hiện tại, cụt, đời thực**, slang AAVE (cuh, dead ass, finna, straight trash, fold, cooked). Cho phép chửi nhẹ khi hợp vai.
- Sỉ nhục cá nhân đánh thẳng: *"That jersey straight trash"*, *"You're a Thunder loser"*, *"Girls can't play"*.
- **TUYỆT ĐỐI không stiff/văn vở.** Cảm xúc thật > chơi chữ.

**Promise object (vật giao ước):** một kỷ vật đội bóng (dây chuyền/huy chương của bố, áo gia truyền, foam finger) — gài sớm, trả ở cuối.

---

## 4. THIẾT KẾ HÌNH ẢNH & NHÂN VẬT (visual moat)

| Yếu tố | Khoá cứng |
|--------|-----------|
| **Token nhân vật** | Đầu = quả bóng (thấy đường seam/da/chỉ khâu), thân người, da-bóng 100% (không da người). **Bóng rổ = thiết kế bóng MỚI NHẤT 2026** (da composite cam, seam đen tinh, finish mờ-satin). |
| **Logo trán** | Embossed nổi, đúng màu đội, cùng chất liệu bóng. 3 trạng thái: `ORIGINAL` / `HIDDEN_RIVAL` (lộ màu đội đối thủ ở mép) / `POST_TRANSFORMATION`. |
| **Trang phục** | Áo đội thật + số & tên cầu thủ **HƯ CẤU** (REED 24) + streetwear (jeans/short) + giày (AF1/Jordan/cleats). |
| **Color-code** | Mỗi phe 1 màu đội bao trùm set → nhìn là biết "phe nào" ngay. |
| **Ánh sáng** | Chiaroscuro cho buồn · amber/đèn dầu cho hy vọng · xanh lạnh cho tàn nhẫn · gold cho đoàn tụ · xanh-đỏ nhấp nháy cho karma. |
| **Trẻ em** | Đầu to hơn (2/5), má phính; teen 1/3; người lớn 1/3 đầy đủ. |
| **Bối cảnh** | Phòng khách-đền-thờ-đội-bóng · nhà xuống cấp · garage · hành lang trường · sân vận động · sân sau tập lúc bình minh · tiệm tạp hóa. |

**Character sheet = 16:9** (1 ECU + 4 góc xoay), **cảnh & motion = 9:16**.

---

## 5. PACE & WPM (chuẩn slow-storytelling ~62 WPM)

Tính từ chính series tham khảo (chậm, nhiều khoảng lặng để diễn cảm xúc):

| Part | Từ thoại | Thời lượng | WPM |
|------|---------|-----------|-----|
| 1 | 130 | 2′ | 65 |
| 2 | 140 | 2′ | 70 |
| 3 | 200 | 3′ | ~66.7 |
| 4 | 180 | 3′ | 60 |
| 5 | 160 | 3′ | ~53.3 |
| **TB** | **810** | **13′** | **~62.3** |

**Quy tắc:** `NGÂN SÁCH THOẠI = (giây/60) × 62 từ` (chấp nhận 55-70 WPM). Mỗi clip 10s thường
chỉ có **~4-6s nói**, phần còn lại là **giữ phản ứng im lặng**. Câu thoại 4-9 từ. **≤2 người nói/cảnh** (nhiều người có mặt thì OK, nhất là hook).

---

## 6. PIPELINE TỔNG THỂ (4 bước)

```
① topic-sports-drama   → 10 SERIES BRIEF (3 luồng: 4 evergreen + 3 result-trend + 3 culture-trend), khoá cứng
② script-sports-drama  → mở 1 PART thành 4-ACT shot list ~10s @62 WPM + handoff TOPIC_DATA
③ MASTER-PROMPT-sports → 6 phase render: Asset Bank → Image → GROK → KLING → Veo Omni → bảng EN/VI
④ CapCut               → ghép 10s clip, trim, lồng tiếng/sub, nhạc, grade, xuất 1080×1920
```

### Bước ① — Skill `topic-sports-drama` (default 10, 3 luồng)
- **A — EVERGREEN (4):** drama vượt thời gian (ST-1…ST-8), đăng lúc nào cũng được.
- **B — RESULT TREND-JACK (3) — "bú fame" KẾT QUẢ:** PHASE 1 chạy **search thời gian thực** →
  **EVENT BOARD** sự kiện thể thao nóng → khoá **SOURCE EVENT + FRESHNESS WINDOW + FALLBACK**.
- **C — CULTURE TREND-JACK (3) — "bú fame" VĂN HOÁ/SLANG/SOUND ("brainrot lane"):** PHASE 1
  search **sound/slang/format TikTok đang viral** (cuh, "we got cooked", audio trend) →
  **FORMAT BOARD** → khoá **TREND FORMAT + RIDES SLANG/SOUND + FRESHNESS (rất ngắn)**.
  Có thể standalone/2-3 part, punchier — nhưng VẪN giữ drama (không phải comedy thuần).
- **PHASE 1 in luôn THỐNG KÊ LUỒNG** (số topic mỗi luồng + sport/theme/tier/freshness).
- Output: **SERIES BRIEF** khoá cứng (cast 6 vai + @Handle + token + voice + visual
  signature + audience insight + promise object + catchphrase + trope + 6-beat→part).

> **Lưu ý:** "cuh"/slang là **lớp giọng (register)** dùng cho CẢ 3 luồng; luồng C chỉ là
> luồng *cưỡi thêm* 1 sound/slang/format cụ thể đang trend.

### Bước ② — Skill `script-sports-drama` (viết 1 part)
- Input: 1 brief (hoặc logline) + PART + LENGTH + TONE.
- 7 phase → **2 lớp**: (1) shooting script theo act→shot 10s, (2) lời TTS sạch + (Phase 7) khối **TOPIC_DATA** dán thẳng vào master prompt.

### Bước ③ — `MASTER-PROMPT-sports.md` (V16.3) — 6 phase, engine **GROK + KLING + Veo**
| Phase | Ra gì |
|-------|-------|
| 1 Asset Bank | Character sheet turnaround (16:9) + plate 9:16, real-team hex, bóng 2026 |
| 2 Image Prompts | Ảnh từng cảnh 9:16, format "Strictly adhere…" + @asset + gaze + no-text |
| 3 GROK Motion | Multi-shot 4 cảnh/clip, tag `Scene N GROK` |
| 4 KLING Motion | Bản gọn của GROK, **≤2500 ký tự**, tag `Scene N KLING` |
| 5 Veo Omni w/ refs | Audio gốc, **không ảnh mồi**, **≤7 @asset**, tag `Scene N VEO` |
| 6 Bảng phân cảnh | Song ngữ EN/VI cho CapCut |

> **Render sạch chữ 100%.** Caption/subtitle/EmphasisCaption/time-skip đều thêm tay trong CapCut.

### Bước ④ — CapCut
1. Render N clip × 10s (9:16) bằng GROK/KLING (hoặc Veo nếu cần audio gốc).
2. Trim mềm đuôi (SLOW: SHOCK/LIGHT/STANDARD bỏ 3s; HEAVY/FINAL bỏ 2s).
3. Ghép hard-cut theo thứ tự cảnh.
4. Thoại: Veo có sẵn; GROK/KLING câm → lồng ElevenLabs theo VOICE CASTING LOCK.
5. Burn subtitle EN + EmphasisCaption + HookText (cảnh 1) + TimeSkipMarker.
6. Thêm nhạc SAU (identity conflict = piano; MVP/victory = anthem; surgery = dark suspense).
7. Grade theo cảm xúc, xuất 1080×1920.

---

## 7. "BÚ FAME" — QUY TRÌNH TREND-JACK CHI TIẾT

> **Có 2 loại trend để bú** (= 2 luồng riêng):
> - **B — RESULT (kết quả/tin trận):** EVENT BOARD.
> - **C — CULTURE (sound/slang/format TikTok):** FORMAT BOARD. Đây là lane #brainrot —
>   cưỡi 1 sound/slang đang viral (cuh, "we got cooked", audio trend); freshness CỰC ngắn.

1. **Search thời gian thực** lúc lên ý tưởng:
   - *Result:* Game 7 vừa xử, sweep, upset, trade bom tấn, MVP/draft, khoảnh khắc courtside viral, hoặc **trận lớn sắp diễn ra** (hype trước Game 1).
   - *Culture:* sound/audio TikTok đang lên, slang/meme đang trend, format/challenge.
2. **TREND BOARD** → chọn sự kiện + ghi **nguồn + ngày**.
3. **4 góc khai thác:**
   - (a) **Gia đình bên thắng vênh váo** → bully arc.
   - (b) **Gia đình bên thua đau** → đứa trẻ bị bắt nạt vì đội thua → karma. *(= Thunder Boy)*
   - (c) **Nhà chia phe** trước trận lớn (2 đội kình địch dưới 1 mái nhà).
   - (d) **Riff khoảnh khắc viral** (1 pha bóng nổi tiếng → drama gia đình hư cấu).
4. **FRESHNESS WINDOW:** ship trong **0-2 ngày** (như Thunder Boy bám đúng Game 7). Nguội → dùng **EVERGREEN FALLBACK** re-skin thành vượt thời gian.

**Trend nóng nhất lúc viết playbook (2/6/2026):** Spurs hạ Thunder Game 7 **111–103** ([ESPN](https://www.espn.com/nba/story/_/id/48906594/oklahoma-city-thunder-san-antonio-spurs-game-7-nba-playoffs-2026-live-updates)); **Finals Knicks vs Spurs tip-off 3/6** ([NBC Sports](https://www.nbcsports.com/nba/news/2026-nba-playoffs-bracket-schedule-scores-matchups)). *(Nội dung đã được diễn đạt lại để tuân thủ bản quyền.)*

---

## 8. SERIES MẪU CHUẨN VÀNG — "Thunder Boy" (5 part)

`Mồ côi bị ruồng → làm người hầu/bạo hành → clip nhục viral → lội ngược dòng → karma + chữa lành`.
Đây là bản dựng đầy đủ trong `reference/thunder-boy-spurs-series-scripts.md` — dùng làm
khuôn khi viết series mới. Đòn bẩy tái dùng: **trẻ em được bảo vệ** (đồng cảm) · **kình
địch đội bóng** (stakes có sẵn) · **kỷ vật** (bản sắc + payoff) · **color-code** (ai-là-ai) ·
**karma + tha thứ** (kết thỏa mãn) · **nhục tăng dần** (hành lang → clip → xe loa → graffiti).

---

## 9. THƯ VIỆN ĐỘI BÓNG (hex thật — trích nhanh)

| NBA | Hex | NFL | Hex |
|-----|-----|-----|-----|
| Lakers | Purple `#552583` / Gold `#FDB927` | Cowboys | Navy `#003594` / Silver |
| Celtics | Green `#007A33` | Eagles | Midnight Green `#004C54` |
| Thunder (OKC) | Blue `#007AC1` / Orange | Chiefs | Red `#E31837` / Yellow `#FFB81C` |
| Spurs | Black / Silver `#C4CED4` | 49ers | Red `#AA0000` / Gold `#B3995D` |
| Warriors | Blue `#1D428A` / Yellow `#FFC72C` | Steelers | Black / Yellow `#FFB612` |

> Bảng đầy đủ (NBA/NFL/MLB/NHL/MLS/NCAA) ở `production-prompts/MASTER-PROMPT-sports.md` §4.6.
> **Luôn dùng hex chính xác**, đừng để "tím"/"xanh" chung chung.

---

## 10. AN TOÀN THƯƠNG HIỆU / SẢN XUẤT CÓ TRÁCH NHIỆM

- ✅ Dùng tên đội + hex thật; logo **vẽ giống nhưng cách điệu nhẹ** (không copy pixel-perfect).
- ✅ Tên/số cầu thủ **HƯ CẤU** (REED 24). 
- ⛔ **KHÔNG khắc họa / lồng tiếng cầu thủ, HLV có thật** — chỉ gia đình fan hư cấu. (Bú fame = bám *kết quả/đội*, không bám *người thật* → tránh phỉ báng.)
- ✅ Gắn nhãn **"AI-generated"** khi đăng.
- ✅ Beat bắt nạt/bạo hành giữ **không graphic** và **kết có hậu** (karma + tha thứ).

---

## 11. CHECKLIST TRƯỚC KHI RENDER (QA nhanh)

```
□ Hook ≤2s, nhiều nhân vật trên khung (ensemble) HOẶC đứa trẻ cô đơn im lặng
□ Cấu trúc 4-ACT, mỗi act có cảm xúc đích
□ 1 hero / 1 villain rõ ràng, không mơ hồ
□ ≥1 close-up mặt đứa trẻ (mắt ướt)
□ Promise object + catchphrase (gài → trả)
□ Karmic payoff plant→detonate (trend = dùng kết quả trận thật)
□ Color-code 2 phe + logo trán embossed mọi cảnh
□ Câu thoại 4-9 từ, ≤2 người nói/cảnh, WPM 55-70
□ Real-team hex chính xác · cầu thủ hư cấu · KHÔNG người thật
□ Render SẠCH CHỮ (caption thêm ở CapCut)
□ ≤14 asset · kết cliffhanger (part giữa) / đoàn tụ (finale)
```

---

## 12. CADENCE & TĂNG TRƯỞNG (lấp đúng điểm yếu của kênh nguồn)

- 2 kênh nguồn đang ở 32K–64K → **đòn bẩy là consistency**: ra **series đều tay**, đăng cả playlist, cliffhanger mọi part.
- View không đều → **siết hook + chọn topic tốt** (dùng skill topic).
- Mới English → **bản địa hóa** (pipeline `markets/latam/` có thể fork cho fan bóng đá Nam Mỹ — bộ tộc còn dữ hơn).
- Đề xuất: chạy **song song 3 luồng** — evergreen (ổn định, an toàn) + result-trend (bùng nổ theo kết quả) + culture-trend (bám sound/slang/format).

---

## 13. QUICK-START (làm 1 video từ A→Z)

1. Gọi **`topic-sports-drama`** → nhận 10 brief (4 evergreen + 3 result-trend + 3 culture-trend). Chọn 1.
2. Dán brief vào **`script-sports-drama`**, chọn `PART 1` → nhận shooting script + lời TTS + khối **TOPIC_DATA**.
3. Dán **TOPIC_DATA** vào **`MASTER-PROMPT-sports.md`**, gõ `Continue` lần lượt Phase 1→6.
4. Lấy **Asset Bank** tạo character sheet (16:9) + plate (9:16) trên Midjourney/Flux.
5. Lấy **GROK / KLING** (hoặc **Veo Omni**) render từng cảnh 10s (9:16).
6. Ráp **CapCut** theo bảng phân cảnh EN/VI: trim → ghép → lồng tiếng/sub → nhạc → grade → xuất.
7. Đăng kèm nhãn AI; nếu là trend-jack, **đăng trong freshness window**.

---

> Cập nhật playbook khi pipeline đổi. Mọi chi tiết kỹ thuật sống trong các file ở bảng đầu trang.
