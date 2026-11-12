# 02 – Kiến trúc module Bảng thanh toán (v2)

> Phiên bản: v2 · Ngày: 11/11/2026 · Người phụ trách thiết kế: nhóm chưa chỉ định
> Đầu vào: SYS-US-01..05 v2, các sequence v2 (gồm SYS-US-01b), danh mục 03, thiết kế dữ liệu 05 và ERD v2, TA-SPEC §1–6, `src/Qtkd.Api/` và xác nhận của nhóm tại P-39, P-42.
> AI: Codex / GPT-6 · [P-39](../../../workflow/prompt-log.md#p-39--đồng-bộ-01-và-02-với-thiết-kế-v2)
> Trạng thái: Bản sau review – Design Pending Approval

## 1. Phạm vi và căn cứ

TA-SPEC là căn cứ đối chiếu với đề. Kiến trúc bám System Spec và sequence v2 về hành vi, danh mục 03 về tên thao tác và thiết kế 05 về cách lưu, ràng buộc và đồng thời. Xác nhận trong chat về quyền hủy, lý do hủy, lập mới cùng kỳ và quy tắc tính chung của US-01/04 được ghi ở P-39. Các câu hỏi còn mở theo 01, 03 và 05. SYS-US, OQ và NFR-PAY là mã nội bộ. [TA-SPEC](../../../requirements/payment-management/spec.md) · [Tóm tắt yêu cầu](01-requirements-summary-v2.md) · [Danh mục sequence](03-detailed-design-v2.md) · [Thiết kế dữ liệu](05-data-design-v2.md)

| Chức năng | Quy tắc nhóm đưa vào v2 | Đối chiếu đề và sequence |
|---|---|---|
| [SYS-US-01 và 01b](../../../analysis/payment-management/v2/sys-us-01-v2.md) | NVKD phụ trách lập bảng từ hợp đồng Active. Trên Draft đã lưu, NVKD sửa kỳ hoặc ghi chú. Khi đổi kỳ hoặc tải lại nguồn, dùng chung kiểm tra kỳ và nguồn với luồng lập, loại chính bảng đang sửa khỏi kiểm tra chồng lấn. | TA-SPEC §2, §4.1, PAY-01..03, §6 (tr.1–3). [Sequence lập bảng](diagrams/seq-us-01-v2.svg) · [Sequence sửa Draft](diagrams/seq-us-01-update-v2.svg). |
| [SYS-US-02 và 02b](../../../analysis/payment-management/v2/sys-us-02-v2.md) | NVKD phụ trách trình Draft, kiểm tra lại nguồn, tổng không âm và đủ dòng cho mọi dịch vụ hợp đồng. Chống trình trùng. Gửi thông báo trong hệ thống theo vai trò duyệt, cho gửi lại trên lần trình hiện tại. | TA-SPEC §4.2, PAY-04, PAY-06 (tr.2). [Trình duyệt](diagrams/seq-us-02-1-v2.puml) · [Gửi lại](diagrams/seq-us-02-2-v2.puml). |
| [SYS-US-03 và 03b](../../../analysis/payment-management/v2/sys-us-03-v2.md) | Tổng đã lưu gồm GTGT từ 500 triệu đồng trở lên do GĐKD xử lý, dưới mức đó do KTT. Cấm người lập tự duyệt/từ chối. Duyệt kiểm tra lại nguồn. Từ chối cần lý do tối đa 500 từ. Rejected về Draft khi NVKD phụ trách bấm “Chỉnh sửa”. | TA-SPEC §3, §4.3, PAY-06..08 (tr.1–2). Phương án System Spec v2 cho OQ-02 và OQ-04. [Duyệt/từ chối](diagrams/seq-us-03-1-v2.puml) · [Mở lại](diagrams/seq-us-03-2-v2.puml). |
| [SYS-US-04 và 04b](../../../analysis/payment-management/v2/sys-us-04-v2.md) | KTT lập hồ sơ có biên bản xác nhận hai bên và lý do từng thay đổi. Một hồ sơ chờ duyệt mỗi bảng. GĐKD xử lý hồ sơ bất kể tổng tiền. Chỉ hồ sơ đã duyệt có hiệu lực. Bảng gốc giữ Approved. | TA-SPEC §4.4, PAY-05, §6 (tr.2–3). Phương án hồ sơ riêng theo System Spec v2, còn `OQ-03` theo 03 và 05. [Lập hồ sơ](diagrams/seq-us-04-1-v2.puml) · [Xử lý hồ sơ](diagrams/seq-us-04-2-v2.puml). |
| [SYS-US-05](../../../analysis/payment-management/v2/sys-us-05-v2.md) | NVKD phụ trách hủy Draft kèm lý do. Bảng Cancelled giữ để tra cứu và giải phóng khoảng kỳ cho bảng mới. | TA-SPEC §3, §4.5, PAY-01, §6 (tr.1–3). Xác nhận của đại diện nhóm về OQ-US05-01/02/03 ghi ở P-39. [Sequence hủy](diagrams/seq-us-05-v2.puml). |

Chưa đủ đầu vào `open-questions-v2.md` và `requirements-checklist-v2.md` cho bộ tóm tắt BA đầy đủ. Bảng trên dẫn trực tiếp đến điều kiện và bước của System Spec v2. Các OQ được nhắc lại để đối chiếu quyết định của nhóm với đề gốc.

## 2. Hiện trạng và kiến trúc đề xuất

**AS-IS.** `Qtkd.Api` là ASP.NET Core Minimal API .NET 8. `Program.cs` đăng ký `ContractService` singleton, expose API demo hợp đồng và tuần tự hóa enum dạng chuỗi. `ContractService` dùng `ConcurrentDictionary` và khóa trong tiến trình khi trình hợp đồng. `Contract` có trạng thái `Active` nhưng API demo chưa có luồng kích hoạt. Trong cây `src/` hiện có model/service hợp đồng, chưa có module bảng thanh toán, phân quyền, audit, CSDL hay kiểm thử. [Program.cs](../../../../src/Qtkd.Api/Program.cs) · [ContractService.cs](../../../../src/Qtkd.Api/Services/ContractService.cs) · [Contract.cs](../../../../src/Qtkd.Api/Models/Contract.cs) · [Qtkd.Api.csproj](../../../../src/Qtkd.Api/Qtkd.Api.csproj)

**[ĐỀ XUẤT KỸ THUẬT]** Triển khai Bảng thanh toán thành một module riêng trong cùng ASP.NET Core host. Các thao tác ghi dùng CSDL quan hệ để kiểm tra đồng thời và ghi audit cùng giao dịch. Phương án tách dịch vụ độc lập sẽ thêm tích hợp mạng và vận hành riêng, trong khi luồng v2 dùng chung dữ liệu bảng, lần trình, hồ sơ và audit. Phương án giữ dữ liệu trong bộ nhớ như API demo không bảo toàn lịch sử qua lần khởi động lại. Chọn cùng host cho phạm vi hiện tại. [TA-SPEC §1, §6; SYS-US-01..05 v2]

| Thành phần đề xuất | Trách nhiệm |
|---|---|
| Giao diện Bảng thanh toán / `PaymentController` | Nhận yêu cầu, lấy danh tính và vai trò từ phiên đăng nhập, nhận phiên bản bản ghi khi có thao tác ghi. Phân quyền theo hợp đồng, vai trò và người lập được kiểm tra ở server trong từng use case. `PaymentController` là tên cổng vào trong sequence, có thể triển khai bằng nhóm endpoint Minimal API. |
| `PaymentService` | Lập, sửa kỳ/ghi chú trên Draft, tải lại nguồn, trình, gửi lại thông báo, hủy. Dùng chung kiểm tra và tính tiền khi lập, đổi kỳ hoặc tải lại nguồn. Phân công lấy từ nguồn hợp đồng. |
| `PaymentApprovalService` | Duyệt, từ chối và mở lại bảng bị từ chối. Dùng cùng hàm `RequiredApproverRole()` với `PaymentService`, tính theo tổng đã lưu, gồm GTGT. Giữ `createdBy` từ lúc lập để so quyền và gửi kết quả. |
| `PaymentAdjustmentService` | Lập, duyệt, từ chối hồ sơ. Tính đề xuất từ số liệu hiệu lực hiện tại và thuế suất gốc. Đọc số liệu hiệu lực theo `adjustment_no` tăng dần của các hồ sơ đã duyệt, theo 05 §11. |
| `IContractReader`, `IPriceReader`, `IQuantityReader` | Cổng chỉ đọc. Hợp đồng cung cấp hiệu lực, phân công, kỳ và danh mục dịch vụ. Bảng giá cung cấp mã, trạng thái và đơn giá. Sản lượng cung cấp bản ghi, tình trạng đối soát và thông tin phát hiện thay đổi. Các adapter cần cung cấp dữ liệu theo lô. |
| `IUserDirectory`, `INotifier` | Tra người dùng theo vai trò và gửi thông báo trong hệ thống. `NotifySubmission` nhận khóa `(sheetId, submissionNo, recipientId)` và trả `SENT` cho khóa đã gửi thành công. Thông báo kết quả duyệt hoặc từ chối gửi cho NVKD tạo bảng. |
| `INotificationRepository` | Quản lý `payment_submissions` và `payment_notifications` theo 03 §US-PAY-02 và 05 §3.5. `PrepareSubmission` lưu vai trò và nội dung lần trình cùng danh sách nếu có. `GetSubmissionNotificationPlan`, `EnsureRecipients` và `MarkNotification` đọc kế hoạch, lập danh sách một lần và cập nhật kết quả gửi. |
| `IPaymentRepository`, `IAdjustmentRepository`, `IUnitOfWork`, `IAuditLog` | Lưu bảng, dòng, nguồn đã dùng, hồ sơ và lịch sử audit. Khóa và ghi có điều kiện theo từng nghiệp vụ trong §3. Audit lưu loại đối tượng, mã bảng/hồ sơ, người, thời điểm và thay đổi trước/sau, kèm lý do hoặc tham chiếu biên bản khi có. |

[Sơ đồ component tổng quan](diagrams/component-v2.svg) · [Nguồn PlantUML](diagrams/component-v2.puml) · [Danh mục sequence và tên thao tác](03-detailed-design-v2.md) · [Sơ đồ trạng thái](diagrams/state-machine-v2.svg) · [ERD](diagrams/erd-v2.svg)

## 3. Lưu trữ, đồng thời và lỗi

1. **Lập bảng và giữ kỳ** [SYS-US-01 bước 7, 14–15, A15; SYS-US-05 S5; 05 §3.1, §8, §12]. `period_start` và `period_end` đều là ngày được tính trong kỳ. `FindOverlap` báo lỗi sớm. Theo DD-13, nếu kỳ được xác nhận là gồm trọn tháng dương lịch, giao dịch lập ghi `payment_period_claims` với khóa `(contract_id, month_start)` cho từng tháng cùng bảng, dòng, nguồn và audit. Khóa chặn cả trường hợp kỳ tháng chồng với kỳ quý hoặc hai yêu cầu lập đồng thời. Hủy xóa các claim cùng giao dịch với chuyển `Cancelled` và audit. `Rejected` vẫn giữ claim. Nếu kỳ có thể bắt đầu giữa tháng, phương án P5 trong 05 kiểm tra giao nhau theo khoảng ngày trên PostgreSQL. Quy tắc kỳ **Blocked by OQ-01** theo 05. Giữ chỗ theo tháng **Blocked by OQ-D-02**.
2. **Cập nhật bảng** [SYS-US-01b §1.2, SYS-US-02 §1.1 bước 9, SYS-US-03 §1.1 E10 và §1.2 E05, SYS-US-05 bước 7; 05 §7, §12]. Dùng điều kiện `id + trạng thái + version` và tăng `version` khi thay đổi bảng được lưu. Chỉ thao tác trình thành công tăng `submissionNo`. Khi trình và duyệt, so `source_version` của sản lượng nếu nguồn cung cấp. 05 nêu phương án so sản lượng và trạng thái đối soát nếu thiếu dấu phiên bản, với giới hạn có thể bỏ sót thay đổi khác (`OQ-D-03`).

   **Sửa Draft.** A4.1 chỉ đọc và tính theo kỳ trên biểu mẫu. Khi lưu, đổi kỳ hoặc đã tải lại thì kiểm tra lại nguồn. Bỏ qua chính bảng đang sửa và bảng `Cancelled` khi kiểm tra chồng lấn. Khi đổi kỳ, cập nhật kỳ, phần giữ chỗ theo phương án đã chọn, dòng/nguồn/tổng và audit trước/sau trong cùng giao dịch. Xung đột hoặc rollback giữ nguyên cả kỳ cũ lẫn dữ liệu cũ. Chỉ sửa ghi chú thì giữ kỳ và số liệu. Với E7.2, đề xuất gắn `operationId` với bản ghi audit và bản chụp của lần cập nhật để xác minh đúng phiên bản sau lưu. Chi tiết đổi kỳ và lưu dấu lần cập nhật cần đồng bộ tiếp ở 05 §9–12. [03 – Danh mục sequence](03-detailed-design-v2.md) · [04 – Hợp đồng API](04-api-contract-v2.md)
3. **Tách số liệu gốc và số liệu hiệu lực** [SYS-US-04 §1.1 bước 3, 5–7; §1.2 bước 3–6, R, 5a; 05 §11–12]. Phương án hồ sơ riêng **Blocked by OQ-03** theo 05. Khóa dòng bảng gốc khi lập hoặc xử lý hồ sơ, kiểm tra tối đa một `Pending` và cập nhật có điều kiện trạng thái/version hồ sơ. Khi đọc, áp các thay đổi dòng của hồ sơ `Approved` theo `adjustment_no` tăng dần. Tổng hiệu lực lấy `proposed_total` của hồ sơ đã duyệt có `adjustment_no` lớn nhất, hoặc tổng gốc nếu chưa có hồ sơ được duyệt. Số liệu đã duyệt của bảng gốc được giữ nguyên.
4. **Thông báo theo lần trình** [SYS-US-02 §1.1 bước 8–10, A8/A10; §1.2 bước 2–4, A3/A3.1; 03 §US-PAY-02; 05 §3.5, §12]. `PrepareSubmission` lưu `payment_submissions` và các dòng `payment_notifications` đang `Pending` cùng giao dịch chuyển bảng và ghi audit. Nếu chưa có người nhận, để `recipients_resolved_at` là `NULL`. Gửi sau commit. Khi gửi lại trên bảng `PendingApproval`, đọc lần trình hiện tại, dùng vai trò đã lưu để tìm người nhận nếu chưa có danh sách. `EnsureRecipients` chỉ lập danh sách một lần bằng ghi có điều kiện và chèn người nhận trong cùng giao dịch. Nếu danh sách đã có, chỉ gửi các dòng chưa `Sent`.

   **[ĐỀ XUẤT KỸ THUẬT]** Theo phương án mặc định ở 05 §3.5, module Bảng thanh toán sở hữu bản ghi thông báo trong hệ thống. Khóa duy nhất theo bảng, loại thông báo, lần trình và người nhận bảo vệ dữ liệu lưu. `INotifier` xử lý lặp theo khóa gửi trình duyệt `(sheetId, submissionNo, recipientId)`. Nếu sau này dùng dịch vụ thông báo chung, `payment_notifications` theo dõi kết quả và dịch vụ nhận cần xử lý lặp theo cùng khóa. Với kết quả duyệt/từ chối, 05 §12 dự kiến lưu thông báo cùng thay đổi và audit, còn sequence US-03 thể hiện bước gửi sau commit. Lỗi gửi giữ nguyên kết quả đã lưu.
5. **Kết quả giao dịch** [SYS-US-01 E15.1/E15.2; 02 E9/E9.1; 03 E09–E11; 04 §1.1 7b và §1.2 5a; 05 A7–A7.2]. Nếu biết giao dịch thất bại, hoàn tác dữ liệu và audit. Nếu kết quả chưa xác định, trả trạng thái chưa rõ và đọc lại để xác minh trước khi thao tác tiếp. Lần lưu nháp dùng `operationId` để tìm đúng lần lưu như sequence US-01. Lỗi đọc hoặc truy vấn rỗng không tự chứng minh giao dịch đã thất bại.

## 4. Đề xuất tính GTGT và làm tròn

**[QUYẾT ĐỊNH ĐÃ XÁC NHẬN]** Đại diện nhóm, ngày 11/11/2026, xác nhận US-01 dùng quy tắc tính của US-04 (P-39). Dùng chung bộ tính tiền cho lập/tải lại Draft và hồ sơ điều chỉnh. Hồ sơ dùng thuế suất đã lưu trên bảng gốc. [SYS-US-01 bước 10, 14 và hậu điều kiện; SYS-US-04 §1.1 Mô tả và bước 6; 05 §6–7]

**[ĐỀ XUẤT KỸ THUẬT – OQ-US03-03, chờ nhóm duyệt chi tiết]** Đọc một thuế suất đã được cấu hình cho hợp đồng và kỳ qua `IContractReader` hoặc adapter của nguồn quản lý cấu hình. Lưu giá trị thực dùng cùng tham chiếu nguồn trên Draft. Khi tải lại Draft, đọc lại giá trị từ nguồn. Nếu nguồn chưa trả về được đúng một giá trị áp dụng cho cả kỳ thì báo thiếu cấu hình và giữ nguyên dữ liệu. Chưa có trường thuế suất trong `Contract.cs` hiện tại. Phương án nhập thuế suất thủ công từng bảng linh hoạt hơn nhưng thêm quyền nhập và khả năng áp khác nhau cho cùng hợp đồng/kỳ.

Đề xuất dùng số thập phân chính xác, làm tròn lên đến đồng ở thành tiền từng dòng, cộng các dòng thành tạm tính, tính và làm tròn tiền GTGT một lần, rồi cộng tạm tính với tiền GTGT thành tổng. Như vậy các số hiển thị cộng khớp với tổng đã lưu. Phương án giữ phần lẻ đến cuối và làm tròn tổng một lần giảm chênh lệch cộng dồn. Hai cách có thể cho tổng khác nhau và đổi thẩm quyền tại biên 500.000.000 đồng. Các kiểm tra biên cần dùng cùng tổng đã lưu cho cả trình và duyệt. Chi tiết nguồn thuế suất, điểm làm tròn và cách xử lý kỳ có nhiều mức thuế chờ nhóm duyệt trước khi triển khai.

## 5. Kiểm chứng thiết kế

| Yêu cầu | Kịch bản cần kiểm thử khi có triển khai |
|---|---|
| PAY-01..03, US-01/05 | Hai lần lập chồng lấn tháng–quý, hai kỳ cùng chứa một ngày biên, hai kỳ liền kề không chung ngày, hủy rồi lập lại với ID mới. Đọc bảng giá và sản lượng theo lô, kiểm tra đối soát và đối chiếu nguồn của từng dòng với bản đã lưu. |
| PAY-04, US-02 | Hai lần trình cùng version chỉ tạo một lần trình và một audit. Thử tổng bằng 0, tổng âm, thiếu dòng. Thử lần trình chưa có người nhận, lỗi gửi một phần và gửi lại đồng thời. Nếu mất phản hồi sau khi đã gửi thành công, thử lại cùng khóa chỉ trả kết quả đã gửi. |
| PAY-06..08, US-03 | Vai trò tại 499.999.999 / 500.000.000 / 500.000.001 đồng. Người lập tự duyệt/từ chối bị chặn. Nguồn đổi chặn duyệt. Từ chối giữ Rejected cho đến khi NVKD phụ trách mở lại. |
| PAY-05, US-04 | Hai lần lập hồ sơ đồng thời chỉ tạo một hồ sơ Pending. Duyệt và từ chối cạnh tranh chỉ một lần thắng. Kiểm tra nhiều hồ sơ đã duyệt nối tiếp và hồ sơ bị từ chối, đồng thời xác nhận bảng gốc giữ nguyên. |
| NFR-PAY-01 [TA-SPEC §6, tr.3] | Tạo lỗi ghi audit ở từng giao dịch để kiểm tra không lưu chuyển trạng thái/điều chỉnh dở dang. Kiểm tra người, thời điểm và nội dung trước/sau. |
| NFR-PAY-02 [TA-SPEC §6, tr.3; SYS-US-01, mô tả] | Đo từ lúc server nhận yêu cầu lưu nháp đến khi trả kết quả đã lưu, với dưới 200 dòng sau gộp (ví dụ 199 dòng). Mục tiêu ≤3 giây. Đọc nguồn theo lô, tránh truy vấn mỗi dòng và dùng chỉ mục tra cứu theo hợp đồng/kỳ. Chưa đo hiệu năng. |

Đối chiếu tên và ràng buộc theo 03, 05 và ERD. Hai sequence US-02 đã tách trình duyệt và gửi lại. SYS-US-02b có nhánh tìm lại người nhận khi lần trình chưa có danh sách. Sequence US-01 có hai khối độc lập cho lập và sửa Draft. Kiểm chứng sửa Draft gồm tải thử không ghi, đổi kỳ hợp lệ, kỳ mới bị chiếm, xung đột phiên bản và xác minh khi mất phản hồi. Class diagram v2 còn thiếu. Kết quả kiểm tra tài liệu ghi ở P-39, P-40 và P-46. [Hợp đồng API v2](04-api-contract-v2.md)

## Thay đổi so với v1

| Vị trí | Thay đổi | Căn cứ |
|---|---|---|
| Giữ kỳ, nguồn và phân quyền | Kỳ tháng/quý dùng cả ngày đầu và ngày cuối, giải phóng kỳ khi hủy, kiểm tra lại nguồn khi trình và khi duyệt, dùng tổng đã lưu gồm GTGT để chọn vai trò duyệt. | SYS-US-01, 02, 03, 05 v2, 05 §7–8 và P-39 (OQ-01, OQ-02, OQ-D-02, OQ-D-03, OQ-US05-02). |
| Điều phối và dữ liệu | Hồ sơ điều chỉnh có vòng đời riêng. Lần trình lưu được việc chưa có người nhận và hỗ trợ gửi lại. | SYS-US-02b và 04/04b v2 (OQ-US02-02, OQ-03). |
| Bộ tính tiền | US-01 và US-04 dùng chung quy tắc. Nguồn thuế suất lần đầu và điểm làm tròn có phương án để nhóm duyệt. | SYS-US-01, 04 v2, 05 §6 và P-39 (OQ-US03-03). |
