---
name: naming-versioning
description: Quy ước đặt tên file, thư mục version v1/v2, khối thông tin đầu file, mã ID (OQ, AC, DD, R, P) và thứ tự phụ thuộc sys-spec → sequence → kiến trúc → chi tiết → API → dữ liệu → truy vết cho module Bảng thanh toán. Mọi skill khác dùng quy ước này khi tạo hoặc đổi tên file.
---

# Skill: naming-versioning – Đặt tên, version và thứ tự làm

Vai trò: **mọi vai trò** trong [AGENTS.md](../../AGENTS.md). Đọc trước khi tạo,
đổi tên hoặc sao chép bất kỳ file đầu ra nào. AGENTS.md và [rules/](../../rules/README.md) vẫn ưu tiên khi khác biệt.
Kiểm tra tự động: `python scripts/verify_agent_config.py` (mục naming).

## 1. Hai version

| Version | Ý nghĩa | Khi nào đóng băng |
|---|---|---|
| `v1` | Bản lần chạy đầu: AI soạn từ đặc tả, nhóm chỉ sửa lỗi định dạng/tên | Khi tạo báo cáo `ai-review-01-v1.md` đầu tiên. Sau đó **không sửa** v1 |
| `v2` | Bản sau review: v1 + các nhận xét được nhóm chấp nhận + OQ đã có câu trả lời | Khi nhóm chốt nộp |

- Đề yêu cầu "bản lần chạy đầu và bản sau review (có lịch sử commit hoặc hai
  thư mục riêng)" [TA-PDF tr.3, Yêu cầu bài tập mục 3]. Workspace dùng **hai thư
  mục riêng** và vẫn commit Git; gắn tag `design-v1` khi đóng băng v1.
- Tạo v2: sao chép **toàn bộ** v1 sang `v2/`, đổi hậu tố `-v1` → `-v2` trong tên
  file và trong liên kết, rồi mới sửa. File không đổi nội dung vẫn có mặt ở v2,
  ghi "Không đổi so với v1" trong mục thay đổi.
- Trong một version, file chỉ dẫn tới file **cùng version** (v2 không link sang v1,
  trừ mục "Thay đổi so với v1").
- Chỉ dùng `v1`, `v2`. Cần thêm vòng review thì vẫn ghi vào v2 và tăng số báo cáo
  review (`ai-review-02-v2.md`), không tạo `v3` khi nhóm chưa quyết định.

## 2. Quy tắc tên chung

- Chữ thường, không dấu, nối bằng `-` (kebab-case), **không khoảng trắng**.
- Hậu tố version luôn ở cuối tên, trước đuôi file: `<ten>-v1.md`, `<ten>-v2.puml`.
- Hậu tố phải trùng thư mục chứa: file trong `v1/` kết thúc `-v1`.
- Số thứ tự hai chữ số: `01`, `02`… (`NN` = số US 01..05; `kk` = số thứ tự).
- Ảnh kết xuất cùng tên gốc với nguồn: `seq-us-02-v1.puml` → `seq-us-02-v1.svg`.
- Trong PlantUML, tên sau `@startuml` = tên file không đuôi.

## 3. Bảng tên file

Gốc phân tích: `docs/analysis/payment-management/vK/` (K = 1 hoặc 2).

| File | Nội dung | Vai trò/skill |
|---|---|---|
| `sys-us-NN-vK.md` | Đặc tả use case hệ thống cho US-PAY-NN (vd. `sys-us-01-v1.md`) | ba / sys-spec |
| `open-questions-vK.md` | Bảng OQ dùng chung, ID ổn định qua các version | ba |
| `requirements-checklist-vK.md` | 5 US, 8 PAY, 2 NFR → trạng thái/OQ | ba |
| `requirements-analysis-vK.md` | Tùy chọn: tổng hợp PAY/NFR nếu không nằm hết trong sys-us | ba |

Gốc thiết kế: `docs/design/payment-management/vK/`.

| File | Nội dung | Vai trò/skill |
|---|---|---|
| `01-requirements-summary-vK.md` | Tóm tắt yêu cầu, OQ (gồm OQ-D) | design |
| `02-architecture-design-vK.md` | AS-IS, TO-BE, thành phần, tích hợp | design / uml-diagrams |
| `03-detailed-design-vK.md` | Lớp, luồng, trạng thái, guard, lỗi, **danh mục tên dùng chung**, danh mục sơ đồ | design / uml-diagrams, sequence-diagram |
| `04-api-contract-vK.md` | Hợp đồng API | design |
| `05-data-design-vK.md` | Mô hình dữ liệu, ràng buộc, audit | design / data-design |
| `06-traceability-matrix-vK.md` | Ma trận truy vết | design / traceability-matrix |
| `07-design-decisions-vK.md` | Quyết định kỹ thuật DD-kk | design |
| `08-handoff-to-developer-vK.md` | Tùy chọn (không thuộc danh mục mục 1 của đề) | design |

Sơ đồ: `docs/design/payment-management/vK/diagrams/`.

| File | Loại | Ghi chú |
|---|---|---|
| `seq-us-NN-vK.puml` | Sequence của US-PAY-NN | Mặc định một file/US, vd. `seq-us-02-v1.puml` |
| `seq-us-NN-<thao-tac>-vK.puml` | Sequence tách theo thao tác | Chỉ khi một US có nhiều thao tác; `<thao-tac>` ∈ `create`, `update`, `submit`, `approve`, `reject`, `adjust`, `cancel`, vd. `seq-us-03-approve-v1.puml` |
| `component-vK.puml` | Component (kiến trúc) | Đi với 02 |
| `class-vK.puml` | Class | Đi với 03 |
| `state-machine-vK.puml` | State machine | Đi với 03 |
| `erd-vK.puml` | ERD (mô hình dữ liệu, không phải UML) | Tùy chọn, đi với 05 |
| `use-case-vK.puml`, `activity-<thao-tac>-vK.puml` | Tùy chọn | Chỉ khi cần |

Khi nhập một bộ tài liệu có sẵn theo từng US, có thể giữ đặc tả, Open Questions
và sequence cùng ảnh trong `docs/design/payment-management/vK/us-pay-NN/`.
Dùng `sys-us-NN-vK.md`, `open-questions-vK.md` và tên sequence theo bảng trên.

Review: `docs/review/payment-management/` (không chia thư mục, version nằm trong tên).

| File | Nội dung | Ai ghi |
|---|---|---|
| `ai-review-NN-vK.md` | Báo cáo AI reviewer lần NN, review bản vK (vd. `ai-review-01-v1.md`) | reviewer |
| `review-assessment-NN-vK.md` | Nhóm đánh giá từng nhận xét của `ai-review-NN-vK`: Đúng/Sai/Thừa | nhóm (người) |
| `evaluation-report.md` | **Báo cáo đánh giá nộp (mục 2 của đề)**: bảng vấn đề trong đặc tả + tổng hợp Đúng/Sai/Thừa | nhóm |

`NN` của review tăng liên tục qua mọi version (01, 02…), không bắt đầu lại ở v2.

Nhật ký: `docs/workflow/prompt-log.md` (một file, mỗi lần chạy một mục `P-kk`).

## 4. Mã ID

| Mã | Mẫu | Định nghĩa tại | Ghi chú |
|---|---|---|---|
| Yêu cầu gốc | `US-PAY-0N`, `PAY-0N` | TA-SPEC | Mã của đề, không đổi |
| NFR | `NFR-PAY-01`, `NFR-PAY-02` | TA-SPEC §6 | Mã nội bộ |
| OQ có sẵn | `OQ-01`..`OQ-05` | `open-questions-vK.md` | Đã giữ chỗ cho 5 vấn đề biết trước, xem [ngữ cảnh chung §4](../_shared/payment-context.md) |
| OQ do BA phát hiện | `OQ-USNN-kk` (vd. `OQ-US02-01`) | Phần 2 của `sys-us-NN-vK.md`, chép vào `open-questions-vK.md` | Mỗi người viết sys-us tự đánh số trong US của mình → không trùng khi làm song song |
| OQ do design phát hiện | `OQ-D-kk` | `01-requirements-summary-vK.md` | |
| AC dẫn xuất | `AC-USNN-kk` | Phần 3 của `sys-us-NN-vK.md` | Mã tự đặt |
| Quyết định kỹ thuật | `DD-kk` | `07-design-decisions-vK.md` | |
| Nhận xét review | `RNN-kk` (vd. `R01-03`) | `ai-review-NN-vK.md` | `NN` = số báo cáo |
| Prompt | `P-kk` | `docs/workflow/prompt-log.md` | |

- ID **không đổi** giữa v1 và v2. OQ đã trả lời vẫn giữ ID, đổi trạng thái.
- ID bị bỏ thì ghi "Đã hủy – lý do", không tái sử dụng số.
- Trước khi đặt mã mới: `grep -rn "OQ-\|AC-US\|DD-\|R[0-9][0-9]-" docs/` để tránh trùng.

## 5. Khối thông tin đầu file

Markdown – ngay dưới tiêu đề `# <Tên tài liệu> (vK)`:

```markdown
> Phiên bản: v1 · Ngày: 07/11/2026 · Người phụ trách: <tên thành viên>
> Đầu vào: sys-us-02-v1.md; open-questions-v1.md; TA-SPEC §4.2, §5 PAY-04
> AI: <công cụ/model> · Prompt: P-03 trong docs/workflow/prompt-log.md
> Trạng thái: Bản lần chạy đầu – Design Pending Approval
```

PlantUML – ngay sau `@startuml <ten-file>`:

```plantuml
title <Tên sơ đồ> (US-PAY-02) – v1
' Phiên bản: v1 | Đầu vào: sys-us-02-v1.md | Prompt: P-03
' Mục đích / Phạm vi / US / PAY / OQ: ...
' Trạng thái: Design Pending Approval
```

Trạng thái chuẩn: v1 `Bản lần chạy đầu – … Pending Approval`; v2 `Bản sau review –
… Pending Approval`. Chỉ ghi "Đã duyệt" khi có người/ngày/tham chiếu xác nhận.

Ở v2, cuối mỗi file có mục:

```markdown
## Thay đổi so với v1

| # | Vị trí | Thay đổi | Căn cứ (R-ID đã chấp nhận / OQ đã trả lời) |
|---|---|---|---|
```

## 6. Thứ tự phụ thuộc

Làm theo thứ tự; bước sau **chỉ** dùng đầu ra cùng version của bước trước.
Thiếu đầu vào bắt buộc thì dừng, báo "Chưa đủ đầu vào: <file>", không tự suy ra.

| Bước | Vai trò | Đầu ra (vK) | Đầu vào bắt buộc |
|---|---|---|---|
| 1 | ba | `sys-us-NN-vK.md` (5 file, chia người làm song song) | TA-SPEC |
| 2 | ba | `open-questions-vK.md`, `requirements-checklist-vK.md` | Bước 1 |
| 3 | design | `01-requirements-summary-vK.md` | Bước 1–2 |
| 4 | design | `seq-us-NN-vK.puml` | `sys-us-NN-vK.md` của đúng US đó |
| 5 | design | `02-architecture-design-vK.md`, `component-vK.puml` | Bước 4, `src/Qtkd.Api/` |
| 6 | design | `03-detailed-design-vK.md`, `class-vK.puml`, `state-machine-vK.puml` | Bước 4–5 |
| 7 | design | `04-api-contract-vK.md` | Bước 4, 6 |
| 8 | design | `05-data-design-vK.md` (+ `erd-vK.puml`) | Bước 6–7 |
| 9 | design | `07-design-decisions-vK.md` | Ghi dần từ bước 4 |
| 10 | design | `06-traceability-matrix-vK.md` | Tất cả bước trên |
| 11 | reviewer (chat mới) | `ai-review-NN-vK.md` | Toàn bộ vK |
| 12 | nhóm | `review-assessment-NN-vK.md`, `evaluation-report.md` | Bước 11 |
| 13 | design | Thư mục `v2/` | Nhận xét được chấp nhận ở bước 12 |

Hạn nộp mục 1–2 của đề cần tối thiểu: bước 1–12 cho v1. v2 (mục 3) có thể làm
sau, nhưng thư mục đã có sẵn.

## 7. Tự kiểm trước khi trả lời

- [ ] Tên file đúng bảng mục 3, hậu tố khớp thư mục, không khoảng trắng/dấu.
- [ ] Khối thông tin đầu file đủ: version, đầu vào cùng version, prompt, trạng thái.
- [ ] Không sửa file trong `v1/` sau khi đã có `ai-review-01-v1.md`.
- [ ] Liên kết chỉ trỏ cùng version; ID mới không trùng ID cũ.
- [ ] Chạy `python scripts/verify_agent_config.py` và ghi kết quả.
