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
    - + giá trị thuế

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
