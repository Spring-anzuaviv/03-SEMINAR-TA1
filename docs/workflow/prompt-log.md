# Nhật ký prompt

Mỗi lần chạy AI một mục, ID `P-kk` tăng dần, không sửa mục cũ (sai thì thêm mục
mới ghi đính chính). Quy trình: [README.md](README.md).

## Mẫu

```markdown
### P-kk – <việc làm ngắn gọn>

| Trường | Giá trị |
|---|---|
| Ngày / người chạy | |
| Công cụ / model | |
| Vai trò / skill / version | vd. ba / sys-spec / v1 |
| Nguồn đã đưa vào | vd. AGENTS.md, spec.md |
| File đầu ra | vd. docs/analysis/payment-management/v1/sys-us-02-v1.md |
| Kiểm chứng | lệnh + kết quả, hoặc "chưa kiểm chứng" |
| Phần nhóm sửa | mô tả + commit |

Prompt nguyên văn:

    <dán prompt>
```

## Nhật ký

### P-01 – Tái cấu trúc workspace, quy ước tên và version

| Trường | Giá trị |
|---|---|
| Ngày / người chạy | 07/11/2026 / Nguyễn Ngọc Mai Xuân |
| Công cụ / model | Claude Code (desktop) / Claude Opus 5.5 |
| Vai trò / skill / version | Thiết lập workspace (không phải ba/design/reviewer) / – / – |
| Nguồn đã đưa vào | assignment-ta-1-2.pdf, AGENTS.md, skills/* |
| File đầu ra | Cấu trúc `payment-management/v1, v2`; `spec.md`, `sources.md`; skill `naming-versioning`; cập nhật các skill, AGENTS.md, README, `scripts/verify_agent_config.py` |
| Kiểm chứng | `python scripts/verify_agent_config.py` → `RESULT: PASS (0 failed checks)`; thử thêm file tên sai (`sys-us-02-v2.md` trong v1, `sequence-01.puml`, thư mục `sequence diagram`, `@startuml` lệch tên) → bị báo FAIL đúng chỗ |
| Phần nhóm sửa | Chưa có |

Prompt nguyên văn:

    đọc file này và deadline nộp bài chỉ nộp mục 1 2 của phần YÊU CẦU BÀI TẬP, vì vậy
    mà bạn hãy giúp tôi cấu trúc source lại và các file readme, quy định cách đặt tên
    (viết trong skill nào đó, ví dụ đặt tên file sys spec thì đặt là sys-us-01-v1,
    tương tự cho sequence diagram) do nhóm tôi viết sys spec trước mới có thể suy ra
    được những cái sau như sequence diagram, kiến trúc r thiết kế dữ liệu, lưu ý những
    cái sau như kiến trúc hay thiết kế dữ liệu gì đó cũng nên có version luôn
    cần chia ra 2 version (tôi đã tạo folder version trước đó r)
    có thể chỉnh lại các skill nếu được

### P-02 – Nhập bộ US-PAY-04 v1

| Trường | Giá trị |
|---|---|
| Ngày / người chạy | 07/11/2026 / Lộc |
| Công cụ / model | Codex desktop / GPT-6 |
| Vai trò / skill / version | Nhập tài liệu có sẵn / naming-versioning / v1 |
| Nguồn đã đưa vào | Bộ US-PAY-04 Before Review của repo `03-QTKD-Seminar`, AGENTS.md, TA-SPEC §4.4, §5 PAY-05, §6 và danh mục OQ của workspace |
| File đầu ra | [System Spec](../analysis/payment-management/v1/sys-us-04-v1.md), [Open Questions](../analysis/payment-management/v1/open-questions-v1.md), [PlantUML](../design/payment-management/v1/diagrams/seq-us-04-v1.puml) và [SVG](../design/payment-management/v1/diagrams/seq-us-04-v1.svg) |
| Kiểm chứng | PlantUML 1.2025.4 `-checkonly` và `-tsvg` cho `seq-us-04-v1.puml` đều thành công. `python scripts/verify_agent_config.py` trả `RESULT: PASS (0 failed checks)`. |
| Phần AI viết / nhóm sửa | AI nhập bản hiện có, chuẩn hóa tên file, liên kết và mã OQ, kết xuất lại SVG và bổ sung kiểm tra tên cho thư mục theo US. Chưa có chỉnh sửa của nhóm trên bản nhập. |

Prompt nguyên văn

    hãy tạo 1 folder của us-pay-04 bên trong v1 và bỏ những cái của tôi cần bỏ vào và sau đó push lên nhánh github để tôi PR và merge

### P-03 – Đặc tả và sequence diagram US-PAY-03 (v1)

| Trường | Giá trị |
|---|---|
| Ngày / người chạy | 07/11/2026 / (nhóm điền) |
| Công cụ / model | Claude Code / Claude Sonnet 5.5 |
| Vai trò / skill / version | ba + design / sys-spec, sequence-diagram / v1 |
| Nguồn đã đưa vào | AGENTS.md, assignment-ta-1-2.pdf (tr.1–3), spec.md, skills/sys-spec, sequence-diagram, naming-versioning, _shared/payment-context |
| File đầu ra | docs/analysis/payment-management/v1/sys-us-03-v1.md, open-questions-v1.md; docs/design/payment-management/v1/diagrams/seq-us-03-v1.puml; docs/design/payment-management/v1/03-detailed-design-v1.md (chỉ mục danh mục sơ đồ) |
| Kiểm chứng | `python scripts/verify_agent_config.py` (xem kết quả trong phản hồi). PlantUML: chưa kiểm tra kết xuất (máy không có Java/plantuml.jar) |
| Phần AI viết / nhóm sửa | AI viết toàn bộ; nhóm chưa sửa |

Prompt nguyên văn:

    @docs/requirements/payment-management\asignment-ta-1-2.pdf  Thiết kế US-PAY-03: viết đặc tả,  sequence diagram. Nếu có điểm cần xác nhận hoặc mơ hồ thì ghi lại để tôi xác nhận

### P-04 – Ghi câu trả lời xác nhận OQ của US-PAY-03 vào v2

| Trường | Giá trị |
|---|---|
| Ngày / người chạy | 07/11/2026 / (nhóm điền) |
| Công cụ / model | Claude Code / Claude Sonnet 5.5 |
| Vai trò / skill / version | ba + design / sys-spec, sequence-diagram / v2 |
| Nguồn đã đưa vào | Các file v1 của US-PAY-03 (giữ nguyên), câu trả lời của người phụ trách trong chat |
| File đầu ra | docs/analysis/payment-management/v2/sys-us-03-v2.md, open-questions-v2.md; docs/design/payment-management/v2/diagrams/seq-us-03-v2.puml, 03-detailed-design-v2.md |
| Kiểm chứng | `python scripts/verify_agent_config.py` (kết quả trong phản hồi); PlantUML chưa kiểm tra kết xuất |
| Phần AI viết / nhóm sửa | AI viết; nhóm chưa sửa. Họ tên người xác nhận chờ nhóm điền |

Prompt nguyên văn:

    xác nhận:
    - từ ... trở lên
    - rejected rồi draft
    - người lập là người tạo draft, PAY-07 có áp dụng, một người 1 vai trò
    - duyệt theo vai trò, không duyệt thay nhau
    - có tính VAT
    - có thấy
    - có thông báo
    - có nhưng module bên kế toán là ngoài phạm vi

### P-05 – Ghi thêm xác nhận OQ US-PAY-03 vào v1 (đính chính P-04)

| Trường | Giá trị |
|---|---|
| Ngày / người chạy | 07/11/2026 / (nhóm điền) |
| Công cụ / model | Claude Code / Claude Sonnet 5.5 |
| Vai trò / skill / version | ba + design / sys-us-03, sequence-diagram / v1 |
| Nguồn đã đưa vào | File v1 của US-PAY-03, câu trả lời của người phụ trách trong chat |
| File đầu ra | docs/analysis/payment-management/v1/sys-us-03-v1.md, open-questions-v1.md; docs/design/payment-management/v1/diagrams/seq-us-03-v1.puml, 03-detailed-design-v1.md |
| Kiểm chứng | `python scripts/verify_agent_config.py` (kết quả trong phản hồi); PlantUML chưa kiểm tra kết xuất |
| Phần AI viết / nhóm sửa | AI viết; nhóm chưa sửa |
| Đính chính P-04 | P-04 đã tạo các file `*-v2` cho US-PAY-03; theo yêu cầu "tất cả viết trong v1, chưa làm v2" các file đó đã bị xóa (chưa từng commit). Toàn bộ xác nhận của P-04 và P-05 nằm trong v1. |

Prompt nguyên văn:

    Tất cả viết trong v1, chưa làm v2
    - tổng tiền lấy tại thời điểm lập
    - làm tròn theo tiền Việt
    - thuế mặc định để tôi xác nhận với khách hàng sau
    - chỉ được sửa ở trạng thái Draft
    - text có giới hạn 500 từ
    - thông báo trong hệ thống
    - khu NVKD thực hiện chỉnh sửa bảng reject

### P-06 – Ghi xác nhận lượt 3 OQ US-PAY-03 vào v1

| Trường | Giá trị |
|---|---|
| Ngày / người chạy | 07/11/2026 / (nhóm điền) |
| Công cụ / model | Claude Code / Claude Sonnet 5.5 |
| Vai trò / skill / version | ba + design / sys-us-03, sequence-diagram / v1 |
| Nguồn đã đưa vào | File v1 của US-PAY-03, câu trả lời của người phụ trách trong chat |
| File đầu ra | docs/analysis/payment-management/v1/sys-us-03-v1.md, open-questions-v1.md; docs/design/payment-management/v1/diagrams/seq-us-03-v1.puml, 03-detailed-design-v1.md |
| Kiểm chứng | `python scripts/verify_agent_config.py` (kết quả trong phản hồi); PlantUML chưa kiểm tra kết xuất |
| Phần AI viết / nhóm sửa | AI viết; nhóm chưa sửa |

Prompt nguyên văn:

    - Cần xác nhận, chỉ cần biết là thuế
    - làm tròn dòng tổng, làm tròn lên
    - có kèm lý do
    - bạn hiểu đúng

### P-07 – Ghi xác nhận lượt 4 OQ US-PAY-03 vào v1

| Trường | Giá trị |
|---|---|
| Ngày / người chạy | 07/11/2026 / (nhóm điền) |
| Công cụ / model | Claude Code / Claude Sonnet 5.5 |
| Vai trò / skill / version | ba + design / sys-us-03, sequence-diagram / v1 |
| Nguồn đã đưa vào | File v1 của US-PAY-03, câu trả lời của người phụ trách trong chat |
| File đầu ra | docs/analysis/payment-management/v1/sys-us-03-v1.md, open-questions-v1.md; docs/design/payment-management/v1/diagrams/seq-us-03-v1.puml, 03-detailed-design-v1.md |
| Kiểm chứng | `python scripts/verify_agent_config.py` (kết quả trong phản hồi); PlantUML chưa kiểm tra kết xuất |
| Phần AI viết / nhóm sửa | AI viết; nhóm chưa sửa |

Prompt nguyên văn:

    - phải
    - giá trị thuế là 1 giá trị x hoặc % trên tổng

### P-08 – Bổ sung họ tên người phụ trách và người xác nhận (US-PAY-03)

| Trường | Giá trị |
|---|---|
| Ngày / người chạy | 07/11/2026 / Đan Anh |
| Công cụ / model | Claude Code / Claude Sonnet 5.5 |
| Vai trò / skill / version | ba + design / sys-us-03, sequence-diagram / v1 |
| Nguồn đã đưa vào | Câu trả lời của người phụ trách trong chat |
| File đầu ra | docs/analysis/payment-management/v1/sys-us-03-v1.md, open-questions-v1.md; docs/design/payment-management/v1/03-detailed-design-v1.md |
| Kiểm chứng | `python scripts/verify_agent_config.py` (kết quả trong phản hồi) |
| Phần AI viết / nhóm sửa | AI cập nhật họ tên theo yêu cầu |
| Đính chính | Các mục P-03..P-07 ghi người chạy là "(nhóm điền)"; người chạy và người xác nhận OQ của các lượt đó là **Đan Anh**. Mục cũ giữ nguyên theo quy tắc nhật ký chỉ thêm. |

Prompt nguyên văn:

    - Đan Anh
    - nhớ ghi lại

### P-09 – Tổ chức lại file US-PAY-03 (analysis vs design)

| Trường | Giá trị |
|---|---|
| Ngày / người chạy | 07/11/2026 / Đan Anh |
| Công cụ / model | Claude Code / Claude Sonnet 5.5 |
| Vai trò / skill / version | ba + design / sys-us-03, sequence-diagram / v1 |
| Nguồn đã đưa vào | File v1 của US-PAY-03 |
| File đầu ra | analysis/v1: `sys-us-03-v1.md`, `open-questions-v1.md` (phân tích + câu hỏi mở). design/v1: chỉ `diagrams/seq-us-03-v1.puml`. Đã xóa `design/v1/03-detailed-design-v1.md` (chưa commit); bảng đối chiếu bước SYS và tên dùng tạm chuyển vào khối chú thích đầu file puml. |
| Kiểm chứng | `python scripts/verify_agent_config.py` (kết quả trong phản hồi) |
| Phần AI viết / nhóm sửa | AI thực hiện theo yêu cầu |

Prompt nguyên văn:

    Tổ chức lại các file: analysis sẽ gồm các phân tích và câu hỏi mở, design gồm sequence diagram

### P-10 – Xếp lại file US-PAY-04 đúng thư mục

| Trường | Giá trị |
|---|---|
| Ngày / người chạy | 07/11/2026 / Đan Anh |
| Công cụ / model | Claude Code / Claude Sonnet 5.5 |
| Vai trò / skill / version | Thiết lập workspace / naming-versioning / v1 |
| Nguồn đã đưa vào | Bộ US-PAY-04 do Lộc nhập ở P-02 |
| File đầu ra | `analysis/v1/sys-us-04-v1.md`; OQ của US-PAY-04 gộp vào `analysis/v1/open-questions-v1.md`; `design/v1/diagrams/seq-us-04-v1.puml` và `.svg`. Đã xóa thư mục `design/v1/us-pay-04/`. |
| Kiểm chứng | `python scripts/verify_agent_config.py` (kết quả trong phản hồi); nội dung US-PAY-04 giữ nguyên, chỉ sửa liên kết tương đối |
| Phần AI viết / nhóm sửa | AI di chuyển/gộp theo yêu cầu. Đính chính P-02: liên kết trong mục P-02 đã đổi sang đường dẫn mới (chỉ sửa đường dẫn, không sửa nội dung). |

Prompt nguyên văn:

    docs\design\payment-management\v1\us-pay-04 xếp các file cho đúng chổ

### P-11 – Đặc tả use case hệ thống sys-us-05-v1 (US-PAY-05)

| Trường | Giá trị |
|---|---|
| Ngày / người chạy | 07/11/2026 / BA Team |
| Công cụ / model | Gemini 3.8 Flash |
| Vai trò / skill / version | ba / sys-spec / v1 |
| Nguồn đã đưa vào | AGENTS.md, spec.md (§1, §2, §3, §4.5, §5, §6), assignment-ta-1-2.pdf (tr.1, tr.2, tr.3), payment-context.md, naming-versioning |
| File đầu ra | `docs/analysis/payment-management/v1/sys-us-05-v1.md`, `docs/analysis/payment-management/v1/open-questions-v1.md` |
| Kiểm chứng | `python scripts/verify_agent_config.py` → PASS (0 failed checks); kiểm tra khớp hai chiều OQ: PASS (OQ-US05-01, OQ-US05-02, OQ-US05-03) |
| Phần nhóm sửa | Chưa có |

Prompt nguyên văn:

    Đọc AGENTS.md, đóng vai agent ba, dùng skill sys-spec cho US-PAY-05, version v1.
    Ghi docs/analysis/payment-management/v1/sys-us-05-v1.md. Mỗi điểm chưa rõ phải có
    OQ, nguồn và lý do cần xác nhận; không tự chốt nghiệp vụ.

### P-12 – Sequence diagram seq-us-05-v1.puml (US-PAY-05)

| Trường | Giá trị |
|---|---|
| Ngày / người chạy | 07/11/2026 / Design Team |
| Công cụ / model | Gemini 3.8 Flash |
| Vai trò / skill / version | design / sequence-diagram / v1 |
| Nguồn đã đưa vào | `docs/analysis/payment-management/v1/sys-us-05-v1.md`, `open-questions-v1.md`, TA-SPEC §1, §3, §4.5, §6; TA-PDF tr.1, tr.2, tr.3; skill sequence-diagram, naming-versioning |
| File đầu ra | `docs/design/payment-management/v1/diagrams/seq-us-05-v1.puml` |
| Kiểm chứng | `python scripts/verify_agent_config.py` → PASS (0 failed checks); đối chiếu đầy đủ các bước dòng cơ bản/thay thế; chưa kiểm tra kết xuất sơ đồ (máy chưa cấu hình plantuml.jar trên PATH) |
| Phần nhóm sửa | Chưa có |

Prompt nguyên văn:

    Đọc AGENTS.md, đóng vai agent design, dùng skill sequence-diagram cho US-PAY-05,
    version v1, đầu vào sys-us-05-v1.md. Ghi vào docs/design/payment-management/v1/diagrams/.
    Giữ OQ còn mở; phần phụ thuộc ghi Blocked by OQ.

### P-13 – Đánh giá độc lập US-PAY-05 (v1)

| Trường | Giá trị |
|---|---|
| Ngày / người chạy | 07/11/2026 / Reviewer |
| Công cụ / model | Gemini 3.8 Flash |
| Vai trò / skill / version | reviewer / – / v1 |
| Nguồn đã đưa vào | `spec.md` (§1–6), `assignment-ta-1-2.pdf` (tr.1–3), `sys-us-05-v1.md`, `open-questions-v1.md`, `diagrams/seq-us-05-v1.puml` |
| File đầu ra | `docs/review/payment-management/ai-review-us-05-v1.md` |
| Kiểm chứng | `python scripts/verify_agent_config.py` → PASS (0 failed checks); đối chiếu đầy đủ bảng bao phủ yêu cầu US-PAY-05, PAY-01, PAY-05, NFR-PAY-01/02 |
| Phần nhóm sửa | Chưa có |

Prompt nguyên văn:

    Đọc AGENTS.md và đóng vai agent reviewer. đối chiếu đặc tả TA và bản thiết kế v1, chỉ làm cho riêng cho US-PAY-05, tại docs/design/payment-management/v1/ cùng docs/analysis/payment-management/v1/.  Ghi báo cáo mới
    docs/review/payment-management/ai-review-us-05-v1.md
    Không sửa thiết kế hoặc tự đóng OQ.

### P-14 – Triển khai sys-us-05-v2.md và seq-us-05-v2.puml sau user review

| Trường | Giá trị |
|---|---|
| Ngày / người chạy | 07/11/2026 / BA & Design Team |
| Công cụ / model | Gemini 3.8 Flash |
| Vai trò / skill / version | ba & design / sys-spec & sequence-diagram / v2 |
| Nguồn đã đưa vào | `user-review-us-05.md`, `sys-us-05-v1.md`, `open-questions-v1.md`, `seq-us-05-v1.puml`, `ai-review-us-05-v1.md`, TA-SPEC §1–6, TA-PDF tr.1–3 |
| File đầu ra | `docs/analysis/payment-management/v2/sys-us-05-v2.md`, `docs/analysis/payment-management/v2/open-questions-v2.md`, `docs/design/payment-management/v2/diagrams/seq-us-05-v2.puml` |
| Kiểm chứng | `python scripts/verify_agent_config.py` → PASS (0 failed checks); đối chiếu đầy đủ các quyết định đã xác nhận (OQ-US05-01: NVKD quản lý HĐ, OQ-US05-02: được lập lại kỳ đó, OQ-US05-03: lý do hủy tùy chọn, bỏ nhánh A4 cũ) |
| Phần nhóm sửa | Chưa có |

Prompt nguyên văn:

    Đọc AGENTS.md, đóng vai agent ba, dựa vào docs\review\payment-management\user-review-us-05.md, dùng skill sys-spec cho US-PAY-05, version v2. Ghi docs/analysis/payment-management/v2/sys-us-05-v2.md
    Sau đó, đóng vai agent design, dựa vào docs\review\payment-management\user-review-us-05.md,  dùng skill sequence-diagram cho US-PAY-05, version v2, đầu vào sys-us-05-v2.md. Ghi vào docs/design/payment-management/v2/diagrams/.

### P-15 – Bổ sung minh chứng lần soạn SYS-US-02 ban đầu (v1)

| Trường | Giá trị |
|---|---|
| Ngày / người chạy | 08/11/2026 / người dùng chat, chưa cung cấp tên |
| Công cụ / model | Codex / GPT-6; PowerShell, Python, apply_patch |
| Vai trò / skill / version | ba / sys-spec, naming-versioning / v1 |
| Nguồn | TA-SPEC §1–6, sources.md, OQ chung v1, sys-us-03/04/05-v1.md; PDF đính kèm và TA-PDF cục bộ chỉ kiểm tra SHA-256 |
| Đầu ra | docs/analysis/payment-management/v1/sys-us-02-v1.md |
| Kiểm chứng thực tế | Hai PDF cùng SHA-256 BC8B34CC847343151A496C2A515A7178BF90A834D5BEE909BDDCF56179BD218E. Đọc PDF thất bại vì thiếu pypdf; đã dùng TA-SPEC. Lệnh verify ban đầu lỗi mã hóa charmap; python -X utf8 scripts/verify_agent_config.py → PASS, 0 failed checks. |
| Phần AI / nhóm sửa | AI soạn toàn bộ; chưa có nhóm sửa. Mục này được ghi bổ sung khi thực hiện P-16; minh chứng ban đầu nằm cuối sys spec. Không tạo commit. |

Prompt nguyên văn:

    hãy viết phần sys-us-02 theo bài tập này cho tôi vào thư mục v1 của project

File đính kèm: C:/Users/PC/Downloads/BAITAP_TA_1-2.pdf.

### P-16 – Đối chiếu BA và tạo sequence US-PAY-02 (v1)

| Trường | Giá trị |
|---|---|
| Ngày / người chạy | 08/11/2026 / người dùng chat, chưa cung cấp tên |
| Công cụ / model | Codex / GPT-6; PowerShell; Python; PlantUML 1.2025.2; Java 1.8.0_251; Graphviz 2.44.1 được PlantUML -version nhận diện |
| Vai trò / skill / version | ba rồi design trong cùng chat / sequence-diagram, naming-versioning, payment-context / v1 |
| Nguồn đã đọc | AGENTS.md; các skill; workflow README; TA-SPEC §1–6; sources.md; sys-us-02-v1.md; open-questions-v1.md; đầu báo cáo ai-review-us-05-v1.md (phạm vi review); đầu sequence US03/05 để đối chiếu tên; danh sách review/thiết kế; prompt-log |
| Version được phép sửa | Không có ai-review-01-v1.md, chưa có review US02. ai-review-us-05-v1.md chỉ review US05. Tiếp tục v1 cho US02; không sửa bản US05 đã review; không tạo v2 và không suy ra phê duyệt từ review US05. |
| Đầu ra BA | Sửa tối thiểu sys-us-02-v1.md (nhật ký, làm rõ Rejected còn blocked); bổ sung OQ-05, OQ-US02-01/02 và ghi ảnh hưởng của ID chung vào open-questions-v1.md. Giữ nguyên mọi dòng OQ cũ, không đóng OQ. |
| Đầu ra design | docs/design/payment-management/v1/diagrams/seq-us-02-v1.puml, .svg, .png; 03-detailed-design-v1.md chỉ danh mục/tên tạm/truy vết/kiểm chứng; 07-design-decisions-v1.md chỉ DD-01 cho submit. |
| Phần AI / nhóm sửa | AI thực hiện các thay đổi của lần này; chưa có nhóm sửa hoặc xác nhận nghiệp vụ; Design Pending Approval. Không sửa src, nguồn TA hoặc báo cáo review; không tạo commit. |

Prompt nguyên văn:

    Kiểm tra sys spec US-PAY-02 và tình trạng review để xác định version được phép cập nhật.

    Đóng vai agent ba: đối chiếu sys spec US-PAY-02 với đặc tả cục bộ và bảng Open Questions chung. Cập nhật OQ liên quan, giữ nguyên ID hiện có, không ghi đè câu hỏi của US khác và không tự đóng câu hỏi chưa có xác nhận.

    Sau đó đóng vai agent design, dùng skill sequence-diagram để tạo hoặc cập nhật sequence US-PAY-02 từ sys spec cùng version. Bao phủ luồng chính, nhánh lỗi, chống trình duyệt trùng và audit; ghi rõ `Blocked by OQ-...` ở phần chưa chốt.

    Kiểm tra sơ đồ và ghi kết quả thực tế vào nhật ký prompt.

Kiểm chứng thực tế:

- Đọc nguồn bằng Get-Content, liệt kê review/thiết kế, Test-Path cho ai-review-01-v1.md → False. Không đọc lại PDF trực tiếp ở lượt này, không dùng tài liệu nghiệp vụ trực tuyến.
- Tìm PlantUML trong các vị trí cục bộ không thấy jar; tìm rộng có một số thư mục Access denied. Java hiện có trên PATH là 1.8.0_251.
- Tải công cụ (không phải nguồn nghiệp vụ) từ Maven Central bằng Invoke-WebRequest vào thư mục tạm: lần trong môi trường hạn chế lỗi “No such host is known”; chạy lại với quyền truy cập mạng thành công. java -jar ... -version → PlantUML 1.2025.2, Installation seems OK. Không lưu jar vào repo.
- Lần gọi jar qua biến TEMP của môi trường hạn chế lỗi “Unable to access jarfile” vì TEMP khác môi trường tải. Đã dùng đường dẫn thực C:/Users/PC/AppData/Local/Temp/plantuml-1.2025.2.jar ở các lệnh sau.
- `java -jar C:/Users/PC/AppData/Local/Temp/plantuml-1.2025.2.jar -charset UTF-8 -checkonly docs/design/payment-management/v1/diagrams/seq-us-02-v1.puml` → exit 0.
- Cùng lệnh trên thay -checkonly bằng -tsvg, rồi -tpng → cả hai exit 0. SVG 82.584 byte; PNG 343.409 byte; kích thước 1941 × 3863. Đã mở PNG bằng view_image và kiểm tra trực quan: đủ các phần từ tiêu đề tới legend, không thấy cắt nội dung hoặc lỗi chữ.
- Kiểm tra đối chiếu Python qua stdin: lần đầu assertion thất bại vì lấy mọi chuỗi OQ trong sys spec, gồm cả OQ-US03-05 chỉ được nhắc để phân biệt thông báo kết quả duyệt. Điều chỉnh phạm vi kiểm tra thành ID ở bảng câu hỏi: PASS, đủ 8 ID được đồng bộ giữa sys/OQ/sequence. 18 dòng OQ cũ giữ nguyên so với git HEAD. Cặp start/end và tên sơ đồ đúng; SVG XML hợp lệ, không có Syntax Error. Bảng đối chiếu trong 03 bao phủ bước 1–8, A2, A3/A3.1, A4/A4.1, A5, A6/A6.1, A7 và AC-US02-01..13.
- `python -X utf8 scripts/verify_agent_config.py` → PASS (0 failed checks). Không kiểm thử ứng dụng, chưa đo NFR hiệu năng; kiểm chứng tài liệu không phải phê duyệt nghiệp vụ.
