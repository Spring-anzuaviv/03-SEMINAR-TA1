# 05 – Thiết kế dữ liệu dùng chung cho module Bảng thanh toán (v2)

Sơ đồ: [erd-v2.puml](diagrams/erd-v2.puml) ([SVG](diagrams/erd-v2.svg)). Đây là **ERD (mô hình
dữ liệu)**, không phải UML class diagram. Một mô hình dữ liệu dùng chung cho cả 5 US: mọi
sequence v2 đọc/ghi cùng các bảng dưới đây.

## 1. Nguồn và phạm vi

- Tên bảng/cột lấy theo tên dùng tạm trong 8 sequence v2, ví dụ `submissionNo`, `rejectReason`,
  `cancelReason`, `operationId`, `sourceRecordIds`, `Pending/Approved/Declined`. Các tên này
  được gom ở §14.4. Field API trong `04-api-contract-v2.md` được ánh xạ sang cột ở §14.5.

**Phạm vi** [ĐẶC TẢ] [TA-SPEC §1; TA-PDF tr.1]: chỉ dữ liệu của module Bảng thanh toán. Dữ liệu
hợp đồng, bảng giá, sản lượng, người dùng/vai trò và phân công hợp đồng thuộc module khác. Module
này chỉ đọc chúng qua `IContractReader`, `IPriceReader`, `IQuantityReader`, `IUserDirectory`
(tên theo seq-us-01-v2, seq-us-02-1-v2, seq-us-02-2-v2). Thiết kế chỉ lưu khóa tham chiếu và bản sao giá trị tại thời điểm
tính, **không có bảng hay CRUD** cho các module đó.

## 2. Danh sách entity

| #   | Bảng                         | Class / tên dùng tạm (seq v2)                                                 | Mục đích                                                                                                              | Use case v2                       | Yêu cầu                      |
| --- | ---------------------------- | ----------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------- | ---------------------------- |
| 1   | `payment_sheets`             | `PaymentSheet` (`sheet`)                                                      | Bảng thanh toán: kỳ, trạng thái, tiền, người thao tác, lý do, version                                                 | 01, 02, 02b, 03, 03b, 04, 04b, 05 | US-PAY-01..05; PAY-01, 04–08 |
| 2   | `payment_lines`              | `PaymentLine` (`lines`)                                                       | Một dòng cho mỗi dịch vụ, chứa sản lượng gộp, đơn giá và thành tiền tại lúc lưu                                       | 01, 02, 03, 04                    | PAY-02, PAY-03, PAY-04       |
| 3   | `payment_line_sources`       | `sourceRecordIds`                                                             | Các bản ghi sản lượng nguồn tạo nên từng dòng, dùng để kiểm tra lại nguồn khi trình hoặc duyệt                        | 01, 02, 03                        | PAY-02, PAY-03               |
| 4   | `payment_period_claims`      | `FindOverlap` / `includeCreating`                                             | Giữ chỗ từng tháng của kỳ để CSDL chặn kỳ trùng hoặc chồng lấn, kể cả khi hai yêu cầu lập chạy đồng thời              | 01, 05                            | PAY-01                       |
| 5   | `payment_submissions`        | `INotificationRepository.PrepareSubmission` / `GetSubmissionNotificationPlan` | Một bản ghi cho mỗi lần trình: vai trò duyệt, nội dung thông báo, người/lúc trình, thời điểm lập danh sách người nhận, kết quả duyệt/từ chối của lần trình đó | 02, 02b, 03                       | §4.2, PAY-06                 |
| 6   | `payment_notifications`      | `INotificationRepository`, `notificationStatus`                               | Thông báo trong hệ thống: trình duyệt cho người duyệt, kết quả duyệt/từ chối cho người lập; theo dõi gửi và gửi lại   | 02, 02b, 03                       | §4.2, §4.3                   |
| 7   | `payment_adjustments`        | `IAdjustmentRepository` (hồ sơ)                                               | Hồ sơ điều chỉnh bảng Approved, gồm biên bản, số liệu đề xuất và trạng thái hồ sơ                                     | 04, 04b                           | US-PAY-04 ↔ PAY-05 (OQ-03)   |
| 8   | `payment_adjustment_changes` | `changes`                                                                     | Từng thay đổi trong hồ sơ, gồm giá trị trước/sau và lý do                                                             | 04, 04b                           | US-PAY-04 (OQ-03)            |
| 9   | `audit_entries`              | `IAuditLog.Append`                                                            | Nhật ký chỉ thêm cho mọi thay đổi trạng thái và mọi điều chỉnh                                                        | tất cả                            | NFR-PAY-01                   |

## 3. Chi tiết từng bảng

Quy ước kiểu (PostgreSQL / SQL Server): `UUID` = `uuid` / `uniqueidentifier`; `TIMESTAMPTZ` =
`timestamptz` / `datetimeoffset`; `TEXT` = `text` / `nvarchar(max)`; `JSON` = `jsonb` /
`nvarchar(max)` có `ISJSON`. Mã người dùng lưu `VARCHAR(50)` vì module người dùng chưa có trong
AS-IS. Cột `*_by` lưu mã người dùng, không có FK chéo module.

### 3.1. `payment_sheets`

| Cột                            | Kiểu                     | Null  | Khóa / ràng buộc                                  | Mô tả                                                                                                                                                                                                        | Nguồn / nhãn                                                                               | OQ                           |
| ------------------------------ | ------------------------ | ----- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ---------------------------- |
| `id`                           | UUID                     | Không | PK                                                | Định danh bảng                                                                                                                                                                                               | [ĐỀ XUẤT KỸ THUẬT]                                                                         | –                            |
| `code`                         | VARCHAR(30)              | Không | UNIQUE `ux_sheet_code`                            | “Mã bảng” hiển thị trong thông báo trình duyệt. Định dạng do service sinh                                                                                                                                    | [ĐẶC TẢ] SYS-US-02 bước 10; định dạng: [ĐỀ XUẤT KỸ THUẬT] DD-19                            | –                            |
| `create_operation_id`          | UUID                     | Không | UNIQUE `ux_sheet_create_op`                       | `operationId` của lần lập; E7 `VerifySaveOutcome` tìm theo cột này. Lần cập nhật dùng `audit_entries.operation_id` (§3.8)                                                                                    | [ĐỀ XUẤT KỸ THUẬT] seq-us-01-v2 E15.2; 04-v2 E5/E7; DD-17                                  | –                            |
| `contract_id`                  | INT                      | Không | Tham chiếu logic module Hợp đồng                  | Hợp đồng; kiểu theo AS-IS `Contract.Id`                                                                                                                                                                      | [ĐẶC TẢ] §4.1; SYS-US-01                                                                   | –                            |
| `period_type`                  | VARCHAR(10)              | Không | CHECK ∈ (`Month`, `Quarter`)                      | Loại kỳ theo cấu hình hợp đồng                                                                                                                                                                               | [SYS v2 – OQ-01] SYS-US-01 TĐK 3                                                           | OQ-01                        |
| `period_start`                 | DATE                     | Không |                                                   | Ngày đầu kỳ. Sửa được khi Draft (SYS-US-01b)                                                                                                                                                                 | [ĐẶC TẢ] §2; SYS-US-01b                                                                    | OQ-01, OQ-D-02               |
| `period_end`                   | DATE                     | Không | CHECK `period_end >= period_start`                | Ngày cuối kỳ (tính cả ngày cuối). Sửa được khi Draft                                                                                                                                                         | [ĐẶC TẢ] §2; SYS-US-01b                                                                    | OQ-01, OQ-D-02               |
| `price_list_id`                | VARCHAR(50)              | Không | Tham chiếu logic module Bảng giá                  | Bảng giá Active do hệ thống tự lấy, NVKD không chọn. Bảng giá Active không đổi nội dung, nên mã này đủ xác định đơn giá đã dùng. Khi đổi kỳ hoặc tải lại nguồn trên Draft thì lấy lại bảng giá đang hiệu lực | [SYS v2] SYS-US-01 mô tả, bước 9; SYS-US-01b; OQ-US01-01 đã xác nhận (01-v2 §6)            | OQ-US01-01                   |
| `status`                       | VARCHAR(20)              | Không | CHECK ∈ 5 giá trị §3                              | `Draft`, `PendingApproval`, `Approved`, `Rejected`, `Cancelled`                                                                                                                                              | [ĐẶC TẢ] §3                                                                                | –                            |
| `subtotal_amount`              | DECIMAL(19,4)            | Không |                                                   | Tạm tính = Σ `payment_lines.line_amount`                                                                                                                                                                     | [SYS v2 – OQ-US03-03] SYS-US-01 mô tả                                                      | OQ-US03-03                   |
| `tax_rate`                     | DECIMAL(5,4)             | Không | CHECK `tax_rate >= 0`                             | Thuế suất GTGT dùng khi tính; hồ sơ điều chỉnh dùng lại giá trị này                                                                                                                                          | [SYS v2 – OQ-US03-03] SYS-US-01 hậu ĐK; SYS-US-04 mô tả                                    | OQ-US03-03 (nguồn thuế suất) |
| `tax_rate_source_ref`          | VARCHAR(100)             | Có    |                                                   | Tham chiếu cấu hình thuế suất của hợp đồng/kỳ đã dùng để tính                                                                                                                                                | [ĐỀ XUẤT KỸ THUẬT] 02-v2 §4 “lưu giá trị thực dùng cùng tham chiếu nguồn trên Draft”       | OQ-US03-03                   |
| `tax_amount`                   | DECIMAL(19,4)            | Không |                                                   | Tiền thuế                                                                                                                                                                                                    | [SYS v2 – OQ-US03-03]                                                                      | OQ-US03-03                   |
| `total_amount`                 | DECIMAL(19,4)            | Không | CHECK `total_amount >= 0` `ck_sheet_total_nonneg` | Tổng tiền đã gồm thuế, dùng để chọn người duyệt                                                                                                                                                              | [SYS v2] SYS-US-01 bước 11, 14 (tổng âm không cho lưu); SYS-US-02 bước 7                   | OQ-US03-03                   |
| `note`                         | TEXT                     | Có    |                                                   | Ghi chú. Cùng với kỳ là hai trường NVKD sửa được trên Draft                                                                                                                                                  | [QUYẾT ĐỊNH ĐÃ XÁC NHẬN] người dùng 12/11/2026, P-42; SYS-US-01b “Thông tin được thay đổi” | –                            |
| `calculated_at`                | TIMESTAMPTZ              | Không |                                                   | Thời điểm tính số liệu; đặt lại khi lập, đổi kỳ hoặc tải lại nguồn                                                                                                                                           | [ĐẶC TẢ] PAY-03; DD-04; SYS-US-01b                                                         | –                            |
| `created_by`                   | VARCHAR(50)              | Không | Không đổi sau khi tạo                             | **Người lập** = người tạo bảng Draft. Dùng cho PAY-07 và người nhận thông báo kết quả                                                                                                                        | [ĐẶC TẢ] PAY-07; [SYS v2 – OQ-US03-01] SYS-US-03 TĐK 3                                     | OQ-US03-01                   |
| `created_at`                   | TIMESTAMPTZ              | Không |                                                   |                                                                                                                                                                                                              | [ĐỀ XUẤT KỸ THUẬT]                                                                         | –                            |
| `updated_by`, `updated_at`     | VARCHAR(50), TIMESTAMPTZ | Có    |                                                   | Lần sửa Draft gần nhất. NVKD phụ trách có thể không phải người lập                                                                                                                                           | [SYS v2 – OQ-US01-03] SYS-US-01 Actor                                                      | OQ-US01-03                   |
| `submission_no`                | INT                      | Không | DEFAULT 0; CHECK `>= 0`                           | Số của lần trình hiện tại; tăng 1 mỗi lần trình thành công. Dữ liệu từng lần trình nằm ở `payment_submissions` (§3.5)                                                                                        | [SYS v2] SYS-US-02 hậu ĐK, bước 9; seq-us-02-1-v2 bước 9 `Transition`                      | –                            |
| `cancel_reason`                | TEXT                     | Có    |                                                   | Lý do hủy (bắt buộc khi hủy)                                                                                                                                                                                 | [SYS v2 – OQ-US05-03] SYS-US-05 S4; DD-12                                                  | OQ-US05-03                   |
| `cancelled_by`, `cancelled_at` | VARCHAR(50), TIMESTAMPTZ | Có    |                                                   |                                                                                                                                                                                                              | [ĐỀ XUẤT KỸ THUẬT]                                                                         | –                            |
| `version`                      | INT                      | Không | DEFAULT 1; tăng mỗi lần ghi                       | Khóa lạc quan (`expectedVersion`)                                                                                                                                                                            | [SYS v2] SYS-US-02 bước 1, 9, E9; DD-02, DD-08                                             | –                            |

Ràng buộc nhất quán theo trạng thái [ĐỀ XUẤT KỸ THUẬT]:

- `ck_sheet_cancel`: `status <> 'Cancelled' OR (cancel_reason IS NOT NULL AND cancelled_by IS NOT NULL)`.
- `ck_sheet_submitted`: `status NOT IN ('PendingApproval','Approved','Rejected') OR submission_no >= 1`.

Bảng không còn cột `decided_by`, `decided_at`, `rejection_reason` (P-51, DD-20). Kết quả duyệt/từ
chối lưu theo lần trình ở `payment_submissions` (§3.5). Bảng `Approved`/`Rejected` luôn có lần trình
hiện tại mang kết quả tương ứng; service bảo đảm trong cùng giao dịch (§12), CSDL không ép được
vì là ràng buộc giữa hai bảng.

Không có cột ngưỡng 500 triệu. Không đặt CHECK `payment_submissions.required_role` theo `total_amount`: thẩm quyền
duyệt là quy tắc nghiệp vụ ở service (OQ-02).

### 3.2. `payment_lines`

| Cột                | Kiểu          | Null  | Khóa / ràng buộc                                              | Mô tả                                                                | Nguồn / nhãn                                                                                      | OQ         |
| ------------------ | ------------- | ----- | ------------------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ---------- |
| `id`               | UUID          | Không | PK                                                            |                                                                      |                                                                                                   | –          |
| `payment_sheet_id` | UUID          | Không | FK → `payment_sheets.id` ON DELETE RESTRICT                   | Thuộc bảng                                                           | [ĐẶC TẢ] §2                                                                                       | –          |
| `line_no`          | INT           | Không | UNIQUE (`payment_sheet_id`, `line_no`)                        | Thứ tự hiển thị                                                      | [ĐỀ XUẤT KỸ THUẬT]                                                                                | –          |
| `service_code`     | VARCHAR(50)   | Không | UNIQUE (`payment_sheet_id`, `service_code`) `ux_line_service` | Dịch vụ. Mỗi dịch vụ một dòng vì sản lượng được gộp                  | [SYS v2 – OQ-US01-04] SYS-US-01 hậu ĐK “sản lượng gộp”; SYS-US-04 “dòng thêm không trùng dịch vụ” | OQ-US01-04 |
| `service_name`     | VARCHAR(200)  | Có    |                                                               | Bản sao tên dịch vụ để hiển thị                                      | [ĐỀ XUẤT KỸ THUẬT]                                                                                | –          |
| `quantity`         | DECIMAL(19,4) | Không |                                                               | Sản lượng gộp từ các bản ghi đã đối soát                             | [ĐẶC TẢ] PAY-02; SYS-US-01                                                                        | OQ-US01-04 |
| `unit_price`       | DECIMAL(19,4) | Không |                                                               | Đơn giá tại lúc lưu                                                  | [ĐẶC TẢ] PAY-03                                                                                   | –          |
| `price_item_ref`   | VARCHAR(100)  | Có    |                                                               | Mã mục giá trong bảng giá đã dùng                                    | [ĐỀ XUẤT KỸ THUẬT] DD-04                                                                          | –          |
| `line_amount`      | DECIMAL(19,4) | Không |                                                               | Thành tiền = `quantity × unit_price`, làm tròn theo quy tắc lập bảng | [ĐẶC TẢ] PAY-03; làm tròn: [SYS v2 – OQ-US03-03]                                                  | OQ-US03-03 |

Mỗi dịch vụ khai báo trong hợp đồng có một dòng, kể cả khi sản lượng hoặc đơn giá bằng 0 (thành
tiền 0) [OQ-US01-04 đã xác nhận, 01-v2 §6]. Vì vậy khi trình duyệt, bảng có 1..\* dòng
(SYS-US-02 bước 7), nhưng CSDL không ép điều này.

### 3.3. `payment_line_sources`

| Cột                  | Kiểu          | Null  | Khóa / ràng buộc                                                                        | Mô tả                                                                                          | Nguồn / nhãn                                                                | OQ      |
| -------------------- | ------------- | ----- | --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- | ------- |
| `payment_line_id`    | UUID          | Không | PK (`payment_line_id`, `quantity_record_id`); FK → `payment_lines.id` ON DELETE CASCADE | Dòng được gộp                                                                                  | [SYS v2] SYS-US-01 hậu ĐK “danh sách bản ghi sản lượng nguồn của từng dòng” | –       |
| `quantity_record_id` | VARCHAR(100)  | Không | Tham chiếu logic module Sản lượng                                                       | Bản ghi sản lượng nguồn (`sourceRecordIds`)                                                    | seq-us-02-1-v2 bước 6 `GetRecords(sheet.sourceRecordIds)`                   | –       |
| `quantity`           | DECIMAL(19,4) | Không |                                                                                         | Sản lượng của bản ghi tại lúc lưu                                                              | [ĐẶC TẢ] PAY-03; DD-14                                                      | –       |
| `source_version`     | VARCHAR(100)  | Có    |                                                                                         | Dấu phiên bản hoặc thời điểm cập nhật của bản ghi nguồn, dùng để biết bản ghi “không thay đổi” | [ĐỀ XUẤT KỸ THUẬT] SYS-US-02 bước 6, SYS-US-03 bước 7; DD-14                | OQ-D-03 |

Khi đổi kỳ hoặc tải lại nguồn (SYS-US-01b), xóa toàn bộ dòng và nguồn cũ rồi thêm dòng và nguồn
mới trong một giao dịch. Việc xóa chỉ được phép khi bảng còn ở Draft (§9). Audit giữ ảnh chụp
trước/sau (§10). Dòng của dịch vụ không có bản ghi sản lượng trong kỳ có 0 dòng nguồn.

### 3.4. `payment_period_claims` – chống trùng/chồng lấn kỳ (DD-13)

| Cột                | Kiểu | Null  | Khóa / ràng buộc                  | Mô tả                                      | Nguồn / nhãn             | OQ      |
| ------------------ | ---- | ----- | --------------------------------- | ------------------------------------------ | ------------------------ | ------- |
| `contract_id`      | INT  | Không | PK (`contract_id`, `month_start`) | Hợp đồng                                   | [ĐẶC TẢ] PAY-01          | OQ-01   |
| `month_start`      | DATE | Không | CHECK là ngày 1 của tháng         | Tháng thuộc kỳ của bảng. Kỳ quý tạo 3 dòng | [ĐỀ XUẤT KỸ THUẬT] DD-13 | OQ-D-02 |
| `payment_sheet_id` | UUID | Không | FK → `payment_sheets.id`          | Bảng đang giữ chỗ tháng                    |                          | –       |

Chi tiết cách hoạt động: §8.

### 3.5. `payment_submissions` và `payment_notifications` – lần trình và thông báo (DD-15)

seq-us-02-1-v2 bước 9 gọi `PrepareSubmission(sheetId, submissionNo, requiredRole, recipients,
nội dung)` trong giao dịch trình duyệt để “lưu vai trò theo lần trình; danh sách có thể rỗng ở A8”.
seq-us-02-2-v2 bước 3 đọc lại bằng `GetSubmissionNotificationPlan` và lập danh sách một lần bằng
`EnsureRecipients`. Vì vậy dữ liệu tách thành hai bảng: một dòng cho mỗi lần trình và một dòng
cho mỗi người nhận.

**`payment_submissions`**

| Cột                            | Kiểu                     | Null  | Khóa / ràng buộc                                                   | Mô tả                                                                                                        | Nguồn / nhãn                                                                                               | OQ                            |
| ------------------------------ | ------------------------ | ----- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- | ----------------------------- |
| `payment_sheet_id`             | UUID                     | Không | PK (`payment_sheet_id`, `submission_no`); FK → `payment_sheets.id` | Bảng                                                                                                         |                                                                                                            | –                             |
| `submission_no`                | INT                      | Không | CHECK `>= 1`                                                       | Số lần trình; khớp `payment_sheets.submission_no` lúc trình                                                  | [SYS v2] SYS-US-02 bước 9                                                                                  | –                             |
| `required_role`                | VARCHAR(10)              | Không | CHECK ∈ (`KTT`, `GDKD`)                                            | Vai trò duyệt xác định tại bước 8 từ tổng tiền đã lưu. SYS-US-02b tìm người nhận theo vai trò này            | [SYS v2 – OQ-02] SYS-US-02 bước 8; SYS-US-02b bước 3; DD-19                                                | OQ-02, OQ-US03-02, OQ-US03-03 |
| `content_json`                 | JSON                     | Không |                                                                    | Nội dung thông báo của lần trình: mã bảng, hợp đồng, kỳ, tổng tiền                                           | [SYS v2] SYS-US-02 bước 10, hậu ĐK                                                                         | –                             |
| `submitted_by`, `submitted_at` | VARCHAR(50), TIMESTAMPTZ | Không |                                                                    | NVKD và thời điểm trình (người trình có thể khác người lập)                                                  | [ĐẶC TẢ] §4.2; [SYS v2 – OQ-US02-01]                                                                       | OQ-US02-01                    |
| `recipients_resolved_at`       | TIMESTAMPTZ              | Có    |                                                                    | Thời điểm đã lập danh sách người nhận. `NULL` = lần trình chưa có người nhận (SYS-US-02 A8; SYS-US-02b A3.1) | seq-us-02-2-v2 `EnsureRecipients`: “chỉ lập danh sách khi lần trình chưa có danh sách”; [ĐỀ XUẤT KỸ THUẬT] | –                             |
| `decision`                     | VARCHAR(10)              | Có    | CHECK ∈ (`Approved`, `Rejected`)                                   | Kết quả của lần trình. `NULL` = lần trình đang chờ duyệt                                                     | [ĐẶC TẢ] §4.3; [ĐỀ XUẤT KỸ THUẬT] DD-20 (P-51)                                                             | –                             |
| `decided_by`, `decided_at`     | VARCHAR(50), TIMESTAMPTZ | Có    |                                                                    | KTT/GĐKD và thời điểm duyệt hoặc từ chối lần trình này                                                       | [ĐẶC TẢ] §4.3; SYS-US-03 hậu ĐK; DD-20                                                                     | –                             |
| `rejection_reason`             | TEXT                     | Có    |                                                                    | Lý do từ chối của lần trình, tối đa 500 từ (service kiểm tra). Giữ nguyên sau `reopen` và sau các lần trình sau | [ĐẶC TẢ] PAY-08; [SYS v2 – OQ-US03-04] SYS-US-03 TĐK 5, SYS-US-03b; DD-12, DD-20                           | OQ-US03-04                    |

Lần trình hiện tại = dòng có `submission_no` bằng `payment_sheets.submission_no`. Lịch sử các lần
trình cũ vẫn được giữ, mỗi lần kèm kết quả duyệt/từ chối của chính lần đó.

`ck_submission_decision` [ĐỀ XUẤT KỸ THUẬT]: `(decision IS NULL AND decided_by IS NULL AND decided_at IS NULL
AND rejection_reason IS NULL) OR (decision = 'Approved' AND decided_by IS NOT NULL AND decided_at IS NOT NULL
AND rejection_reason IS NULL) OR (decision = 'Rejected' AND decided_by IS NOT NULL AND decided_at IS NOT NULL
AND rejection_reason IS NOT NULL)`. Mỗi lần trình có tối đa một kết quả; kết quả đã ghi không đổi.

Lý do từ chối hiển thị trên bảng (`PaymentSheetDto.rejectionReason`) lấy từ lần trình hiện tại. Sau
`reopen`, lần trình hiện tại vẫn là lần bị từ chối nên lý do vẫn hiện để NVKD tham chiếu (SYS-US-03b).
Sau khi trình lại, lần trình mới chưa có kết quả; lý do cũ xem trong lịch sử lần trình.

**`payment_notifications`**

| Cột                | Kiểu         | Null  | Khóa / ràng buộc                                                                           | Mô tả                                                                       | Nguồn / nhãn                                                                                                                                     | OQ                     |
| ------------------ | ------------ | ----- | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------- |
| `id`               | UUID         | Không | PK                                                                                         |                                                                             |                                                                                                                                                  | –                      |
| `payment_sheet_id` | UUID         | Không | FK (`payment_sheet_id`, `submission_no`) → `payment_submissions`                           | Bảng                                                                        |                                                                                                                                                  | –                      |
| `kind`             | VARCHAR(10)  | Không | CHECK ∈ (`submit`, `approve`, `reject`)                                                    | `submit` gửi người duyệt; `approve`/`reject` gửi người lập                  | [SYS v2 – OQ-US02-02, OQ-US03-05] SYS-US-02 bước 10; SYS-US-03 bước 9                                                                            | OQ-US02-02, OQ-US03-05 |
| `submission_no`    | INT          | Không | UNIQUE (`payment_sheet_id`, `kind`, `submission_no`, `recipient_id`) `ux_notification_key` | Lần trình mà thông báo thuộc về                                             | [SYS v2] SYS-US-02 bước 10 “mỗi người chỉ nhận một thông báo cho mỗi lần trình”; seq-us-02-1/02-2-v2 khóa `(sheetId, submissionNo, recipientId)` | –                      |
| `recipient_id`     | VARCHAR(50)  | Không |                                                                                            | Người nhận, gồm mọi người giữ vai trò duyệt hoặc người lập bảng             | [SYS v2 – OQ-US03-02]                                                                                                                            | OQ-US03-02             |
| `content_json`     | JSON         | Không |                                                                                            | Nội dung lúc tạo: mã bảng, hợp đồng, kỳ, tổng tiền; thêm lý do nếu `reject` | [SYS v2] SYS-US-02 bước 10; SYS-US-03 A01 bước 9                                                                                                 | –                      |
| `status`           | VARCHAR(10)  | Không | CHECK ∈ (`Pending`, `Sent`, `Failed`)                                                      | Trạng thái gửi (`notificationStatus`); **không phải trạng thái bảng**       | seq-us-02-1/02-2-v2 `MarkNotification(key, result)` (`SENT`/`FAILED`)                                                                            | –                      |
| `attempt_count`    | INT          | Không | DEFAULT 0                                                                                  | Số lần gửi                                                                  | [ĐỀ XUẤT KỸ THUẬT]                                                                                                                               | –                      |
| `created_at`       | TIMESTAMPTZ  | Không |                                                                                            |                                                                             |                                                                                                                                                  | –                      |
| `sent_at`          | TIMESTAMPTZ  | Có    |                                                                                            | Lần gửi thành công                                                          |                                                                                                                                                  | –                      |
| `last_error`       | VARCHAR(500) | Có    |                                                                                            | Lỗi gửi gần nhất (không chứa dữ liệu bí mật)                                | [ĐỀ XUẤT KỸ THUẬT]                                                                                                                               | –                      |

Ghi chú:

- Trình duyệt (SYS-US-02 bước 9): cùng giao dịch với chuyển trạng thái và audit, thêm một dòng
  `payment_submissions` và một dòng `payment_notifications` (`Pending`) cho mỗi người nhận. Nếu có
  người nhận thì đặt `recipients_resolved_at`; nếu danh sách rỗng (A8) thì để `NULL`.
- Gửi lại khi chưa có danh sách (SYS-US-02b bước 3): `EnsureRecipients` chạy
  `UPDATE payment_submissions SET recipients_resolved_at = now() WHERE … AND recipients_resolved_at IS NULL`
  rồi thêm các dòng thông báo trong cùng giao dịch. Nếu 0 dòng bị ảnh hưởng, nghĩa là yêu cầu khác
  đã lập danh sách, thì đọc lại danh sách đó. Nhờ vậy hai lần gửi lại đồng thời không tạo hai
  danh sách. Nếu vẫn không tìm được người nhận thì không ghi gì (A3.1).
- SYS-US-02b chỉ gửi lại dòng có `status <> 'Sent'`. Nếu mọi dòng đã `Sent` thì báo “Đã gửi đủ
  thông báo” (A3). Khóa `ux_notification_key` bảo đảm người đã nhận không nhận thêm thông báo
  của cùng lần trình.
- Gửi lại thông báo không đổi `payment_sheets` và không ghi audit (SYS-US-02b hậu ĐK).
- SYS-US-03 A02 không quy định gửi lại thông báo kết quả. Dòng `approve`/`reject` có
  `Failed` chỉ để tra cứu.
- Bảng này giả định module tự lưu thông báo trong hệ thống. Nếu nhóm dùng một dịch vụ thông báo
  chung, bảng chỉ còn vai trò theo dõi gửi. Cần chốt ở `02-architecture-design-v2.md`.

### 3.6. `payment_adjustments` – hồ sơ điều chỉnh (Blocked by OQ-03)

[GIẢ ĐỊNH – Cần xác nhận] Đây là phương án “hồ sơ riêng” theo SYS-US-04/04b v2 (phương án A
của OQ-03). Bảng gốc giữ `Approved`, số liệu gốc không đổi.

| Cột                                                          | Kiểu                     | Null  | Khóa / ràng buộc                                           | Mô tả                                                                                              | Nguồn / nhãn                                       | OQ         |
| ------------------------------------------------------------ | ------------------------ | ----- | ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------- | ---------- |
| `id`                                                         | UUID                     | Không | PK                                                         |                                                                                                    |                                                    | –          |
| `payment_sheet_id`                                           | UUID                     | Không | FK → `payment_sheets.id`                                   | Bảng gốc ở `Approved`                                                                              | SYS-US-04 mô tả                                    | OQ-03      |
| `adjustment_no`                                              | INT                      | Không | UNIQUE (`payment_sheet_id`, `adjustment_no`)               | Thứ tự hồ sơ trong bảng; dùng để xếp hồ sơ đã duyệt (`ListApproved` “theo thứ tự”)                 | seq-us-04-1-v2                                     | –          |
| `status`                                                     | VARCHAR(10)              | Không | CHECK ∈ (`Pending`, `Approved`, `Declined`)                | Chờ duyệt / Đã duyệt / Bị từ chối. **Trạng thái của hồ sơ, không phải trạng thái bảng thanh toán** | SYS-US-04/04b; 03-v2                               | OQ-03      |
| `minutes_no`                                                 | VARCHAR(50)              | Không |                                                            | Số biên bản                                                                                        | SYS-US-04 TĐK 2                                    | OQ-US04-01 |
| `minutes_date`                                               | DATE                     | Không |                                                            | Ngày lập biên bản                                                                                  | SYS-US-04 TĐK 2                                    | OQ-US04-01 |
| `minutes_file_key`                                           | VARCHAR(200)             | Không |                                                            | Khóa file đính kèm trong kho file. CSDL chỉ lưu metadata                                           | SYS-US-04 TĐK 2; [ĐỀ XUẤT KỸ THUẬT]                | OQ-US04-01 |
| `minutes_file_name`                                          | VARCHAR(255)             | Không |                                                            | Tên file gốc                                                                                       | [ĐỀ XUẤT KỸ THUẬT]                                 | –          |
| `party_a_confirmed`, `party_b_confirmed`                     | BOOLEAN                  | Không | CHECK cả hai = TRUE khi lưu                                | Xác nhận của hai bên                                                                               | SYS-US-04 bước 4; hình thức xác nhận: OQ-US04-01   | OQ-US04-01 |
| `effective_total_before`                                     | DECIMAL(19,4)            | Không |                                                            | Tổng hiệu lực lúc lập hồ sơ                                                                        | SYS-US-04 bước 3; SYS-US-04b bước 5 “trước và sau” | –          |
| `proposed_subtotal`, `proposed_tax_amount`, `proposed_total` | DECIMAL(19,4)            | Không | Không đặt CHECK (xem ghi chú dưới bảng)                    | Số liệu đề xuất sau điều chỉnh, tính theo thuế suất của bảng gốc                                   | SYS-US-04 bước 6                                   | OQ-US03-03 |
| `created_by`, `created_at`                                   | VARCHAR(50), TIMESTAMPTZ | Không |                                                            | KTT lập hồ sơ (dùng cho kiểm tra “không tự duyệt”)                                                 | SYS-US-04b TĐK 3                                   | –          |
| `decided_by`, `decided_at`                                   | VARCHAR(50), TIMESTAMPTZ | Có    |                                                            | GĐKD duyệt hoặc từ chối                                                                            | SYS-US-04b hậu ĐK                                  | OQ-US04-02 |
| `decline_reason`                                             | TEXT                     | Có    | CHECK `status <> 'Declined' OR decline_reason IS NOT NULL` | Lý do từ chối hồ sơ                                                                                | SYS-US-04b TĐK 4                                   | –          |
| `version`                                                    | INT                      | Không | DEFAULT 1                                                  | Khóa lạc quan khi chuyển trạng thái (`expectedVersion`)                                            | seq-us-04-2-v2 `Transition(..., expectedVersion)`  | –          |

`ux_adjustment_one_pending`: UNIQUE (`payment_sheet_id`) **WHERE `status = 'Pending'`**. Đây
là partial index trên PostgreSQL hoặc filtered index trên SQL Server. Ràng buộc này bảo đảm mỗi
bảng có tối đa một hồ sơ chờ duyệt, kể cả khi có hai yêu cầu đồng thời (SYS-US-04 TĐK 4, 7a).

SYS-US-04 không nêu tổng sau điều chỉnh có được âm hay không, nên không thêm CHECK cho
`proposed_total`. Nếu cần → OQ-US04-01.

### 3.7. `payment_adjustment_changes`

| Cột                                                     | Kiểu          | Null  | Khóa / ràng buộc                                                         | Mô tả                                                        | Nguồn                                |
| ------------------------------------------------------- | ------------- | ----- | ------------------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------ |
| `id`                                                    | UUID          | Không | PK                                                                       |                                                              |                                      |
| `adjustment_id`                                         | UUID          | Không | FK → `payment_adjustments.id` ON DELETE RESTRICT                         | Hồ sơ                                                        | SYS-US-04                            |
| `change_no`                                             | INT           | Không | UNIQUE (`adjustment_id`, `change_no`)                                    | Thứ tự                                                       | [ĐỀ XUẤT KỸ THUẬT]                   |
| `change_type`                                           | VARCHAR(10)   | Không | CHECK ∈ (`Modify`, `Add`, `Remove`)                                      | Sửa / thêm / bớt dòng                                        | SYS-US-04 TĐK 3, bước 5              |
| `service_code`                                          | VARCHAR(50)   | Không | UNIQUE (`adjustment_id`, `service_code`)                                 | Dịch vụ của dòng bị tác động; khóa nghiệp vụ của dòng (§3.2) | SYS-US-04 bước 5                     |
| `quantity_before`, `unit_price_before`, `amount_before` | DECIMAL(19,4) | Có    | NULL khi `Add`                                                           | Giá trị hiệu lực trước                                       | SYS-US-04 hậu ĐK “giá trị trước/sau” |
| `quantity_after`, `unit_price_after`, `amount_after`    | DECIMAL(19,4) | Có    | NULL khi `Remove`; CHECK `quantity_after >= 0 AND unit_price_after >= 0` | Giá trị sau                                                  | SYS-US-04 bước 5 “không âm”          |
| `reason`                                                | TEXT          | Không | CHECK không rỗng (service cắt khoảng trắng)                              | Lý do của từng thay đổi                                      | SYS-US-04 TĐK 3                      |

Không có cột đổi hợp đồng, kỳ hoặc thuế suất vì những thay đổi đó nằm ngoài phạm vi (SYS-US-04 5a).

### 3.8. `audit_entries` (NFR-PAY-01; DD-03, DD-11, DD-18)

| Cột                         | Kiểu        | Null                                     | Khóa / ràng buộc                                                                                                         | Mô tả                                                                                                                                                                                        |
| --------------------------- | ----------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                        | UUID        | Không                                    | PK                                                                                                                       |                                                                                                                                                                                              |
| `payment_sheet_id`          | UUID        | Không                                    | FK → `payment_sheets.id`                                                                                                 | Bảng liên quan. Luôn có giá trị để xem toàn bộ lịch sử của một bảng                                                                                                                          |
| `adjustment_id`             | UUID        | Có                                       | FK → `payment_adjustments.id`                                                                                            | Chỉ có giá trị với thao tác trên hồ sơ điều chỉnh                                                                                                                                            |
| `target_type`               | VARCHAR(20) | Không                                    | CHECK ∈ (`PaymentSheet`, `PaymentAdjustment`); CHECK `(target_type = 'PaymentAdjustment') = (adjustment_id IS NOT NULL)` | Đối tượng có trạng thái thay đổi                                                                                                                                                             |
| `action`                    | VARCHAR(20) | Không                                    | CHECK ∈ (`create`, `update`, `submit`, `approve`, `reject`, `reopen`, `cancel`, `adjust`)                                | Động từ dùng chung với sequence                                                                                                                                                              |
| `actor_id`                  | VARCHAR(50) | Không                                    |                                                                                                                          | **Ai**                                                                                                                                                                                       |
| `actor_role`                | VARCHAR(10) | Không                                    | CHECK ∈ (`NVKD`, `KTT`, `GDKD`)                                                                                          | Vai trò lúc thao tác (mỗi người một vai trò – SYS-US-01/03 TĐK)                                                                                                                              |
| `occurred_at`               | TIMESTAMPTZ | Không                                    |                                                                                                                          | **Lúc nào** (giờ server)                                                                                                                                                                     |
| `from_status`, `to_status`  | VARCHAR(20) | Có                                       | `from_status` NULL khi tạo                                                                                               | Trạng thái trước/sau của đối tượng `target_type`                                                                                                                                             |
| `before_json`, `after_json` | JSON        | `before` có thể NULL; `after` không NULL |                                                                                                                          | **Thay đổi gì**: ảnh chụp các trường/dòng bị đổi                                                                                                                                             |
| `reason`                    | TEXT        | Có                                       |                                                                                                                          | Lý do từ chối, hủy, điều chỉnh hoặc từ chối hồ sơ                                                                                                                                            |
| `submission_no`             | INT         | Có                                       |                                                                                                                          | Lần trình liên quan (submit/approve/reject)                                                                                                                                                  |
| `operation_id`              | UUID        | Có                                       | UNIQUE (`payment_sheet_id`, `operation_id`) WHERE `operation_id IS NOT NULL` `ux_audit_operation`                        | `operationId` client cấp cho lần lập hoặc cập nhật. E23 `VerifySaveOutcome(operationId, sheetId)` tìm bản ghi `update` theo cặp này và trả `after_json` (bản chụp bảng sau ghi, gồm version) |

Bảng chỉ thêm (append-only): tài khoản ứng dụng chỉ có quyền `INSERT`/`SELECT`, không có
`UPDATE`/`DELETE` [ĐỀ XUẤT KỸ THUẬT]. Index `ix_audit_sheet_time` (`payment_sheet_id`,
`occurred_at`) và `ix_audit_adjustment` (`adjustment_id`).

## 4. Quan hệ và cardinality

| Quan hệ                                                                    | Cardinality   | Ghi chú                                                                                 |
| -------------------------------------------------------------------------- | ------------- | --------------------------------------------------------------------------------------- |
| `payment_sheets` – `payment_lines`                                         | 1 – 0..\*     | Khi trình thì cần 1..\* (SYS-US-02 bước 7), nhưng CSDL không ép                         |
| `payment_lines` – `payment_line_sources`                                   | 1 – 0..\*     | 0 khi dịch vụ của hợp đồng không có bản ghi sản lượng trong kỳ (OQ-US01-04 đã xác nhận) |
| `payment_sheets` – `payment_period_claims`                                 | 1 – 0..3      | 1 dòng với kỳ tháng, 3 dòng với kỳ quý; 0 dòng khi `Cancelled`                          |
| `payment_sheets` – `payment_submissions`                                   | 1 – 0..\*     | Một dòng mỗi lần trình; Draft chưa trình thì 0                                          |
| `payment_submissions` – `payment_notifications`                            | 1 – 0..\*     | 0 khi lần trình chưa có người nhận (A8); thêm thông báo approve/reject của lần trình đó |
| `payment_sheets` – `payment_adjustments`                                   | 1 – 0..\*     | Chỉ khi `Approved`; tối đa 1 `Pending`                                                  |
| `payment_adjustments` – `payment_adjustment_changes`                       | 1 – 1..\*     | SYS-US-04 TĐK 3 “ít nhất một thay đổi”                                                  |
| `payment_sheets` – `audit_entries`                                         | 1 – 1..\*     | Luôn có ít nhất bản ghi `create`                                                        |
| `payment_adjustments` – `audit_entries`                                    | 1 – 1..\*     | Ít nhất bản ghi lập hồ sơ                                                               |
| `payment_sheets` → Hợp đồng / Bảng giá; `payment_line_sources` → Sản lượng | N – 1 (logic) | Không có FK chéo module                                                                 |

## 5. Ràng buộc và index

| Tên                                                        | Định nghĩa                                                                   | Mục đích                                                                                                  | Yêu cầu                                |
| ---------------------------------------------------------- | ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| `ck_sheet_status`                                          | `status IN ('Draft','PendingApproval','Approved','Rejected','Cancelled')`    | Chỉ 5 trạng thái                                                                                          | §3                                     |
| `ck_sheet_total_nonneg`                                    | `total_amount >= 0`                                                          | Chặn lưu tổng âm ở cả lập và trình                                                                        | SYS-US-01 bước 11/14; PAY-04           |
| `ck_sheet_cancel`, `ck_sheet_submitted`                    | §3.1                                                                         | Cột bắt buộc theo trạng thái                                                                              | §4.5, §4.2                             |
| `ck_submission_decision`                                   | §3.5                                                                         | Kết quả lần trình đủ người/thời điểm; từ chối phải có lý do                                               | §4.3, PAY-08                           |
| `ux_sheet_code`, `ux_sheet_create_op`                      | UNIQUE                                                                       | Mã bảng; xác minh kết quả lưu                                                                             | SYS-US-02 bước 10; SYS-US-01 E15.2     |
| `ux_line_service`                                          | UNIQUE (`payment_sheet_id`, `service_code`)                                  | Mỗi dịch vụ một dòng                                                                                      | SYS-US-01 (gộp); SYS-US-04 bước 5      |
| `pk_period_claims`                                         | PK (`contract_id`, `month_start`)                                            | Không trùng/chồng lấn kỳ, kể cả “đang tạo”                                                                | PAY-01; SYS-US-01 bước 7, 15, A15      |
| `ux_notification_key`                                      | UNIQUE (`payment_sheet_id`, `kind`, `submission_no`, `recipient_id`)         | Mỗi người một thông báo cho mỗi lần trình                                                                 | SYS-US-02 bước 10; SYS-US-02b          |
| `pk_payment_submissions`                                   | PK (`payment_sheet_id`, `submission_no`); FK từ `payment_notifications`      | Một bản ghi mỗi lần trình; thông báo luôn thuộc đúng lần trình                                            | SYS-US-02 bước 9–10; SYS-US-02b bước 3 |
| `ux_adjustment_one_pending`                                | UNIQUE (`payment_sheet_id`) WHERE `status='Pending'`                         | Mỗi bảng tối đa một hồ sơ chờ duyệt                                                                       | SYS-US-04 TĐK 4, 7a                    |
| `ck_audit_action`                                          | 8 động từ (§3.8)                                                             | Thống nhất tên thao tác                                                                                   | NFR-PAY-01                             |
| `ix_sheet_status`                                          | (`status`) trên `payment_sheets`                                             | Lọc bảng `PendingApproval` cho danh sách chờ duyệt                                                        | SYS-US-03                              |
| `ix_submission_role`                                       | (`required_role`, `submitted_at`) trên `payment_submissions`                 | Danh sách chờ duyệt theo vai trò KTT/GĐKD (nối `payment_sheets` theo `id` + `submission_no` hiện tại)     | SYS-US-03                              |
| `ix_sheet_contract_period`                                 | (`contract_id`, `period_start`)                                              | Danh sách bảng của hợp đồng; tìm kỳ đã lập (`ListPeriodsCovered`)                                         | SYS-US-01 bước 3                       |
| `ix_line_source_record`                                    | (`quantity_record_id`) trên `payment_line_sources`                           | Tra ngược bản ghi sản lượng đã được bảng nào dùng                                                         | PAY-03 (truy vết)                      |
| `ix_notification_pending`                                  | (`payment_sheet_id`, `submission_no`, `status`)                              | `GetSubmissionNotificationPlan(id, submissionNo)`                                                         | SYS-US-02b                             |
| `ix_audit_sheet_time`, `ix_audit_adjustment`               | §3.8                                                                         | Xem lịch sử                                                                                               | NFR-PAY-01                             |
| `ux_audit_operation`                                       | UNIQUE (`payment_sheet_id`, `operation_id`) WHERE `operation_id IS NOT NULL` | Một `operationId` chỉ gắn một lần ghi; dùng lại cho nội dung khác → `OPERATION_ID_CONFLICT`; xác minh E23 | SYS-US-01b E7.2; 04-v2 E8/E23          |

Ngưỡng 500 triệu (OQ-02) và quy tắc “mọi dịch vụ khai báo trong hợp đồng đều có dòng” (OQ-05)
**không** đưa vào ràng buộc CSDL. Danh sách dịch vụ thuộc module Hợp đồng, nên service kiểm tra
các quy tắc này.

## 6. Tiền và sản lượng

- [ĐỀ XUẤT KỸ THUẬT] Tiền, đơn giá và sản lượng dùng `DECIMAL(19,4)`, **không dùng float/double**
  để tránh sai số nhị phân. Thuế suất dùng `DECIMAL(5,4)` (ví dụ 0.1000 = 10%). Đơn vị tiền là
  đồng [ĐẶC TẢ] §4.3 “500.000.000 đ”.
- Làm tròn: SYS-US-04 mô tả “làm tròn lên theo đồng”. Đại diện nhóm xác nhận US-01 dùng quy tắc
  tính của US-04 (P-39). 02-v2 §4 đề xuất làm tròn lên đến đồng ở thành tiền từng dòng và ở tiền
  GTGT, rồi cộng thành tổng; thuế suất đọc theo hợp đồng/kỳ và lưu kèm `tax_rate_source_ref`.
  SYS-US-01 chưa nêu làm tròn ở dòng, tạm tính hay thuế. Scale 4 cho phép lưu đúng giá trị sau
  làm tròn mà không phải đổi schema khi quy tắc được chốt. **Blocked by OQ-US03-03** (vị trí và
  cách làm tròn, nguồn thuế suất).
- **Tổng được lưu, không tính lại khi đọc** (giữ như v1). Lý do: SYS-US-02 bước 8 và SYS-US-03
  bước 5 xác định người duyệt từ “tổng tiền đã lưu”. Khi lập hoặc tải lại nguồn, service tính
  trong cùng giao dịch và bảo đảm `subtotal_amount = Σ line_amount` và
  `total_amount = subtotal_amount + tax_amount` trước khi ghi.
- Kiểm tra định kỳ (khuyến nghị, không phải constraint): truy vấn so khớp tổng với tổng các dòng
  để phát hiện dữ liệu lệch.

## 7. Dữ liệu tại thời điểm tính (PAY-03)

Phương án đáp ứng PAY-03 “thành tiền = sản lượng × đơn giá tại thời điểm tính” (DD-04, DD-14):

| Dữ liệu chụp lại                                            | Cột                                                                          | Dùng ở                                                                                   |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Sản lượng gộp và đơn giá của dòng                           | `payment_lines.quantity`, `unit_price`, `line_amount`                        | Hiển thị, tổng tiền, điều chỉnh                                                          |
| Danh sách bản ghi sản lượng nguồn và sản lượng từng bản ghi | `payment_line_sources.*`                                                     | Kiểm tra “không thay đổi” khi trình (SYS-US-02 bước 6) và duyệt (SYS-US-03 bước 7)       |
| Bảng giá đã dùng                                            | `payment_sheets.price_list_id`, `payment_lines.unit_price`, `price_item_ref` | Kiểm tra “bảng giá đã dùng còn Active” (bảng giá Active không đổi nội dung – OQ-US01-01) |
| Thuế suất, nguồn thuế suất, thời điểm tính                  | `payment_sheets.tax_rate`, `tax_rate_source_ref`, `calculated_at`            | Tính lại và điều chỉnh (thuế suất bảng gốc)                                              |

Nhờ các bản chụp này, bảng không đổi khi module nguồn thay đổi. Chỉ thao tác “Tải lại dữ liệu
nguồn” khi bảng còn Draft mới thay toàn bộ dòng, nguồn và tổng (SYS-US-01).

Cách phát hiện bản ghi “đã thay đổi”: so `source_version` nếu module Sản lượng cung cấp, nếu không
thì so `quantity` và trạng thái đối soát. **OQ-D-03.**

## 8. Khóa duy nhất theo kỳ (PAY-01) – Blocked by OQ-01

SYS-US-01 v2 chọn: kỳ theo cấu hình tháng/quý của hợp đồng, **không chồng lấn khoảng ngày** với
bảng chưa hủy, chặn cả kỳ “đang tạo”, và bỏ qua bảng `Cancelled` [SYS v2 – OQ-01, OQ-US05-02,
OQ-D-01]. Bảng `Rejected` vẫn giữ kỳ vì nó “chưa hủy”. Đề gốc vẫn còn mâu thuẫn §2 ↔ PAY-01 nên
phần này chưa phải bản chốt.

**Phương án đề xuất – P4 giữ chỗ theo tháng (DD-13):**

- Khi lập bảng, trong cùng giao dịch với `INSERT payment_sheets`, thêm một dòng
  `payment_period_claims` cho **mỗi tháng** trong kỳ (tháng: 1 dòng; quý: 3 dòng).
- PK (`contract_id`, `month_start`) chặn mọi kỳ chồng lấn, kể cả bảng tháng chồng với bảng quý.
- “Đang tạo” (`includeCreating`, SYS-US-01 bước 7, A15): giao dịch thứ hai chèn cùng khóa sẽ chờ
  giao dịch thứ nhất. Nếu giao dịch thứ nhất commit, giao dịch thứ hai bị vi phạm khóa và nhận
  `PERIOD_OCCUPIED`. Không cần bảng “phiên đang tạo” riêng.
- Hủy bảng (SYS-US-05): trong cùng giao dịch `Draft → Cancelled`, xóa các claim của bảng để giải
  phóng kỳ (SYS-US-05 S5). Lịch sử vẫn nằm trong `audit_entries`.
- Đổi kỳ khi sửa Draft (SYS-US-01b; seq-us-01-update-v2 bước 7): trong cùng giao dịch `update`,
  xóa claim cũ của bảng rồi thêm claim của kỳ mới. Vì claim cũ đã xóa, kiểm tra tự loại chính
  bảng đang sửa. Vi phạm PK → `PERIOD_OCCUPIED` (A7), rollback giữ nguyên kỳ cũ và claim cũ.
- `Rejected` → giữ claim. `Approved` → giữ claim vĩnh viễn.

Điều kiện đúng: kỳ luôn gồm **trọn các tháng dương lịch** **[GIẢ ĐỊNH – Cần xác nhận: OQ-D-02]**.

| Phương án                                                      | Định nghĩa                                                                                                                 | Khi nào dùng                                                                      |
| -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| P4 – giữ chỗ theo tháng (đề xuất)                              | Bảng `payment_period_claims` ở trên                                                                                        | OQ-D-02 = kỳ trọn tháng; chạy được trên PostgreSQL và SQL Server                  |
| P5 – exclusion constraint                                      | `EXCLUDE USING gist (contract_id WITH =, daterange(period_start, period_end, '[]') WITH &&) WHERE (status <> 'Cancelled')` | Chỉ dùng được với PostgreSQL; đúng với mọi khoảng ngày, kể cả kỳ không trọn tháng |
| P2 (v1) – UNIQUE (`contract_id`, `period_start`, `period_end`) | Chỉ chặn kỳ trùng khít                                                                                                     | **Không đủ** cho yêu cầu “không chồng lấn” của SYS v2                             |
| P3 (v1) – duy nhất theo tháng                                  | Giống P4                                                                                                                   | Nếu OQ-01 trả lời “duy nhất theo tháng”, P4 vẫn đáp ứng                           |

Kiểm tra `FindOverlap` trước khi ghi chỉ để báo lỗi sớm trên giao diện (bước 7). Ràng buộc ở CSDL
mới là bảo đảm cuối cùng (bước 15).

## 9. Trạng thái và quy trình

Mọi chuyển trạng thái đều ghi có điều kiện:
`UPDATE payment_sheets SET status=:to, …, version=version+1 WHERE id=:id AND status=:from AND version=:expectedVersion`.
Nếu 0 dòng bị ảnh hưởng, giao dịch bị hủy và trả xung đột (DD-02).

| Thao tác (UC)            | from → to                      | Cột cập nhật thêm                                                                                                               | Bảng khác trong cùng giao dịch                                                                                                                                                                          |
| ------------------------ | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `create` (SYS-US-01)     | – → `Draft`                    | toàn bộ cột §3.1, `submission_no=0`                                                                                             | INSERT `payment_lines`, `payment_line_sources`, `payment_period_claims`, audit                                                                                                                          |
| `update` (SYS-US-01b)    | `Draft` → `Draft`              | `note`; nếu đổi kỳ: `period_*`; nếu đổi kỳ hoặc tải lại nguồn: tiền, `price_list_id`, `tax_rate*`, `calculated_at`; `updated_*` | Thay dòng và nguồn; đổi `payment_period_claims` nếu đổi kỳ; audit trước/sau kèm `operation_id`                                                                                                          |
| `submit` (SYS-US-02)     | `Draft` → `PendingApproval`    | `submission_no+1`                                                                                                               | audit; INSERT `payment_submissions` (vai trò, nội dung, `recipients_resolved_at` nếu có người nhận); INSERT `payment_notifications` (`Pending`) cho từng người nhận                                     |
| (gửi lại – SYS-US-02b)   | không đổi                      | –                                                                                                                               | Nếu chưa có danh sách: UPDATE có điều kiện `payment_submissions.recipients_resolved_at` + INSERT `payment_notifications`; sau gửi: UPDATE trạng thái thông báo. **Không** audit, **không** tăng version |
| `approve` (SYS-US-03)    | `PendingApproval` → `Approved` | –                                                                                                                               | UPDATE `payment_submissions` lần trình hiện tại: `decision='Approved'`, `decided_*`; audit; INSERT thông báo `approve` cho `created_by` |
| `reject` (SYS-US-03 A01) | `PendingApproval` → `Rejected` | –                                                                                                                               | UPDATE `payment_submissions` lần trình hiện tại: `decision='Rejected'`, `decided_*`, `rejection_reason`; audit có lý do; INSERT thông báo `reject` |
| `reopen` (SYS-US-03b)    | `Rejected` → `Draft`           | –                                                                                                                               | audit. Không sửa `payment_submissions`: kết quả và lý do của lần bị từ chối giữ nguyên                                                                                                         |
| `cancel` (SYS-US-05)     | `Draft` → `Cancelled`          | `cancel_reason`, `cancelled_*`                                                                                                  | DELETE `payment_period_claims` của bảng; audit có lý do                                                                                                                                                 |
| `adjust` (SYS-US-04/04b) | bảng giữ `Approved`            | **không ghi** `payment_sheets`                                                                                                  | Ghi `payment_adjustments`, `payment_adjustment_changes`, audit (§11)                                                                                                                                    |

Bảng `Approved` và `Cancelled` không được sửa trực tiếp (PAY-05; §4.5; SYS-US-04 Ràng buộc
chung). Service kiểm tra trạng thái. Có thể thêm trigger CSDL chặn UPDATE/DELETE trên
`payment_sheets`, `payment_lines` và `payment_line_sources` khi bảng không còn `Draft`
[ĐỀ XUẤT KỸ THUẬT – tùy chọn]. Riêng chuyển từ `PendingApproval`/`Rejected` và cột audit/thông
báo vẫn được phép.

Người lập (`created_by`) không đổi qua `update`/`reopen`. Vì vậy PAY-07 vẫn chặn đúng người tạo
Draft, kể cả khi một NVKD khác sửa bảng (SYS-US-03 TĐK 3).

## 10. Audit (NFR-PAY-01)

| Thao tác                 | `target_type`     | from → to                  | `before_json` / `after_json`                                                                      | `reason`            |
| ------------------------ | ----------------- | -------------------------- | ------------------------------------------------------------------------------------------------- | ------------------- |
| `create`                 | PaymentSheet      | NULL → Draft               | NULL / toàn bộ bảng + dòng + nguồn; `operation_id` = `create_operation_id`                        | –                   |
| `update`                 | PaymentSheet      | Draft → Draft              | bản chụp bảng (kỳ, ghi chú, dòng, tổng, version) **trước / sau**; `operation_id` của lần cập nhật | –                   |
| `submit`                 | PaymentSheet      | Draft → PendingApproval    | `{version, submissionNo}` / `{version, submissionNo, requiredRole}`                               | –                   |
| `approve`                | PaymentSheet      | PendingApproval → Approved | `{version}` / `{version}`                                                                         | –                   |
| `reject`                 | PaymentSheet      | PendingApproval → Rejected | `{version}` / `{version, rejectionReason}`                                                        | lý do               |
| `reopen`                 | PaymentSheet      | Rejected → Draft           | `{version}` / `{version}`                                                                         | –                   |
| `cancel`                 | PaymentSheet      | Draft → Cancelled          | `{version, period}` / `{version}`                                                                 | lý do               |
| `adjust` (lập hồ sơ)     | PaymentAdjustment | NULL → Pending             | số liệu hiệu lực / thay đổi, số liệu đề xuất, biên bản                                            | lý do từng thay đổi |
| `adjust` (duyệt hồ sơ)   | PaymentAdjustment | Pending → Approved         | số liệu hiệu lực **trước / sau**                                                                  | –                   |
| `adjust` (từ chối hồ sơ) | PaymentAdjustment | Pending → Declined         | `{status}` / `{status}`                                                                           | lý do               |

Audit được ghi **trong cùng giao dịch** với thay đổi. Nếu ghi audit lỗi, toàn bộ giao dịch bị
rollback (DD-03). Thao tác bị từ chối hoặc xung đột không tạo audit (SYS-US-02 E9; SYS-US-03
hậu ĐK thất bại). Không ghi audit cho thao tác chỉ đọc hoặc gửi lại thông báo.

## 11. Điều chỉnh bảng Approved (US-PAY-04 ↔ PAY-05) – Blocked by OQ-03

[GIẢ ĐỊNH – Cần xác nhận: OQ-03, OQ-US04-01, OQ-US04-02] SYS v2 chọn hồ sơ điều chỉnh riêng
(phương án A). Cách thiết kế dữ liệu:

- Không ghi bảng gốc, nên PAY-05 vẫn đúng với dữ liệu đã duyệt.
- **Số liệu hiệu lực** = bảng gốc + các hồ sơ `Approved` áp dụng theo `adjustment_no` tăng dần
  (SYS-US-04b). Số liệu này được **suy ra khi đọc, không lưu lên bảng gốc** (DD-16):
  - tổng hiệu lực = `proposed_total` của hồ sơ `Approved` có `adjustment_no` lớn nhất; nếu chưa
    có hồ sơ nào thì dùng `payment_sheets.total_amount`;
  - dòng hiệu lực = `payment_lines` áp lần lượt các `payment_adjustment_changes` của hồ sơ đã duyệt.
    Kết quả đúng vì mỗi bảng chỉ có một hồ sơ `Pending`, nên hồ sơ luôn được lập trên số liệu
    hiệu lực mới nhất;
  - đề xuất view `v_payment_sheet_effective` để kế toán đọc.
- Phương án thay thế: lưu toàn bộ dòng sau điều chỉnh của từng hồ sơ (bảng snapshot). Cách này
  đọc nhanh hơn nhưng trùng dữ liệu. Với dưới 200 dòng, chưa cần.
- Phương án B (sửa trực tiếp bảng gốc) **không** được thiết kế ở v2 vì SYS v2 đã chọn A. Nếu OQ-03
  được trả lời là B, §3.6–3.7 và §9 phải làm lại.
- Kế toán dùng số mới khi nào và xử lý ra sao nếu đã xuất hóa đơn: OQ-US04-02. Dữ liệu chỉ cung
  cấp `decided_at` của hồ sơ.

## 12. Transaction và đồng thời

Isolation đề xuất: READ COMMITTED kèm ghi có điều kiện, unique/PK constraint và khóa dòng khi
cần [ĐỀ XUẤT KỸ THUẬT]. Thông báo được gửi **sau commit**, ngoài giao dịch (DD-05).

| Thao tác            | Ghi trong một giao dịch                                                                                                                               | Kiểm soát đồng thời                                                                                                           | Sequence v2                               |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| create              | `payment_sheets` + `payment_lines` + `payment_line_sources` + `payment_period_claims` + audit                                                         | PK claim (A15); `ux_sheet_create_op`                                                                                          | seq-us-01-v2 bước 15, E15.1/E15.2         |
| update              | UPDATE có điều kiện + thay dòng/nguồn + DELETE/INSERT claim nếu đổi kỳ + audit có `operation_id`                                                      | `status='Draft'`, `version` (A7); PK claim (kỳ mới bị chiếm → `PERIOD_OCCUPIED`); `ux_audit_operation`                        | seq-us-01-update-v2 bước 7, A7, E7.1/E7.2 |
| submit              | UPDATE có điều kiện + audit + INSERT `payment_submissions` + INSERT thông báo `Pending` (`PrepareSubmission`)                                         | `status`, `version` (E9: tối đa một yêu cầu thắng); PK lần trình                                                              | seq-us-02-1-v2 bước 9                     |
| resend              | `EnsureRecipients`: UPDATE `payment_submissions` … `WHERE recipients_resolved_at IS NULL` + INSERT thông báo; mỗi `MarkNotification` là một ghi riêng | Chỉ một yêu cầu lập được danh sách (0 dòng → đọc lại danh sách đã có); `ux_notification_key`; chỉ gửi dòng `status <> 'Sent'` | seq-us-02-2-v2 bước 3–4                   |
| approve / reject    | UPDATE có điều kiện `payment_sheets` + UPDATE `payment_submissions` (kết quả lần trình hiện tại) + audit + INSERT thông báo                          | `status`, `version` (E10); `decision IS NULL` của lần trình hiện tại – 0 dòng thì rollback                                    | seq-us-03-1-v2 bước 8, R8 |
| reopen              | UPDATE có điều kiện + audit                                                                                                                           | `status`, `version` (E05)                                                                                                     | seq-us-03-2-v2                            |
| cancel              | UPDATE có điều kiện + DELETE claim + audit                                                                                                            | `status`, `version` (A7)                                                                                                      | seq-us-05-v2                              |
| lập hồ sơ           | `SELECT … FOR UPDATE` bảng gốc (`GetByIdForUpdate`) + INSERT hồ sơ + thay đổi + audit                                                                 | Khóa dòng bảng; `ux_adjustment_one_pending` (7a)                                                                              | seq-us-04-1-v2                            |
| duyệt/từ chối hồ sơ | Khóa bảng gốc + UPDATE có điều kiện hồ sơ + audit                                                                                                     | `status='Pending'`, `version` của hồ sơ (5a)                                                                                  | seq-us-04-2-v2                            |

Xác minh kết quả không rõ (`RESULT_UNKNOWN`):

- create: tìm theo `create_operation_id` (seq-us-01-v2 `FindSaveOutcome`). Có dòng → `COMMITTED`.
  Không có dòng thì **chưa đủ** để kết luận chưa lưu, theo đúng chú thích sequence.
- update: tìm `audit_entries` theo (`payment_sheet_id`, `operation_id`) (seq-us-01-update-v2
  `FindSaveOutcome(operationId, sheetId)`; 04-v2 E23). Có dòng → `COMMITTED`, trả `after_json`
  và version của đúng lần đó; không dùng version hiện tại để suy ra kết quả.
- Các thao tác khác: client đọc lại `status`/`version` của bảng hoặc hồ sơ.

NFR-PAY-02 (lưu nháp ≤ 3 giây với dưới 200 dòng): giao dịch create chèn khoảng 200 dòng
`payment_lines`, số dòng nguồn tương ứng, tối đa 3 claim và 1 audit. Nên dùng chèn theo lô
(batch insert) và có các index ở §5. Đây là phương án, **chưa đo**.

## 13. Migration

AS-IS chưa có CSDL. Đề xuất:

1. Chọn CSDL có giao dịch và partial/filtered unique index (PostgreSQL hoặc SQL Server). Nếu cần
   P5 (§8) thì phải dùng PostgreSQL.
2. Migration đầu tiên (ví dụ EF Core) tạo 9 bảng, CHECK, PK/FK và index ở §3–5. Phân quyền tài
   khoản ứng dụng: chỉ `INSERT`/`SELECT` trên `audit_entries`.
3. Không có dữ liệu khởi tạo. Hợp đồng, bảng giá, sản lượng và người dùng đọc qua interface.
4. `ux_adjustment_one_pending`, các bảng `payment_adjustment*` và `payment_period_claims` phụ thuộc
   OQ-03 / OQ-01 / OQ-D-02. Nếu câu trả lời khác SYS v2, cần migration sửa trước khi có dữ liệu thật.

Chưa viết mã migration.

## 14. Open Questions, quyết định kỹ thuật và tên dùng tạm

### 14.1. OQ ảnh hưởng dữ liệu

| ID                     | Nội dung                                                                 | Phần dữ liệu phụ thuộc                                                  | Trạng thái                                                                                                                                                      |
| ---------------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| OQ-01                  | Kỳ tháng/quý ↔ duy nhất theo tháng                                       | §8 (claim, `period_type`)                                               | SYS v2 chọn “không chồng lấn theo kỳ cấu hình” – Cần xác nhận                                                                                                   |
| OQ-02                  | Đúng 500 triệu ai duyệt                                                  | `payment_submissions.required_role` (§3.5)                              | SYS v2: ≥ 500 tr → GĐKD – Cần xác nhận                                                                                                                          |
| OQ-03                  | Điều chỉnh Approved                                                      | §3.6, §3.7, §11                                                         | SYS v2: hồ sơ riêng – Cần xác nhận                                                                                                                              |
| OQ-04, OQ-US03-07      | Đích sau từ chối; ai đưa về Draft                                        | `reopen` (§9)                                                           | SYS v2: Rejected, NVKD bấm “Chỉnh sửa” – Cần xác nhận                                                                                                           |
| OQ-05                  | Dòng dịch vụ bắt buộc                                                    | Không có constraint (§5)                                                | SYS v2: mọi dịch vụ khai báo trong hợp đồng – Cần xác nhận                                                                                                      |
| OQ-D-01                | Rejected có giữ kỳ không                                                 | §8                                                                      | SYS v2: giữ (chưa hủy) – Cần xác nhận                                                                                                                           |
| OQ-US01-01, 04         | Bảng giá Active không đổi; dịch vụ không có sản lượng vẫn có dòng tiền 0 | `price_list_id` (bỏ `price_list_version`), `payment_line_sources` 0..\* | Đã xác nhận (01-v2 §6)                                                                                                                                          |
| OQ-US01-05             | Mốc Active                                                               | – (kiểm tra ở service)                                                  | Theo SYS v2 – Cần xác nhận                                                                                                                                      |
| OQ-US01-02, 03         | Trường sửa trên Draft = kỳ + ghi chú; quyền theo phân công               | `period_*`, `note`, `updated_*`, claim                                  | OQ-US01-02: [QUYẾT ĐỊNH ĐÃ XÁC NHẬN] người dùng 12/11/2026, P-42. OQ-US01-03: theo SYS v2 – Cần xác nhận                                                        |
| OQ-US02-02, OQ-US03-05 | Thông báo trong hệ thống, gửi lại                                        | `payment_submissions`, `payment_notifications`                          | Theo SYS v2 – Cần xác nhận                                                                                                                                      |
| OQ-US03-01, 02, 04     | Người lập; theo vai trò; lý do ≤ 500 từ                                  | `created_by`, `recipient_id`, `rejection_reason`                        | Theo SYS v2 – Cần xác nhận                                                                                                                                      |
| OQ-US03-03             | Thuế GTGT, làm tròn, nguồn thuế suất                                     | §6; `tax_rate`, `tax_rate_source_ref`                                   | US-01 dùng quy tắc tính của US-04: [QUYẾT ĐỊNH ĐÃ XÁC NHẬN] đại diện nhóm 11/11/2026, P-39. Nguồn thuế suất và điểm làm tròn: **Blocked**, phương án ở 02-v2 §4 |
| OQ-US04-01, 02         | Tiêu chí biên bản, hình thức xác nhận hai bên; thời điểm áp dụng số mới  | `minutes_*`, `party_*_confirmed`; §11                                   | Cần xác nhận                                                                                                                                                    |
| OQ-US05-01, 02, 03     | Quyền hủy; lập lại sau hủy; lý do hủy bắt buộc                           | DELETE claim khi hủy; `cancel_reason`                                   | [QUYẾT ĐỊNH ĐÃ XÁC NHẬN] đại diện nhóm 11/11/2026, P-39 (01-v2 §6)                                                                                              |

### 14.2. OQ mới của phần dữ liệu (OQ-D, mã tự đặt – cần chép vào `01-requirements-summary-v2.md`)

| ID      | Vị trí nguồn                                                   | Loại  | Mô tả                                                                                     | Lý do cần xác nhận                                                                  | Lựa chọn                                                                    | Ảnh hưởng | Trạng thái   |
| ------- | -------------------------------------------------------------- | ----- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------- | ------------ |
| OQ-D-02 | TA-SPEC §2 “theo tháng hoặc quý”; SYS-US-01 TĐK 3              | Thiếu | Kỳ có luôn trùng tháng/quý dương lịch không, hay có thể bắt đầu giữa tháng theo hợp đồng? | Cách chặn chồng lấn phụ thuộc điều này                                              | A: trọn tháng → P4; B: ngày bất kỳ → P5                                     | §8, §13   | Cần xác nhận |
| OQ-D-03 | SYS-US-02 bước 6; SYS-US-03 bước 7 “sản lượng… không thay đổi” | Thiếu | Module Sản lượng có cung cấp dấu phiên bản/thời điểm cập nhật cho từng bản ghi không?     | Không có dấu này thì chỉ so được giá trị và trạng thái, có thể bỏ sót thay đổi khác | A: có version → so `source_version`; B: so `quantity` + trạng thái đối soát | §3.3, §7  | Cần xác nhận |

### 14.3. Quyết định kỹ thuật mới (cần chép vào `07-design-decisions-v2.md`)

| ID    | Lựa chọn                                                                                                                                                                       | Phương án thay thế                                                                             | Lý do / hệ quả                                                                                                                            |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| DD-13 | Giữ chỗ kỳ bằng `payment_period_claims` theo tháng; xóa claim khi hủy                                                                                                          | Exclusion constraint (PostgreSQL); kiểm tra trước khi ghi + SERIALIZABLE                       | Chạy được trên cả hai CSDL; tự chặn “đang tạo”. Phụ thuộc OQ-D-02                                                                         |
| DD-14 | Lưu bản ghi sản lượng nguồn theo dòng kèm sản lượng và `source_version`                                                                                                        | Chỉ lưu danh sách id                                                                           | Kiểm tra “không thay đổi” khi trình/duyệt; tăng số dòng ghi                                                                               |
| DD-15 | `payment_submissions` (một dòng mỗi lần trình: vai trò, nội dung, `recipients_resolved_at`) + `payment_notifications` (khóa bảng, loại, lần trình, người nhận; trạng thái gửi) | Không lưu (v1 §13); outbox chung; chỉ suy “chưa có người nhận” từ việc không có dòng thông báo | seq-us-02-1/02-2-v2 lưu vai trò, danh sách và nội dung theo lần trình; SYS-US-02b dùng dữ liệu của chính lần trình                        |
| DD-16 | Hồ sơ điều chỉnh = header + thay đổi; số liệu hiệu lực suy ra khi đọc                                                                                                          | Lưu snapshot dòng sau điều chỉnh                                                               | Không ghi bảng gốc (PAY-05); dữ liệu ít trùng. Blocked by OQ-03                                                                           |
| DD-17 | `create_operation_id` UNIQUE cho lần lập; `audit_entries.operation_id` UNIQUE theo bảng cho lần cập nhật                                                                       | Bảng nhật ký thao tác riêng; so version hiện tại                                               | Đáp ứng `FindSaveOutcome` của seq-us-01-v2 và seq-us-01-update-v2 (E7/E23 ở 04-v2) với ít cột nhất; audit `update` đã có bản chụp sau ghi |
| DD-18 | Audit chung cho bảng và hồ sơ (`target_type`, `adjustment_id`, `submission_no`); thêm động từ `reopen`                                                                         | Bảng audit riêng cho hồ sơ                                                                     | Một nơi tra lịch sử theo bảng; tên `reopen` lấy từ seq-us-03-2-v2                                                                         |
| DD-19 | Vai trò duyệt lưu theo lần trình (`payment_submissions.required_role`); `code` mã bảng do service sinh                                                                         | Lưu một cột vai trò trên `payment_sheets`; tính lại mỗi lần đọc                                | Gửi lại dùng đúng vai trò “đã xác định tại bước 8”; giữ lịch sử từng lần trình                                                            |
| DD-20 | Kết quả duyệt/từ chối lưu theo lần trình (`payment_submissions.decision`, `decided_*`, `rejection_reason`); bỏ ba cột này khỏi `payment_sheets` (P-51) | Giữ cột “kết quả gần nhất” trên `payment_sheets` (v2 trước P-51); giữ cả hai làm bản sao; gắn kết quả vào lần sửa Draft | Mỗi lần trình có tối đa một kết quả nên quan hệ rõ; giữ lịch sử từ chối nhiều vòng mà không phải đọc audit; một nguồn dữ liệu duy nhất. Lần sửa Draft chưa có người duyệt nên không mang kết quả. Hệ quả: đọc lý do phải nối lần trình hiện tại; ràng buộc trạng thái bảng ↔ kết quả do service giữ |

### 14.4. Tên dùng tạm – cần đồng bộ vào 03/class/04 v2

| Tên trong sequence v2                                                                    | Bảng.cột                                                                      | Ghi chú                                         |
| ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------- |
| `PaymentSheet`, `sheet.status/version/contractId/total/createdBy`                        | `payment_sheets.*`                                                            | Giữ như v1                                      |
| `submissionNo`                                                                           | `payment_sheets.submission_no`; `payment_notifications.submission_no`         | Mới ở v2                                        |
| `rejectionReason` (seq-03, 04-v2; trước P-51 seq-03 dùng `rejectReason`)                 | `payment_submissions.rejection_reason` (lần trình hiện tại)                   | P-51: chuyển từ `payment_sheets`                |
| `cancelReason`                                                                           | `payment_sheets.cancel_reason`                                                |                                                 |
| `operationId` (lập / cập nhật)                                                           | `payment_sheets.create_operation_id` / `audit_entries.operation_id`           | seq-us-01-v2, seq-us-01-update-v2               |
| `sourceRecordIds`                                                                        | `payment_line_sources.quantity_record_id`                                     |                                                 |
| `notificationStatus` (`SENT`/`FAILED`)                                                   | `payment_notifications.status` (`Sent`/`Failed`/`Pending`)                    | JSON đề xuất PascalCase giống trạng thái bảng   |
| `requiredRole`, `PrepareSubmission`, `GetSubmissionNotificationPlan`, `EnsureRecipients` | `payment_submissions.required_role`, `content_json`, `recipients_resolved_at` | Theo seq-us-02-1/02-2-v2 và 03-v2 mục US-PAY-02 |
| `reopen`                                                                                 | `audit_entries.action`                                                        | Động từ mới so với 7 động từ v1                 |
| `RecordDecision`, `decision`                                                             | `payment_submissions.decision`, `decided_by`, `decided_at`, `rejection_reason` | seq-us-03-1-v2 (P-51)                           |
| Hồ sơ `Pending/Approved/Declined`; `minutes`, `changes`, `proposedFigures`               | `payment_adjustments.*`, `payment_adjustment_changes.*`                       | Theo 03-v2                                      |

### 14.5. Ánh xạ field API (04-api-contract-v2) ↔ cột

| DTO / request (04-v2 §1–3)                                                                                          | Cột                                                                                                                                  | Ghi chú                                                                                       |
| ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------- |
| `PaymentSheetDto.id`, `code`, `contractId`, `status`, `version`, `submissionNo`, `priceListId`                      | `payment_sheets.id`, `code`, `contract_id`, `status`, `version`, `submission_no`, `price_list_id`                                    |                                                                                               |
| `period { type, start, end }` (`PeriodDto`)                                                                         | `period_type`, `period_start`, `period_end`                                                                                          |                                                                                               |
| `subtotalAmount`, `taxRate`, `taxAmount`, `totalAmount`, `calculatedAt`, `note`                                     | `subtotal_amount`, `tax_rate`, `tax_amount`, `total_amount`, `calculated_at`, `note`                                                 | Chuỗi thập phân ≤ 4 chữ số lẻ ↔ `DECIMAL(19,4)` / `DECIMAL(5,4)`                              |
| `createdBy`, `createdAt`, `cancelReason`                                                                            | `created_by`, `created_at`, `cancel_reason`                                                                                          | `updated_*`, `cancelled_*`, `tax_rate_source_ref` có cột nhưng chưa trả ra API |
| `rejectionReason`                                                                                                   | `payment_submissions.rejection_reason` của lần trình hiện tại                                                                        | `null` nếu lần trình hiện tại chưa bị từ chối (P-51)                  |
| `submissions[] { submissionNo, submittedBy, submittedAt, requiredRole, decision, decidedBy, decidedAt, rejectionReason }` (E6) | `payment_submissions.*` tương ứng                                                                                     | Lịch sử lần trình và kết quả (P-51)                                   |
| `PaymentLineDto.id`, `lineNo`, `serviceCode`, `serviceName`, `quantity`, `unitPrice`, `lineAmount`                  | `payment_lines.*` tương ứng                                                                                                          | `price_item_ref` không trả ra API                                                             |
| `PaymentLineDto.sourceRecordIds[]`                                                                                  | `payment_line_sources.quantity_record_id`                                                                                            | Mảng có thể rỗng (OQ-US01-04)                                                                 |
| `SubmissionResultDto.requiredRole`                                                                                  | `payment_submissions.required_role` (lần trình hiện tại)                                                                             |                                                                                               |
| `notificationStatus` (`Sent` / `NoRecipients` / `Failed`)                                                           | Tổng hợp từ `payment_submissions.recipients_resolved_at` và `payment_notifications.status`                                           | Không lưu; mỗi người nhận lưu `Pending`/`Sent`/`Failed`                                       |
| E5 `operationId` / E8 `operationId`                                                                                 | `payment_sheets.create_operation_id` / `audit_entries.operation_id`                                                                  | E7 / E23                                                                                      |
| E8 `expectedVersion`, `period`, `note`, `reloadSource`                                                              | `version` (điều kiện ghi), `period_*`, `note`; `reloadSource` không lưu                                                              |                                                                                               |
| `AdjustmentDto.id`, `sheetId`, `adjustmentNo`, `status`, `version`, `createdBy/At`, `decidedBy/At`, `declineReason` | `payment_adjustments.*` tương ứng                                                                                                    |                                                                                               |
| `minutes { number, date, partyAConfirmed, partyBConfirmed, fileName, downloadUrl }`                                 | `minutes_no`, `minutes_date`, `party_a_confirmed`, `party_b_confirmed`, `minutes_file_name`; `downloadUrl` cấp từ `minutes_file_key` | URL có thời hạn, không lưu                                                                    |
| `effectiveTotalBefore`, `proposedSubtotal`, `proposedTaxAmount`, `proposedTotal`                                    | cột cùng tên dạng snake_case                                                                                                         |                                                                                               |
| `changes[] { changeType, serviceCode, reason, before, after }`; `before/after { quantity, unitPrice, lineAmount }`  | `payment_adjustment_changes.change_type`, `service_code`, `reason`, `*_before`, `*_after` (`lineAmount` ↔ `amount_*`)                |                                                                                               |
| `effectiveTotal` (E17–E19)                                                                                          | Không lưu, suy ra theo §11                                                                                                           |                                                                                               |

## 15. Truy vết nhanh yêu cầu → dữ liệu

| Yêu cầu                    | Dữ liệu                                                                                                                      |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| US-PAY-01 / SYS-US-01, 01b | `payment_sheets`, `payment_lines`, `payment_line_sources`, `payment_period_claims`, audit `create`/`update` (`operation_id`) |
| US-PAY-02 / SYS-US-02, 02b | `submission_no`, `version`, `payment_submissions`, `payment_notifications`, audit `submit`                                   |
| US-PAY-03 / SYS-US-03, 03b | `decided_*`, `rejection_reason`, `created_by`, thông báo `approve`/`reject`, audit `approve`/`reject`/`reopen`               |
| US-PAY-04 / SYS-US-04, 04b | `payment_adjustments`, `payment_adjustment_changes`, audit `adjust` (Blocked by OQ-03)                                       |
| US-PAY-05 / SYS-US-05      | `cancel_reason`, `cancelled_*`, xóa claim, audit `cancel`                                                                    |
| PAY-01                     | `contract_id`, `period_*`, `payment_period_claims` (Blocked by OQ-01, OQ-D-02)                                               |
| PAY-02                     | `payment_line_sources` (bản ghi đã đối soát)                                                                                 |
| PAY-03                     | §7 snapshot                                                                                                                  |
| PAY-04                     | `ck_sheet_total_nonneg`; ghi có điều kiện `version` (chống trình trùng); dòng bắt buộc ở service (OQ-05)                     |
| PAY-05                     | §9 chặn sửa; §11 không ghi bảng gốc                                                                                          |
| PAY-06                     | `total_amount`, `payment_submissions.required_role` (OQ-02)                                                                  |
| PAY-07                     | `created_by`                                                                                                                 |
| PAY-08                     | `payment_submissions.rejection_reason`, `reopen`                                                                             |
| NFR-PAY-01                 | `audit_entries`                                                                                                              |
| NFR-PAY-02                 | §12 (chèn theo lô, index) – chưa đo                                                                                          |

## 16. Kiểm chứng

- Mỗi bảng ↔ tên dùng tạm trong sequence v2: §2, §14.4. Field API của `04-api-contract-v2.md` ↔
  cột: §14.5 (P-47). **Chưa đối chiếu với `class-v2.puml` vì file chưa tồn tại.**
- P-47: đọc lại `src/Qtkd.Api/` (không đổi từ 07/11/2026, vẫn chỉ có hợp đồng lưu trong bộ nhớ,
  `Contract.Id` kiểu `int`) – không ảnh hưởng ERD. Thay đổi đến từ SYS-US-01b, seq-us-01-update-v2,
  01/02/04-v2: đổi kỳ khi sửa Draft, `operation_id` cho lần cập nhật, `tax_rate_source_ref`, bỏ
  `price_list_version`, dòng có thể không có nguồn.
- Mọi US-PAY-01..05, PAY-01..08 và NFR-PAY-01/02 có ít nhất một dòng ở §15.
- `grep -n "Blocked by OQ" 05-data-design-v2.md` cho OQ-01, OQ-03, OQ-US03-03; cả ba có trong §14.1.
- ERD: kết quả kết xuất ghi trong P-37, P-38 của prompt-log.
- P-38: đối chiếu lại 8 sequence v2 sau commit `bae5c59` (tách seq-us-02 thành 02-1/02-2; seq-us-03-2 chỉ đổi tham chiếu). Lệch duy nhất về dữ liệu: `PrepareSubmission`/`GetSubmissionNotificationPlan`/`EnsureRecipients` lưu vai trò, danh sách và nội dung **theo lần trình** → thêm `payment_submissions` (§3.5). Các sequence còn lại không đổi tên bảng/cột.

## Thay đổi so với v1

| #   | Vị trí        | Thay đổi                                                                                                                                                                                                                                       | Căn cứ                                                  |
| --- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| 1   | §3.1          | Thêm `code`, `create_operation_id`, `period_type` (đổi tên từ `period_kind`), `subtotal_amount`, `tax_rate`, `tax_rate_source_ref`, `tax_amount`, `note`, `updated_*`, `submission_no`, `cancelled_*`; CHECK tổng ≥ 0 và CHECK theo trạng thái | SYS-US-01, 02, 05 v2; seq-us-01/02-v2                   |
| 2   | §3.2–3.3      | Một dòng mỗi dịch vụ (`ux_line_service`); tách nguồn sản lượng thành `payment_line_sources`; bỏ `calculated_at`/`*_source_ref` cấp dòng                                                                                                        | SYS-US-01 v2 “sản lượng gộp”, “danh sách bản ghi nguồn” |
| 3   | §3.4, §8      | Thay `ux_sheet_period` chưa chốt bằng claim theo tháng (P4) vì SYS v2 yêu cầu chặn chồng lấn và “đang tạo”                                                                                                                                     | SYS-US-01 bước 7, 15 v2; SYS-US-05 v2                   |
| 4   | §3.5          | Thêm `payment_submissions` (vai trò, nội dung, danh sách theo lần trình) và `payment_notifications` (v1 không lưu thông báo); vai trò duyệt và người/lúc trình chuyển từ bảng sang lần trình                                                   | SYS-US-02, 02b, 03 v2; seq-us-02-1/02-2-v2              |
| 5   | §3.6–3.7, §11 | Hồ sơ điều chỉnh đầy đủ theo SYS-US-04/04b: biên bản, thay đổi trước/sau, số liệu đề xuất, trạng thái hồ sơ, tối đa một Pending                                                                                                                | SYS-US-04 v2; seq-us-04-1/2-v2                          |
| 6   | §3.8, §10     | Audit thêm `adjustment_id`, `target_type`, `submission_no`, động từ `reopen`                                                                                                                                                                   | seq-us-03-2-v2, seq-us-04-2-v2                          |
| 7   | §9            | Đích sau từ chối = `Rejected`, về `Draft` qua `reopen`                                                                                                                                                                                         | SYS-US-03, 03b v2                                       |
| 8   | §13 v1        | Ánh xạ API ↔ cột chuyển thành §14.5 theo `04-api-contract-v2.md`; audit thêm `operation_id` cho lần cập nhật (SYS-US-01b)                                                                                                                      | 04-v2; SYS-US-01b                                       |
| 9   | §3.1, §3.5, §5, §9, §12, §14 | P-51: kết quả duyệt/từ chối (`decision`, `decided_*`, `rejection_reason`) chuyển từ `payment_sheets` sang `payment_submissions`, giữ lịch sử theo lần trình; thêm `ck_submission_decision`, bỏ `ck_sheet_reject`; DD-20 | Yêu cầu người dùng 14/11/2026 (P-51); SYS-US-03, 03b v2 |
