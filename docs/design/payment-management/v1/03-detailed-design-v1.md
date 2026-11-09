# 03 – Thiết kế chi tiết: danh mục tên, class, state (v1)

> Phiên bản: v1 · Ngày: 09/11/2026 · Người phụ trách: Chờ nhóm điền
> Đầu vào: `sys-us-01..05-v1.md`; `open-questions-v1.md`; `seq-us-01..05-v1.puml`; TA-SPEC §1–6; `src/Qtkd.Api/`
> AI: ChatGPT 5.5 · Prompt: P-21 trong [prompt-log](../../../workflow/prompt-log.md)
> Trạng thái: Bản lần chạy đầu – Design Pending Approval

Phạm vi lần này: **danh mục tên dùng chung**, bảng đối chiếu tên trong 5 sequence,
mô tả class và state machine. Chưa gồm hợp đồng API chi tiết (04) và dữ liệu (05).
Nhãn: [ĐẶC TẢ], [AC dẫn xuất], [ĐỀ XUẤT KỸ THUẬT], [GIẢ ĐỊNH – Cần xác nhận].

## 1. Danh mục tên dùng chung

Nguồn duy nhất của tên cho 02, class, state, 04, 05, 06 của v1. Tên chọn theo tên
được nhiều sequence dùng nhất; lựa chọn tên là [ĐỀ XUẤT KỸ THUẬT] (DD-01 trong
[07-design-decisions-v1.md](07-design-decisions-v1.md)), không phải quy tắc nghiệp vụ.

Quy ước chữ: event state machine và `action` audit viết thường (`submit`); method C#
viết PascalCase (`Submit`); cùng một động từ cho cùng một thao tác.

### 1.1. Thao tác

| Thao tác (event / audit action) | Method service                    | Endpoint đề xuất (chi tiết ở 04)            | US        | Đổi trạng thái                                                 |
| ------------------------------- | --------------------------------- | ------------------------------------------- | --------- | -------------------------------------------------------------- |
| `create`                        | `PaymentService.Create`           | `POST /api/payment-sheets`                  | US-PAY-01 | `[*]` → `Draft`                                                |
| `update`                        | `PaymentService.Update`           | `PUT /api/payment-sheets/{id}`              | US-PAY-01 | `Draft` → `Draft`                                              |
| `submit`                        | `PaymentService.Submit`           | `POST /api/payment-sheets/{id}/submit`      | US-PAY-02 | `Draft` → `PendingApproval`                                    |
| `approve`                       | `PaymentApprovalService.Approve`  | `POST /api/payment-sheets/{id}/approve`     | US-PAY-03 | `PendingApproval` → `Approved`                                 |
| `reject`                        | `PaymentApprovalService.Reject`   | `POST /api/payment-sheets/{id}/reject`      | US-PAY-03 | `PendingApproval` → `Rejected` hoặc `Draft` – Blocked by OQ-04 |
| `adjust`                        | `PaymentAdjustmentService.Adjust` | `POST /api/payment-sheets/{id}/adjustments` | US-PAY-04 | Blocked by OQ-03                                               |
| `cancel`                        | `PaymentService.Cancel`           | `POST /api/payment-sheets/{id}/cancel`      | US-PAY-05 | `Draft` → `Cancelled`                                          |

Thao tác chỉ đọc phục vụ form của US-PAY-01 (không đổi trạng thái, không audit thay
đổi bảng): `OpenCreateForm`, `SelectContract`, `SelectPeriod`, `Preview`, `OpenDraft`
[ĐỀ XUẤT KỸ THUẬT] [seq-us-01-v1; sys-us-01-v1 §1.3].

### 1.2. Class, interface, enum

| Tên chuẩn                  | Loại                     | Trách nhiệm                                                                           | US         |
| -------------------------- | ------------------------ | ------------------------------------------------------------------------------------- | ---------- |
| `PaymentSheet`             | Entity                   | Bảng thanh toán: hợp đồng, kỳ, bảng giá, trạng thái, tổng, người lập, version         | 01–05      |
| `PaymentLine`              | Entity                   | Dòng thanh toán: dịch vụ, sản lượng, đơn giá, thành tiền, tham chiếu nguồn            | 01         |
| `PaymentSheetStatus`       | Enum                     | Đúng 5 giá trị §3: `Draft`, `PendingApproval`, `Approved`, `Rejected`, `Cancelled`    | 01–05      |
| `BillingPeriod`            | Value object             | Kỳ thanh toán – cách biểu diễn tháng/quý Blocked by OQ-01                             | 01         |
| `AuditEntry`               | Entity                   | Bản ghi audit: ai, lúc nào, thao tác, trước/sau, lý do, biên bản                      | 01–05      |
| `PaymentAdjustment`        | Entity                   | Hồ sơ điều chỉnh riêng – chỉ tồn tại nếu chọn phương án A của OQ-03                   | 04         |
| `UserRole`                 | Enum                     | `NVKD`, `KTT`, `GDKD` (§2)                                                            | 01–05      |
| `CurrentUser`              | Value object             | Người gọi đã xác thực: `UserId`, `Role`                                               | 01–05      |
| `PaymentController`        | API                      | Nhận HTTP, xác thực, chuyển lỗi thành mã HTTP                                         | 01–05      |
| `PaymentService`           | Service                  | create/update/submit/cancel và các bước form US-PAY-01                                | 01, 02, 05 |
| `PaymentApprovalService`   | Service                  | approve/reject, PAY-07, PAY-08 (PAY-06 qua `PaymentSheet.RequiredApproverRole()`)     | 03         |
| `PaymentAdjustmentService` | Service                  | adjust – Blocked by OQ-03                                                             | 04         |
| `IPaymentRepository`       | Interface                | Đọc/ghi `PaymentSheet` + `PaymentLine`, cập nhật có điều kiện theo trạng thái/version | 01–05      |
| `IAdjustmentRepository`    | Interface                | Ghi `PaymentAdjustment` – chỉ phương án A                                             | 04         |
| `IAuditLog`                | Interface                | Ghi `AuditEntry` (append-only) trong cùng giao dịch                                   | 01–05      |
| `IUnitOfWork`              | Interface                | `Begin`, `Commit`, `Rollback` – bao thay đổi + audit                                  | 01–05      |
| `INotifier`                | Interface                | `NotifySubmission`, `NotifyResult` – kênh Blocked by OQ-US02-02, OQ-US03-05           | 02, 03     |
| `IContractReader`          | Interface ngoài, chỉ đọc | `ListCandidates`, `GetContract`                                                       | 01         |
| `IPriceReader`             | Interface ngoài, chỉ đọc | `ListCandidates`, `GetPriceList`                                                      | 01         |
| `IQuantityReader`          | Interface ngoài, chỉ đọc | `GetQuantities`                                                                       | 01         |

### 1.3. Mã lỗi chuẩn

HTTP chi tiết sẽ chốt ở 04; bảng này thống nhất **tên** mã lỗi [ĐỀ XUẤT KỸ THUẬT].

| Mã                         | HTTP đề xuất | Khi nào                                                       | Thay cho tên tạm trong seq                            |
| -------------------------- | ------------ | ------------------------------------------------------------- | ----------------------------------------------------- |
| `UNAUTHENTICATED`          | 401          | Chưa xác thực                                                 | –                                                     |
| `FORBIDDEN`                | 403          | Sai vai trò/quyền                                             | –                                                     |
| `NOT_FOUND`                | 404          | Không có bảng                                                 | –                                                     |
| `INVALID_INPUT`            | 400          | Dữ liệu yêu cầu không hợp lệ                                  | –                                                     |
| `INVALID_PERIOD`           | 400          | Kỳ sai cấu hình                                               | –                                                     |
| `VERSION_REQUIRED`         | 400          | Thiếu version khi update                                      | –                                                     |
| `INVALID_STATE`            | 409          | Trạng thái không cho phép thao tác                            | seq-us-05 dùng 400                                    |
| `CONCURRENT_MODIFICATION`  | 409          | Cập nhật có điều kiện thất bại do trạng thái/version đã đổi   | `CONCURRENT_CHANGE` (02), `CONCURRENCY_CONFLICT` (05) |
| `DUPLICATE_SUBMIT`         | 409          | Trình lại bảng đã `PendingApproval` (PAY-04)                  | –                                                     |
| `PAYMENT_EXISTS`           | 409          | Kỳ đã có bảng (PAY-01) – phạm vi Blocked by OQ-01, OQ-US05-02 | –                                                     |
| `CONTRACT_NOT_ACTIVE`      | 409          | Hợp đồng không Active (PAY-01)                                | –                                                     |
| `PRICE_NOT_SUITABLE`       | 409          | Không có bảng giá phù hợp (PAY-01)                            | –                                                     |
| `QUANTITY_NOT_RECONCILED`  | 409          | Sản lượng chưa Đã đối soát (PAY-02)                           | –                                                     |
| `NEGATIVE_TOTAL`           | 400          | Tổng âm (PAY-04)                                              | –                                                     |
| `REQUIRED_SERVICE_MISSING` | 400          | Thiếu dòng bắt buộc (PAY-04) – Blocked by OQ-05               | –                                                     |
| `APPROVER_NOT_AUTHORIZED`  | 403          | Sai người duyệt theo tổng (PAY-06) – Blocked by OQ-02         | –                                                     |
| `SELF_APPROVAL_FORBIDDEN`  | 403          | Người lập tự duyệt/từ chối (PAY-07)                           | –                                                     |
| `REASON_REQUIRED`          | 400          | Thiếu lý do (PAY-08; hủy: OQ-US05-03)                         | `INVALID_REASON` (05)                                 |
| `REASON_TOO_LONG`          | 400          | Lý do vượt giới hạn – [GIẢ ĐỊNH – Cần xác nhận] OQ-US03-04    | –                                                     |
| `SOURCE_UNAVAILABLE`       | 503          | Lỗi đọc hợp đồng/giá/sản lượng                                | –                                                     |
| `RESULT_UNKNOWN`           | 503          | Không biết kết quả commit                                     | –                                                     |
| `PERSISTENCE_ERROR`        | 500          | Lỗi lưu/audit/commit, đã rollback                             | `INTERNAL_ERROR` (05)                                 |

## 2. Đối chiếu tên cũ trong 5 sequence v1 → tên chuẩn

**Đã đồng bộ ở P-24 (09/11/2026)** theo yêu cầu người dùng: 5 file `seq-us-0N-v1.puml`
nay dùng tên chuẩn ở §1 và endpoint ở 04; luồng, nhánh, OQ giữ nguyên. Bản trước khi
đồng bộ còn trong lịch sử Git (commit `edd6223`). Bảng dưới giữ lại để truy vết tên cũ → tên mới.

| Sequence  | Tên đang dùng                                                                      | Tên chuẩn                                                                                      |
| --------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| seq-us-01 | `PaymentForm` (UI), `PaymentController`, `PaymentService`                          | giữ nguyên                                                                                     |
| seq-us-01 | `PaymentRepository.findConflict/getById/create/update`                             | `IPaymentRepository.FindConflict/GetById/Create/Update`                                        |
| seq-us-01 | `AuditLog.append`; `PaymentDatabase.begin/commit/rollback`                         | `IAuditLog.Append`; `IUnitOfWork.Begin/Commit/Rollback`                                        |
| seq-us-02 | `PaymentRepository.transition`, `Database`, `resolveRequiredApprover`              | `IPaymentRepository.Transition`; `IUnitOfWork`; `PaymentSheet.RequiredApproverRole()`          |
| seq-us-02 | `Notification.notifySubmission`                                                    | `INotifier.NotifySubmission`                                                                   |
| seq-us-02 | `CONCURRENT_CHANGE`                                                                | `CONCURRENT_MODIFICATION`                                                                      |
| seq-us-03 | `API (approve / reject)`                                                           | `PaymentController`                                                                            |
| seq-us-03 | `POST /api/payments/{id}/approve`, `/reject`                                       | `POST /api/payment-sheets/{id}/approve`, `/reject`                                             |
| seq-us-03 | `Notification.notifyResult`; `resolveRequiredApprover`; `S -> S : commit/rollback` | `INotifier.NotifyResult`; `PaymentSheet.RequiredApproverRole()`; `IUnitOfWork.Commit/Rollback` |
| seq-us-04 | `Màn hình điều chỉnh` gọi thẳng `PaymentAdjustmentService`                         | UI → `PaymentController.Adjust` → `PaymentAdjustmentService.Adjust`                            |
| seq-us-04 | `PaymentRepository.UpdateApproved` (phương án B)                                   | `IPaymentRepository.UpdateApproved` – Blocked by OQ-03                                         |
| seq-us-04 | `AdjustmentRepository.Create`, `AuditRepository.Append`                            | `IAdjustmentRepository.Create`; `IAuditLog.Append`                                             |
| seq-us-05 | `/api/payment-sheets/{id}/cancel`, `CancelAsync`                                   | giữ endpoint; `PaymentService.Cancel`                                                          |
| seq-us-05 | `GetByIdAsync`, `UpdateStatusAsync`                                                | `IPaymentRepository.GetById`, `Transition`                                                     |
| seq-us-05 | `AuditLogService.RecordStateChangeAsync`                                           | `IAuditLog.Append`                                                                             |
| seq-us-05 | `INVALID_STATE` 400, `INVALID_REASON`, `CONCURRENCY_CONFLICT`, `INTERNAL_ERROR`    | `INVALID_STATE` 409, `REASON_REQUIRED`, `CONCURRENT_MODIFICATION`, `PERSISTENCE_ERROR`         |

Khác biệt không chỉ về tên, ghi lại để review/v2 xem xét (không tự sửa ở v1):

- Thứ tự kiểm tra: seq-us-02 kiểm tra quyền trước khi đọc bảng; seq-us-03, 05 đọc
  bảng trước. Đề không quy định thứ tự [ĐỀ XUẤT KỸ THUẬT].
- seq-us-04 không có mã lỗi/HTTP và không có controller; seq-us-05 có SQL cụ thể
  (`SELECT/UPDATE PaymentSheets`) – mức chi tiết khác các seq còn lại.
- Trước P-24, seq-us-05 kiểm tra xung đột bằng `Version`, seq-us-03 bằng điều kiện trạng
  thái, seq-us-02 dùng cả hai. Nay cả 5 seq dùng cập nhật có điều kiện **trạng thái +
  version** với `expectedVersion` từ client (DD-02, DD-08).

## 3. Sơ đồ

| File                                                    | Loại                 | Mục đích                     | US/PAY                | Kết xuất                |
| ------------------------------------------------------- | -------------------- | ---------------------------- | --------------------- | ----------------------- |
| [seq-us-01-v1.puml](diagrams/seq-us-01-v1.puml)         | Sequence             | Lập/sửa Draft                | US-PAY-01; PAY-01..03 | SVG xuất lại (P-24)     |
| [seq-us-02-v1.puml](diagrams/seq-us-02-v1.puml)         | Sequence             | Trình duyệt                  | US-PAY-02; PAY-04, 06 | SVG/PNG xuất lại (P-24) |
| [seq-us-03-v1.puml](diagrams/seq-us-03-v1.puml)         | Sequence             | Duyệt/từ chối                | US-PAY-03; PAY-05..08 | SVG (P-24)              |
| [seq-us-04-v1.puml](diagrams/seq-us-04-v1.puml)         | Sequence             | Điều chỉnh Approved          | US-PAY-04; PAY-05     | SVG xuất lại (P-24)     |
| [seq-us-05-v1.puml](diagrams/seq-us-05-v1.puml)         | Sequence             | Hủy Draft                    | US-PAY-05             | SVG (P-24)              |
| [class-v1.puml](diagrams/class-v1.puml)                 | Class                | Lớp miền, service, interface | 01–05                 | Xem mục 6               |
| [state-machine-v1.puml](diagrams/state-machine-v1.puml) | State                | Vòng đời bảng                | 01–05                 | Xem mục 6               |
| [component-v1.puml](diagrams/component-v1.puml)         | Component            | Ranh giới module (đi với 02) | 01–05                 | Xem mục 6               |
| [erd-v1.puml](diagrams/erd-v1.puml)                     | ERD (không phải UML) | Mô hình dữ liệu (đi với 05)  | 01–05                 | Xem mục 6               |

## 4. Class – mô tả

Sơ đồ: [class-v1.puml](diagrams/class-v1.puml).

- `PaymentSheet 1 *-- 0..* PaymentLine` (composition). Bảng có thể không có dòng hay
  không: Blocked by OQ-US01-04.
- `PaymentSheet 1 -- 1..* AuditEntry`: ít nhất bản ghi `create` (đề xuất ghi audit
  cả khi tạo Draft – sys-us-01 §1.2) [ĐỀ XUẤT KỸ THUẬT].
- `PaymentSheet 1 -- 0..* PaymentAdjustment`: chỉ phương án A của OQ-03.
- `PaymentLine` lưu `Quantity`, `UnitPrice`, `LineAmount` và tham chiếu bản ghi nguồn
  đã dùng để tính – phương án đáp ứng PAY-03 "tại thời điểm tính" [ĐỀ XUẤT KỸ THUẬT].
- Tiền và sản lượng dùng `decimal`; độ chính xác, làm tròn, thuế Blocked by OQ-US03-03.
- `PaymentSheet.CreatedBy` dùng cho PAY-07; định nghĩa "người lập" Blocked by OQ-US03-01.
- `BillingPeriod` chưa chốt tháng/quý (OQ-01); `IPaymentRepository.FindConflict` nhận
  chính sách duy nhất làm tham số, Cancelled có chiếm kỳ không: OQ-US05-02.
- Service kiểm tra quyền/trạng thái/PAY; repository chỉ thực hiện ghi có điều kiện
  (`Transition`, `Update` với `expectedStatus` + `expectedVersion`).
- Module ngoài chỉ có interface đọc, nằm trong package `<<external, read-only>>`.

## 5. State machine – bảng chuyển trạng thái

Sơ đồ: [state-machine-v1.puml](diagrams/state-machine-v1.puml). Mọi chuyển có action
`/ ghi audit` cùng giao dịch (NFR-PAY-01, TA-SPEC §6).

| #   | Từ → Đến                       | Event         | Guard                                                                     | Action                          | Căn cứ                     | OQ                                           |
| --- | ------------------------------ | ------------- | ------------------------------------------------------------------------- | ------------------------------- | -------------------------- | -------------------------------------------- |
| T1  | `[*]` → `Draft`                | `create`      | NVKD; HĐ Active; bảng giá phù hợp; sản lượng Đã đối soát; kỳ chưa có bảng | Sinh dòng, tính tổng, audit     | §4.1; PAY-01..03           | OQ-01, OQ-US01-01, 03, 04, 05, OQ-US05-02    |
| T2  | `Draft` → `Draft`              | `update`      | Draft; version khớp; trường được phép                                     | Tính lại, audit trước/sau       | §4.1                       | OQ-US01-02, OQ-US01-03                       |
| T3  | `Draft` → `PendingApproval`    | `submit`      | NVKD có quyền; tổng ≥ 0; đủ dòng bắt buộc; không trùng                    | Audit, thông báo người duyệt    | §4.2; PAY-04, 06           | OQ-05, OQ-US02-01, OQ-02, OQ-US02-02         |
| T4  | `Draft` → `Cancelled`          | `cancel`      | Có quyền hủy; lý do theo xác nhận                                         | Audit                           | §3; §4.5                   | OQ-US05-01, OQ-US05-03                       |
| T5  | `PendingApproval` → `Approved` | `approve`     | Vai trò = người duyệt theo tổng; không phải người lập                     | Audit, thông báo kết quả (?)    | §4.3; PAY-06, 07           | OQ-02, OQ-US03-01, 02, 03, 05                |
| T6a | `PendingApproval` → `Rejected` | `reject`      | Lý do không rỗng; vai trò; không phải người lập                           | Lưu lý do, audit                | §3; §4.3                   | **Blocked by OQ-04** (phương án theo §3)     |
| T6b | `PendingApproval` → `Draft`    | `reject`      | như T6a                                                                   | Lưu lý do, audit                | PAY-08                     | **Blocked by OQ-04** (phương án theo PAY-08) |
| T7  | `Rejected` → `Draft`           | chưa xác định | chưa xác định                                                             | Audit                           | PAY-08 "quay về Draft"     | **Blocked by OQ-04, OQ-US03-07**             |
| T8  | `Approved` → `Approved`        | `adjust`      | KTT; có biên bản                                                          | Ghi điều chỉnh, audit trước/sau | §4.4 ↔ PAY-05              | **Blocked by OQ-03**, OQ-US04-01, 02         |
| T9  | `Cancelled` → `[*]`            | –             | –                                                                         | –                               | §4.5 "không dùng lại được" | –                                            |

Không thêm trạng thái mới. Phương án A của OQ-03 (hồ sơ điều chỉnh riêng) không đổi
`PaymentSheet` nên không có chuyển trạng thái; phương án B là T8. `Rejected` hiện không
có lối ra đã xác nhận và không có chuyển sang `Cancelled` trong §3 – xem OQ-D-01 ở
[01-requirements-summary-v1.md](01-requirements-summary-v1.md).

## 6. Kiểm chứng

Ghi tại mục Kiểm chứng của [01-requirements-summary-v1.md](01-requirements-summary-v1.md#kiểm-chứng)
và P-21, P-22 trong prompt-log. Chữ ký method trong class đã đồng bộ với
[04-api-contract-v1.md](04-api-contract-v1.md) (thêm `expectedVersion` – DD-08) ở P-22.
