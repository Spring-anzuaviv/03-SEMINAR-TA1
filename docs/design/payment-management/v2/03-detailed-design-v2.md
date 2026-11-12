# 03 – Danh mục sequence (v2)

## US-PAY-04

> Đầu vào: [sys-us-04-v2.md](../../../analysis/payment-management/v2/sys-us-04-v2.md), đúng bản người dùng cung cấp; TA-SPEC §4.4, PAY-05 và §6.
> Trạng thái: Design Pending Approval. Mục này chỉ ghi danh mục của US-04, chưa phải thiết kế chi tiết chung cho toàn module.

### Sơ đồ sequence

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

### Tên dùng tạm cần đồng bộ

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

### Kiểm chứng

Dùng Java 21.0.12 và PlantUML 1.2024.3 (jar của extension VS Code jebbs.plantuml 2.18.1), ngày 11/11/2026, P-36. Với `plantuml.jar` là jar công cụ cục bộ, đã chạy:

```text
java -DPLANTUML_LIMIT_SIZE=16384 -jar plantuml.jar -charset UTF-8 -checkonly docs/design/payment-management/v2/diagrams/seq-us-04-1-v2.puml docs/design/payment-management/v2/diagrams/seq-us-04-2-v2.puml
java -DPLANTUML_LIMIT_SIZE=16384 -jar plantuml.jar -charset UTF-8 -tsvg docs/design/payment-management/v2/diagrams/seq-us-04-1-v2.puml docs/design/payment-management/v2/diagrams/seq-us-04-2-v2.puml
```

Cả hai lệnh thành công. Python xác nhận đủ nhãn bước/ngoại lệ của từng bảng, tên `@startuml` khớp tên file và SVG XML hợp lệ; không còn nhãn B1–B7 hoặc X1. PNG tạm cũng được kết xuất và xem để kiểm tra bố cục cả hai sơ đồ. Kiểm tra tài liệu không thay thế kiểm thử giao dịch của ứng dụng.

### Thay đổi so với v1

- Thể hiện hồ sơ điều chỉnh riêng theo System Spec v2; giữ nguyên bảng Approved.
- Bổ sung GĐKD duyệt/từ chối, hiệu lực sau duyệt, lý do từ chối và audit.
- Đối chiếu từng nhánh với bước của System Spec v2; v1 được giữ nguyên.
- P-36: tách thành hai sequence theo mục 1.1 và 1.2; mỗi sơ đồ đánh số bước từ 1, nhánh từ chối dùng R; chuyển X1 thành ghi chú Ràng buộc chung.

## US-PAY-02

> Trạng thái: Design Pending Approval. Đầu vào: [SYS-US-02 và SYS-US-02b](../../../analysis/payment-management/v2/sys-us-02-v2.md).
> Căn cứ: TA-SPEC §2–3, §4.2–4.3, PAY-01..04, PAY-06, PAY-08 và §6 (NFR-PAY-01). Đối chiếu theo mã bước của bản v2.

### Sơ đồ sequence US-PAY-02

| Use case | Nguồn | Ảnh | Mục đích |
|---|---|---|---|
| SYS-US-02 | [PlantUML](diagrams/seq-us-02-1-v2.puml) | [SVG](diagrams/seq-us-02-1-v2.svg) | NVKD trình duyệt bảng, lưu lần trình và audit, sau đó gửi thông báo. |
| SYS-US-02b | [PlantUML](diagrams/seq-us-02-2-v2.puml) | [SVG](diagrams/seq-us-02-2-v2.svg) | NVKD gửi lại thông báo của lần trình hiện tại. |

| Use case | Bước và nhánh | Đoạn sequence |
|---|---|---|
| SYS-US-02 | 1–5, E2–E5.2 | Kiểm tra đăng nhập, vai trò, tồn tại, phân công và trạng thái. Với bảng Rejected, NVKD mở sửa theo SYS-US-03b trước khi trình lại. |
| SYS-US-02 | 6–7, E6, E7, E7.1 | Kiểm tra nguồn còn hợp lệ, tổng tiền không âm và đủ dòng cho mọi dịch vụ khai báo trong hợp đồng. |
| SYS-US-02 | 8, A8 | Chọn vai trò duyệt và lấy danh sách người nhận. Danh sách rỗng vẫn cho phép lưu lần trình và báo NVKD sau khi lưu thành công. |
| SYS-US-02 | 9, E9, E9.1 | Ghi có điều kiện Draft và phiên bản khớp, tăng phiên bản và số lần trình, ghi audit cùng giao dịch. Nếu xung đột thì yêu cầu đọc lại bảng. Nếu kết quả lưu chưa xác định thì yêu cầu xem lại bảng trước khi trình lại. |
| SYS-US-02 | 10–11, A10 | Gửi sau khi xác nhận lưu thành công. Nếu gửi lỗi, bảng vẫn PendingApproval và NVKD có thể chọn gửi lại. |
| SYS-US-02b | 1–2, E2 | Bắt đầu từ thao tác “Gửi lại thông báo”. Kiểm tra đăng nhập, vai trò, tồn tại, phân công và PendingApproval. |
| SYS-US-02b | 3, A3, A3.1 | Tìm người giữ vai trò đã lưu nếu danh sách rỗng. Báo chưa có người nhận nếu vẫn rỗng, báo đã gửi đủ nếu mọi người đã nhận, hoặc gửi cho những người chưa nhận. |
| SYS-US-02b | 4, A4 | Báo kết quả và cho phép gửi lại sau nếu vẫn lỗi. Thao tác giữ nguyên trạng thái, số lần trình và audit trình duyệt. |

Các phương án v2 liên quan đến quyền theo phân công (OQ-US02-01), thông báo và gửi lại (OQ-US02-02, OQ-US03-02), tổng so ngưỡng và đúng 500 triệu (OQ-US03-03, OQ-02), dịch vụ bắt buộc (OQ-05) và mở sửa bảng Rejected (OQ-04, OQ-US03-07) còn chờ xác nhận nghiệp vụ.

### Tên dùng tạm US-PAY-02

| Thành phần | Tên và trách nhiệm |
|---|---|
| PaymentController, PaymentService | `POST /api/payment-sheets/{id}/submit` gọi `Submit`. `POST /api/payment-sheets/{id}/submit/notifications/resend` gọi `ResendSubmissionNotifications`. |
| IPaymentRepository, IUnitOfWork, IAuditLog | `GetById`, `Transition`, `Begin`, `Commit`, `Rollback`, `Append`. Cập nhật có điều kiện trạng thái và phiên bản. |
| Các interface chỉ đọc | `IContractReader.GetContract`, `IPriceReader.GetPriceList`, `IQuantityReader.GetRecords`, `IUserDirectory.ListByRole`. |
| INotificationRepository, INotifier | `PrepareSubmission` lưu vai trò, danh sách và nội dung theo lần trình. `GetSubmissionNotificationPlan`, `EnsureRecipients`, `MarkNotification` theo dõi người nhận. `NotifySubmission` dùng khóa (bảng, lần trình, người nhận) để chống gửi trùng. |
| Kết quả HTTP | 200 cho kết quả trình duyệt hoặc gửi lại hợp lệ. 400 `NEGATIVE_TOTAL`, `REQUIRED_SERVICE_MISSING`. 401 `UNAUTHENTICATED`. 403 `FORBIDDEN`. 404 `NOT_FOUND`. 409 `DUPLICATE_SUBMIT`, `INVALID_STATE`, `SOURCE_NOT_VALID`, `CONCURRENT_MODIFICATION`. 500 `PERSISTENCE_ERROR`. 503 `SOURCE_UNAVAILABLE`, `RESULT_UNKNOWN`. |

Các tên, mã lỗi và cách lưu dữ liệu thông báo là đề xuất kỹ thuật để đồng bộ với hợp đồng API và quyết định thiết kế v2 khi có.

### Kiểm chứng US-PAY-02

Đã chạy PlantUML 1.2025.2 với `-charset UTF-8 -checkonly` và `-charset UTF-8 -tsvg` cho cả hai nguồn. Cả hai lệnh thành công và đã kiểm tra bố cục ảnh kết xuất.

## US-PAY-01 – Hai sequence độc lập trong cùng file

> Bổ sung: 12/11/2026 · Prompt: P-45 · AI: Codex / GPT-6.
> Đầu vào: [SYS-US-01 v2](../../../analysis/payment-management/v2/sys-us-01-v2.md), mục 1.1 và mục 1.2 SYS-US-01b đã được người dùng xác nhận trong chat. Trạng thái: Design Pending Approval.

Theo chỉ định của người dùng, [seq-us-01-v2.puml](diagrams/seq-us-01-v2.puml) chứa **hai khối `@startuml` độc lập**, không dùng nhánh lập/sửa hoặc nối luồng sửa vào sau khi lập. Khối lập giữ nguyên nội dung; khối sửa có actor, lifeline và số thứ tự riêng. Đây là ngoại lệ theo yêu cầu lưu cùng file; không tạo thêm bản nguồn `.puml` trùng nội dung.

| Khối nguồn trong cùng file | Ảnh riêng | Phạm vi |
|---|---|---|
| `@startuml seq-us-01-v2` | [seq-us-01-v2.svg](diagrams/seq-us-01-v2.svg) | SYS-US-01 mục 1.1, lập mới; giữ nguyên khối nguồn đã có. |
| `@startuml seq-us-01-update-v2` | [seq-us-01-update-v2.svg](diagrams/seq-us-01-update-v2.svg) | SYS-US-01b mục 1.2, chỉnh sửa bảng Draft đã lưu; không phụ thuộc việc thực hiện luồng lập. |

### Đối chiếu SYS-US-01b với sequence chỉnh sửa

| Bước/nhánh | Thể hiện trong khối chỉnh sửa |
|---|---|
| 1–3; A2; EC.1 | GetById đọc bảng, kiểm tra quyền NVKD phụ trách và Draft, hiển thị form; không bắt buộc là người tạo. Không tồn tại/sai quyền/trạng thái là A2; lỗi đọc là EC.1. |
| 4 | Cho nhập kỳ thanh toán và ghi chú; hợp đồng/khách hàng, sản lượng, đơn giá, tiền chỉ đọc. |
| A4.1 | ReloadSource đọc/tính theo kỳ đang chọn, chỉ cập nhật form. Loại trừ chính bảng và Cancelled khi tra trùng; không ghi nguồn hoặc lưu bảng trong thao tác này. |
| 5; A5 | Kiểm tra field bắt buộc trước gửi Update; tô đỏ đúng field và quay bước 4; ghi chú trống hợp lệ. |
| 6; A6; EC.1 | Đọc lại bảng/quyền/trạng thái. Đổi kỳ hoặc reloadSource thì dùng nguồn hiện tại để tính lại; chỉ sửa ghi chú thì giữ số liệu. Điều kiện không đạt về bước 4 hoặc kết thúc, lỗi kỹ thuật cho thử lại bước 6. |
| 7; A7; E7.1 | Update có điều kiện ID/Draft/version và bảo vệ kỳ, cùng audit trước/sau. Xung đột quay bước 1 tải mới; lỗi ghi/audit chắc chắn chưa lưu rollback và quay bước 5. |
| 8 | Trả dữ liệu đã commit, giữ cùng ID và trạng thái Draft; thông báo “Cập nhật bảng thanh toán thành công”. |
| AC.1 | Đóng trước lưu: giữ bảng cũ, không Update, kết thúc. |
| E7.2 | Chưa rõ commit hoặc mất phản hồi: chỉ xác minh/kết thúc; đã lưu trả đúng bảng/version của lần cập nhật để tới bước 8; chắc chắn chưa lưu mới quay bước 5. |

### Tên và đề xuất kỹ thuật cần đồng bộ

- GetById và Update dùng tên trong API v2 E6/E8; ReloadSource theo thao tác đã mô tả ở E8. E8 hiện chưa nhận `period` mới, còn thao tác tải nguồn chỉ trên form và xác minh lần update chưa có endpoint riêng. Sơ đồ dùng lời gọi luận lý, đánh dấu `period` và `operationId` là phần mở rộng đề xuất; không tuyên bố hợp đồng HTTP hiện tại đã hỗ trợ chúng. Lượt này không sửa API.
- ReadAndCalculateDraftSources là nhóm tương tác dùng lại giữa A4.1 và bước 6: GetContract, FindOverlap, GetQuantities, GetActiveForContract, tính tiền theo quy tắc SYS. Các reader chỉ đọc, không tạo/sửa hợp đồng, bảng giá hoặc sản lượng.
- IPaymentRepository.Update ghi trên bảng hiện có; expectedVersion và expectedStatus=Draft ngăn ghi đè. Đổi giữ chỗ kỳ cũ sang kỳ mới, dòng và audit phải cùng giao dịch; rollback giữ nguyên kỳ/số liệu cũ. Ràng buộc không trùng loại trừ chính bảng và các bảng Cancelled. Cơ chế cụ thể phải đồng bộ với thiết kế dữ liệu.
- `operationId` do UI cấp trước khi gửi lần lưu, để vẫn tra được khi mất toàn bộ phản hồi. Update ghi nhận kết quả gắn đúng thao tác; VerifySaveOutcome/FindSaveOutcome trong khối sửa nhận sheetId và operationId. Chỉ trả chắc chắn chưa commit khi có bằng chứng; truy vấn rỗng hoặc lỗi xác minh vẫn là chưa rõ. Đây là đề xuất cho E7.2; không dùng chỉ version hiện tại để gán kết quả cho một lần update.
- Begin trả kết quả mở; các thao tác ghi tiếp chỉ chạy khi thao tác trước OK. Chỉ rollback khi giao dịch còn mở và kết quả được xác định; không tuyên bố rollback được một giao dịch có thể đã commit. Không tự thêm SLA sửa Draft hoặc quy tắc VAT/làm tròn chưa có căn cứ mới.

### Kiểm chứng US-PAY-01b

Lệnh và kết quả cuối lượt tại P-45 trong [nhật ký](../../../workflow/prompt-log.md). Kiểm tra hai khối độc lập, giữ nguyên khối lập, đủ nhãn 1–8 và A2/A4.1/A5/A6/A7/AC.1/EC.1/E7.1/E7.2; chạy PlantUML `-checkonly`, `-tsvg` cho file chung và xem PNG sơ đồ chỉnh sửa. Kiểm tra cú pháp/render không thay thế kiểm thử API/giao dịch hoặc phê duyệt thiết kế.
