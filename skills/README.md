# Skill quy trình – Bảng thanh toán TA 1–2

Các skill là hướng dẫn từng bước cho một loại sản phẩm, dùng chung cho mọi công cụ
AI (Claude, Codex, Cursor…). Skill **không thay** [AGENTS.md](../AGENTS.md): luôn
đọc AGENTS.md trước; nếu skill và AGENTS.md khác nhau thì AGENTS.md thắng.
Mọi skill dùng [ngữ cảnh chung](_shared/payment-context.md) (nguồn, ID, OQ giữ chỗ,
ảnh chụp AS-IS, tên dùng chung, kiểm tra PlantUML) và quy ước tên/version trong
[naming-versioning](naming-versioning/SKILL.md).

## Thứ tự làm

Sys spec viết trước; mọi sản phẩm sau suy ra từ sys spec **cùng version**.
`vK` là `v1` (bản lần chạy đầu) hoặc `v2` (bản sau review).

| Bước | Skill | Vai trò | Đầu ra (ví dụ v1) |
|---|---|---|---|
| 0 | [naming-versioning](naming-versioning/SKILL.md) | mọi vai trò | Quy ước, không tạo file |
| 1 | [sys-spec](sys-spec/SKILL.md) | ba | `analysis/.../v1/sys-us-01-v1.md` … `sys-us-05-v1.md` |
| 2 | (AGENTS.md vai trò ba) | ba | `open-questions-v1.md`, `requirements-checklist-v1.md` |
| 3 | (AGENTS.md vai trò design) | design | `01-requirements-summary-v1.md` |
| 4 | [sequence-diagram](sequence-diagram/SKILL.md) | design | `diagrams/seq-us-01-v1.puml` … |
| 5 | [uml-diagrams](uml-diagrams/SKILL.md) | design | `02-architecture-design-v1.md`, `diagrams/component-v1.puml` |
| 6 | [uml-diagrams](uml-diagrams/SKILL.md) | design | `03-detailed-design-v1.md`, `class-v1.puml`, `state-machine-v1.puml` |
| 7 | (AGENTS.md vai trò design) | design | `04-api-contract-v1.md` |
| 8 | [data-design](data-design/SKILL.md) | design | `05-data-design-v1.md` (+ `erd-v1.puml`) |
| 9 | (AGENTS.md vai trò design) | design | `07-design-decisions-v1.md` (ghi dần từ bước 4) |
| 10 | [traceability-matrix](traceability-matrix/SKILL.md) | design | `06-traceability-matrix-v1.md` |
| 11 | (AGENTS.md vai trò reviewer, chat mới) | reviewer | `review/.../ai-review-01-v1.md` |
| 12 | – | nhóm | `review-assessment-01-v1.md`, `evaluation-report.md` |

Chi tiết đầu vào bắt buộc từng bước: [naming-versioning §6](naming-versioning/SKILL.md#6-thứ-tự-phụ-thuộc).
Đường dẫn rút gọn: `analysis/...` = `docs/analysis/payment-management/`,
`diagrams/` = `docs/design/payment-management/vK/diagrams/`.

## Cách gọi

```text
Đọc AGENTS.md, đóng vai agent <ba|design> và dùng skill <tên> trong
skills/<tên>/SKILL.md cho <phạm vi, vd. US-PAY-02>, version <v1|v2>.
Đọc skills/_shared/payment-context.md và skills/naming-versioning/SKILL.md.
Nêu nguồn đã đọc, file sẽ ghi và phần Blocked by OQ trước khi làm.
```

Ví dụ:

```text
Đọc AGENTS.md, đóng vai agent ba, dùng skill sys-spec cho US-PAY-02, version v1.
```

```text
Đọc AGENTS.md, đóng vai agent design, dùng skill sequence-diagram cho US-PAY-03,
version v1, đầu vào sys-us-03-v1.md. Giữ OQ-02 và OQ-04 ở trạng thái Cần xác nhận.
```

Skill không cấp quyền phê duyệt nghiệp vụ, không cho sửa `src/`, đặc tả hay báo
cáo reviewer. Reviewer không có skill riêng; dùng vai trò reviewer trong
AGENTS.md ở chat mới. Ghi mỗi lần chạy vào
[prompt-log](../docs/workflow/prompt-log.md).
