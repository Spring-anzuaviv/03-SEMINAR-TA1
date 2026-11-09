# 05 – Thiết kế dữ liệu (v1)

> Phiên bản: v1 · Ngày: 09/11/2026 · Người phụ trách: Chờ nhóm điền
> Đầu vào: [class-v1.puml](diagrams/class-v1.puml); [03-detailed-design-v1.md](03-detailed-design-v1.md); [04-api-contract-v1.md](04-api-contract-v1.md); [07-design-decisions-v1.md](07-design-decisions-v1.md); `sys-us-01..05-v1.md`; `open-questions-v1.md`; `src/Qtkd.Api/`
> AI: ChatGPT 5.5 · Prompt: P-22 trong [prompt-log](../../../workflow/prompt-log.md)
> Trạng thái: Bản lần chạy đầu – Design Pending Approval

Sơ đồ: [erd-v1.puml](diagrams/erd-v1.puml) – **ERD (mô hình dữ liệu)**, không phải
UML class diagram. Kiểu cột, index, ràng buộc là [ĐỀ XUẤT KỸ THUẬT]; phần phụ thuộc OQ
ghi `Blocked by OQ-…` và trình bày phương án, không chốt.

## 1. Nguồn và phạm vi

Chỉ dữ liệu của module Bảng thanh toán. Hợp đồng, bảng giá, sản lượng thuộc module khác:
chỉ lưu **khóa tham chiếu** và **bản sao giá trị tại thời điểm tính**, không có bảng hay
CRUD cho các module đó [TA-SPEC §1].

## 2. AS-IS lưu trữ

Đọc lại `src/Qtkd.Api/` ngày 09/11/2026: chỉ `ContractService` lưu hợp đồng trong
`ConcurrentDictionary` (bộ nhớ). **Chưa có CSDL, ORM, migration** nào. Mọi bảng dưới đây là TO-BE.

## 3. Danh sách entity

| Bảng                  | Class (class-v1)    | Mục đích                                                   | US / yêu cầu                 |
| --------------------- | ------------------- | ---------------------------------------------------------- | ---------------------------- |
| `payment_sheets`      | `PaymentSheet`      | Bảng thanh toán, trạng thái, tổng, người thao tác, version | US-PAY-01..05; PAY-01, 04–08 |
| `payment_lines`       | `PaymentLine`       | Dòng dịch vụ với giá trị tại thời điểm tính                | US-PAY-01; PAY-02, PAY-03    |
| `audit_entries`       | `AuditEntry`        | Nhật ký mọi thay đổi trạng thái/điều chỉnh                 | NFR-PAY-01                   |
| `payment_adjustments` | `PaymentAdjustment` | Hồ sơ điều chỉnh riêng – **chỉ phương án A**               | US-PAY-04 – Blocked by OQ-03 |

## 4. Chi tiết bảng

### 4.1. `payment_sheets`

| Cột                            | Kiểu                     | Null  | Khóa / ràng buộc                                            | Mô tả                                         | Nguồn / nhãn         | OQ                       |
| ------------------------------ | ------------------------ | ----- | ----------------------------------------------------------- | --------------------------------------------- | -------------------- | ------------------------ |
| `id`                           | UUID                     | Không | PK                                                          | Định danh bảng                                | [ĐỀ XUẤT KỸ THUẬT]   | –                        |
| `contract_id`                  | INT                      | Không | Tham chiếu logic tới module Hợp đồng (không FK chéo module) | Hợp đồng; kiểu `int` theo AS-IS `Contract.Id` | [ĐẶC TẢ] §4.1; AS-IS | –                        |
| `period_kind`                  | VARCHAR(10)              | Không | CHECK ∈ (`Month`, `Quarter`)                                | Loại kỳ                                       | [ĐẶC TẢ] §2          | Blocked by OQ-01         |
| `period_start`                 | DATE                     | Không |                                                             | Ngày đầu kỳ                                   | [ĐẶC TẢ] §2          | OQ-01                    |
| `period_end`                   | DATE                     | Không | CHECK `period_end >= period_start`                          | Ngày cuối kỳ                                  | [ĐẶC TẢ] §2          | OQ-01                    |
| `price_list_id`                | VARCHAR(50)              | Không | Tham chiếu logic module Bảng giá                            | Bảng giá đã chọn                              | [ĐẶC TẢ] PAY-01      | OQ-US01-01               |
| `status`                       | VARCHAR(20)              | Không | CHECK ∈ 5 giá trị §3                                        | Trạng thái                                    | [ĐẶC TẢ] §3          | –                        |
| `total_amount`                 | DECIMAL(19,4)            | Không | Không CHECK ≥ 0 (PAY-04 chỉ chặn khi **trình**)             | Tổng tiền = Σ `line_amount`                   | [ĐẶC TẢ] §4.1        | Làm tròn/VAT: OQ-US03-03 |
| `calculated_at`                | TIMESTAMPTZ              | Không |                                                             | Thời điểm tính                                | PAY-03; DD-04        | OQ-US01-01               |
| `created_by`                   | VARCHAR(50)              | Không |                                                             | Người lập (PAY-07)                            | [ĐẶC TẢ] PAY-07      | OQ-US03-01               |
| `created_at`                   | TIMESTAMPTZ              | Không |                                                             |                                               | [ĐỀ XUẤT KỸ THUẬT]   | –                        |
| `submitted_by`, `submitted_at` | VARCHAR(50), TIMESTAMPTZ | Có    |                                                             | Người/lúc trình gần nhất                      | §4.2                 | –                        |
| `decided_by`, `decided_at`     | VARCHAR(50), TIMESTAMPTZ | Có    |                                                             | Người/lúc duyệt hoặc từ chối gần nhất         | §4.3                 | –                        |
| `rejection_reason`             | TEXT                     | Có    |                                                             | Lý do từ chối gần nhất (DD-12)                | [ĐẶC TẢ] PAY-08      | Giới hạn: OQ-US03-04     |
| `cancel_reason`                | TEXT                     | Có    |                                                             | Lý do hủy (DD-12)                             | §4.5                 | Bắt buộc?: OQ-US05-03    |
| `version`                      | INT                      | Không | DEFAULT 1; tăng mỗi lần ghi                                 | Khóa lạc quan                                 | DD-02                | –                        |

Lịch sử đầy đủ của trình/duyệt/từ chối nằm ở `audit_entries`; các cột `*_by/*_at` trên
bảng chỉ giữ lần gần nhất để hiển thị.

### 4.2. `payment_lines`

| Cột                   | Kiểu          | Null  | Khóa / ràng buộc                            | Mô tả                      | Nguồn / nhãn         | OQ                        |
| --------------------- | ------------- | ----- | ------------------------------------------- | -------------------------- | -------------------- | ------------------------- |
| `id`                  | UUID          | Không | PK                                          |                            |                      | –                         |
| `payment_sheet_id`    | UUID          | Không | FK → `payment_sheets.id` ON DELETE RESTRICT | Thuộc bảng                 | §2 "dòng thanh toán" | –                         |
| `line_no`             | INT           | Không | UNIQUE (`payment_sheet_id`, `line_no`)      | Thứ tự                     | [ĐỀ XUẤT KỸ THUẬT]   | –                         |
| `service_code`        | VARCHAR(50)   | Không | Không UNIQUE theo bảng                      | Dịch vụ                    | [ĐẶC TẢ] §2          | Gộp/tách dòng: OQ-US01-04 |
| `quantity`            | DECIMAL(19,4) | Không |                                             | Sản lượng đã đối soát      | [ĐẶC TẢ] PAY-02      | OQ-US01-04                |
| `unit_price`          | DECIMAL(19,4) | Không |                                             | Đơn giá tại thời điểm tính | [ĐẶC TẢ] PAY-03      | OQ-US01-01                |
| `line_amount`         | DECIMAL(19,4) | Không |                                             | `quantity × unit_price`    | [ĐẶC TẢ] PAY-03      | Làm tròn: OQ-US03-03      |
| `quantity_source_ref` | VARCHAR(100)  | Không |                                             | Bản ghi sản lượng nguồn    | DD-04                | –                         |
| `price_source_ref`    | VARCHAR(100)  | Không |                                             | Bản ghi đơn giá nguồn      | DD-04                | –                         |
| `calculated_at`       | TIMESTAMPTZ   | Không |                                             |                            | DD-04                | –                         |

### 4.3. `audit_entries` (NFR-PAY-01, DD-03, DD-11)

| Cột                | Kiểu         | Null  | Khóa / ràng buộc                                                                | Mô tả                            |
| ------------------ | ------------ | ----- | ------------------------------------------------------------------------------- | -------------------------------- |
| `id`               | UUID         | Không | PK                                                                              |                                  |
| `payment_sheet_id` | UUID         | Không | FK → `payment_sheets.id` ON DELETE RESTRICT                                     | Bảng bị thay đổi                 |
| `action`           | VARCHAR(20)  | Không | CHECK ∈ (`create`, `update`, `submit`, `approve`, `reject`, `adjust`, `cancel`) | Thao tác (động từ chung ở 03)    |
| `actor_id`         | VARCHAR(50)  | Không |                                                                                 | **Ai**                           |
| `actor_role`       | VARCHAR(10)  | Không | CHECK ∈ (`NVKD`, `KTT`, `GDKD`)                                                 | Vai trò lúc thao tác             |
| `occurred_at`      | TIMESTAMPTZ  | Không |                                                                                 | **Lúc nào**                      |
| `from_status`      | VARCHAR(20)  | Có    | NULL cho `create`                                                               | Trạng thái trước                 |
| `to_status`        | VARCHAR(20)  | Có    |                                                                                 | Trạng thái sau                   |
| `before_json`      | JSON         | Có    | NULL cho `create`                                                               | **Thay đổi gì** – ảnh chụp trước |
| `after_json`       | JSON         | Không |                                                                                 | Ảnh chụp sau                     |
| `reason`           | TEXT         | Có    |                                                                                 | Lý do từ chối/hủy/điều chỉnh     |
| `attachment_ref`   | VARCHAR(100) | Có    |                                                                                 | Mã biên bản (US-PAY-04)          |

Append-only: ứng dụng chỉ `INSERT`; tài khoản ứng dụng không có quyền `UPDATE/DELETE`
trên bảng này [ĐỀ XUẤT KỸ THUẬT]. Index (`payment_sheet_id`, `occurred_at`).

### 4.4. `payment_adjustments` – Blocked by OQ-03 (chỉ phương án A)

| Cột                | Kiểu         | Null  | Khóa / ràng buộc         | Mô tả                     | OQ         |
| ------------------ | ------------ | ----- | ------------------------ | ------------------------- | ---------- |
| `id`               | UUID         | Không | PK                       |                           | –          |
| `payment_sheet_id` | UUID         | Không | FK → `payment_sheets.id` | Bảng gốc (giữ `Approved`) | OQ-03      |
| `content`          | TEXT         | Không |                          | Nội dung điều chỉnh       | OQ-US04-01 |
| `minutes_ref`      | VARCHAR(100) | Không |                          | Mã biên bản xác nhận      | OQ-US04-01 |
| `created_by`       | VARCHAR(50)  | Không |                          | KTT                       | –          |
| `created_at`       | TIMESTAMPTZ  | Không |                          |                           | –          |

Có cần cột số tiền chênh lệch/dòng bị điều chỉnh không: Blocked by OQ-US04-01. Phương án B
không dùng bảng này: cập nhật `payment_sheets`/`payment_lines` và audit lưu trước/sau.

## 5. Quan hệ và cardinality

| Quan hệ                                  | Cardinality   | Ghi chú                               |
| ---------------------------------------- | ------------- | ------------------------------------- |
| `payment_sheets` – `payment_lines`       | 1 – 0..\*     | Bảng rỗng có hợp lệ không: OQ-US01-04 |
| `payment_sheets` – `audit_entries`       | 1 – 1..\*     | Ít nhất bản ghi `create`              |
| `payment_sheets` – `payment_adjustments` | 1 – 0..\*     | Chỉ phương án A                       |
| `payment_sheets` → Hợp đồng / Bảng giá   | N – 1 (logic) | Không FK chéo module                  |

## 6. Ràng buộc và index

| Tên                        | Định nghĩa                                                                | Mục đích                         | Yêu cầu                 |
| -------------------------- | ------------------------------------------------------------------------- | -------------------------------- | ----------------------- |
| `ck_sheet_status`          | `status IN ('Draft','PendingApproval','Approved','Rejected','Cancelled')` | Chỉ 5 trạng thái                 | §3                      |
| `ck_audit_action`          | `action IN (…7 thao tác…)`                                                | Thống nhất tên thao tác          | NFR-PAY-01              |
| `ux_line_no`               | UNIQUE (`payment_sheet_id`, `line_no`)                                    | Thứ tự dòng                      | –                       |
| `ux_sheet_period`          | **Chưa chốt** – xem §8                                                    | Một bảng/HĐ/kỳ                   | PAY-01 – Blocked        |
| `ix_sheet_status`          | (`status`, `submitted_at`)                                                | Danh sách chờ duyệt cho KTT/GĐKD | US-PAY-03               |
| `ix_sheet_contract_period` | (`contract_id`, `period_start`)                                           | E3 kiểm tra trùng, E7 tra cứu    | PAY-01; sys-us-01 A15.2 |
| `ix_audit_sheet_time`      | (`payment_sheet_id`, `occurred_at`)                                       | Xem lịch sử                      | NFR-PAY-01              |

Không đưa ngưỡng 500 triệu (OQ-02) hay quy tắc dòng bắt buộc (OQ-05) vào ràng buộc CSDL:
đó là kiểm tra nghiệp vụ ở service, còn đang chờ xác nhận.

## 7. Tiền, sản lượng và dữ liệu tại thời điểm tính

- [ĐỀ XUẤT KỸ THUẬT] Dùng `DECIMAL(19,4)` cho tiền và sản lượng, **không** dùng float/double
  (tránh sai số nhị phân). Số chữ số lưu dư để chưa phải chốt cách làm tròn. Đơn vị: đồng.
  Làm tròn từng dòng hay tổng, có VAT không, thứ tự tính: **Blocked by OQ-US03-03**.
- `total_amount` được **lưu** (không tính lại khi đọc) để ngưỡng duyệt dùng đúng tổng đã
  trình; service tính lại từ dòng khi create/update và bảo đảm `total_amount = Σ line_amount`
  trước khi ghi [ĐỀ XUẤT KỸ THUẬT].
- PAY-03 "đơn giá tại thời điểm tính": `payment_lines` lưu `quantity`, `unit_price`,
  `line_amount`, `*_source_ref`, `calculated_at` (DD-04) – bảng không đổi khi module nguồn
  thay đổi. Giá đổi giữa xem trước và lưu: OQ-US01-01.

## 8. Khóa duy nhất theo kỳ (PAY-01) – chưa chốt

Đề: "mỗi hợp đồng chỉ có một bảng thanh toán cho mỗi tháng" (PAY-01) nhưng kỳ là "tháng
hoặc quý tùy cấu hình" (§2). Ba câu hỏi chồng nhau: **OQ-01** (đơn vị kỳ), **OQ-US05-02**
(bảng `Cancelled` có chiếm kỳ không), **OQ-D-01** (bảng `Rejected` có chiếm kỳ không).

| Phương án                                    | Định nghĩa minh họa                                                                                   | Khi nào đúng                              |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| P1 – theo kỳ cấu hình, Cancelled không chiếm | `UNIQUE (contract_id, period_start, period_end) WHERE status <> 'Cancelled'` (partial/filtered index) | OQ-01 = theo kỳ; OQ-US05-02 = cho lập lại |
| P2 – theo kỳ cấu hình, Cancelled vẫn chiếm   | `UNIQUE (contract_id, period_start, period_end)`                                                      | OQ-US05-02 = không cho lập lại            |
| P3 – theo tháng                              | Cần bảng phụ `payment_sheet_months(contract_id, month)` mỗi bảng quý chiếm 3 dòng, UNIQUE theo tháng  | OQ-01 = duy nhất theo tháng               |

Dù chọn phương án nào, ràng buộc phải ở **CSDL** (không chỉ kiểm tra trước khi ghi) để hai
yêu cầu đồng thời không tạo hai bảng – yêu cầu thua nhận `PAYMENT_EXISTS` (sys-us-01 A15).
Bảng `Rejected` tính hay không tính vào điều kiện: OQ-D-01.

## 9. Trạng thái và quy trình

- `status` chỉ nhận 5 giá trị §3; mọi chuyển đổi đi qua `UPDATE … SET status = :to,
version = version + 1 WHERE id = :id AND status = :from AND version = :expectedVersion`
  (DD-02). 0 dòng bị ảnh hưởng → `CONCURRENT_MODIFICATION`/`DUPLICATE_SUBMIT`/`INVALID_STATE`
  tùy trạng thái đọc lại.
- Đích sau từ chối (`Rejected` hay `Draft`): Blocked by OQ-04 – cột `status` hỗ trợ cả hai.

## 10. Audit (NFR-PAY-01)

| Thao tác | from → to                                | `before_json` / `after_json`               | `reason`           | `attachment_ref` |
| -------- | ---------------------------------------- | ------------------------------------------ | ------------------ | ---------------- |
| create   | NULL → Draft                             | NULL / toàn bộ bảng + dòng                 | –                  | –                |
| update   | Draft → Draft                            | các trường/dòng trước / sau                | –                  | –                |
| submit   | Draft → PendingApproval                  | `{status, version}`                        | –                  | –                |
| approve  | PendingApproval → Approved               | `{status, version}`                        | –                  | –                |
| reject   | PendingApproval → Rejected/Draft (OQ-04) | `{status, version}`                        | lý do              | –                |
| adjust   | Approved → Approved (B) / không đổi (A)  | trường trước / sau (B); nội dung hồ sơ (A) | nội dung           | mã biên bản      |
| cancel   | Draft → Cancelled                        | `{status, version}`                        | lý do (OQ-US05-03) | –                |

Ghi trong cùng giao dịch với thay đổi; lỗi audit → rollback (DD-03).

## 11. Transaction và đồng thời

| Thao tác                           | Trong một giao dịch                                                     | Kiểm soát đồng thời             | Sequence                       |
| ---------------------------------- | ----------------------------------------------------------------------- | ------------------------------- | ------------------------------ |
| create                             | INSERT `payment_sheets` + `payment_lines` + `audit_entries`             | Ràng buộc duy nhất theo kỳ (§8) | seq-us-01 "Transaction create" |
| update                             | UPDATE có điều kiện + thay dòng + audit                                 | `status`, `version`             | seq-us-01 "Transaction update" |
| submit / approve / reject / cancel | UPDATE có điều kiện + audit                                             | `status`, `version`             | seq-us-02, 03, 05              |
| adjust                             | A: INSERT `payment_adjustments` + audit; B: UPDATE có điều kiện + audit | `version`                       | seq-us-04                      |

Isolation: READ COMMITTED đủ vì mọi ghi đều có điều kiện trên chính dòng bị ghi
[ĐỀ XUẤT KỸ THUẬT]. Thông báo gửi sau commit, ngoài giao dịch (DD-05).

## 12. Migration

AS-IS chưa có CSDL. Đề xuất: chọn CSDL có giao dịch và partial/filtered unique index
(PostgreSQL hoặc SQL Server); tạo schema ban đầu bằng migration của ORM (vd. EF Core)
gồm 4 bảng, CHECK và index ở trên; không có dữ liệu khởi tạo. Ràng buộc `ux_sheet_period`
chỉ thêm khi OQ-01/OQ-US05-02/OQ-D-01 có câu trả lời. Chưa viết mã migration.

## 13. Ánh xạ API ↔ cột

| Field API (`PaymentSheetDto`, 04)                                     | Cột                                                                       |
| --------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `id`, `contractId`, `priceListId`, `status`, `totalAmount`, `version` | `id`, `contract_id`, `price_list_id`, `status`, `total_amount`, `version` |
| `period`                                                              | `period_kind` + `period_start` + `period_end` (định dạng chuỗi: OQ-01)    |
| `createdBy/At`, `submittedBy/At`, `decidedBy/At`                      | cột tương ứng                                                             |
| `rejectionReason`, `cancelReason`                                     | `rejection_reason`, `cancel_reason`                                       |
| `lines[]`                                                             | `payment_lines`                                                           |
| `notification` (E9)                                                   | Không lưu – kết quả gửi lúc gọi (DD-05)                                   |
| `calculationContext` (E4/E5)                                          | Không lưu; `calculated_at` lưu thời điểm tính                             |

## 14. Open Questions ảnh hưởng dữ liệu

OQ-01, OQ-US05-02, OQ-D-01 (khóa duy nhất); OQ-US03-03 (tiền); OQ-US01-01, OQ-US01-04 (dòng);
OQ-03, OQ-US04-01, OQ-US04-02 (điều chỉnh); OQ-04 (đích từ chối); OQ-US03-01 (người lập);
OQ-US03-04, OQ-US05-03 (lý do). Không có OQ mới do phần dữ liệu.
