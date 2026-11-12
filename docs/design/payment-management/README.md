# Thiết kế – Bảng thanh toán

Đầu ra vai trò **design** ([AGENTS.md](../../../AGENTS.md)), đúng đường dẫn
`docs/design/payment-management/` mà đề yêu cầu [TA-PDF tr.3, Yêu cầu bài tập mục 1].
Tên file và version theo [naming-versioning](../../../skills/naming-versioning/SKILL.md).

| Thư mục | Ý nghĩa |
|---|---|
| [v1/](v1) | Bản lần chạy đầu (mục 3 của đề) – đóng băng khi có `ai-review-01-v1.md` |
| [v2/](v2) | Bản sau review – sao chép đủ v1 rồi sửa theo nhận xét được chấp nhận |

Mọi file thiết kế suy ra từ sys spec cùng version trong
[docs/analysis/payment-management/](../../analysis/payment-management/README.md).

## Danh mục sản phẩm (ví dụ v1) ↔ yêu cầu của đề

| Đề yêu cầu (mục 1) | File trong `v1/` | Bước | Đầu vào bắt buộc | Trạng thái |
|---|---|---|---|---|
| Tóm tắt yêu cầu | `01-requirements-summary-v1.md` | 3 | `sys-us-*-v1`, `open-questions-v1` | Đã lập (P-21) |
| Sequence diagram | `diagrams/seq-us-01-v1.puml` … `seq-us-05-v1.puml` | 4 | `sys-us-NN-v1.md` cùng US | Đủ 5 file |
| Kiến trúc | `02-architecture-design-v1.md`, `diagrams/component-v1.puml` | 5 | sequence v1, `src/Qtkd.Api/` | Đã lập (P-21) |
| Class / state diagram | `03-detailed-design-v1.md`, `diagrams/class-v1.puml`, `diagrams/state-machine-v1.puml` | 6 | sequence, kiến trúc v1 | Đã lập (P-21) |
| API contract | `04-api-contract-v1.md` | 7 | sequence, 03 v1 | Đã lập (P-22) |
| Thiết kế dữ liệu | `05-data-design-v1.md` (+ `diagrams/erd-v1.puml`) | 8 | class, 04 v1 | Đã lập (P-22) |
| (bổ sung) Quyết định kỹ thuật | `07-design-decisions-v1.md` | 9 | ghi dần | DD-01..12 (P-21, P-22) |
| Ma trận truy vết | `06-traceability-matrix-v1.md` | 10 | toàn bộ v1 | Đã lập (P-22) |
| (tùy chọn) Bàn giao | `08-handoff-to-developer-v1.md` | – | toàn bộ v1 | Không bắt buộc |

## Hiện trạng v2

| Sản phẩm | File trong `v2/` | Ghi chú |
|---|---|---|
| Tóm tắt, kiến trúc, chi tiết, API, dữ liệu, truy vết | `01-requirements-summary-v2.md` … `06-traceability-matrix-v2.md` | Mỗi file có mục "Thay đổi so với v1" (03 ghi theo từng US) |
| Quyết định kỹ thuật | `07-design-decisions-v2.md` | Chưa có file |
| Sequence US-01 | `diagrams/seq-us-01-v2.puml` | Một file hai khối `@startuml` (lập mới, sửa Draft); ảnh `seq-us-01-1-v2.svg`, `seq-us-01-2-v2.svg` |
| Sequence US-02..04 | `diagrams/seq-us-0N-1-v2.puml`, `seq-us-0N-2-v2.puml` | Tách hai thao tác mỗi US |
| Sequence US-05 | `diagrams/seq-us-05-v2.puml` | |
| Class, component, state, ERD | `diagrams/class-v2`, `component-v2`, `state-machine-v2`, `erd-v2` (`.puml` + `.svg`) | |

Hậu tố tách `-1`/`-2` chưa khớp mẫu `seq-us-NN-<thao-tac>-vK` của
[naming-versioning](../../../skills/naming-versioning/SKILL.md), nên
`scripts/verify_agent_config.py` hiện báo FAIL ở bước kiểm tra tên file.

Ảnh kết xuất (`.svg`/`.png`) đặt cạnh file `.puml`, cùng tên gốc. Chưa kết xuất thì
ghi `Chưa kiểm tra kết xuất sơ đồ` trong danh mục sơ đồ của 03.

Trạng thái mọi bản: `Design Pending Approval` cho tới khi người phụ trách duyệt.
