# 03 – Danh mục sequence US-PAY-04 (v2)

> Đầu vào: [sys-us-04-v2.md](../../../analysis/payment-management/v2/sys-us-04-v2.md), đúng bản người dùng cung cấp; TA-SPEC §4.4, PAY-05 và §6.
> Trạng thái: Design Pending Approval. Mục này chỉ ghi danh mục của US-04, chưa phải thiết kế chi tiết chung cho toàn module.

## Sơ đồ sequence

| Nguồn | Ảnh | Phạm vi | Kiểm chứng |
|---|---|---|---|
| [seq-us-04-1-v2.puml](diagrams/seq-us-04-1-v2.puml) | [SVG](diagrams/seq-us-04-1-v2.svg) | SYS-US-04, mục 1.1: KTT lập hồ sơ, kiểm tra, lưu và audit | Đã kiểm tra cú pháp, kết xuất SVG/PNG và xem ảnh ngày 11/11/2026 (P-36). |
| [seq-us-04-2-v2.puml](diagrams/seq-us-04-2-v2.puml) | [SVG](diagrams/seq-us-04-2-v2.svg) | SYS-US-04b, mục 1.2: GĐKD duyệt hoặc từ chối, kiểm tra, cập nhật hồ sơ và audit | Đã kiểm tra cú pháp, kết xuất SVG/PNG và xem ảnh ngày 11/11/2026 (P-36). |

Hai sơ đồ biểu diễn hai yêu cầu độc lập. SYS-US-04b là mã nội bộ theo đặc tả v2, không phải US mới trong đề. Hậu tố `-1`/`-2` theo yêu cầu người dùng để giống cách tách US03; đây là ngoại lệ so với quy ước tên theo thao tác trong naming-versioning. Bản gộp được thay bằng hai bản tách.

| Bước trong System Spec | Đoạn sequence |
|---|---|
| Mục 1.1, 1–8 | Sơ đồ 1: nhập biên bản và thay đổi, kiểm tra, tính số liệu, lưu hồ sơ Chờ duyệt và audit. |
| Mục 1.1, 2a, 3a, 4a, 5a | Sơ đồ 1: các nhánh break dừng yêu cầu khi sai quyền, bảng, biên bản hoặc nội dung. |
| Mục 1.1, 7a, 7b | Sơ đồ 1: hồ sơ chờ duyệt trùng; lỗi lưu/audit/giao dịch; rollback khi xác định chưa lưu thành công. |
| Mục 1.1, Ràng buộc chung | Ghi chú cuối sơ đồ 1: bảng Approved không được sửa trực tiếp, trình hoặc hủy; chỉ điều chỉnh qua hồ sơ. |
| Mục 1.2, 1–6 | Sơ đồ 2, nhánh Duyệt: quyền GĐKD, hồ sơ Chờ duyệt, cấm tự duyệt, cập nhật hồ sơ và audit trước/sau. |
| Mục 1.2, R | Sơ đồ 2, nhánh Từ chối: lý do bắt buộc, lưu trạng thái và audit; số liệu hiệu lực không đổi. |
| Mục 1.2, 2a, 3a, 4a, 5a | Sơ đồ 2: các nhánh break về quyền, trạng thái, người lập, xung đột và lỗi ghi. |

## Tên dùng tạm cần đồng bộ

Chưa có hợp đồng API/class v2 dùng chung để đối chiếu. Các tên sau là đề xuất kỹ thuật, giữ cùng cách gọi với sequence US-04 đã có; không xác lập endpoint mới.

| Thành phần | Trách nhiệm và thao tác |
|---|---|
| PaymentAdjustmentService | Adjust(sheetId, minutes, changes, currentUser), ApproveAdjustment, DeclineAdjustment; kiểm tra và điều phối. |
| IPaymentRepository | GetByIdForUpdate: đọc và khóa bảng, không cập nhật số liệu/trạng thái bảng gốc. |
| IAdjustmentRepository | ListApproved, FindPending, Create, GetById, Transition. |
| IAuditLog | Append: người thao tác, thời điểm, nội dung trước/sau và lý do/biên bản. |
| IUnitOfWork | Begin, Commit, Rollback; hồ sơ và audit dùng cùng giao dịch. |

Khóa theo bảng, ràng buộc tối đa một hồ sơ Pending và cập nhật có điều kiện trạng thái/version là đề xuất thực hiện yêu cầu đồng thời của System Spec. Khóa giúp tính số liệu và ghi audit trên cùng dữ liệu; phương án khác là kiểm tra phiên bản số liệu hiệu lực. Các thao tác cùng bảng phải chờ nhau trong thời gian khóa. Hồ sơ dùng Pending/Approved/Declined tương ứng Chờ duyệt/Đã duyệt/Bị từ chối, tách khỏi trạng thái bảng thanh toán.

Cách xử lý hồ sơ riêng và thẩm quyền duyệt là phương án trong System Spec, còn chờ xác nhận nghiệp vụ OQ-03, OQ-US04-01/02/03 đã nêu trong bộ phân tích trước. Sơ đồ không thêm vai trò hay luồng thông báo. Không có danh mục AC trong bản System Spec hiện tại nên đối chiếu theo mã bước, không đặt lại mã AC.

## Kiểm chứng

Dùng Java 21.0.12 và PlantUML 1.2024.3 (jar của extension VS Code jebbs.plantuml 2.18.1), ngày 11/11/2026, P-36. Với `plantuml.jar` là jar công cụ cục bộ, đã chạy:

```text
java -DPLANTUML_LIMIT_SIZE=16384 -jar plantuml.jar -charset UTF-8 -checkonly docs/design/payment-management/v2/diagrams/seq-us-04-1-v2.puml docs/design/payment-management/v2/diagrams/seq-us-04-2-v2.puml
java -DPLANTUML_LIMIT_SIZE=16384 -jar plantuml.jar -charset UTF-8 -tsvg docs/design/payment-management/v2/diagrams/seq-us-04-1-v2.puml docs/design/payment-management/v2/diagrams/seq-us-04-2-v2.puml
```

Cả hai lệnh thành công. Python xác nhận đủ nhãn bước/ngoại lệ của từng bảng, tên `@startuml` khớp tên file và SVG XML hợp lệ; không còn nhãn B1–B7 hoặc X1. PNG tạm cũng được kết xuất và xem để kiểm tra bố cục cả hai sơ đồ. Kiểm tra tài liệu không thay thế kiểm thử giao dịch của ứng dụng.

## Thay đổi so với v1

- Thể hiện hồ sơ điều chỉnh riêng theo System Spec v2; giữ nguyên bảng Approved.
- Bổ sung GĐKD duyệt/từ chối, hiệu lực sau duyệt, lý do từ chối và audit.
- Đối chiếu từng nhánh với bước của System Spec v2; v1 được giữ nguyên.
- P-36: tách thành hai sequence theo mục 1.1 và 1.2; mỗi sơ đồ đánh số bước từ 1, nhánh từ chối dùng R; chuyển X1 thành ghi chú Ràng buộc chung.
