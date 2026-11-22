---
name: tiktok-topic-studio
description: "Skill 1/3 của kênh 'Tyler meets…' / 'My homeboy' (profile tylermeets-westbrook, bản chuyên biệt từ BASE_RAW v4.0). Chọn đề tài cho tập mới: kiểu bạn trong 20 tính cách hoặc chủ đề trend của học sinh trung học Mỹ, chạy 5-Axis Twin Check với các tập đã có (TM01 Jaylen, TM02 Marcus, TMG01 Brody GTA 6, TM03 Destiny) bằng tiktok_script_assembler.py twin-5axis + twin-seo-check, chọn 4 bối cảnh chưa dùng mà kit Blender dựng được, khóa Frame-0 (cold open + câu 'What the fuck is wrong with this dude?'), chia 4 phần P01..P04 theo 4 bối cảnh và xuất TT_TOPIC_PACKET_V1 + START_COMMAND sang tiktok-script-all-in-one. Dùng khi người dùng muốn tìm đề tài, chọn tập kế tiếp, kiểm trùng, hoặc nói 'làm TT-00x'."
---

# TikTok Topic Studio — kênh "Tyler meets…" (`tylermeets-westbrook` · rev 1 · từ BASE_RAW v4.0)

- Trao đổi với người dùng bằng **tiếng Việt**. Đề tài, hook, tiêu đề đăng và lời thoại bằng **tiếng Anh** (thị trường nước ngoài).
- Luôn đọc trước: `PROJECT_STATE.md`, `docs/homeboy/SERIES_TYLER_MEETS.md`, `docs/homeboy/CAST_BIBLE.md`, và skill sản xuất `.claude/skills/tyler-meets-homeboy-production/SKILL.md` (luật người dùng mục 1, bối cảnh đã dùng mục 6).
- Công cụ: `TTA=.claude/skills/tiktok-script-all-in-one/scripts/tiktok_script_assembler.py` (chạy từ gốc dự án, Python 3, không cần thư viện ngoài).
- Skill này chỉ chọn và đóng gói đề tài. Viết kịch bản thuộc `tiktok-script-all-in-one`; mổ số liệu sau đăng thuộc `tiktok-studio-doctor`.

---

## 0) TIKTOK_NICHE_PROFILE (tự đủ, dùng chung cho cả 3 skill)

| Trục | Giá trị kênh | Provenance |
|---|---|---|
| `profile_id` / rev | `tylermeets-westbrook` / 1 · base `v4.0` · assembler `4.0-tm1` | OWNER_LOCKED |
| Định dạng | Hoạt hình 3D low-poly đầu tròn, mặt decal, dựng bằng Blender (0 credit ảnh), 1080×1920 30 fps, tràn khung 9:16 | OWNER_LOCKED |
| Vũ trụ | Westbrook High (Mỹ). Tyler là người kể ngôi "I", người chứng kiến, có mặt mọi tập, ngoại hình cố định (tóc đen bù xù, áo vàng "I PAUSED MY GAME TO BE HERE") | OWNER_LOCKED |
| Tư thế người nói | `FICTION_CHARACTER` (Tyler kể chuyện hư cấu như trình bằng chứng trước tòa) | OWNER_LOCKED |
| Động cơ truyện | Mỗi tập gặp 1 kiểu bạn (20 tính cách) hoặc 1 trend: cold open → "What the fuck is wrong with this dude?" → "This is <Tên>." → leo thang qua 3 bối cảnh → cú lật ở bối cảnh 4 (Tyler bị liên lụy, nhân vật kia "thắng") → câu chốt 3 vế → sandwich của Tyler bị phá | OWNER_LOCKED |
| Khán giả (chân dung tâm lý) | Học sinh/sinh viên 13–24 ở Mỹ và nước nói tiếng Anh, lướt FYP giờ ra chơi hoặc tối. Câu hỏi thầm khi dừng ngón tay: *"Wait, I know a kid exactly like that."* Tư thế cảm xúc duy nhất: **`RECOGNITION` (nhận ra người quen + được cười cùng Tyler, người tỉnh táo duy nhất)**. ≥ 70 % tập phục vụ đúng chân dung này | HYPOTHESIS_TO_TEST (chưa có số liệu Studio) |
| Vùng FYP | `target_fyp_region`: US · `qualified_geo_focus`: US, UK, CA, AU | US: INFERRED từ bối cảnh; tiếng Anh: OWNER_LOCKED |
| Nhánh thời lượng | `creator_rewards`: 68–77 s (đo: TM01 76.6 s, TM02 76.3 s, TMG01 70.9 s), `T_fast ≥ 62.0 s` | MEASURED_BASELINE |
| Tốc độ đọc | Lời: tâm 171 wpm, khoảng 159–176 wpm (đo trên 3 tập). Khoảng nghỉ của kit: 0.45 s giữa các câu, 1.0 s trước câu chốt, 0.6 s đuôi (≈ 10 s/tập) | MEASURED_SAMPLE |
| Đơn vị đếm | `words` | OWNER_LOCKED |
| Chế độ lời | `dialogue_scenes`: Tyler `[NARR]` đọc gần hết; nhân vật của tập và vai phụ có giọng SonicVoice riêng; vai phụ ≤ 8 từ/câu | OWNER_LOCKED |
| Sự thật | `FICTION_CREATIVE`. Hài từ **hành vi**. Không chê ngoại hình, sắc tộc, gia đình; nhân vật nữ không bị bạo lực/tình dục hóa; `identity_lock = UNSPECIFIED`. Thương hiệu thật chỉ được nhắc tên trong lời, hình phải tự vẽ | OWNER_LOCKED |
| Hình–lời | **Trên video chỉ có phụ đề** (1–3 từ, giữa khung 60 %, từ khóa vàng). Không thẻ dữ liệu, không chữ đồ họa. "Nói gì hình hiện nấy" thực hiện **trong thế giới 3D**: cảnh cận `INS_`/`CU_` đồ vật, biển chữ dựng bằng `tex_quad`, ảnh chèn điện thoại tự vẽ | OWNER_LOCKED |
| Giai đoạn kênh | `STAGE_1A_FOLLOWER_SPRINT` (giả định; số follower chưa cung cấp) | HYPOTHESIS_TO_TEST |

**Thay cho bản nền:** "14 Thẻ Dữ liệu dọc" của BASE_RAW không áp dụng (vi phạm luật 9 "chỉ phụ đề"). Thay bằng **14 Neo Hình trong thế giới**: cận đồ vật `INS_`, biển chữ `tex_quad`, bảng trắng/bảng đen, màn hình điện thoại tự vẽ (story, selfie, livestream), đồng hồ treo tường, tờ phiếu phạt, nhãn hộp, bảng điểm, áo in câu hài, ruy băng giải thưởng, đèn báo nhấp nháy (`flash`), đạo cụ cầm tay (`bake_to`), phản ứng vai phụ, cận mặt Tyler đơ (`CU_ME_*`).

---

## 1) Hai cửa FYP áp vào series này

1. **Cửa 1, định danh tệp:** 3 giây đầu phải là *nhân vật trường học Mỹ làm đúng tính cách*, tiếng Anh, giọng to. Lời 3 s đầu và tiêu đề đăng phải chứa cụm tìm kiếm đúng ngách (`types of friends in school`, `that one friend who…`, `my homeboy`, tên trend). Không gửi link về VN trong 48 h đầu (xem `tiktok-studio-doctor`).
2. **Cửa 2, giữ chân:** cold open to + câu WTF ở 0–7 s, "This is <Tên>." ≤ 12 s, 5–6 cú cắt/10 s, đỉnh hài ở 55–65 % thời lượng (cú lật bối cảnh 3–4), câu chốt 3 vế rồi cắt ngay. Share/save đến từ cảm giác *"tag thằng bạn mày"*.

Nhánh mặc định: **`creator_rewards`** (68–77 s, 4 phần). Chỉ dùng `serial_sub60` khi người dùng chủ động muốn clip < 60 s.

---

## 2) Nguồn nghiên cứu (theo thứ tự)

| Việc | Công cụ | Ghi chú |
|---|---|---|
| Trend học sinh Mỹ đang lên | WebSearch (mode `extended` cho tin mới), Know Your Meme, bài tổng hợp slang có ngày | Ghi ngày của nguồn; trend > 6 tháng gắn `stale_risk` |
| Outlier ngắn | `vidiq_instagram_tiktok_outlier_search` (nếu có MCP vidIQ), Apify `clockworks/tiktok-scraper` (`shouldDownloadVideos: false`) | Không có MCP thì ghi `blockers_and_limitations: no outlier tool` và hạ `evidence_confidence` |
| Kho của chính kênh | `references/episode_index.md`, `episodes/*/out/*_post.txt`, `PROJECT_STATE.md` | Nguồn của own-past cho twin check |
| Nguồn tính cách | `docs/homeboy/SERIES_TYLER_MEETS.md`, `source/Character_Scripts*.txt` | **Chỉ lấy tính cách**, không chép lời, câu đùa hay tình huống |

Tách bạch `OBSERVED_MARKET_EVIDENCE` (view, comment) với lập luận sáng tạo. Lượt xem của trend không chứng minh tập của kênh sẽ thắng.

---

## 3) Quy trình 7 pha (bản kênh)

### Pha 1 — Danh sách ứng viên (5–7)
- Lấy từ 20 tính cách (ưu tiên số chưa làm, bỏ #01, #02, #03 đang chờ duyệt) và 1–2 trend có tên rõ, kiểm được.
- Mỗi ứng viên: tên nhân vật, hành động mở đầu + tiếng miệng, câu hỏi khán giả, thang leo thang 3 nấc, cú lật, sandwich bị phá kiểu gì.

### Pha 2 — Kiểm trùng 5 trục + SEO
Chấm `Question · Stage · Ladder · Payoff · Look` với mọi tập đã có:
```bash
python $TTA twin-5axis --question "<câu hỏi khán giả>" --stage "<4 bối cảnh>" --ladder "<3 nấc>" \
  --payoff "<cú lật + câu chốt>" --look "<tóc, áo, phụ kiện>" --sets "<set1,set2,set3,set4>" --json-out work/<id>_5axis.json
python $TTA twin-seo-check --candidate "<hook>" --candidate "<tiêu đề đăng>" \
  --seo-keywords "types of friends in school,that one friend,my homeboy" --json-out work/<id>_twinseo.json
```
- `≥ 3/5` trục trùng, hoặc trùng cả `Question + Payoff`, hoặc dùng lại set trong `USED_SETS` = **TWIN_BLOCKER**: đổi bối cảnh, nấc leo thang hoặc cú lật (đổi từ đồng nghĩa là không đủ).
- Sandwich bị phá là running gag chung, **không tính là trùng Payoff**; Payoff là *cách* nó bị phá + cú lật chính.
- Kho tập trong assembler: `EPISODE_REGISTRY`, `USED_SETS`, `FREE_SETS`, `OWN_PAST_HOOKS`. **Sau mỗi tập được duyệt, thêm tập đó vào ba danh sách này.**

### Pha 3 — Góc tiếp cận
- Tối đa 2 lớp: kiểu bạn × 1 khung leo thang (*Escalation, Expectation vs Reality, Forensic/"bằng chứng", Point of No Return, Spectrum*).
- `No-Formula-Forcing`: không cảnh sát, không bạo lực thật, không sỉ nhục; người lớn chỉ phạt kiểu trường học (detention, bị loại, bị tịch thu).

### Pha 4 — Frame-0 bốn thành tố (bản kênh)
1. **Chuyển động ở 0.0 s:** nhân vật của tập đang làm hành động đặc trưng (chạy, vung tay, nhai…), không mở bằng cảnh tĩnh.
2. **Cú nhấn âm 0.0 s:** câu hét của nhân vật + tiếng miệng đúng chữ (kiểm ASR sau này).
3. **Chữ Frame-0:** chính là **phụ đề** của beat đầu L00 (≤ 9 từ, đọc được khi tắt tiếng). Không thêm chữ khác.
4. **Vật thể/tình huống hữu hình:** đồ vật gắn với tính cách nằm trong khung ngay từ đầu (điện thoại, lon nước, phiếu bài tập…).
Kiểm thêm khung vuông 1080×1080 giữa ảnh cho thumbnail hồ sơ: mặt nhân vật phải nằm trong đó.

### Pha 5 — Chấm Scorecard 100 (bản kênh)
(1) Tiền đề "ai cũng có một thằng bạn như vậy" + Frame-0 (30) · (2) Bằng chứng thị trường / SEO (20) · (3) Vượt 5-Axis + set mới (15) · (4) Độ thuần `RECOGNITION` + thang 3 nấc không khoảng chết > 3 s (15) · (5) Khớp 68–77 s và `T_fast ≥ 62 s` (10) · (6) **Dựng được bằng kit hiện có** (rig, set mới viết được trong `hb_setsN.py`, ảnh chèn PIL) + sạch từ bóp FYP (10). Chọn ứng viên điểm cao nhất; ghi điểm của các ứng viên còn lại.

### Pha 6 — Chia 4 phần theo 4 bối cảnh
| Phần | Bối cảnh | Chức năng | Ngân sách gợi ý (từ) |
|---|---|---|---|
| P01 | Set 1 | Cold open L00 → WTF L01 → "This is <Tên>." + 2–3 câu tả tính cách → nấc 1 | 45–55 |
| P02 | Set 2 | Nấc 2, vai phụ người lớn hoặc bạn học | 40–50 |
| P03 | Set 3 | Nấc 3 + sandwich bị phá (thường giờ trưa) | 40–50 |
| P04 | Set 4 | Cú lật ở 55–65 % → hệ quả → câu chốt 3 vế | 40–50 |
Tổng 175–190 từ, ~22 dòng. Dòng đánh số liên tục `L00..L2x` xuyên các phần.

### Pha 7 — Xuất `TT_TOPIC_PACKET_V1` + `START_COMMAND`
Lưu `episodes/<KIT_ID>/TT/<TOPIC_ID>_TT_TOPIC_PACKET_V1.yaml`. Schema (giữ nguyên tên trường của bản nền để `tiktok-studio-doctor` đọc được):

```yaml
schema_version: TT_TOPIC_PACKET_V1
packet_spec_revision: "4.0-tm1"
identity: {topic_id: "TT-00x", kit_episode_id: "TM0x", slug: "", packet_revision: 1,
           niche_profile_id: "tylermeets-westbrook", profile_revision: 1,
           base_versions: "tiktok-topic-studio@4.0-tm1 | tiktok-script-all-in-one@4.0-tm1"}
selection_and_scope: {selection_status: "", decision_source: "", execution_mode: "",
                      execution_scope: "", adaptation_route: "ORIGINAL_BUILD", readiness: "", blockers_and_limitations: []}
niche_and_psychological_avatar: {niche_name: "US high-school friend-type comedy (3D low-poly)", content_archetype_and_story_engine: "",
  brand_posture: "FICTION_CHARACTER", channel_stage: "STAGE_1A_FOLLOWER_SPRINT", target_person_and_inner_question: "",
  emotional_posture: "RECOGNITION_SECOND_ACT", avatar_purity_check: "", target_fyp_region_and_qualified_geo: "US; US/UK/CA/AU",
  script_language: "en-US", format_track: "creator_rewards", fiction_and_fact_policy: "FICTION_CREATIVE",
  identity_and_non_stereotype_lock: "UNSPECIFIED", exploration_element_tested: ""}
angle_and_packaging_9x16: {core_question_and_viewer_promise: "", concrete_stage_and_opening_object: "",
  unique_angle_familiar_plus_new: "", format_stack: {aaaa_or_story_engine: "", outer_container: "", inner_escalation_engine: ""},
  visual_hook_archetype_1_to_8: "", frame_0_four_elements: {motion_at_0s: "", audio_hit_at_0s: "",
  frame0_safezone_text: "<= caption of L00 beat 1>", spoken_hook_what_plus_why: ""},
  tiktok_search_seo_keywords: [], fyp_throttle_word_check: "", spectacle_or_emotional_peak_at_55_65pct: "",
  ending_loop_or_part2_plan: "", post_title_one_line: ""}
runtime_and_part_budgets: {target_seconds_range: "68-77", voice_delivery_mode: "dialogue_scenes", count_unit: "words",
  rate_basis: "MEASURED_SAMPLE", speaking_rate_center_min_max: [171, 159, 176], non_speech_budget_seconds: "kit gap model",
  part_budgets_csv: "", sets_csv: "", cast_csv: "", hero_code: ""}
market_twin_and_source_governance: {evidence_confidence: "", outlier_references: [],
  five_axis_twin_check: {closest_matches_scored: [], verdict: ""}, source_register: [], claim_ledger: []}
ordered_modular_outline: {parts: [{part_id: "P01", set: "", budget_units: 0, function_and_state_delta: "",
  concrete_action_and_in_world_visual_anchors: [], exit_bridge: ""}], open_loop_payoff_map: [],
  voice_and_must_keep_constraints: {voice_guide_summary: "", user_must_keep: [], strictly_do_not_copy: []}}
kit_build_plan: {new_sets_to_code: [], new_props: [], new_hair_or_accessories: [], inserts_2d: [], voice_search_terms: {}}
```

`START_COMMAND` (dán ngay dưới packet):
```text
Dùng $tiktok-script-all-in-one. Nhận TT_TOPIC_PACKET_V1 <đường dẫn>. Chạy AGENT_AUTONOMOUS_STEP_LOOP:
init (sets/cast/hero theo packet) -> P01 (3-5 hook, chọn 1) -> verify-part -> opening-audit --p01-only
-> P02..P04 mỗi phần một lượt -> stitch-draft -> beat-audit -> QA 8 trục P0/P1 -> lock-export.
Dừng trước TTS và render.
```

---

## 4) Kỷ luật sau đăng (tóm tắt, chi tiết ở `tiktok-studio-doctor`)
Không tự xem lặp từ máy cùng mạng; không gửi link về VN trong 48 h đầu; không xóa rồi đăng lại bản sửa; đăng chéo Shorts/Reels từ file render gốc không watermark. Mỗi tập chỉ thử **1 biến mới** (`exploration_element_tested`).

## 5) Mẫu lệnh
```text
Dùng $tiktok-topic-studio. Tìm 5 đề tài cho tập kế tiếp, chạy twin-5axis + twin-seo-check, chấm Scorecard, chọn 1 và xuất packet.
Dùng $tiktok-topic-studio. Tôi chốt nhân vật số <NN> làm TT-00x. Chia P01..P04 theo 4 bối cảnh mới và xuất packet + START_COMMAND.
```
