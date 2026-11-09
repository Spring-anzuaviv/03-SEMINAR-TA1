# 04 – Hợp đồng API (v1)

> Phiên bản: v1 · Ngày: 09/11/2026 · Người phụ trách: Chờ nhóm điền
> Đầu vào: `seq-us-01..05-v1.puml`; `sys-us-01..05-v1.md`; [03-detailed-design-v1.md](03-detailed-design-v1.md) (tên, mã lỗi); [07-design-decisions-v1.md](07-design-decisions-v1.md) (DD-02, DD-07..12); `src/Qtkd.Api/Program.cs`
> AI: Claude Code / Claude Opus 5.5 · Prompt: P-22 trong [prompt-log](../../../workflow/prompt-log.md)
> Trạng thái: Bản lần chạy đầu – Design Pending Approval

Toàn bộ endpoint, field, mã HTTP là [ĐỀ XUẤT KỸ THUẬT] để hiện thực luồng trong
sys-us/seq; không phải yêu cầu của đề. Phần phụ thuộc OQ ghi `Blocked by OQ-…`.
Chưa có OpenAPI; file này là hợp đồng duy nhất.

## 1. Quy ước chung

| Mục | Quy ước | Căn cứ |
|---|---|---|
| Base path | `/api/payment-sheets` | DD-07 |
| Định dạng | JSON UTF-8; enum dạng chuỗi (như AS-IS `JsonStringEnumConverter`) | AS-IS `Program.cs` |
| Xác thực | Mọi endpoint yêu cầu người dùng đã xác thực; server lấy `userId`, `role` ∈ {`NVKD`, `KTT`, `GDKD`}. Cơ chế (cookie/token) chưa chọn – AS-IS chưa có | §2; 02 §3 |
| Version | Mọi thao tác ghi trên bảng đã có gửi `expectedVersion`; server ghi có điều kiện trạng thái + version | DD-02, DD-08 |
| Thành công | Trả `PaymentSheetDto` (trừ API form/preview) | DD-09 |
| Lỗi | `ApiError { code, message, details? }`; mã lỗi theo [03 §1.3](03-detailed-design-v1.md#13-mã-lỗi-chuẩn) | DD-09, DD-10 |
| Tiền, sản lượng | Số thập phân dạng **chuỗi** trong JSON (vd. `"125000000"`) để không mất chính xác; số chữ số thập phân/làm tròn Blocked by OQ-US03-03 | DD-04 |
| Kỳ | `period` – định dạng Blocked by OQ-01 (tạm `"2026-11"` cho tháng, `"2026-Q4"` cho quý) | OQ-01 |
| Thứ tự kiểm tra | Xác thực → vai trò → tồn tại → quyền trên bảng → trạng thái/version → quy tắc PAY → ghi | 03 §2 |

### 1.1. Kiểu dữ liệu

```json
// PaymentSheetDto
{
  "id": "3f2c…",
  "contractId": 101,
  "period": "2026-11",
  "priceListId": "PL-2026-01",
  "status": "Draft",                 // Draft | PendingApproval | Approved | Rejected | Cancelled
  "totalAmount": "125000000",
  "lines": [ /* PaymentLineDto */ ],
  "createdBy": "nvkd01",
  "createdAt": "2026-11-09T08:00:00+07:00",
  "submittedBy": null, "submittedAt": null,
  "decidedBy": null, "decidedAt": null,
  "rejectionReason": null,
  "cancelReason": null,
  "version": 1
}

// PaymentLineDto
{ "serviceCode": "SV01", "quantity": "1000", "unitPrice": "125000",
  "lineAmount": "125000000", "quantitySourceRef": "Q-…", "priceSourceRef": "PL-…#SV01",
  "calculatedAt": "2026-11-09T08:00:00+07:00" }

// ApiError
{ "code": "INVALID_STATE", "message": "Bảng không ở trạng thái cho phép thao tác.",
  "details": [ { "field": "period", "code": "INVALID_PERIOD" } ] }
```

## 2. Danh sách endpoint

| # | Method + path | Thao tác | Vai trò | Đổi trạng thái | US |
|---|---|---|---|---|---|
| E1 | `GET /api/payment-sheets/form/contracts` | OpenCreateForm | NVKD | – | 01 |
| E2 | `GET /api/payment-sheets/form/contracts/{contractId}` | SelectContract | NVKD | – | 01 |
| E3 | `GET /api/payment-sheets/form/contracts/{contractId}/price-lists?period=` | SelectPeriod | NVKD | – | 01 |
| E4 | `POST /api/payment-sheets/preview` | Preview | NVKD | – | 01 |
| E5 | `POST /api/payment-sheets` | create | NVKD | `[*]` → `Draft` | 01 |
| E6 | `GET /api/payment-sheets/{id}` | OpenDraft / xem để thao tác | Theo quyền thao tác | – | 01–05 |
| E7 | `GET /api/payment-sheets?contractId=&period=` | Kiểm tra kết quả khi `RESULT_UNKNOWN` | NVKD | – | 01 |
| E8 | `PUT /api/payment-sheets/{id}` | update | NVKD | `Draft` → `Draft` | 01 |
| E9 | `POST /api/payment-sheets/{id}/submit` | submit | NVKD | `Draft` → `PendingApproval` | 02 |
| E10 | `POST /api/payment-sheets/{id}/approve` | approve | KTT / GĐKD | `PendingApproval` → `Approved` | 03 |
| E11 | `POST /api/payment-sheets/{id}/reject` | reject | KTT / GĐKD | `PendingApproval` → `Rejected` / `Draft` (OQ-04) | 03 |
| E12 | `POST /api/payment-sheets/{id}/adjustments` | adjust | KTT | Blocked by OQ-03 | 04 |
| E13 | `POST /api/payment-sheets/{id}/cancel` | cancel | Blocked by OQ-US05-01 | `Draft` → `Cancelled` | 05 |

Không có endpoint ghi tới hợp đồng, bảng giá, sản lượng (TA-SPEC §1). E6/E7 là API đọc
phục vụ luồng thao tác, không phải chức năng tra cứu mới.

## 3. Chi tiết endpoint

### E1–E4. Form lập bảng (US-PAY-01, chỉ đọc)

Không ghi bảng, không ghi audit thay đổi bảng (sys-us-01 §1.3 bước 1–12).

| # | Request | Response 200 | Lỗi | Ghi chú |
|---|---|---|---|---|
| E1 | – | `{ contracts: [{ contractId, contractNo, customerName, status }] }` | 401, 403 `FORBIDDEN`, 503 `SOURCE_UNAVAILABLE` | Phạm vi danh sách Blocked by OQ-US01-03 |
| E2 | path `contractId` | `{ contract, periodConfig }` | 404 `NOT_FOUND`, 409 `CONTRACT_NOT_ACTIVE`, 503 | Mốc Active: OQ-US01-05 |
| E3 | `period` (query) | `{ priceLists: [{ priceListId, name, effectiveFrom, effectiveTo }] }` | 400 `INVALID_PERIOD`, 409 `PAYMENT_EXISTS`, 409 `PRICE_NOT_SUITABLE`, 503 | Kỳ: OQ-01; trùng: OQ-US05-02; tiêu chí giá: OQ-US01-01 |
| E4 | `{ contractId, period, priceListId }` | `{ lines: [PaymentLineDto], totalAmount, calculationContext }` | 400 `INVALID_INPUT`, 409 `PRICE_NOT_SUITABLE`, 409 `QUANTITY_NOT_RECONCILED`, 503 | `lineAmount = quantity × unitPrice` (PAY-03); xử lý tiền cuối: OQ-US03-03; dữ liệu rỗng: OQ-US01-04 |

`calculationContext` là token mô tả lần tính (thời điểm, phiên bản nguồn) để E5 so
sánh; server **không** tin tổng/dòng client gửi lại.

### E5. Tạo bảng Draft – `POST /api/payment-sheets`

| Mục | Nội dung |
|---|---|
| Vai trò | NVKD (§2, §4.1); phạm vi hợp đồng: Blocked by OQ-US01-03 |
| Request | `{ "contractId": 101, "period": "2026-11", "priceListId": "PL-2026-01", "calculationContext": "…" }` |
| Xử lý | Tái kiểm tra PAY-01..03 phía server, tính lại dòng, ghi bảng + dòng + audit `create` trong một giao dịch; ràng buộc duy nhất theo kỳ khi ghi |
| 201 | `PaymentSheetDto` với `status = Draft`, `version = 1`; header `Location: /api/payment-sheets/{id}` |
| Lỗi | 400 `INVALID_INPUT`/`INVALID_PERIOD`; 401; 403 `FORBIDDEN`; 409 `CONTRACT_NOT_ACTIVE`, `PAYMENT_EXISTS`, `PRICE_NOT_SUITABLE`, `QUANTITY_NOT_RECONCILED`; 503 `SOURCE_UNAVAILABLE`, `RESULT_UNKNOWN`; 500 `PERSISTENCE_ERROR` |
| Trùng lặp | Gửi lại sau khi đã tạo → 409 `PAYMENT_EXISTS` (ràng buộc duy nhất). Sau `RESULT_UNKNOWN`, client gọi E7 trước khi gửi lại (sys-us-01 A15.2) |
| Blocked | Phạm vi duy nhất OQ-01, OQ-US05-02; nguồn đổi giữa preview và create OQ-US01-01/04/05 |
| AC | AC-US01-01, 04–16, 20, 26 |

### E6. Đọc bảng – `GET /api/payment-sheets/{id}`

200 `PaymentSheetDto` (gồm `version` để gửi lại ở thao tác ghi). Lỗi 401, 403, 404.
Ai được đọc bảng nào: theo quyền thao tác tương ứng (OQ-US01-03, OQ-US02-01, OQ-US05-01);
người duyệt đọc bảng `PendingApproval` cần duyệt. [ĐỀ XUẤT KỸ THUẬT]

### E7. Tìm theo hợp đồng + kỳ – `GET /api/payment-sheets?contractId=&period=`

200 `{ items: [PaymentSheetDto] }` (có thể gồm bảng `Cancelled`). Chỉ phục vụ xác minh
kết quả tạo khi `RESULT_UNKNOWN` (sys-us-01 A15.2). [ĐỀ XUẤT KỸ THUẬT]

### E8. Sửa Draft – `PUT /api/payment-sheets/{id}`

| Mục | Nội dung |
|---|---|
| Vai trò | NVKD; quyền sửa Draft của người khác: Blocked by OQ-US01-03 |
| Request | `{ "expectedVersion": 3, "changes": { … } }` – **cấu trúc `changes` Blocked by OQ-US01-02** (trường nào được sửa, có đọc lại nguồn không) |
| Xử lý | Kiểm tra `Draft` + version, tính lại phía server, cập nhật có điều kiện, audit `update` với Before/After |
| 200 | `PaymentSheetDto`, `version` tăng 1 |
| Lỗi | 400 `INVALID_INPUT`, `VERSION_REQUIRED`; 401; 403; 404; 409 `INVALID_STATE`, `CONCURRENT_MODIFICATION`; 503 `RESULT_UNKNOWN`; 500 `PERSISTENCE_ERROR` |
| Rejected | Sửa bảng `Rejected`: Blocked by OQ-04, OQ-US03-07 – hiện trả 409 `INVALID_STATE` |
| AC | AC-US01-17, 18, 19 |

### E9. Trình duyệt – `POST /api/payment-sheets/{id}/submit`

| Mục | Nội dung |
|---|---|
| Vai trò | NVKD; bảng nào được trình: Blocked by OQ-US02-01 |
| Request | `{ "expectedVersion": 4 }` |
| Xử lý | Kiểm tra `Draft`; PAY-04: `totalAmount < 0` → chặn, `= 0` không chặn; thiếu dòng bắt buộc → chặn (Blocked by OQ-05); xác định vai trò người duyệt theo tổng (đúng 500 triệu Blocked by OQ-02); chuyển `PendingApproval` + audit `submit` trong giao dịch; sau commit gửi thông báo |
| 200 | `PaymentSheetDto` với `status = PendingApproval`, kèm `notification: { status: "Sent" \| "Failed" }` – xử lý khi `Failed` Blocked by OQ-US02-02 |
| Lỗi | 400 `NEGATIVE_TOTAL`, `REQUIRED_SERVICE_MISSING`, `VERSION_REQUIRED`; 401; 403; 404; 409 `DUPLICATE_SUBMIT` (đã `PendingApproval`), `INVALID_STATE` (`Approved`, `Cancelled`, `Rejected`), `CONCURRENT_MODIFICATION`; 500 `PERSISTENCE_ERROR` |
| Chống trùng (PAY-04) | (1) Bảng đã `PendingApproval` → `DUPLICATE_SUBMIT`; (2) hai request cùng `expectedVersion` → chỉ một ghi được, request kia `CONCURRENT_MODIFICATION`; không có audit cho request thua |
| AC | AC-US02-01..13 |

### E10. Duyệt – `POST /api/payment-sheets/{id}/approve`

| Mục | Nội dung |
|---|---|
| Vai trò | KTT hoặc GĐKD theo tổng (PAY-06; đúng 500 triệu: OQ-02; vai trò/cá nhân: OQ-US03-02) |
| Request | `{ "expectedVersion": 5 }` |
| Xử lý | `PendingApproval`; vai trò đúng; `userId != createdBy` (PAY-07; người lập: OQ-US03-01); chuyển `Approved` + audit `approve`; sau commit thông báo kết quả (OQ-US03-05) |
| 200 | `PaymentSheetDto` với `status = Approved`, `decidedBy`, `decidedAt` |
| Lỗi | 400 `VERSION_REQUIRED`; 401; 403 `FORBIDDEN`, `APPROVER_NOT_AUTHORIZED`, `SELF_APPROVAL_FORBIDDEN`; 404; 409 `INVALID_STATE`, `CONCURRENT_MODIFICATION`; 500 `PERSISTENCE_ERROR` |
| AC | AC-US03-01, 03–08, 12–15 |

### E11. Từ chối – `POST /api/payment-sheets/{id}/reject`

| Mục | Nội dung |
|---|---|
| Vai trò | Như E10; PAY-07 với từ chối: Blocked by OQ-US03-01 |
| Request | `{ "expectedVersion": 5, "reason": "Sai sản lượng dịch vụ SV02" }` |
| Validation | `reason` bắt buộc, không chỉ khoảng trắng (PAY-08); giới hạn độ dài: [GIẢ ĐỊNH – Cần xác nhận] OQ-US03-04 |
| Xử lý | Lưu `rejectionReason` + audit `reject` có `reason` (DD-12); trạng thái đích **Blocked by OQ-04**: phương án §3 → `Rejected`, phương án PAY-08 → `Draft` |
| 200 | `PaymentSheetDto` với `status` theo OQ-04 và `rejectionReason` |
| Lỗi | 400 `REASON_REQUIRED`, `REASON_TOO_LONG`, `VERSION_REQUIRED`; 401; 403 như E10; 404; 409 `INVALID_STATE`, `CONCURRENT_MODIFICATION`; 500 |
| AC | AC-US03-02, 03–07, 09–14 |

### E12. Điều chỉnh bảng Approved – `POST /api/payment-sheets/{id}/adjustments`

**Toàn bộ endpoint Blocked by OQ-03.** Vẽ cả hai phương án để trao đổi.

| Mục | Nội dung |
|---|---|
| Vai trò | KTT (§4.4) |
| Request | `{ "expectedVersion": 6, "content": "Giảm 5.000.000 đ do sai sản lượng SV02", "minutesRef": "BB-2026-11-015", "changes": { … } }` – `minutesRef` là mã biên bản đã lưu; cách tải tệp biên bản chưa thiết kế; tiêu chí biên bản và `changes`: Blocked by OQ-US04-01 |
| Phương án A | Tạo `PaymentAdjustment` liên kết bảng; bảng giữ `Approved`, `version` không đổi; 201 `{ adjustmentId, paymentSheet: PaymentSheetDto }` |
| Phương án B | Cập nhật trường được phép trên bảng gốc theo ngoại lệ PAY-05; `version` tăng; 200 `PaymentSheetDto`; trạng thái sau điều chỉnh/duyệt lại: OQ-US04-02 |
| Cả hai | Audit `adjust` có Before/After, `attachmentRef = minutesRef`, cùng giao dịch |
| Lỗi | 400 `INVALID_INPUT` (thiếu biên bản/nội dung), `VERSION_REQUIRED`; 401; 403 `FORBIDDEN`; 404; 409 `INVALID_STATE` (không `Approved`), `CONCURRENT_MODIFICATION`; 500 |
| AC | AC-US04-01..10 |

### E13. Hủy bảng nháp – `POST /api/payment-sheets/{id}/cancel`

| Mục | Nội dung |
|---|---|
| Vai trò | Blocked by OQ-US05-01 (người lập / NVKD phụ trách / cả KTT, GĐKD) |
| Request | `{ "expectedVersion": 2, "reason": "Lập nhầm kỳ" }` – `reason` bắt buộc/tùy chọn: Blocked by OQ-US05-03 |
| Xử lý | Chỉ `Draft`; chuyển `Cancelled`, lưu `cancelReason` (nếu có) + audit `cancel` trong giao dịch |
| 200 | `PaymentSheetDto` với `status = Cancelled` |
| Lỗi | 400 `REASON_REQUIRED` (nếu bắt buộc), `VERSION_REQUIRED`; 401; 403; 404; 409 `INVALID_STATE`, `CONCURRENT_MODIFICATION`; 500 `PERSISTENCE_ERROR` |
| Sau hủy | Mọi thao tác ghi trên bảng `Cancelled` → 409 `INVALID_STATE`. Lập bảng mới cùng kỳ: Blocked by OQ-US05-02 |
| AC | AC-US05-01..09 |

## 4. Ví dụ

Trình duyệt thành công:

```http
POST /api/payment-sheets/3f2c…/submit
Content-Type: application/json

{ "expectedVersion": 4 }
```

```http
HTTP/1.1 200 OK
{ "id": "3f2c…", "status": "PendingApproval", "totalAmount": "125000000",
  "version": 5, "notification": { "status": "Sent" }, … }
```

Trình lại lần hai (PAY-04):

```http
HTTP/1.1 409 Conflict
{ "code": "DUPLICATE_SUBMIT", "message": "Bảng đã được trình duyệt." }
```

Người lập tự duyệt (PAY-07):

```http
POST /api/payment-sheets/3f2c…/approve      (userId = createdBy)
HTTP/1.1 403 Forbidden
{ "code": "SELF_APPROVAL_FORBIDDEN", "message": "Người lập không được duyệt bảng của mình." }
```

Từ chối thiếu lý do (PAY-08):

```http
POST /api/payment-sheets/3f2c…/reject
{ "expectedVersion": 5, "reason": "   " }

HTTP/1.1 400 Bad Request
{ "code": "REASON_REQUIRED", "message": "Phải nhập lý do từ chối." }
```

## 5. Đối chiếu sequence ↔ endpoint

| Sequence | Message trong seq | Endpoint |
|---|---|---|
| seq-us-01 | `openCreateForm`, `selectContract`, `selectPeriod`, `preview`, `create`, `openDraft`, `update` | E1, E2, E3, E4, E5, E6, E8 |
| seq-us-02 | `submit(id)` | E9 (thêm `expectedVersion` – DD-08) |
| seq-us-03 | `approve(paymentId)`, `reject(paymentId, reason)`; path `/api/payments/...` | E10, E11 (path đổi – DD-07) |
| seq-us-04 | `Adjust(mã bảng, nội dung, biên bản)` | E12 |
| seq-us-05 | `POST /api/payment-sheets/{id}/cancel` | E13 (409 thay cho 400 – DD-10) |
