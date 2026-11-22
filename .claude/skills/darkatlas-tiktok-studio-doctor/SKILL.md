---
name: darkatlas-tiktok-studio-doctor
description: "Skill 3/3 của bộ TikTok Dark Atlas (DA1, cá nhân hoá từ BASE_RAW v4.0 cho profile darkatlas-us-states-en). Chẩn đoán sau đăng cho video truyền thuyết bang Mỹ ~72 s: khoá vệ sinh địa lý 48 h (US ≥60–80 %, Views/Unique ≤2.0), tách View Power / Money Power, mổ biểu đồ giữ chân D+3/D+7 theo từng beat của 03-TT-TIMELINE.csv và theo 10 nhịp Dark Atlas (jumpscare, thẻ hook, thẻ tiêu đề, terrifying part, lộ mặt), co mẫu n/(n+5) bằng tiktok_script_assembler.py fyp-diagnose, cập nhật Sổ Giả Thuyết H1–H6 và xuất TT_DIAGNOSTIC_DELTA_V1 về Skill 1 và 2. Dùng khi người dùng gửi ảnh/số liệu TikTok Studio của một tập Dark Atlas."
---

# Dark Atlas TikTok Studio Doctor (`v4.0-DA1`, 22/11/2026)

- Hồ sơ kênh, Sổ Giả Thuyết và danh mục tập: xem mục 0 của [darkatlas-tiktok-topic-studio](../darkatlas-tiktok-topic-studio/SKILL.md). Kịch bản và timeline: [darkatlas-tiktok-script-all-in-one](../darkatlas-tiktok-script-all-in-one/SKILL.md).
- Chỉ kết luận từ số liệu người dùng đưa (ảnh chụp TikTok Studio, CSV). Không suy ra số liệu không có; cột thiếu thì bỏ và chia lại trọng số, không điền 0.

## 0) Luật 48 h đầu (kênh nuôi FYP Mỹ, người vận hành ở Việt Nam)
1. **Không** xem lặp từ máy/mạng của nhóm; **không** gửi link vào nhóm chat Việt Nam hay ngoài Mỹ. Một lô view từ VN kéo lô phân phối kế tiếp lệch địa lý, làm sập `Qualified Views` và RPM.
2. Kiểm nhiễm bẩn:
   ```bash
   python -I .claude/skills/darkatlas-tiktok-script-all-in-one/scripts/tiktok_script_assembler.py fyp-diagnose \
     --qualified-geo-pct <US%> --views <V> --unique-viewers <U> --current-followers <F> --fol-per-k <R>
   ```
   US < 60 % → `WARN_GEO_DILUTED`; Views/Unique > 2,0 trên video 72 s → `CONTAMINATED_LOOP`.
3. **Cửa 1:** TikTok Studio → Viewers → Locations (US ≥ 60–80 %) và Search queries có chứa `<state> legend`, `<creature>` không. Lệch chủ đề → siết caption Frame-0 `IN <STATE>,`, câu 3 s đầu và 3–5 từ khoá Search ở tập sau.

## 1) Đọc 1 video theo 6 bước
1. **View Power vs Money Power:** mọi tập Dark Atlas cùng nhánh 72 s → so được với nhau; không so với clip <60 s.
2. **4 cổng lô:** `0–3s hold` (cú jumpscare có giữ ngón cái?) · `avg watch` & `watched full %` (mục tiêu avg ≥ 35 s) · `ss_per_k = (shares+saves)/views×1000` · `fol_per_k`.
3. **Tôn trọng nhịp lô, CẤM xoá đăng lại:** đuôi Search thường lên ở D+3 → D+14. Sửa ở tập mới.
4. **Cờ Unoriginal/Ineligible:** kit tự vẽ 100 % bằng code → kháng nghị bằng 3 ảnh `1600×1000`: (a) code `render_epXX.py` + ảnh `stills.jpg`, (b) `script.txt` + `SOURCES.md` có ngày, (c) log render/QA `qa_full.py`. Kiểm có vô tình dùng clip người khác hoặc âm thanh có bản quyền không.
5. **Chấm ngang ở D+7** (phân vị trên các tập cùng tuổi):
   `ViewPower = 0.40 P(views) + 0.15 P(full%) + 0.15 P(avg_s) + 0.15 P(ss/k) + 0.15 P(fol/k)` · `MoneyPower = 0.50 P(qual_views) + 0.20 P(avg_s) + 0.30 P(rpm)`.
6. **Đúng 1 biến mới mỗi tập** (`exploration_element` trong packet) để biết nhân quả.

## 2) Mổ giữ chân theo 10 nhịp Dark Atlas (ghép biểu đồ Retention với `03-TT-TIMELINE-<slug>.csv` và `05-TT-SHOTLIST`)
| Gãy ở | Nhịp/cảnh nghi vấn | Thuốc cho tập sau |
|---|---|---|
| 0–2 s rơi thẳng | Cảnh mở tĩnh, jumpscare trễ quá 1,7 s, caption không có tên bang | Jumpscare 0,8–1,2 s, mặt chiếm trọn khung + tiếng sinh vật; caption `IN <STATE>,` ngay 0,0 s |
| 3–9 s | Câu 1 quá dài (>20 từ), thẻ hook xuất hiện muộn hơn 9 s | Rút nhịp 1; mệnh lệnh ≤6 từ; thẻ hook ở 5–8 s |
| 10–17 s | Thẻ tiêu đề quá dài/tĩnh | Thẻ tiêu đề ≤4 s, có chuyển động riêng (biến thể mới) |
| 17–38 s trượt đều | Dữ kiện thật khô, không có thẻ năm/biển báo/trang báo | Thêm thẻ dọc đúng lúc đọc số; mỗi cảnh đổi ≥1 biến |
| Trước 60 s | "Terrifying part" quá sớm (<45 %), quy tắc mơ hồ | Đặt pivot 51–61 %; quy tắc cụ thể, hành động được |
| Cuối bài, full % thấp | Câu cuối không lặp tiền đề, lộ mặt trễ, đuôi >1 s | Câu đảo ngược nối câu mở; kết 0,7–0,8 s sau chữ cuối |

## 3) Co mẫu nhỏ & Sổ Giả Thuyết
- `ShrunkEffect = (ȳ_có − ȳ_không) × n/(n+5)`, `n = min(n_có, n_không)`; `n < 4` → `LOW_SAMPLE_NOISE`. Muốn khẳng định +5 điểm % giữ chân (σ ≈ 8) cần ~40 tập mỗi nhánh → với kênh này, coi mọi kết luận trước 20 tập là **định hướng**, không phải luật.
- Cập nhật H1–H6 (và thêm H7+). Bác bỏ thì **gạch ngang `~~...~~` + mã tập phản chứng**, không xoá.

## 4) Xuất `TT_DIAGNOSTIC_DELTA_V1`
```yaml
schema_version: TT_DIAGNOSTIC_DELTA_V1
account_and_window: {niche_profile_id: darkatlas-us-states-en, topic_id: "", diagnosed_at: "", geo_and_loop_hygiene: ""}
gate_1_seed_classification: {qualified_geo_share_pct: "", detected_search_queries_match_niche: ""}
gate_2_batch_performance: {track_evaluated: creator_rewards, hold_3s_and_watched_full_pct: "", ss_per_k_and_fol_per_k: "", qualified_views_and_rpm: ""}
retention_beat_autopsy: {steepest_drop_beats: [], dark_atlas_beat_at_drop: [], winning_spikes_or_cards: []}
hypothesis_ledger_updates: {confirmed_or_upgraded: [], falsified_strikethrough: []}
next_action_deltas: {single_exploration_element_next: "", for_topic_studio: "", for_script_studio: "", for_render_kit: ""}
```
Lưu vào `dark_atlas/TT/<TT-00x>_<slug>/07-TT-DIAGNOSTIC-D7.yaml` và cập nhật bảng 0.3 của Skill 1.
