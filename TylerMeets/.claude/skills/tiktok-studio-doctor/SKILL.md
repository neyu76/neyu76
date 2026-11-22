---
name: tiktok-studio-doctor
description: "Skill 3/3 của kênh 'Tyler meets…' / 'My homeboy' (profile tylermeets-westbrook, bản chuyên biệt từ BASE_RAW v4.0). Đọc số liệu TikTok Studio của một tập đã đăng (ảnh chụp hoặc số người dùng gửi) ở D+3 và D+7: kiểm vệ sinh địa lý 48 h (qualified_geo_pct, Views/Unique), tách View Power và Money Power, mổ biểu đồ giữ chân theo từng beat khớp 03-TT-TIMELINE.csv (key cảnh, bối cảnh, dòng Lxx), tính shrinkage n/(n+5) qua tiktok_script_assembler.py fyp-diagnose, cập nhật HYPOTHESIS_LEDGER và xuất TT_DIAGNOSTIC_DELTA_V1 về tiktok-topic-studio và tiktok-script-all-in-one. Dùng khi người dùng gửi số liệu hoặc ảnh TikTok Studio của TM01, TM02, TMG01 hoặc tập mới."
---

# TikTok Studio Doctor — kênh "Tyler meets…" (`tylermeets-westbrook` · rev 1 · từ BASE_RAW v4.0)

- Báo cáo bằng tiếng Việt. Chỉ kết luận từ số người dùng gửi; thiếu số thì ghi `NOT_PROVIDED`, **không tự điền 0**.
- `TTA=.claude/skills/tiktok-script-all-in-one/scripts/tiktok_script_assembler.py`.
- Hồ sơ kênh đầy đủ: mục 0 của `.claude/skills/tiktok-topic-studio/SKILL.md`. Sổ giả thuyết: `docs/tiktok/HYPOTHESIS_LEDGER.md`.

## 0) Vệ sinh 48 h đầu (kênh nhắm US/UK/CA/AU, người làm ở VN)
1. Không xem lặp từ điện thoại/máy tính cùng Wi-Fi nhà; không gửi link cho bạn bè hay nhóm chat ở VN; không bật VPN nhảy quốc gia để "test".
2. Kiểm:
```bash
python $TTA fyp-diagnose --qualified-geo-pct <G> --views <V> --unique-viewers <U> --json-out work/<id>_fyp.json
```
- `qualified_geo_pct < 60 %` → lệch hạt giống địa lý (thường do lượt xem từ VN).
- `Views/Unique > 2.0` ở clip ~72 s → nghi tự xem lặp.
3. Kiểm **Search queries** dưới video: TikTok có gắn đúng `types of friends`, `my homeboy`, tên kiểu bạn/trend không? Sai thì siết lời 3 s đầu + tiêu đề ở tập sau.

## 1) Sáu bước đọc một tập
1. **View Power vs Money Power:** các tập của series đều ~70–77 s (nhánh Creator Rewards). Chỉ so tập với tập trong series; không so với clip < 60 s.
2. **Bốn cổng lô FYP:** `0–3 s hold` (cold open) · `avg watch` + `watched full %` · `ss_per_k = (shares + saves)/views × 1000` · `fol_per_k = new followers/views × 1000`.
3. **Không xóa đăng lại.** Để nguyên, sửa ở tập mới.
4. **Cờ Unoriginal/Ineligible:** nội dung tự dựng Blender → kháng nghị bằng 3 ảnh 1600×1000: (a) cửa sổ Blender/`tools/hb/<id>_scene.py`, (b) `01-TT-SCRIPT` + `04-TT-MANIFEST` có `locked_at` trước giờ xuất, (c) bảng khung hình `final_sheet.png`. Rủi ro riêng: nhạc nền `bed_main_V07.wav` tách từ video mẫu (người dùng đã chấp nhận rủi ro) có thể bị nhận diện bản quyền → ghi vào ledger nếu bị tắt tiếng/giới hạn.
5. **Mốc tuổi:** chấm ngang ở D+7 (D+3 chỉ là tín hiệu sớm).
   - `ViewPower = 0.40 P(views) + 0.15 P(full%) + 0.15 P(avg_s) + 0.15 P(ss/k) + 0.15 P(fol/k)`
   - `MoneyPower = 0.50 P(qual_views) + 0.20 P(avg_s) + 0.30 P(rpm)` (khi đã vào Creator Rewards)
6. **Một biến mới mỗi tập** (`exploration_element_tested` trong packet). Không kết luận biến nào khi một tập đổi nhiều thứ cùng lúc.

## 2) Mổ biểu đồ giữ chân theo `03-TT-TIMELINE-<slug>.csv`
Ghép điểm gãy trên đồ thị Retention với cột `est_start_sec`, `line_id`, `scene_key`, `set` (giây ước tính lệch giây thật ±1–2 s; khi có `episodes/<ID>/timeline.json` của bản dựng thì dùng giây thật của nó).

| Gãy ở đâu | Nguyên nhân thường gặp trong series | Thuốc cho tập sau |
|---|---|---|
| Rơi thẳng 0–2 s | Cold open chậm, cảnh mở tĩnh, beat 1 > 2.6 s, giọng nhân vật rề rà | Hành động to ngay khung 1, stability 0.12 / speed 1.12, phụ đề beat 1 ≤ 9 từ |
| Dốc 3–15 s | "This is <Tên>." muộn, câu tả tính cách dài, cảnh WIDE không thấy mặt | ≤ 12 s, câu ≤ 12 từ, cận mặt nhân vật |
| Trượt đều 15–45 s | Nấc leo thang lặp, bối cảnh trống, vai phụ đứng im | Nấc sau phải to hơn nấc trước; thêm chi tiết lạ và idle cho vai phụ |
| Rơi trước 60 s | Đỉnh quá sớm, P04 dài lê thê | Đỉnh ở 55–65 %, cắt bớt câu nối |
| Watched full thấp | Câu chốt dài, recap | 3 vế ngắn, cắt 0.6 s sau từ cuối |

## 3) Shrinkage, lực thống kê và Sổ Giả Thuyết
```bash
python $TTA fyp-diagnose --mean-with <a> --mean-without <b> --n-with <n1> --n-without <n2> --sigma-pts 8 --delta-pts 5
```
- `ShrunkEffect = (ȳ_có − ȳ_không) × n/(n+5)`, `n = min(n_có, n_không)`; `n < 4` → `LOW_SAMPLE_NOISE`. Với series chỉ vài tập, mọi kết luận là **xu hướng**, không phải luật.
- `docs/tiktok/HYPOTHESIS_LEDGER.md`: `Mã | Giả thuyết | Tập ủng hộ | Tập phản chứng | Độ tin cậy & điều kiện bác bỏ`. Bị bác bỏ thì **gạch ngang** `~~…~~` kèm mã tập, không xóa.

## 4) Đầu ra `TT_DIAGNOSTIC_DELTA_V1`
Lưu `episodes/<ID>/TT/<ID>_TT_DIAGNOSTIC_DELTA_V1_D7.yaml`:
```yaml
schema_version: TT_DIAGNOSTIC_DELTA_V1
account_and_window: {niche_profile_id: tylermeets-westbrook, profile_revision: 1, topic_id: "", kit_episode_id: "",
                     post_age: "D+3|D+7", followers_before: NOT_PROVIDED}
hygiene: {qualified_geo_pct: NOT_PROVIDED, views_per_unique: NOT_PROVIDED, verdict: ""}
gates: {hold_3s_pct: NOT_PROVIDED, avg_watch_s: NOT_PROVIDED, watched_full_pct: NOT_PROVIDED,
        ss_per_k: NOT_PROVIDED, fol_per_k: NOT_PROVIDED, search_share_pct: NOT_PROVIDED}
power_scores: {view_power: NOT_PROVIDED, money_power: NOT_PROVIDED, peer_set: "series episodes at same age"}
retention_autopsy: [{window: "", est_sec: "", line_id: "", scene_key: "", set: "", drop_pts: "", cause: "", fix_next: ""}]
exploration_element_result: {element: "", shrunk_effect: NOT_PROVIDED, confidence: LOW_SAMPLE_NOISE}
ledger_updates: []
handoff:
  to_topic_studio: []     # vd. đổi trọng số kiểu bạn vs trend, cụm SEO mới
  to_script_all_in_one: [] # vd. siết beat 1, đổi vị trí đỉnh
```

## 5) Mẫu lệnh
```text
Dùng $tiktok-studio-doctor. Đây là ảnh TikTok Studio D+7 của <ID> và file 03-TT-TIMELINE. Kiểm vệ sinh 48 h, mổ giữ chân theo beat,
cập nhật HYPOTHESIS_LEDGER và xuất TT_DIAGNOSTIC_DELTA_V1.
```
