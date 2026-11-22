---
name: darkatlas-tiktok-topic-studio
description: "Skill 1/3 của bộ TikTok Dark Atlas (DA1, cá nhân hoá từ BASE_RAW v4.0 cho profile darkatlas-us-states-en). Chọn đề tài cho series truyền thuyết kinh dị các bang Mỹ (video dọc 9:16 ~72 s, tiếng Anh, FYP Mỹ): bản đồ tâm lý người xem đêm khuya, săn outlier qua vidIQ (trực tiếp hoặc qua hub ThuyenMCP), Kiểm Trùng 5 Trục với chính các tập đã làm (EP02 Belsnickel, EP04 Kushtaka, EP05 Nimerigar...) và kênh tham chiếu, quét SEO/từ bóp FYP bằng tiktok_script_assembler.py twin-seo-check, kiểm nguồn dữ kiện thật + quy tắc tôn trọng truyền thuyết bản địa, rồi xuất TT_TOPIC_PACKET_V1 + START_COMMAND sang darkatlas-tiktok-script-all-in-one. Dùng khi người dùng nói chọn đề tài/topic TikTok, TT-00x, tập tiếp theo của series bang Mỹ."
---

# Dark Atlas TikTok Topic Studio (`v4.0-DA1`, 22/11/2026)

- **Bộ 3 skill khép kín:** (1) skill này → `TT_TOPIC_PACKET_V1`; (2) [darkatlas-tiktok-script-all-in-one](../darkatlas-tiktok-script-all-in-one/SKILL.md) → kịch bản 4 file + bảng cảnh khớp kit; (3) [darkatlas-tiktok-studio-doctor](../darkatlas-tiktok-studio-doctor/SKILL.md) → chẩn đoán D+3/D+7 trả `TT_DIAGNOSTIC_DELTA_V1` về đây.
- **Dây chuyền dựng thật nằm ở skill [dark-atlas-tales-production](../dark-atlas-tales-production/SKILL.md)** (khuôn 10 nhịp, jumpscare, render Python, Milo, QA 11 chỉ số). Skill này **không được đề xuất thứ kit không dựng được** (footage thật, 3D, ảnh AI, bản đồ vệ tinh, nhiều giọng).
- Trao đổi với người dùng bằng tiếng Việt; tiêu đề, hook, kịch bản, từ khoá SEO bằng tiếng Anh.

---

## 0) TIKTOK_NICHE_PROFILE (nhúng tự đủ — đồng bộ 100% với Skill 2 và 3)

| Trục | Giá trị khoá | Nhãn nguồn |
|---|---|---|
| `profile_id` / revision | `darkatlas-us-states-en` / `1` · base `tiktok-topic-studio@4.0` | OWNER_LOCKED |
| Ngách | Truyền thuyết quái vật/ma dân gian theo **từng bang Mỹ**, mỗi tập 1 bang + 1 sinh vật | OWNER_LOCKED |
| Thị trường | FYP Mỹ (`target_fyp_region = US`, `qualified_geo_focus = US`), tiếng Anh Mỹ | OWNER_LOCKED |
| Tư thế người nói | `OMNISCIENT_NARRATOR` — giọng Milo trầm, chậm, đều; không xưng "tôi", không kể trải nghiệm cá nhân | OWNER_LOCKED |
| Nhánh thời lượng | `creator_rewards` cố định theo định dạng kit: **68–78 s** (QA), kịch bản 165–180 từ → `T_fast ≥ 62 s` luôn đạt | OWNER_LOCKED + MEASURED_BASELINE |
| Tốc độ đọc | Milo speed 1.05: đo 142 / 144 / 150 từ/phút (EP02/04/05) → center 146, min 138, max 152 | MEASURED_BASELINE |
| Chính sách sự thật | Dữ kiện thật (năm, địa danh, người ghi chép) phải có nguồn trong `SOURCES.md`; phần siêu nhiên luôn mở bằng *"According to the legend" / "They say"*; không bịa trích dẫn, nhân chứng, năm | OWNER_LOCKED |
| Bản địa & nhạy cảm | Ghi rõ tên dân tộc (Tlingit, Shoshone, Paiute…), vẽ đúng mực, không chế giễu, không thêm chi tiết bịa về tập tục thật; quái vật cách điệu, **không máu**. Walking Sam: không nhắc vụ tự tử thật + thẻ 988. El Sombrerón: nói rõ gốc Guatemala/Mexico | OWNER_LOCKED |
| Giai đoạn kênh | Chưa có số liệu → mặc định `STAGE_1A_FOLLOWER_SPRINT` (giả thuyết H5) nhưng **vẫn giữ 72 s** vì định dạng do chủ kênh khoá | HYPOTHESIS_TO_TEST |
| Kênh tham chiếu (không chép) | @darkatlastales (mẫu V01–V03, bản quyền tác giả); kênh "Urban Legends for Every State" (danh sách đề tài gốc) | OBSERVED_MARKET_EVIDENCE |

### 0.1. Bản đồ Tâm lý Khán giả (chân dung lõi ≥70 %)
- **Người thật:** người Mỹ 16–34 tuổi lướt TikTok ban đêm, thích "creepy facts", truyện dân gian, true-crime nhẹ; rất hay **comment khi thấy bang của mình** ("I live in New Mexico and my abuela told me this").
- **Câu hỏi thầm kín khi dừng ngón cái:** *"Có thứ gì ở gần chỗ mình (hoặc nơi mình từng đi) mà mình nên sợ đêm nay không?"*
- **Tư thế cảm xúc duy nhất (`CUSTOM_SINGLE_POSTURE = SAFE_DREAD_WARNING`):** sợ an toàn + được trao một **quy tắc sống sót** ("don't answer her"). Không chuyển sang hài, không giảng đạo, không gore.
- **Động lực Share/Save:** gắn thẻ bạn ở bang đó; lưu để kể lại; tranh luận "phiên bản bà tôi kể khác". → Mỗi tập phải có **1 quy tắc cụ thể** + **1 neo địa danh thật** để người bản xứ nhận ra.

### 0.2. Danh mục tập đã có (dùng cho Kiểm Trùng 5 Trục — cập nhật sau mỗi tập "Đạt")
| Tập | Bang | Sinh vật | Question (câu hỏi) | Stage (sân khấu) | Ladder (bậc leo) | Payoff (cú lật) | Look (hình) |
|---|---|---|---|---|---|---|---|
| EP01 | (Nhật Bản) | Kuchisake-onna | Có trả lời câu "Am I pretty?" không | phố đêm, trường học | câu hỏi → mặt nạ → kéo | muốn giống cô ta | áo đỏ, thành phố Nhật |
| EP02 | Pennsylvania | Belsnickel | Có nhặt kẹo không | nhà trại mùa Giáng sinh | kẹo → chờ → roi | đếm tay chứ không đếm quà | lông thú, nến, tuyết |
| EP04 | Alaska | Kushtaka (Tlingit) | Có đi tìm tiếng trẻ khóc bên nước không | bờ biển đêm | khóc → giả dạng → biến thành rái cá | nó đang chờ bạn tìm | lạnh, nước, sương |
| EP05 | Wyoming | Nimerigar (Shoshone) | Có theo tiếng động nhỏ vào bóng tối không | núi đá, hang, lều | tiếng động → mũi tên → xác ướp | không chỉ có một | ấm, đất đỏ, hang |
| (bỏ) | Texas | Black-Eyed Children | Có mở cửa xe/nhà không | cửa xe | — | — | người dùng bỏ 19/11 |

**Hệ quả cấm lặp ngay:** dụ bằng **tiếng trẻ khóc / nước** (EP04), **người tí hon / mũi tên** (EP05), **Giáng sinh / trẻ con bị phạt** (EP02).

### 0.3. Sổ Giả Thuyết khởi tạo (`HYPOTHESIS_LEDGER` — gạch ngang khi bị bác bỏ, không xoá)
| Mã | Giả thuyết | Ủng hộ | Phản chứng | Điều kiện bác bỏ |
|---|---|---|---|---|
| H1 | Jumpscare mặt quái vật ở 0,8–1,7 s giữ `0–3s hold` cao hơn mở cảnh tĩnh | góp ý chủ kênh 19/11 | — | hold 3s của ≥4 tập có jumpscare không hơn ≥4 tập không có |
| H2 | Tên bang trong 2 từ đầu + caption "IN <STATE>," kéo comment người bản xứ và Search "<state> legend" | — | — | Search < 5 % nguồn traffic sau 6 tập |
| H3 | Quy tắc cụ thể dạng mệnh lệnh ("DON'T ANSWER HER.") tăng Saves | mẫu V01–V03 | — | ss_per_k tập có/không quy tắc chênh < 0,5 sau co mẫu |
| H4 | Truyền thuyết có **neo địa danh thật kiểm chứng được** (nghĩa trang, hồ, biển báo) giữ chân 15–30 s tốt hơn truyền thuyết chung chung | — | — | — |
| H5 | Kênh đang ở STAGE_1A (<10K follower) | chưa có số liệu | — | chủ kênh cung cấp số follower |
| H6 | Thẻ dọc trong-thế-giới (năm, biển báo, trang báo, cờ) ở 20–30 % số cảnh giữ 17–38 s tốt hơn cảnh minh hoạ thuần | EP02 (cờ Đức, trang báo) được duyệt | — | không khác biệt sau co mẫu ở ≥6 tập |

Mỗi tập chỉ thử **đúng 1 `exploration_element`** mới so với tập trước; mọi thứ khác giữ cố định.

---

## 1) Hai cửa FYP áp vào kênh này
- **Cửa 1 (định danh tệp + địa lý):** caption Frame-0 `IN <STATE>,` + tên sinh vật + 3–5 từ khoá Search (`<state> urban legend`, `<creature> legend`, `<state> folklore`, `scary story`). Không gửi link về Việt Nam trong 48 h đầu (xem Skill 3).
- **Cửa 2 (giữ chân + share/save):** jumpscare 0,8–1,7 s → thẻ hook đen chữ đỏ 5–9 s → thẻ tiêu đề 10–16 s → dữ kiện thật → *"But here's the terrifying part"* ở **~51–61 %** (trùng vùng đỉnh 55–65 %) → quy tắc → câu đảo ngược nối về câu mở (**Seamless Loop**).
- **Kết:** luôn Loop về Frame 0 (câu cuối lặp/lật tiền đề). Không cliffhanger "Part 2" (định dạng mỗi tập trọn vẹn); cầu nối series = **playlist "Dark Atlas: US States"** + bang kế tiếp trong mô tả.

## 2) Công cụ nghiên cứu (đọc schema trước khi gọi, ghi credit đã dùng)
| Việc | Công cụ | Ghi chú cho kênh này |
|---|---|---|
| Outlier TikTok/Reels | `vidiq_instagram_tiktok_outlier_search` (MCP vidIQ trực tiếp, hoặc `vidiq_call_tool` qua hub ThuyenMCP `python -I dark_atlas/tools/thuyenmcp.py call vidiq_call_tool '{...}'`) | `audienceQuery` về horror/folklore Mỹ; ưu tiên `durationMin: 62`; cần ≥2 outlier độc lập |
| Cầu tìm kiếm | `vidiq_keyword_research`, `vidiq_youtube_search` | Đo cầu theo tên sinh vật + "<state> legend" |
| Đo 1 video TikTok cụ thể | Apify `clockworks/tiktok-scraper` qua hub (`apify_run_actor`, `shouldDownloadVideos: false`) | Chỉ khi có URL; ghi `ss_per_k` |
| Dữ kiện thật | WebSearch + đọc trang nguồn (Wikipedia, báo địa phương, sách dân tộc học, trang tiểu bang) | Tách `Market Evidence` (view) khỏi `Fact Evidence` (nguồn) |

## 3) Quy trình 7 pha
1. **Pha 1 — Ứng viên:** lấy từ `dark_atlas/SERIES_PLAN_US_STATES.md` trước (người dùng đã duyệt danh sách), rồi mới tới bang chưa làm. Xếp 4 ô cung–cầu (Blue Ocean / Emerging / Red Ocean / Dead Zone).
2. **Pha 2 — Tâm lý + Kiểm Trùng 5 Trục:** chấm `Question · Stage · Ladder · Payoff · Look` với **bảng 0.2** và với video đối thủ gần nhất. **≥3/5 hoặc trùng `Question + Payoff` = `TWIN [BLOCKER]`** → phải đổi sân khấu/bậc leo/cú lật, không chỉ đổi từ. Chạy:
   ```bash
   python -I .claude/skills/darkatlas-tiktok-script-all-in-one/scripts/tiktok_script_assembler.py twin-seo-check \
     --candidate "<hook ứng viên>" --competitor "<hook đối thủ>" \
     --own-past "<hook EP02>" --own-past "<hook EP04>" --own-past "<hook EP05>" \
     --seo-keywords "<state> legend, <creature>" --lang space
   ```
3. **Pha 3 — Góc kể:** khuôn 10 nhịp là `outer_container` cố định; `inner_escalation_engine` chọn 1 trong: *Point of No Return* (một hành động không quay lại được), *Forensic* (dữ kiện thật → điều không giải thích được), *Escalation/Countdown* (giờ, số lần gọi), *Immersive POV "You"*, *Expectation vs Reality*.
4. **Pha 4 — Frame-0 bốn thành tố (bản Dark Atlas):** (a) chuyển động ngay 0,0 s (camera trôi + 1 chuyển động nhỏ trong cảnh); (b) âm: giọng Milo vào 0,0 s + tiếng đặc trưng của sinh vật ở cú hù 0,8–1,7 s; (c) caption `IN <STATE>, IF…` (Oswald in hoa, tâm ~67,5 % chiều cao = y≈1296, trong Safe Zone `x 90..870, y 180..1480`); (d) **vật thể hữu hình** đặt câu hỏi (cái xích đu, cái điện thoại reo, đôi giày bên ngã tư…). Cấm mở bằng cảm xúc trừu tượng hay "Back in 1800…".
5. **Pha 5 — Scorecard 100:** Tiền đề & Frame-0 (30) · Cầu outlier & SEO (20) · Vượt Twin & độ mới (15) · Độ thuần tâm lý & bậc leo không khoảng chết >3 s (15) · Khớp 68–78 s (10) · Nguồn FACT, khả năng dựng bằng kit, sạch từ bóp FYP (10). Đề tài < 75 điểm không chọn.
6. **Pha 6 — Chia phần:** 4 phần theo khuôn 10 nhịp (đếm từ): `P01` nhịp 1–4 (hook → thẻ tiêu đề, ~38–44 từ) · `P02` nhịp 5–6 (dữ kiện thật + According to the legend, ~45–55) · `P03` nhịp 7–8 (terrifying part + quy tắc, ~40–48) · `P04` nhịp 9–10 (So if you… + đảo ngược, ~30–38). Tổng 165–180.
7. **Pha 7 — Xuất `TT_TOPIC_PACKET_V1` + `START_COMMAND`** vào `dark_atlas/TT/<TT-00x>_<slug>/00-TT-TOPIC-PACKET.yaml`.

## 4) Schema `TT_TOPIC_PACKET_V1` (bản Dark Atlas — giữ nguyên tên khoá gốc, thêm khối `dark_atlas_kit`)
```yaml
schema_version: TT_TOPIC_PACKET_V1
packet_spec_revision: "4.0-DA1"
identity: {topic_id: "TT-00x", slug: "", packet_revision: 1, niche_profile_id: "darkatlas-us-states-en", profile_revision: 1,
           base_versions: "darkatlas-tiktok-topic-studio@4.0-DA1 | darkatlas-tiktok-script-all-in-one@4.0-DA1"}
selection_and_scope: {selection_status: "", decision_source: "", execution_mode: "", execution_scope: "", adaptation_route: "ORIGINAL_BUILD", readiness: "", blockers_and_limitations: []}
niche_and_psychological_avatar:
  niche_name: "US state horror legends (Dark Atlas)"
  content_archetype_and_story_engine: "DARK_ATLAS_10_BEAT + <inner engine>"
  brand_posture: OMNISCIENT_NARRATOR
  channel_stage: STAGE_1A_FOLLOWER_SPRINT   # H5, chưa đo
  target_person_and_inner_question: ""
  emotional_posture: CUSTOM_SINGLE_POSTURE  # SAFE_DREAD_WARNING
  avatar_purity_check: ""
  target_fyp_region_and_qualified_geo: "US / US"
  script_language: "en-US"
  format_track: creator_rewards
  fiction_and_fact_policy: "STRICT_NONFICTION facts + framed legend"
  identity_and_non_stereotype_lock: UNSPECIFIED
  exploration_element_tested: ""
angle_and_packaging_9x16: {core_question_and_viewer_promise: "", concrete_stage_and_opening_object: "", unique_angle_familiar_plus_new: "",
  format_stack: {aaaa_or_story_engine: "", outer_container: "DARK_ATLAS_10_BEAT", inner_escalation_engine: ""},
  visual_hook_archetype_1_to_8: "", frame_0_four_elements: {motion_at_0s: "", audio_hit_at_0s: "", frame0_safezone_text: "", spoken_hook_what_plus_why: ""},
  tiktok_search_seo_keywords: [], fyp_throttle_word_check: "PASS", spectacle_or_emotional_peak_at_55_65pct: "", ending_loop_or_part2_plan: "SEAMLESS_LOOP"}
runtime_and_part_budgets: {target_seconds_range: "68-78 (kit QA)", voice_delivery_mode: clean_voiceover, count_unit: words, rate_basis: MEASURED_SAMPLE,
  speaking_rate_center_min_max: [146, 138, 152], non_speech_budget_seconds: 0, part_budgets_csv: "42,50,46,36"}
market_twin_and_source_governance: {evidence_confidence: "", outlier_references: [], five_axis_twin_check: {closest_matches_scored: [], verdict: ""}, source_register: [], claim_ledger: []}
ordered_modular_outline: {parts: [], open_loop_payoff_map: [], voice_and_must_keep_constraints: {voice_guide_summary: "", user_must_keep: [], strictly_do_not_copy: []}}
dark_atlas_kit:                       # khối riêng của kênh — bắt buộc
  episode_dir: "dark_atlas/EPxx_<name>"
  state: ""                           # bang
  people_named: ""                    # dân tộc/cộng đồng giữ truyền thuyết (nếu có)
  state_markers_min4: []              # ≥4 dấu hiệu nhận ra bang ngay
  palette_note: ""                    # bảng màu mới, khác 2 tập trước
  variant_choices: {title_card: "", soft_transition: "", camera_language: "", color: "", face_reveal: "", hook_card_accent: "", signature_sfx: ""}
  jumpscare: {flash_color: "", entry: "", creature_sound: ""}
  custom_sfx_quote: []                # 2–3 âm × 2–3 s; tạo qua dark_atlas/tools/hub_sfx.py (ElevenLabs) — báo giá, chưa tạo
  render_template_base: "tools/render_ep05.py"
  safety_notes: []
```

## 5) START_COMMAND (dán ngay dưới packet)
```text
Dùng $darkatlas-tiktok-script-all-in-one ở AGENT_AUTONOMOUS_STEP_LOOP. Nhận TT_TOPIC_PACKET_V1 tại <đường dẫn>:
soạn 3-5 hook (>=16/20) chọn 1, init assembler (track creator_rewards, words, 146/138/152, budgets từ packet),
viết tuần tự P01..P04 mỗi phần 1 lượt + verify-part, opening-audit --p01-only, stitch-draft, beat-audit, QA 8 trục,
lock-export 4 file, rồi kit-bridge xuất script.txt + 05-TT-SHOTLIST khớp kit. Dừng trước TTS/render.
```

## 6) Luật cứng sau đăng (chi tiết ở Skill 3)
Không tự xem lặp, không gửi link về VN trong 48 h; không xoá đăng lại bản cắt sửa; đăng chéo Shorts/Reels từ **file render gốc không watermark** (`EPxx_<Tên>_DarkAtlas.mp4`). Chưa được yêu cầu thì không đăng gì.
