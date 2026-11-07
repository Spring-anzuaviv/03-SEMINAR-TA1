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
| Tóm tắt yêu cầu | `01-requirements-summary-v1.md` | 3 | `sys-us-*-v1`, `open-questions-v1` | Chưa làm |
| Sequence diagram | `diagrams/seq-us-01-v1.puml` … `seq-us-05-v1.puml` | 4 | `sys-us-NN-v1.md` cùng US | seq-us-05-v1 đã lập |
| Kiến trúc | `02-architecture-design-v1.md`, `diagrams/component-v1.puml` | 5 | sequence v1, `src/Qtkd.Api/` | Chưa làm |
| Class / state diagram | `03-detailed-design-v1.md`, `diagrams/class-v1.puml`, `diagrams/state-machine-v1.puml` | 6 | sequence, kiến trúc v1 | Chưa làm |
| API contract | `04-api-contract-v1.md` | 7 | sequence, 03 v1 | Chưa làm |
| Thiết kế dữ liệu | `05-data-design-v1.md` (+ `diagrams/erd-v1.puml`) | 8 | class, 04 v1 | Chưa làm |
| (bổ sung) Quyết định kỹ thuật | `07-design-decisions-v1.md` | 9 | ghi dần | Chưa làm |
| Ma trận truy vết | `06-traceability-matrix-v1.md` | 10 | toàn bộ v1 | Chưa làm |
| (tùy chọn) Bàn giao | `08-handoff-to-developer-v1.md` | – | toàn bộ v1 | Không bắt buộc |

Ảnh kết xuất (`.svg`/`.png`) đặt cạnh file `.puml`, cùng tên gốc. Chưa kết xuất thì
ghi `Chưa kiểm tra kết xuất sơ đồ` trong danh mục sơ đồ của 03.

Trạng thái mọi bản: `Design Pending Approval` cho tới khi người phụ trách duyệt.
