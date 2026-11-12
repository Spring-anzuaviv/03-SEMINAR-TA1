# 04 – Hợp đồng API module Bảng thanh toán (v2)

> Phiên bản: v2 · Ngày: 11/11/2026 · Người phụ trách: chờ nhóm chỉ định
> Đầu vào: TA-SPEC §1–6, SYS-US-01..05 v2, các sequence v2 gồm SYS-US-01b và tài liệu 01, 02, 03, 05 cùng phiên bản.
> AI: Codex / GPT-6 · [P-40](../../../workflow/prompt-log.md#p-40--tạo-hợp-đồng-api-v2), [P-46](../../../workflow/prompt-log.md#p-46--đồng-bộ-thiết-kế-với-sys-us-01b)
> Trạng thái: Bản đề xuất sau review – Design Pending Approval

## 1. Quy ước chung

**[ĐỀ XUẤT KỸ THUẬT]** Dùng JSON UTF-8 và enum dạng chuỗi dưới `/api/payment-sheets`. Giữ các route đã ghi trong sequence v2. Các route và kiểu dữ liệu được bổ sung dưới đây mô tả hợp đồng đề xuất. Hành vi nghiệp vụ lấy từ System Spec, phạm vi và quyền theo TA-SPEC §1–5. Cơ chế xác thực cụ thể chờ thiết kế triển khai. [TA-SPEC](../../../requirements/payment-management/spec.md) · [01 – Yêu cầu và OQ](01-requirements-summary-v2.md) · [02 – Kiến trúc](02-architecture-design-v2.md) · [03 – Danh mục sequence](03-detailed-design-v2.md) · [05 – Dữ liệu](05-data-design-v2.md)

- **Quyền.** Mọi request cần xác thực. Server lấy `userId` và `role` (`NVKD`, `KTT`, `GDKD`) từ phiên đăng nhập. Kiểm tra vai trò, tồn tại và quyền trên đối tượng trước các kiểm tra trạng thái và nghiệp vụ. NVKD thao tác theo phân công hợp đồng. Thẩm quyền duyệt bảng dựa trên tổng đã lưu gồm GTGT, dùng chung quy tắc với khi trình.
- **Phiên bản.** `version` là số nguyên dương. Request ghi trên bảng/hồ sơ hiện có dùng `expectedVersion` của đúng đối tượng theo bảng endpoint. Ghi có điều kiện theo ID, trạng thái và version. Gửi lại thông báo chỉ tác động lần trình và bản ghi người nhận.
- **Lưu và gửi.** Dữ liệu thay đổi và audit đi cùng giao dịch. Chỉ gửi thông báo sau khi xác nhận commit. Lỗi gửi sau commit trả kết quả nghiệp vụ thành công kèm `notificationStatus`. Khi kết quả ghi chưa rõ, trả `503 RESULT_UNKNOWN` và hướng dẫn đọc lại hoặc xác minh trước khi thao tác tiếp.
- **Định dạng.** ID bảng, hồ sơ và `operationId` là UUID. `contractId` là số nguyên dương. Ngày dùng `YYYY-MM-DD`, thời điểm dùng ISO 8601 có múi giờ. Tiền và sản lượng dùng chuỗi thập phân, tối đa 4 chữ số sau dấu chấm theo 05 §6. `taxRate` là tỷ lệ dạng chuỗi (`"0.1000"` biểu diễn 10%). Ví dụ thuế chỉ minh họa định dạng. Nguồn thuế suất và điểm làm tròn **Blocked by OQ-US03-03**.

| Dữ liệu trả về | Trường và kiểu |
|---|---|
| `PeriodDto` | `type` (`Month`/`Quarter`), `start`, `end` (ngày). Cả `start` và `end` đều thuộc kỳ. Kỳ hợp lệ lấy theo cấu hình hợp đồng. Cách giữ chỗ theo tháng phụ thuộc `OQ-01`, `OQ-D-02` theo 05 §8. |
| `PaymentLineDto` | `id`, `lineNo`, `serviceCode`, `serviceName` (có thể `null`), `quantity`, `unitPrice`, `lineAmount`, `sourceRecordIds` (mảng chuỗi). |
| `PaymentSheetDto` | `id`, `code`, `contractId`, `period`, `status`, `version`, `submissionNo`, `priceListId`, `lines`, `subtotalAmount`, `taxRate`, `taxAmount`, `totalAmount`, `calculatedAt`, `note`, `createdBy`, `createdAt`, `rejectionReason`, `cancelReason`. `note` và lý do có thể `null`. `submissionNo = 0` trước lần trình đầu. `status` thuộc `Draft`, `PendingApproval`, `Approved`, `Rejected`, `Cancelled`. `rejectionReason` ánh xạ `rejection_reason` (sequence dùng biến `rejectReason`). |
| `SubmissionResultDto` | `id`, `status`, `version`, `submissionNo`, `requiredRole`, `notificationStatus`. Với trình/gửi lại, `notificationStatus` là `Sent` nếu đã gửi đủ, `NoRecipients` nếu chưa có danh sách người nhận, `Failed` nếu còn lượt gửi lỗi. Đây là kết quả tổng hợp của API. 05 lưu `Pending`, `Sent`, `Failed` cho từng người nhận. |
| `AdjustmentDto` | `id`, `sheetId`, `adjustmentNo`, `status` (`Pending`, `Approved`, `Declined`), `version`, `createdBy`, `createdAt`, `decidedBy`, `decidedAt`, `declineReason`, `minutes`, `changes`, `effectiveTotalBefore`, `proposedSubtotal`, `proposedTaxAmount`, `proposedTotal`. `decidedBy`, `decidedAt`, `declineReason` có thể `null`. `minutes` gồm số, ngày, hai xác nhận và tên tệp. `changes` gồm `changeType`, `serviceCode`, `reason`, `before`, `after`. Mỗi giá trị trước/sau gồm `quantity`, `unitPrice`, `lineAmount`, hoặc `null` ở phía chưa có dòng. |
| `ApiError` | `{ code: string, message: string, details?: object }`. `details` có thể chứa `fieldErrors`, `failedStep`, `missingServices` hoặc `operationId` theo endpoint. |

## 2. Danh mục endpoint

Path dưới đây đã gồm prefix. `{id}` là ID bảng. Mã `E` là tham chiếu nội bộ để đối chiếu sequence. Các mã có tên trong sequence hiện hành được giữ nguyên.

| ID | Method và path | Thao tác | Actor | Request | Thành công | Trạng thái |
|---|---|---|---|---|---|---|
| E2 | `GET /api/payment-sheets/form/contracts/{contractId}` | `OpenCreateForm` | NVKD phụ trách | Path `contractId` | `200 { contract, periodType, availablePeriods }` | Chỉ đọc |
| E20 | `POST /api/payment-sheets/form/contracts/{contractId}/calculate` | `Calculate` | NVKD phụ trách | `{ period }` | `200 { operationId, period, priceListId, lines, subtotalAmount, taxRate, taxAmount, totalAmount }` | Chỉ tính trên biểu mẫu |
| E5 | `POST /api/payment-sheets` | `Create` | NVKD phụ trách | `{ contractId, period, note?, operationId }` | `201 PaymentSheetDto`, `Location` tới E6. `200` khi phát lại đúng lần lưu đã commit theo §3.1 | → `Draft` |
| E6 | `GET /api/payment-sheets/{id}` | `GetById` | NVKD phụ trách hoặc KTT/GĐKD có thẩm quyền của lần trình cần xem | Path `id` | `200 PaymentSheetDto` | Chỉ đọc |
| E7 | `GET /api/payment-sheets/form/contracts/{contractId}/save-outcomes/{operationId}` | `VerifySaveOutcome` | NVKD phụ trách, người đã gửi lần lưu | Path `contractId`, `operationId` | `200 { outcome, sheet? }` | Chỉ đọc |
| E22 | `POST /api/payment-sheets/{id}/reload-source` | `ReloadSource` | NVKD phụ trách | `{ period }` | `200 { period, priceListId, lines, subtotalAmount, taxRate, taxAmount, totalAmount }` | Chỉ tính trên biểu mẫu Draft |
| E8 | `PUT /api/payment-sheets/{id}` | `Update` | NVKD phụ trách | `{ expectedVersion, period, note, reloadSource?, operationId }` | `200 PaymentSheetDto` | `Draft` → `Draft`, giữ cùng ID |
| E23 | `GET /api/payment-sheets/{id}/save-outcomes/{operationId}` | `VerifySaveOutcome` cho cập nhật | NVKD phụ trách, người đã gửi lần lưu | Path `id`, `operationId` | `200 { outcome, sheet? }` | Chỉ đọc |
| E9 | `POST /api/payment-sheets/{id}/submit` | `Submit` | NVKD phụ trách | `{ expectedVersion }` | `200 SubmissionResultDto` | `Draft` → `PendingApproval` |
| E15 | `POST /api/payment-sheets/{id}/submit/notifications/resend` | `ResendSubmissionNotifications` | NVKD phụ trách | Body rỗng | `200 SubmissionResultDto` | Giữ `PendingApproval` |
| E10 | `POST /api/payment-sheets/{id}/approve` | `Approve` | KTT/GĐKD có thẩm quyền, khác người lập | `{ expectedVersion }` | `200 { sheet, notificationStatus }` | `PendingApproval` → `Approved` |
| E11 | `POST /api/payment-sheets/{id}/reject` | `Reject` | KTT/GĐKD có thẩm quyền, khác người lập | `{ expectedVersion, reason }` | `200 { sheet, notificationStatus }` | `PendingApproval` → `Rejected` |
| E16 | `POST /api/payment-sheets/{id}/reopen` | `Reopen` | NVKD phụ trách | `{ expectedVersion }` | `200 PaymentSheetDto` | `Rejected` → `Draft` |
| E12 | `POST /api/payment-sheets/{id}/adjustments` | `Adjust` | KTT | `multipart/form-data` theo §3.4 | `201 AdjustmentDto`, `Location` tới E17 | Hồ sơ → `Pending`, bảng giữ `Approved` |
| E21 | `GET /api/payment-sheets/{id}/adjustments` | Đọc hồ sơ của bảng | KTT xem hồ sơ mình lập, GĐKD xem hồ sơ cần xử lý hoặc đã xử lý | Path `id` | `200 { items }` theo §3.4 | Chỉ đọc |
| E17 | `GET /api/payment-sheets/{id}/adjustments/{adjustmentId}` | Đọc hồ sơ và biên bản | KTT/GĐKD theo quyền E21 | Path `id`, `adjustmentId` | `200 { sheet, adjustment, effectiveTotal }` | Chỉ đọc |
| E18 | `POST /api/payment-sheets/{id}/adjustments/{adjustmentId}/approve` | `ApproveAdjustment` | GĐKD khác người lập hồ sơ | `{ expectedVersion }` của hồ sơ | `200 { adjustment, effectiveTotal }` | Hồ sơ `Pending` → `Approved` |
| E19 | `POST /api/payment-sheets/{id}/adjustments/{adjustmentId}/decline` | `DeclineAdjustment` | GĐKD khác người lập hồ sơ | `{ expectedVersion, reason }` của hồ sơ | `200 { adjustment, effectiveTotal }` | Hồ sơ `Pending` → `Declined` |
| E13 | `POST /api/payment-sheets/{id}/cancel` | `Cancel` | NVKD phụ trách | `{ expectedVersion, reason }` | `200 { id, status, version, cancelReason }` | `Draft` → `Cancelled` |

## 3. Hành vi theo use case

### 3.1. Lập và sửa Draft

**E2, E20 – Mở biểu mẫu và tính.** `contract` gồm `id`, `customerName`, `status` lấy từ hợp đồng đang xem. `periodType` và `availablePeriods: PeriodDto[]` lấy theo cấu hình và các kỳ chưa bị chiếm. `availablePeriods: []` là A3. Lỗi đọc trả `503 SOURCE_UNAVAILABLE`. Khi NVKD chọn kỳ, E20 kiểm tra kỳ, trùng/chồng lấn, sản lượng và bảng giá Active, sau đó trả số liệu để điền biểu mẫu. `lines` có các trường tính của `PaymentLineDto`, với `id` chỉ xuất hiện sau lưu. Hệ thống tự chọn đúng một bảng giá Active theo SYS-US-01. Sequence bước 9 hiện thể hiện chọn giá và thiếu đơn giá. Kiểm tra có đúng một bảng giá Active lấy từ tiền điều kiện SYS-US-01. [SYS-US-01, bước 1–11, A3/A7/A8/A9/A11/EC.1](../../../analysis/payment-management/v2/sys-us-01-v2.md) · [Sequence lập bảng](diagrams/seq-us-01-v2.puml)

**E5 – Lưu nháp.** Server kiểm tra lại phân công, hiệu lực hợp đồng, kỳ và nguồn, rồi tính lại theo dữ liệu hiện tại. `note` có thể bỏ qua hoặc để `null`. Giá, dòng, thuế và tổng do server tính. Ghi bảng, dòng, nguồn, ràng buộc kỳ và audit trong cùng giao dịch. Kỳ bị chiếm tại thời điểm ghi trả `409 PERIOD_OCCUPIED`. Lỗi ghi đã xác định rollback trả `500 PERSISTENCE_ERROR`. [SYS-US-01 bước 13–16, A14/A15/E15.1/E15.2; PAY-01..03; 05 §8, §12]

**E5, E7 – Xác minh lần lưu.** Đề xuất cấp `operationId` ở E20 để client có ID trước khi gửi E5, kể cả khi mất toàn bộ phản hồi. Sequence hiện cấp ID bên trong thao tác lưu. Khi duyệt hợp đồng này, cần đồng bộ vị trí cấp ID trong sequence. E20 cấp UUID mới cho một lần tính thành công. Client giữ ID gắn với hợp đồng và kỳ đã chọn khi gửi lưu. ID ghi vào `payment_sheets.create_operation_id` với ràng buộc duy nhất theo DD-17. Nếu cùng người dùng và cùng dữ liệu nhập đã commit, E5 trả `200` với dữ liệu của lần lưu đó từ bản chụp audit `create`. Nếu cùng ID bị dùng cho nội dung khác, trả `409 OPERATION_ID_CONFLICT`.

E7 tìm đúng lần lưu và kiểm tra quyền trước khi trả dữ liệu. `outcome` là `COMMITTED` (kèm `sheet` tại lần tạo), `DEFINITELY_NOT_COMMITTED` (chỉ khi có bằng chứng giao dịch chưa commit) hoặc `UNKNOWN`. Truy vấn không thấy ID hoặc gặp lỗi tra cứu để kết quả ở `UNKNOWN`. Nếu E5 trả `RESULT_UNKNOWN`, hoặc mất kết nối khi đã gửi E5, client xác minh bằng E7 trước khi gửi lại. Phương án cấp ID trước tránh nhầm với bảng do yêu cầu khác lập cùng kỳ. [Sequence US-01 E15.2](diagrams/seq-us-01-v2.puml) · [05 §10, §12 và DD-17](05-data-design-v2.md)

**E6, E22 – Mở sửa và tải lại nguồn.** E6 trả bảng và version đã lưu để mở biểu mẫu hoặc đọc lại sau xung đột. E22 kiểm tra NVKD phụ trách, `Draft` và kỳ đang chọn. Dùng lại kiểm tra kỳ, sản lượng, giá và tính tiền của luồng lập, loại chính bảng đang sửa và bảng `Cancelled` khỏi kiểm tra chồng lấn. Kết quả tính chỉ điền biểu mẫu. E22 giữ nguyên dữ liệu đã lưu, version và audit. Sau khi tải thành công, client gửi `reloadSource: true` ở E8 nếu tiếp tục lưu. [SYS-US-01b §1.2 bước 1–5, A2/A4.1/EC.1](../../../analysis/payment-management/v2/sys-us-01-v2.md) · [Sequence sửa Draft](diagrams/seq-us-01-update-v2.svg)

**E8 – Lưu thay đổi.** Client gửi `period` đang chọn và `note` (chuỗi hoặc `null`). `reloadSource` mặc định `false`. Khi kỳ khác kỳ đã lưu hoặc `reloadSource` là `true`, server kiểm tra lại nguồn hiện tại và tính lại tiền theo kỳ đang chọn. Khi kỳ giữ nguyên và `reloadSource` là `false`, chỉ cập nhật ghi chú. Server kiểm tra quyền, `Draft` và `expectedVersion` trước khi ghi có điều kiện. Hợp đồng, khách hàng, sản lượng, đơn giá và các giá trị tiền chỉ đọc trên biểu mẫu. Khi đổi kỳ, cập nhật kỳ và ràng buộc giữ chỗ cùng dòng, nguồn, tổng và audit trước/sau trong cùng giao dịch. Lưu thành công giữ ID, giữ `Draft` và tăng version. Xung đột version hoặc kỳ trả `409`, client tải lại E6. [SYS-US-01b §1.2 bước 5–8, A6/A7/E7.1; 02 §3; 03 mục US-PAY-01]

**E23 – Xác minh lần cập nhật.** Client cấp UUID `operationId` trước khi gửi E8 và giữ lại nếu mất phản hồi. Đề xuất lưu mã này cùng bản chụp sau ghi của audit `update` trong cùng giao dịch, có ràng buộc duy nhất trong phạm vi bảng. Mã của một lần cập nhật đã được ghi nhận dùng để tra qua E23. Yêu cầu E8 dùng lại mã đó trả `409 OPERATION_ID_CONFLICT` và dẫn sang E23. Khi E8 trả `503 RESULT_UNKNOWN`, hoặc mất phản hồi, client dùng E23 để tra theo cặp ID bảng và `operationId`, kiểm tra người đã gửi yêu cầu và phân công hiện tại. Dùng ba giá trị `outcome` như E7. `COMMITTED` kèm bản chụp bảng và version của đúng lần cập nhật. Chỉ khi xác nhận chưa commit mới quay lại lưu. Version hiện tại hoặc truy vấn rỗng chưa đủ làm bằng chứng. 05 §9–12 cần bổ sung chi tiết về giữ chỗ khi đổi kỳ và dữ liệu xác minh. [SYS-US-01b §1.2 E7.2; 03 mục US-PAY-01]

### 3.2. Trình duyệt và gửi lại thông báo

**E9 – Trình duyệt.** Kiểm tra `Draft`, phân công, hợp đồng còn Active, bảng giá đã dùng còn Active, bản ghi sản lượng còn đối soát và không thay đổi. Tổng bằng 0 hợp lệ nếu đạt điều kiện còn lại. Thiếu dòng dịch vụ trả `400 REQUIRED_SERVICE_MISSING` cùng `details.missingServices` gồm mã và tên. Khi bảng đã `PendingApproval` lúc đọc, trả `409 DUPLICATE_SUBMIT`. Khi ghi thua một thao tác đồng thời, trả `409 CONCURRENT_MODIFICATION`. Bảng `Rejected` phải mở lại bằng E16. [SYS-US-02 §1.1, bước 2–9, E5–E9.1](../../../analysis/payment-management/v2/sys-us-02-v2.md) · [Sequence trình duyệt](diagrams/seq-us-02-1-v2.puml)

Thao tác thành công tăng `version` và `submissionNo`, ghi audit và gọi `PrepareSubmission` để lưu vai trò, nội dung và người nhận. Nếu danh sách rỗng, `recipients_resolved_at = NULL`. Sau commit, gửi thông báo trình duyệt. Vai trò lưu theo phương án v2 là `GDKD` từ 500.000.000 đồng gồm GTGT và `KTT` dưới ngưỡng. Điểm đúng ngưỡng **Blocked by OQ-02** theo 03/05. Cách so dấu phiên bản nguồn phụ thuộc `OQ-D-03`. [03 US-PAY-02; 05 §3.5, §7, §12]

**E15 – Gửi lại.** Lấy `submissionNo` hiện tại từ bảng `PendingApproval`. Với lần trình chưa có danh sách, `GetSubmissionNotificationPlan` trả vai trò đã lưu để tra danh bạ, rồi `EnsureRecipients` lưu danh sách một lần nếu tìm thấy. Nếu đã có danh sách, chỉ gửi người chưa `Sent`. Kết quả chưa có người nhận, đã gửi đủ và gửi lỗi đều là `200` với `notificationStatus` tương ứng. Giữ nguyên trạng thái bảng, `version`, số lần trình và audit trình duyệt. Khi lần trình đã đổi hoặc bảng rời `PendingApproval` trước lúc xử lý gửi lại, yêu cầu đọc lại bảng bằng E6. Khóa gửi `(sheetId, submissionNo, recipientId)` giữ nguyên qua các lần thử. `INotifier` trả thành công cho khóa đã gửi và không tạo thông báo thứ hai. [SYS-US-02b §1.2 A3/A3.1/A4/E2; 05 §3.5, §12] · [Sequence gửi lại](diagrams/seq-us-02-2-v2.puml)

### 3.3. Duyệt, từ chối, mở lại và hủy

**E10, E11 – Duyệt và từ chối.** Cả hai yêu cầu `PendingApproval`, đúng vai trò theo tổng đã lưu và người thao tác khác `createdBy`. E10 kiểm tra lại nguồn. E11 yêu cầu `reason` có nội dung sau khi cắt khoảng trắng và tối đa 500 từ. Lưu lý do tại `rejectionReason`. Ghi trạng thái và audit rồi gửi thông báo kết quả cho người tạo. `notificationStatus` của kết quả là `Sent` hoặc `Failed`. SYS-US-02b dành cho thông báo trình duyệt. Điểm biên thẩm quyền theo `OQ-02`, tổng gồm GTGT theo `OQ-US03-03`. [SYS-US-03 §1.1, bước 2–10, A01/A02, E03–E11; PAY-05..08](../../../analysis/payment-management/v2/sys-us-03-v2.md) · [Sequence duyệt và từ chối](diagrams/seq-us-03-1-v2.puml)

**E16 – Mở lại.** NVKD phụ trách bấm **Chỉnh sửa** trên `Rejected`. Server cập nhật có điều kiện, giữ `rejectionReason`, tăng version và ghi audit. Sau đó dùng E8 để sửa Draft và E9 để trình lại. Đây là luồng System Spec v2 theo `OQ-04`, `OQ-US03-07`. [SYS-US-03b §1.2, bước 1–7, E03–E05; PAY-08] · [Sequence mở lại](diagrams/seq-us-03-2-v2.puml)

**E13 – Hủy Draft.** NVKD phụ trách gửi `reason` có nội dung. Chỉ `Draft` được hủy. Với `Rejected`, dùng E16 trước. Cùng giao dịch, ghi `Cancelled`, lưu lý do, tăng version, giải phóng chỗ giữ kỳ theo phương án dữ liệu được duyệt và ghi audit. Bảng đã hủy được giữ để tra cứu. NVKD có thể lập bảng mới cùng kỳ theo xác nhận nhóm ghi ở P-39. [SYS-US-05 P1–P4, S1–S5, AF1/AF2, A2–A7.2](../../../analysis/payment-management/v2/sys-us-05-v2.md) · [Sequence hủy](diagrams/seq-us-05-v2.puml)

### 3.4. Hồ sơ điều chỉnh

**[GIẢ ĐỊNH – Cần xác nhận]** E12, E17–E19 và E21 dùng hồ sơ riêng theo SYS-US-04/04b. Phương án này **Blocked by OQ-03** theo 03/05. Hình thức xác nhận hai bên phụ thuộc `OQ-US04-01`. Nguồn thuế suất và làm tròn phụ thuộc `OQ-US03-03`. Các thao tác trên hồ sơ giữ nguyên trạng thái và số liệu gốc của bảng. [SYS-US-04 §1.1–1.2](../../../analysis/payment-management/v2/sys-us-04-v2.md) · [05 §11](05-data-design-v2.md#11-điều-chỉnh-bảng-approved-us-pay-04--pay-05--blocked-by-oq-03)

**E12 – Lập.** Multipart có hai part bắt buộc. `payload` là JSON `{ minutes: { number, date, partyAConfirmed, partyBConfirmed }, changes }`. `file` là tệp biên bản. Từng mục `changes` có `changeType` (`Modify`, `Add`, `Remove`), `serviceCode` và `reason` có nội dung. `Add` cần `quantity` và `unitPrice`, dịch vụ chưa có. `Modify` cần ít nhất một trong hai trường, dịch vụ có trong số liệu hiệu lực. `Remove` chỉ gửi định danh và lý do của dòng hiện có. Kiểm tra ít nhất một thay đổi, mỗi dịch vụ một thay đổi, và số lượng/đơn giá được gửi không âm. Server tính số liệu đề xuất và số liệu trước/sau, dùng thuế suất gốc. Hợp đồng, kỳ và thuế suất giữ theo bảng gốc.

Khóa dòng bảng `Approved`, kiểm tra tối đa một hồ sơ `Pending`, rồi lưu hồ sơ, tham chiếu tệp, thay đổi và audit cùng giao dịch dữ liệu. Tệp phải lưu thành công trước khi commit metadata. Nếu chắc chắn rollback thì dọn tệp tạm. Nếu commit chưa rõ thì xác minh trước khi dọn. Khi có hồ sơ `Pending` khác trả `409 ADJUSTMENT_ALREADY_PENDING`. [SYS-US-04 bước 3–7, 4a/5a/7a/7b; 05 §3.6–3.7, §12] · [Sequence lập hồ sơ](diagrams/seq-us-04-1-v2.puml)

**E21, E17 – Đọc.** E21 trả `items: [{ id, adjustmentNo, status, version, createdAt }]` trong phạm vi một bảng, cho phép mở hồ sơ và đối chiếu khi chưa rõ kết quả lập. E17 kiểm tra hồ sơ thuộc bảng, trả thông tin bảng gốc, hồ sơ và tổng hiệu lực hiện tại. Tệp biên bản đọc qua URL có thời hạn do server cấp sau kiểm tra quyền ở E17. `minutes.downloadUrl` là trường phản hồi, ánh xạ từ tệp đã lưu. Hai route đọc phục vụ các bước xem biên bản và xác minh, quyền xem theo phạm vi lập/xử lý đã nêu trong bảng endpoint. [SYS-US-04b bước 1–3; sequence US-04-1 nhánh kết quả lưu chưa xác định; 05 §3.6, §12]

**E18, E19 – Xử lý.** Chỉ `GDKD` khác người lập hồ sơ được xử lý hồ sơ `Pending` thuộc bảng `Approved`. Ngưỡng duyệt bảng không áp dụng cho hồ sơ. `expectedVersion` là version hồ sơ. E19 yêu cầu lý do có nội dung. Khi E18 commit, trả tổng hiệu lực đã áp dụng hồ sơ đã duyệt theo `adjustment_no` tăng dần. E19 giữ tổng hiệu lực. Cả hai ghi audit trong cùng giao dịch. Nếu ghi chưa rõ kết quả, đọc lại hồ sơ qua E17. [SYS-US-04b bước 2–6, R/5a; 05 §11–12] · [Sequence xử lý hồ sơ](diagrams/seq-us-04-2-v2.puml)

## 4. HTTP và mã lỗi

Các endpoint dùng `401 UNAUTHENTICATED`, `403 FORBIDDEN`, `404 NOT_FOUND` khi phù hợp. `400 INVALID_INPUT` dành cho request thiếu/sai kiểu, gồm `expectedVersion` không hợp lệ. Lỗi kỹ thuật đọc nguồn/bản ghi mặc định trả `503 SOURCE_UNAVAILABLE`. E10/E11 có ánh xạ đọc riêng như bảng dưới. `500 TECHNICAL_ERROR` dùng cho lỗi xử lý tính toán đã xác định, có thể trả `details.failedStep`. Cách mã hóa dưới đây giữ mã đã xuất hiện trong 03/sequence và bổ sung mã cho các nhánh chưa được đặt tên.

| Endpoint | Lỗi nghiệp vụ và xung đột | Lỗi ghi và phục hồi |
|---|---|---|
| E2, E20, E5 | `400 INVALID_PERIOD`, `400 NEGATIVE_TOTAL`, `409 CONTRACT_NOT_ACTIVE`, `409 PERIOD_OCCUPIED`, `409 QUANTITY_INVALID`, `409 PRICE_MISSING` (thiếu đơn giá), `409 PRICE_NOT_SUITABLE` (thiếu hoặc có nhiều bảng giá Active). E5 thêm `409 OPERATION_ID_CONFLICT`. | E5 dùng `500 PERSISTENCE_ERROR` hoặc `503 RESULT_UNKNOWN` với `details.operationId`. Xác minh qua E7. |
| E6, E7, E23, E21, E17 | Áp dụng lỗi quyền/đọc ở trên. E7/E23 trả `200 { outcome: "UNKNOWN" }` nếu đã kiểm tra quyền nhưng chưa xác minh được kết quả. | Chỉ đọc. |
| E22 | `409 INVALID_STATE` nếu bảng không còn Draft. Áp dụng lỗi kỳ/nguồn/tính như E20 trong phạm vi bảng đang sửa. | Chỉ đọc và tính. |
| E8 | `409 INVALID_STATE`, `409 CONCURRENT_MODIFICATION`, `409 PERIOD_OCCUPIED` (kỳ mới bị chiếm) hoặc `409 OPERATION_ID_CONFLICT`. Khi đổi kỳ hoặc tải lại nguồn, áp dụng lỗi kỳ/nguồn/tính như E22. | `500 PERSISTENCE_ERROR` khi đã xác định chưa lưu. `503 RESULT_UNKNOWN` kèm `details.operationId` khi chưa rõ kết quả. Đọc E6 sau xung đột kỳ/version, dùng E23 khi cần xác minh. |
| E9 | `400 NEGATIVE_TOTAL`, `400 REQUIRED_SERVICE_MISSING`, `409 INVALID_STATE`, `409 DUPLICATE_SUBMIT`, `409 SOURCE_NOT_VALID`, `409 CONCURRENT_MODIFICATION`. | `500 PERSISTENCE_ERROR`, `503 RESULT_UNKNOWN`. Đọc E6. |
| E15 | `409 INVALID_STATE` hoặc `409 CONCURRENT_MODIFICATION` nếu lần trình thay đổi trong khi xử lý. `200` vẫn dùng cho các kết quả giao nhận ở §3.2. | `500 PERSISTENCE_ERROR` nếu ghi kế hoạch hoặc kết quả gửi thất bại. Đọc lại E6, chỉ gửi lại khi bảng còn `PendingApproval` trên lần trình cần gửi. |
| E10, E11 | `409 INVALID_STATE`, `409 CONCURRENT_MODIFICATION`, `403 APPROVER_NOT_AUTHORIZED`, `403 SELF_APPROVAL_FORBIDDEN`. Lỗi đọc bảng trả `503 READ_ERROR`. E10 trả `409 SOURCE_NOT_VALID` khi bước kiểm tra lại nguồn không đạt hoặc đọc nguồn lỗi, theo sequence US-03. E11 thêm `400 REASON_REQUIRED`, `400 REASON_TOO_LONG`. | `500 PERSISTENCE_ERROR`, `503 RESULT_UNKNOWN`. Đọc E6. |
| E16 | `409 INVALID_STATE`, `409 CONCURRENT_MODIFICATION`. | `500 PERSISTENCE_ERROR` khi xác định ghi thất bại. Nếu commit chưa rõ, đề xuất dùng `503 RESULT_UNKNOWN` theo quy ước chung của 02 §3. Đọc E6. |
| E12, E18, E19 | `409 INVALID_STATE`, `409 CONCURRENT_MODIFICATION`. E12 thêm `400 INVALID_MINUTES`, `400 INVALID_ADJUSTMENT_CHANGES`, `409 ADJUSTMENT_ALREADY_PENDING`. E19 thêm `400 REASON_REQUIRED`. Hồ sơ không thuộc bảng trả `404 NOT_FOUND`. | `500 PERSISTENCE_ERROR`, `503 RESULT_UNKNOWN`. Đọc E21 khi chưa biết ID, hoặc E17 khi đã biết. |
| E13 | `400 REASON_REQUIRED`, `409 INVALID_STATE`, `409 CONCURRENT_MODIFICATION`. | `500 PERSISTENCE_ERROR`, `503 RESULT_UNKNOWN`. Đọc E6. |

## 5. Ví dụ request và response

**E5 – Lưu Draft**, với `operationId` nhận từ E20:

```json
{
  "contractId": 101,
  "period": { "type": "Month", "start": "2026-11-01", "end": "2026-11-30" },
  "note": "Đã đối chiếu kỳ tháng 11",
  "operationId": "16fd45b9-bcb0-4bf4-a768-9ec55f4578de"
}
```

**E7 – Chưa đủ bằng chứng xác minh lần lưu**, HTTP `200`:

```json
{ "outcome": "UNKNOWN" }
```

**E5 – Chưa xác định kết quả commit**, HTTP `503`:

```json
{
  "code": "RESULT_UNKNOWN",
  "message": "Chưa xác định được kết quả lưu. Hãy kiểm tra lần lưu trước khi thao tác tiếp.",
  "details": { "operationId": "16fd45b9-bcb0-4bf4-a768-9ec55f4578de" }
}
```

**E9 – Đã trình duyệt, chưa có người nhận**, HTTP `200` theo A8:

```json
{
  "id": "f4bcd1e6-f990-469a-b029-85f2a7a89fe9",
  "status": "PendingApproval",
  "version": 4,
  "submissionNo": 1,
  "requiredRole": "KTT",
  "notificationStatus": "NoRecipients"
}
```

**E11 – Từ chối**, từ version trả về trên E6:

```json
{ "expectedVersion": 4, "reason": "Cần đối soát lại sản lượng dịch vụ SV01." }
```

**E12 – Part `payload`** của request có tệp biên bản trong part `file`:

```json
{
  "minutes": {
    "number": "BB-2026-07",
    "date": "2026-11-11",
    "partyAConfirmed": true,
    "partyBConfirmed": true
  },
  "changes": [
    {
      "changeType": "Modify",
      "serviceCode": "SV01",
      "quantity": "950.0000",
      "reason": "Sản lượng được xác nhận lại trong biên bản."
    }
  ]
}
```

**E8 – Lưu thay đổi kỳ/ghi chú của bảng Draft**:

```json
{
  "expectedVersion": 3,
  "period": { "type": "Month", "start": "2026-12-01", "end": "2026-12-31" },
  "note": "Cập nhật kỳ theo số liệu đã đối soát",
  "reloadSource": false,
  "operationId": "4a756390-b079-4d41-a0ea-25a542557d5b"
}
```

## 6. Truy vết và kiểm chứng

| Yêu cầu | Endpoint | Tiêu chí đối chiếu với 01 §5 và System Spec v2 |
|---|---|---|
| US-PAY-01, SYS-US-01, PAY-01..03 | E2, E20, E5, E6, E7 | Chặn kỳ chồng lấn kể cả ghi đồng thời. Tính lại khi lưu. Xác minh đúng `operationId` của lần tạo khi mất phản hồi. |
| US-PAY-01, SYS-US-01b, PAY-01..03 | E6, E22, E8, E23 | Tải lại chỉ đổi biểu mẫu. Sửa ghi chú giữ kỳ và số liệu. Đổi kỳ lưu cùng ID, tính lại và ghi audit. Chặn kỳ chồng lấn với bảng khác hoặc version cũ. Xác minh đúng `operationId` của lần cập nhật khi mất phản hồi. |
| US-PAY-02/02b, PAY-04/06 | E9, E15 | Hai yêu cầu trình cùng version có tối đa một lần trình và một audit. Kiểm thử tổng bằng 0, tổng âm và thiếu dịch vụ. Gửi lại khi chưa có người nhận, gửi lỗi một phần và mất phản hồi sau khi đã gửi. |
| US-PAY-03/03b, PAY-05..08 | E6, E10, E11, E16 | Kiểm thử quyền ở hai phía ngưỡng và đúng ngưỡng theo phương án v2. Kiểm thử người lập tự xử lý, nguồn đổi, lý do trống/quá 500 từ và giữ lý do sau mở lại. |
| US-PAY-04/04b, PAY-05 | E12, E21, E17–E19 | Chỉ một hồ sơ Pending mỗi bảng. Duyệt và từ chối đồng thời chỉ một kết quả được lưu. Đối chiếu số liệu gốc và hiệu lực trước/sau, theo phương án OQ-03. |
| US-PAY-05, PAY-01 | E13, E5 | Chỉ NVKD phụ trách hủy Draft với lý do. `Cancelled` vẫn đọc được, bảng mới cùng kỳ có ID mới. |
| NFR-PAY-01, TA-SPEC §6 | Các endpoint ghi nghiệp vụ | Kiểm tra audit ai, lúc nào, thay đổi gì. Giả lập lỗi audit để kiểm tra rollback. Gửi lại giữ audit trình duyệt. |
| NFR-PAY-02, TA-SPEC §6 | E5 | Mục tiêu ≤ 3 giây từ khi server nhận lưu đến khi trả kết quả đã lưu, với dưới 200 dòng sau gộp theo SYS-US-01. Chưa đo. |

## Thay đổi so với v1

| Phần | Thay đổi v2 | Căn cứ |
|---|---|---|
| Lập, sửa và xác minh | Mở lập từ hợp đồng đang xem, hệ thống tự lấy giá. Sửa kỳ/ghi chú trên Draft có thao tác tải thử và xác minh riêng theo `operationId` của lần cập nhật. | SYS-US-01 §1.1, SYS-US-01b §1.2; DD-17 cho lập mới; P-46 cho sửa. |
| Trình và xử lý bảng | Thêm gửi lại theo lần trình và mở lại Rejected. Giữ route trình, duyệt, từ chối và hủy từ sequence. | SYS-US-02/02b, SYS-US-03/03b, SYS-US-05; 03 US-PAY-02. |
| Điều chỉnh | Hợp đồng đề xuất cho hồ sơ riêng với tệp biên bản, xử lý của GĐKD và số liệu hiệu lực. | SYS-US-04/04b; 05 §11; OQ-03. |
