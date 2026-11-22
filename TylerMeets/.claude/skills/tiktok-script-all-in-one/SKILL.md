---
name: tiktok-script-all-in-one
description: "Skill 2/3 của kênh 'Tyler meets…' / 'My homeboy' (profile tylermeets-westbrook, bản chuyên biệt từ BASE_RAW v4.0). Nhận TT_TOPIC_PACKET_V1 rồi viết kịch bản tập mới theo kỷ luật CẤM VIẾT 1 HƠI: mỗi lượt tool chỉ viết 1 phần P0k (1 phần = 1 bối cảnh) đúng định dạng shots.txt của kit (Lxx [SPK] beat / beat | KEY / KEY) kèm file phân cảnh .scenes.tsv, chọn 3-5 hook lấy 1 (cổng 16/20), kiểm bằng tiktok_script_assembler.py (verify-part, opening-audit, beat-audit, stitch-draft, lock-export), chấm QA 8 trục P0/P1/P2 và xuất 01-TT-SCRIPT, 02-TT-VOICE, 03-TT-TIMELINE.csv, 04-TT-MANIFEST.json + 05-KIT-shots.txt + 06-KIT-SCENES.csv. Dùng khi viết hoặc sửa kịch bản một tập của series, hoặc khi nhận START_COMMAND từ tiktok-topic-studio."
---

# TikTok Script All-in-One — kênh "Tyler meets…" (`tylermeets-westbrook` · rev 1 · từ BASE_RAW v4.0)

- Báo cáo bằng **tiếng Việt**; lời thoại và tiêu đề bằng **tiếng Anh Mỹ** đời thường của học sinh.
- `TTA=.claude/skills/tiktok-script-all-in-one/scripts/tiktok_script_assembler.py` · chạy từ gốc dự án.
- Đọc trước: packet của tập, `PROJECT_STATE.md`, skill `tyler-meets-homeboy-production` (mục 1 luật người dùng, mục 2 bước A), `references/qa_checklist.md`, và 1 tập mẫu (`episodes/TMG01/shots.txt` + `TMG01_script_lienmach.md`).
- **Skill này dừng ở kịch bản khóa.** Theo `CLAUDE.md`, sau khi lock-export phải **gửi người dùng duyệt** trước khi làm giọng (SonicVoice tốn ký tự) hay dựng Blender.

---

## 0) Hồ sơ kênh (rút gọn từ TIKTOK_NICHE_PROFILE trong `tiktok-topic-studio`)

| Khóa | Giá trị | Provenance |
|---|---|---|
| Nhánh / thời lượng | `creator_rewards`, 68–77 s tổng, `T_fast ≥ 62 s` | MEASURED_BASELINE + DOCTRINE |
| Tốc độ | 171 wpm (159–176) cho lời; nghỉ 0.45 s giữa câu, 1.0 s trước câu chốt, 0.6 s đuôi | MEASURED_SAMPLE |
| Chế độ | `dialogue_scenes`; `NARR` = Tyler; mã người nói 2–5 chữ in hoa (vd. `BRY`, `TEACH`) | OWNER_LOCKED |
| Tư thế cảm xúc | `RECOGNITION`: khán giả nhận ra "thằng bạn như vậy", cười cùng Tyler | HYPOTHESIS_TO_TEST |
| Hình–lời | Chỉ phụ đề trên video. Mọi số, đồ vật, mốc giờ nói trong 0–30 s phải **hiện trong cảnh 3D** đúng beat đó (cận `INS_`, biển chữ, ảnh chèn điện thoại) | OWNER_LOCKED |
| Văn phong | Câu ngắn, nhịp gõ; Tyler deadpan, phóng đại kiểu trình bằng chứng; chửi thề chỉ ở câu WTF của Tyler (người dùng có thể mở thêm) | OWNER_LOCKED |

---

## 1) Kỷ luật CẤM VIẾT 1 HƠI — `AGENT_AUTONOMOUS_STEP_LOOP` (mặc định)

**1 lượt tool = 1 phần.** Cấm ghi nhiều phần trong một lệnh, cấm gọi song song nhiều lệnh ghi `P01..P04`, cấm viết cả bài rồi cắt ra.

Thư mục làm việc: `episodes/<KIT_ID>/TT/` (ws) · đầu ra: `episodes/<KIT_ID>/TT/out/`.

```bash
# 1) Khóa blueprint (1 phần = 1 bối cảnh)
python $TTA init --workspace <ws> --topic-id TT-00x --slug <slug> --kit-id <KIT_ID> --track creator_rewards \
  --part-budgets "50,45,45,45" --sets "set1,set2,set3,set4" --cast "BRY=Bryce,TEACH=Mr. Ortiz" --hero BRY --est-lines 22

# 2) P01: viết <ws>/PARTS/P01.txt + <ws>/PARTS/P01.scenes.tsv trong MỘT lượt, rồi:
python $TTA verify-part --workspace <ws> --topic-id TT-00x --part-id P01 --file <ws>/PARTS/P01.txt
python $TTA opening-audit --workspace <ws> --topic-id TT-00x --p01-only

# 3) P02, P03, P04: mỗi phần một lượt viết + một verify-part
# 4) Ráp, kiểm nhịp, QA, khóa
python $TTA stitch-draft --workspace <ws> --topic-id TT-00x
python $TTA beat-audit  --workspace <ws> --topic-id TT-00x
python $TTA opening-audit --workspace <ws> --topic-id TT-00x
python $TTA lock-export --workspace <ws> --topic-id TT-00x --out-dir <ws>/out
```

Chế độ chat không có tool (`CHAT_LLM_GO_MODE`): lượt 1 = blueprint + 3–5 hook + chọn 1, dừng chờ "go"; mỗi "go" viết đúng 1 phần.

**Sửa sau khi khóa:** sửa vào `PARTS/P0k.txt` (và `.scenes.tsv`), chạy lại `verify-part --revision <r+1>` (tự hủy khóa, tăng `script_version`), các phần sau phần sửa phải verify lại theo thứ tự, rồi `lock-export` lại.

---

## 2) Định dạng file phần

### `PARTS/P0k.txt` — đúng định dạng `shots.txt` của kit
```
L00 [BRY] Bro-bro-bro! I was in Miami! / Yesterday! | OPEN_BRY_RUN / CU_BRY_HYPE
L01 [NARR] What the fuck is wrong with this dude? | CU_ME_WTF
L02 [NARR] This is Bryce. / He has never told the truth. | WIDE_COURT_BRY / MS_BRY_GRIN
```
- `/` tách beat; mỗi beat **đúng 1 key cảnh**. Key: `OPEN_` (cảnh mở), `WIDE_`, `MS_`, `CU_` (cận), `INS_` (cận đồ vật), `OTS_`, `TWO_SHOT_`, `POV_` (nền ảnh chèn). Key cảnh Tyler dùng `ME` (vd. `CU_ME_WTF`).
- Số dòng `Lxx` liên tục xuyên phần. Mỗi beat nên ≥ 0.9 s (≈ 3 từ trở lên); beat ngắn hơn sẽ bị kit gộp vào cảnh trước.
- Số cần hiện bằng chữ số trên phụ đề (vd. "GTA 6") viết bằng chữ trong lời ("GTA six"), ghi chú để sửa `vo16k.cap.json` ở bước giọng.
- Không thẻ cảm xúc TTS (`[laugh]`…), không `—`, `→`, `–`, không URL, không tiêu đề phần.

### `PARTS/P0k.scenes.tsv` — phân cảnh khớp kit (TAB)
```
OPEN_BRY_RUN	outdoor_basketball_court	Bryce chạy vào khung từ trái, tay vẫy phiếu bài tập, phanh trước Tyler; 2 bạn ném rổ phía sau
```
- Cột 2 = id bối cảnh của phần đó (`insert_2d` cho ảnh chèn điện thoại PIL, `any` nếu dùng chung).
- Mô tả: ai, làm gì, camera (cỡ cảnh, hướng), vai phụ đang cử động gì, đồ vật nào phải rõ. Đây là đầu vào trực tiếp để viết hàm `KEY(n)` trong `tools/hb/<id>_scene.py`.

---

## 3) Luật mà `verify-part` chặn cơ học (bản kênh)

| Luật | Nguồn |
|---|---|
| L00 là cold open của nhân vật tập (`--hero`) | luật 2 |
| L01 đúng nguyên văn `[NARR] What the fuck is wrong with this dude?` | luật 2 |
| "This is <Tên>." ở L02/L03 | QA checklist |
| Vai phụ ≤ 8 từ/câu; chửi thề chỉ ở Tyler; quét từ bóp FYP (kill, gun, vape, blood…) | luật 13, CAST_BIBLE |
| Số beat = số key; key đúng tiền tố; mọi key có dòng trong `.scenes.tsv` | kit `plan_shots.py` |
| Không dùng set đã dùng (`USED_SETS`) | luật 4 |
| Lệch ngân sách từ ≤ ±22 % | BASE |
| Cuối bài (`lock-export`): có "sandwich", câu cuối của Tyler ≥ 3 câu ngắn, nhân vật tập ≥ 3 câu, 68–77 s, `T_fast ≥ 62 s`, lossless 01 ↔ 02 ↔ 05 | luật 10, mục 2A |

---

## 4) Kỹ nghệ 0–15 s: chọn 3–5 hook, cổng 20 điểm

Trước khi ghi P01, soạn **3–5 phương án L00 + L01–L03** và chấm 5 tiêu chí (0–4 điểm):
1. **Mute Test:** phụ đề beat 1 + hành động có đủ hiểu khi tắt tiếng?
2. **What + Why:** trong 7 s người xem biết nhân vật *làm gì* và *vì sao lạ*?
3. **Nguy cơ cho Tyler:** có cảm giác Tyler sắp bị kéo vào rắc rối?
4. **Câu hỏi mở sang giây 15–30:** "rồi nó sẽ làm gì tiếp?"
5. **Tự nhiên 0 % mùi AI:** câu như học sinh Mỹ nói thật, có tiếng miệng đúng chữ.

Chỉ chọn bản **≥ 16/20**. Diệt 4 hook killer: mở bằng thời gian/địa điểm ("Last Monday…"), thuật ngữ, rao bán, khoe. Ghi bảng chấm vào `<ws>/HOOKS_P01.md`.

**Mốc giây (opening-audit kiểm):** beat 1 ≤ 2.6 s · L00 kết thúc ≤ 4.8 s · WTF kết thúc ≤ 7.5 s · "This is <Tên>." bắt đầu ≤ 12 s · câu trong 0–15 s ≤ 12 từ.

---

## 5) Sáu mốc cấu trúc trên 4 bối cảnh

| Mốc | Giây (≈72 s) | Phần | Nội dung |
|---|---|---|---|
| 1 Frame-0 hook | 0–7 | P01 | Cold open to, cảm xúc + câu WTF |
| 2 Nhỏ & gần | 7–15 | P01 | "This is <Tên>." + 2–3 câu tả tính cách bằng hành vi, nấc 1 |
| 3 Bậc đầu | 15–30 | P01–P02 | Bối cảnh 2, vai phụ người lớn/bạn học, nấc 2 |
| 4 Ngoặt giữa | ~30–40 | P02–P03 | Tyler chủ động làm gì đó (bằng chứng, kế hoạch) |
| 5 Đỉnh 55–65 % | ~40–47 | P03–P04 | Sandwich bị phá hoặc cú lật lớn nhất; trước đó 1 nhịp lặng (beat ngắn của Tyler) |
| 6 Hệ quả + chốt | 47–end | P04 | Tyler bị phạt/thua, nhân vật thắng; câu chốt 3 vế, cắt ngay, không recap, không "follow for part 2" |

Mỗi phần đổi ≥ 1 biến trạng thái (`TRUST`, `POWER`, `INFORMATION`, `OWNERSHIP` của sandwich…). Ghi `Scene-State Delta` 1 dòng cho mỗi phần trong `<ws>/CONTINUITY.md` (đạo cụ ai đang cầm, ai biết gì).

---

## 6) QA 8 trục (`/100`) — tự sửa hết P0 và P1 trước lock-export

| # | Trục | Điểm | P0 (chặn) | P1 (phải sửa) |
|---|---|---|---|---|
| 1 | Frame-0 + hook ≥ 16/20, mở bằng hành động + đồ vật | 20 | L00 không phải nhân vật tập; thiếu câu WTF | beat 1 > 2.6 s |
| 2 | Sạch nội dung, twin check, từ bóp FYP | 20 | chê ngoại hình/sắc tộc; bạo lực với nữ; set trùng | từ watchlist; twin ≥ 3/5 |
| 3 | Hình–lời trong thế giới 3D | 10 | đồ họa/thẻ chữ ngoài phụ đề | số/đồ vật 0–30 s không có cảnh `INS_`/`CU_` tương ứng |
| 4 | 6 mốc, đỉnh 55–65 %, 0 khoảng chết > 3 s | 15 | thiếu cú lật | đỉnh lệch khỏi 50–70 % |
| 5 | Nhân quả, continuity, state delta | 10 | đạo cụ "dịch chuyển" vô lý | vai phụ đứng như tượng trong mô tả cảnh |
| 6 | Toán thời lượng | 15 | ngoài 68–77 s hoặc `T_fast < 62 s` | lệch ngân sách > 15 % |
| 7 | Giọng tự nhiên, tiếng miệng viết đúng | 5 | — | câu sách vở, tiếng miệng khó đọc liền |
| 8 | Gói 6 file + tiêu đề đăng 1 dòng | 5 | roundtrip lỗi | thiếu `_post.txt` |

Ghi kết quả vào `<ws>/QA_REPORT.md` (điểm từng trục, lỗi đã sửa, lỗi P2 để lại).

---

## 7) Gói xuất (lock-export)

| File | Nội dung |
|---|---|
| `01-TT-SCRIPT-<slug>.txt` | Bản master `Lxx TÊN: lời`, chia khối theo phần |
| `02-TT-VOICE-<slug>.txt` | Lời thuần, mỗi dòng một `Lxx`, khớp 100 % token với 01 và 05 |
| `03-TT-TIMELINE-<slug>.csv` | Mỗi beat: phần, dòng, người nói, key cảnh, set, dải FYP, giây ước tính, neo số |
| `04-TT-MANIFEST-<slug>.json` | Cast, set, ước tính giây, audit, seam, sha256, lệnh bàn giao kit (chưa chạy) |
| `05-KIT-shots.txt` | Chép thẳng sang `episodes/<KIT_ID>/shots.txt` |
| `06-KIT-SCENES-<slug>.csv` | Danh sách key theo thứ tự xuất hiện + set + mô tả cảnh |

Sau khi khóa, viết thêm cho người dùng duyệt (khuôn TMG01): `episodes/<KIT_ID>/<KIT_ID>_script_lienmach.md`, `<KIT_ID>_script_full.md` (bảng cảnh theo 4 bối cảnh, trang phục, giọng dự kiến), `episodes/<KIT_ID>/out/<KIT_ID>_post.txt` (1 dòng tiêu đề), và ghi một mục vào `PROJECT_STATE.md`. **Dừng chờ "chốt".**

## 8) Mẫu lệnh
```text
Dùng $tiktok-script-all-in-one. Nhận packet <đường dẫn>, chạy step loop P01..P04 qua tiktok_script_assembler.py,
3-5 hook chọn 1, opening-audit + beat-audit + QA P0/P1, lock-export. Dừng trước TTS/render.
```
