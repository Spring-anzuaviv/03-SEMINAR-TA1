# SYS-PAY-01 — API contract lập và sửa Draft

08/11/2026 — **Design Pending Approval**. Đây là **[ĐỀ XUẤT KỸ THUẬT]** cho phiên bản [SYS-PAY-01 hiện hành](../../analysis/payment-management/sys-pay-01-lap-bang-thanh-toan-v01.md), không phải API đã triển khai. Nghiệp vụ theo TA-SPEC §4.1, PAY-01..03, §6 và BA CREATE/KT/USER-04; tên theo [03](03-detailed-design.md), dữ liệu theo [05](05-data-design.md), DD theo [07](07-design-decisions.md). Các phần Blocked giữ theo [01](01-requirements-summary.md).

## 1. Quy ước chung

- Base path `/api/payments`; JSON camelCase, enum dạng chuỗi như demo net8.0. Danh sách route hiện có chỉ phục vụ hợp đồng, không có payment API. Không dùng lại enum ContractStatus làm PaymentStatus.
- Mọi endpoint cần principal đã xác thực và vai trò NVKD. Actor/creator lấy server context, không nhận qua body. Cấu hình identity cụ thể chưa có trong AS-IS; header `Authorization: Bearer <token>` dưới đây là phương án tích hợp, không khẳng định đã có nhà cung cấp token. Các endpoint có paymentId kiểm tra người lập, Draft và hợp đồng hiệu lực. Snapshot luôn kiểm tra actor và contract/period phù hợp. [CREATE-03, CREATE-10; DD-06]
- `Content-Type: application/json` cho request body; response JSON. ID bảng/snapshot/request là UUID, contractId là int, các ID nguồn khác là chuỗi opaque. Không tự gán giới hạn độ dài nghiệp vụ chưa được xác nhận.
- Decimal dùng **chuỗi số hệ thập phân**, không dấu phân cách hàng nghìn, không float/exponent. Precision/scale và làm tròn Blocked by CREATE-07. Các ví dụ số nguyên chỉ minh họa serialization, không chốt thuật toán.
- Chỉ POST tạo Payment và PUT sửa Payment bắt buộc `Idempotency-Key: <UUID>`, ánh xạ requestId trong sequence. Hash gồm người gọi, method, target và canonical body (kể cả expectedVersion); cùng request/nội dung replay original status/body, header `Idempotency-Replayed: true`. Khác body/target dùng cùng mã -> 409 REQUEST_ID_REUSED. Các thao tác preview không ghi Payment/audit nghiệp vụ nên không cần receipt. [CREATE-12; DD-04]
- PUT yêu cầu `expectedVersion` trong body, không dùng thêm If-Match để tránh hai nguồn version. Kiểm tra version ngay tại ghi; retry đã commit được xử lý trước kiểm tra version cũ. [BA E9; DD-03]
- Không endpoint trình/duyệt/từ chối/điều chỉnh/hủy trong lần này. Không thêm endpoint CRUD hợp đồng, bảng giá, sản lượng. [TA-SPEC §1; phạm vi SYS-PAY-01]

## 2. DTO dùng chung

| DTO / trường | Kiểu | Quy tắc |
|---|---|---|
| PaymentPeriod | object | type=`Month` hoặc `Quarter`, year integer, periodNumber integer 1..12 hoặc 1..4; phù hợp cấu hình hợp đồng. Loại kỳ khác nhau nhưng chồng lấn còn CREATE-16. |
| DraftInput.contractId | int | Bắt buộc về cấu trúc lệnh; chỉ chọn khi tạo, update phải trùng contractId hiện có. |
| DraftInput.period | PaymentPeriod | Bắt buộc về cấu trúc; server kiểm tra kỳ và chống trùng cả Draft. |
| DraftInput.notes | string hoặc null | Cho sửa; bắt buộc nghiệp vụ/độ dài chưa chốt, CREATE-11a. |
| DraftInput.lines | array LineInput | Danh sách đầy đủ mà lệnh muốn lưu, không phải patch. Khi sửa dùng dữ liệu hiện có và thay các trường được phép. Minimum count chưa chốt CREATE-05/CREATE-11a. |
| LineInput.lineKey | string | Key kỹ thuật do preview cấp; dùng nhận diện dòng trong candidate, không phải nguồn có thể tin từ client. Cách sinh/gom chờ CREATE-06. |
| LineInput.serviceId | string | Dịch vụ; server đối chiếu nguồn/bảng giá. Quyền thêm/sửa dịch vụ không có nguồn còn CREATE-19. |
| LineInput.quantity | decimal string | Giá trị NVKD đề nghị; quyền sai khác số đã đối soát còn CREATE-19, precision CREATE-07. |
| LineInput.sourceLineRefs | array string | Liên kết nguồn từ preview; server xác minh, không tin client tự khẳng định đã đối soát. Cardinality và cách gom còn CREATE-05/06/19. |
| sourceBaseline | UUID | ID ảnh nguồn do server cấp; rawSource không bị thay bởi quantity sửa tay. Phải khớp người gọi và ngữ cảnh candidate. |
| acceptedSource | UUID | ID nguồn mới do server cấp trong SOURCE_CHANGED, không phải JSON bảng giá do client tự khai. |
| paymentId / expectedVersion | UUID / integer | Ngữ cảnh sửa, version dương; bản cập nhật tăng version sau commit. |

Requiredness về cấu trúc API giúp server xác định thao tác; không tự giải quyết danh sách trường **nghiệp vụ** bắt buộc tại CREATE-11a. Các khóa do server quản lý (`creatorId`, `status`, `unitPrice`, `amount`, `totalAmount`, `priceListRef`, timestamps) không được gửi như giá trị ghi đè; trả 400 INVALID_INPUT nếu cố gửi. Bảng giá trong CREATE-08 được thể hiện bằng việc hệ thống xác định/cập nhật giá hiện hành theo KT-01, không mở quyền chọn bảng hết hiệu lực.

DraftPreview trả `contractId`, `period`, `notes`, `lines` (lineKey, serviceId, sourceLineRefs, quantity, unitPrice, amount), `priceListRef`, `totalAmount`, `sourceBaseline`; nếu ngữ cảnh update thì thêm `paymentId`, `version`. PaymentView có cùng dữ liệu cộng `paymentId`, `creatorId`, `status`, `version`, `createdAt`, `updatedAt` và `lines[].lineId`. Không có createdBy giả từ client. Snapshot và dữ liệu tính giá được kiểm soát tại server.

## 3. Danh mục endpoint

| Mã | HTTP / endpoint | Service | Thành công | Idempotency / concurrency | Quy tắc và AC |
|---|---|---|---|---|---|
| API-01 | POST /api/payments/draft-previews | prepareDraft | 200 DraftPreview | Không tạo Payment/khóa kỳ; preview có thể lỗi thời lúc Lưu. | US-PAY-01; PAY-01..03; AC-US01-01..07 |
| API-02 | GET /api/payments/{paymentId}/draft | openDraft | 200 PaymentView | Đọc version và sourceBaseline đã lưu, không tự ghi đè nguồn. | CREATE-03, CREATE-10; AC-US01-08 |
| API-03 | POST /api/payments/draft-previews/changes | previewChanges | 200 DraftPreview | Không ghi Payment; kiểm tra lại người lập nếu có paymentId. | CREATE-08; AC-US01-09 |
| API-04 | POST /api/payments/draft-previews/refresh | refreshPreview | 200 DraftPreview | Không ghi Payment; xác nhận nguồn mới không đồng nghĩa lưu. | CREATE-09; KT-02; AC-US01-11 |
| API-05 | POST /api/payments | saveDraft(create) | 201 PaymentView; Location /api/payments/{paymentId}/draft | Idempotency-Key; unique live-period và receipt tại ghi. | CREATE-12; KT-04; AC-US01-03, 07, 10..13, 15 |
| API-06 | PUT /api/payments/{paymentId}/draft | saveDraft(update) | 200 PaymentView | Idempotency-Key và expectedVersion; unique kỳ loại chính bảng đang sửa. | CREATE-08, CREATE-10, CREATE-12; AC-US01-08..15 |

API-01..06 đều áp dụng auth/ownership như Mục 1 và bảng lỗi Mục 6. Không có pagination, endpoint danh sách hoặc public GET cho vai trò khác vì chưa được giao phạm vi đó.

## 4. Request/response từng thao tác

### API-01 — Chuẩn bị bảng mới

Body: `contractId`, `period`. Server kiểm tra hợp đồng, kỳ, trùng chưa Cancelled, giá và đối soát, lưu snapshot kỹ thuật, trả DraftPreview. Bảng Draft chưa được tạo. Lỗi cụ thể: 409 CONTRACT_INACTIVE/DUPLICATE_PERIOD/PRICE_LIST_INVALID/PRODUCTION_NOT_RECONCILED; 503 SOURCE_UNAVAILABLE hoặc STORE_UNAVAILABLE.

```json
{
  "contractId": 12,
  "period": { "type": "Month", "year": 2026, "periodNumber": 10 }
}
```

Ví dụ DraftPreview cho trường hợp dữ liệu đủ điều kiện, số nguyên không cần minh họa làm tròn:

```json
{
  "contractId": 12,
  "period": { "type": "Month", "year": 2026, "periodNumber": 10 },
  "notes": null,
  "lines": [
    { "lineKey": "line-1", "serviceId": "SVC-01", "sourceLineRefs": ["PROD-01"], "quantity": "2", "unitPrice": "100000", "amount": "200000" }
  ],
  "priceListRef": "PRICE-2026-10",
  "totalAmount": "200000",
  "sourceBaseline": "00000000-0000-4000-8000-000000000001"
}
```

Chưa có quy tắc hoàn chỉnh cho dữ liệu rỗng/đối soát một phần, sinh dòng và precision: Blocked by CREATE-05, CREATE-06, CREATE-07. Không trả thành công giả cho các phần chưa có chính sách.

### API-02 — Mở Draft để sửa

Path: paymentId UUID; không body. Server kiểm tra bảng tồn tại, Draft, creatorId=principal, hợp đồng chưa hết hiệu lực; trả PaymentView với version và sourceBaseline đã dùng khi lưu. Dữ liệu nguồn hiện tại không thay đổi bản đã lưu; so sánh lại khi preview hoặc save. Lỗi 404 NOT_FOUND, 403 FORBIDDEN, 409 INVALID_STATE/CONTRACT_INACTIVE, 503 lỗi nguồn/kho. Đọc không tạo audit điều chỉnh.

### API-03 — Xem trước chỉnh sửa

Body: `input: DraftInput`, `sourceBaseline`; thêm `paymentId` nếu sửa bảng đã có. Server kiểm tra quyền/ngữ cảnh, đọc lại nguồn khi đổi kỳ/dịch vụ, kiểm tra trùng loại chính bảng đang sửa, tính lại; trả DraftPreview. Đổi kỳ có chủ đích tạo baseline cho kỳ mới, không coi việc khác kỳ cũ là nguồn tự thay đổi. Với cùng ngữ cảnh mà rawSource đổi, trả 409 SOURCE_CHANGED; client sửa input không được giả là nguồn đổi. Lỗi INPUT/INVALID_STATE/DUPLICATE_PERIOD/SOURCE_CHANGED, lỗi auth hoặc upstream như Mục 6. Không tạo Payment hoặc audit nghiệp vụ.

### API-04 — Xác nhận cập nhật nguồn

Body: `input: DraftInput`, `sourceBaseline` cũ và `acceptedSource` mới; nếu sửa thêm `paymentId`. Hai snapshot đều phải server cấp và thuộc principal/ngữ cảnh. Server xác minh nguồn mới chưa đổi tiếp; nếu đổi nữa, trả SOURCE_CHANGED với diff mới. Khi hợp lệ, tạo DraftPreview mới với sourceBaseline=nguồn được chấp nhận và tiền tính lại; NVKD xem lại rồi bấm Lưu. Body không được gửi bảng giá/nguồn tùy ý. **Blocked by CREATE-20** cho cách hợp nhất phần sửa tay và nguồn mới; CREATE-19 cho lượng cuối khác đối soát. Đây là hợp đồng khung, không tự chọn hợp nhất toàn bộ hoặc một phần.

### API-05 — Lưu mới

Header Idempotency-Key bắt buộc. Body: `input: DraftInput`, `sourceBaseline`; không paymentId, không expectedVersion. Ví dụ:

```json
{
  "input": {
    "contractId": 12,
    "period": { "type": "Month", "year": 2026, "periodNumber": 10 },
    "notes": null,
    "lines": [ { "lineKey": "line-1", "serviceId": "SVC-01", "sourceLineRefs": ["PROD-01"], "quantity": "2" } ]
  },
  "sourceBaseline": "00000000-0000-4000-8000-000000000001"
}
```

Server nhận diện receipt trước kiểm tra dành cho ghi mới; sau đó kiểm tra lại hợp đồng/nguồn/trường bắt buộc và receipt+xung đột cùng kỳ. Nguồn đổi -> SOURCE_CHANGED, chưa lưu. Tính tiền lại, giao dịch unique kỳ/receipt + bảng/dòng/audit, commit rồi trả 201. Snapshot hoặc quantity do client không được tin chỉ vì có ID hợp lệ. Lỗi thêm 409 DUPLICATE_PERIOD/REQUEST_ID_REUSED/SOURCE_CHANGED, 400 INVALID_INPUT, 500 SAVE_FAILED; không auto-submit. Bảng Cancelled không ngăn lập lại; response có ID mới.

### API-06 — Lưu thay đổi Draft

Path paymentId; header Idempotency-Key; body giống API-05 cộng `expectedVersion` dương. PUT thay toàn bộ tập dòng và dữ liệu được phép, không đổi hợp đồng hoặc người lập; không phải cập nhật từng trường tùy ý. Server kiểm tra creatorId, Draft, version, nguồn và unique kỳ loại chính paymentId. Commit thành công tăng version, giữ createdAt/creatorId và cập nhật updatedAt. Lỗi thêm 409 VERSION_CONFLICT/INVALID_STATE và 403 FORBIDDEN/404 NOT_FOUND. Retry cùng request cũ thành công được replay **trước** kiểm tra version cũ, không tăng version lần nữa.

### Ví dụ PaymentView sau commit API-05

```json
{
  "paymentId": "00000000-0000-4000-8000-000000000010",
  "contractId": 12,
  "creatorId": "user-17",
  "period": { "type": "Month", "year": 2026, "periodNumber": 10 },
  "status": "Draft",
  "notes": null,
  "lines": [
    { "lineId": "00000000-0000-4000-8000-000000000011", "lineKey": "line-1", "serviceId": "SVC-01", "sourceLineRefs": ["PROD-01"], "quantity": "2", "unitPrice": "100000", "amount": "200000" }
  ],
  "priceListRef": "PRICE-2026-10",
  "totalAmount": "200000",
  "sourceBaseline": "00000000-0000-4000-8000-000000000001",
  "version": 1,
  "createdAt": "2026-11-08T03:00:00Z",
  "updatedAt": "2026-11-08T03:00:00Z"
}
```

## 5. Chống trùng và đồng thời

1. Unique receipt(actorId,requestId), so canonical requestHash; cùng request replay original response, không thêm audit. Kết quả có thể cũ nếu bảng đã được sửa sau đó; client gọi API-02 để đọc trạng thái mới khi cần. Không trả receipt người khác.
2. Unique live-period(contractId,type,year,periodNumber) với status khác Cancelled bảo vệ cả hai insert qua kiểm tra sơ bộ. Update kiểm tra thêm version ngay tại ghi và loại chính bảng khỏi lookup. Chi tiết transaction tại 05; khi unique conflict phải đọc receipt để phân biệt cùng thao tác và bảng khác.
3. Nguồn đọc lại trước lưu không bảo đảm nguyên tử xuyên module; OQ-D-01 chưa chốt. Không khẳng định giao dịch thanh toán khóa module nguồn. Việc mất kết nối sau commit không rollback được commit đã thành công; retry phải lấy receipt.
4. Body sửa khác phải dùng requestId mới. Snapshot mới được xác nhận trong A9 cũng là thay đổi nội dung, không tái dùng mã của nội dung cũ. Các lần lỗi chưa commit không có success receipt.

## 6. Error contract

Giữ hai trường code/message của demo, bổ sung details/traceId theo **DD-06**; các mã là đề xuất API, không phải mã trong TA-SPEC. Không dùng HTTP 200 cho lỗi nghiệp vụ.

| HTTP | Code | Điều kiện / response details |
|---|---|---|
| 400 | INVALID_INPUT | JSON/UUID/enum/decimal cấu trúc sai, thiếu trường cấu trúc hoặc trường nghiệp vụ sau khi được chốt; details.fields là danh sách đường dẫn và lý do. |
| 401 | UNAUTHENTICATED | Không có principal hợp lệ. |
| 403 | FORBIDDEN | Sai vai trò, sai người lập hoặc snapshot không thuộc người gọi. |
| 404 | NOT_FOUND | Payment yêu cầu không tồn tại. |
| 409 | CONTRACT_INACTIVE | Không Active hoặc hết hiệu lực. |
| 409 | DUPLICATE_PERIOD | Có bảng khác chưa Cancelled cùng hợp đồng/kỳ, kể cả Draft; không tự lộ dữ liệu người khác. |
| 409 | PRICE_LIST_INVALID | Không có đúng một bảng giá hiệu lực. |
| 409 | PRODUCTION_NOT_RECONCILED | Sản lượng dùng để lập chưa đáp ứng PAY-02; không tự quyết định đối soát một phần. |
| 409 | INVALID_STATE | Bảng không còn Draft khi đọc/sửa. |
| 409 | VERSION_CONFLICT | Version đã đổi; details.currentVersion, không ghi đè. |
| 409 | REQUEST_ID_REUSED | Cùng actor/requestId nhưng khác hash nội dung/method/target. |
| 409 | SOURCE_CHANGED | Nguồn thay đổi; details.sourceBaseline, acceptedSource và diff (sourceKey, field, before, after). Không ghi bảng. |
| 409 | SOURCE_BASELINE_INVALID | ID không tồn tại/không khớp ngữ cảnh input; không tin snapshot client tự khai. |
| 503 | SOURCE_UNAVAILABLE / STORE_UNAVAILABLE | Không đọc được nguồn/kho; không diễn giải như nguồn rỗng hoặc không trùng. |
| 500 | CALCULATION_FAILED / SAVE_FAILED | Lỗi kỹ thuật tính/ghi; rollback mọi ghi trong transaction. Không dùng mã này thay câu hỏi nghiệp vụ chưa chốt. |

```json
{
  "code": "SOURCE_CHANGED",
  "message": "Dữ liệu nguồn đã thay đổi. Vui lòng kiểm tra trước khi lưu.",
  "details": {
    "sourceBaseline": "00000000-0000-4000-8000-000000000001",
    "acceptedSource": "00000000-0000-4000-8000-000000000002",
    "diff": [ { "sourceKey": "PROD-01", "field": "quantity", "before": "2", "after": "3" } ]
  },
  "traceId": "trace-example"
}
```

## 7. Những phần chưa thể chốt và validation

Blocked by CREATE-05, CREATE-06, CREATE-07, CREATE-11a, CREATE-16, CREATE-19, CREATE-20, OQ-D-01. CREATE-17 giữ lệnh cấm khi hết hạn; CREATE-18 không mở cập nhật ngoài Draft. Không thêm lỗi “câu hỏi OQ chưa xác nhận” vào sản phẩm: phải giải quyết các policy trước triển khai endpoint phụ thuộc.

PAY-04 chưa được áp dụng thành cấm lưu tổng âm; PAY-05 được bảo vệ bằng only-Draft; PAY-06/07/08 và US-PAY-02..05 ngoài API lần này. Các ví dụ đã chọn dữ liệu số nguyên để minh họa JSON, chưa chứng minh thuật toán đạt. Chưa có OpenAPI hoặc API thực để chạy contract/integration test. Kế hoạch kiểm chứng tại [06](06-traceability-matrix.md).
