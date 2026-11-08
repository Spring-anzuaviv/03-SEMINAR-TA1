# SYS-PAY-01 — Thiết kế dữ liệu

08/11/2026 — **Design Pending Approval**. Phạm vi tạo/sửa Draft; [TA-SPEC](../../requirements/payment-management/spec.md) §1, §4.1, PAY-01..03, §6; [BA](../../analysis/payment-management/sys-pay-01-lap-bang-thanh-toan-v01.md) CREATE/KT/USER-04. Schema mới là **[ĐỀ XUẤT KỸ THUẬT]**; không phải migration đã chạy. Tên theo [03](03-detailed-design.md), class [class.puml](diagrams/class.puml), API theo [04](04-api-contract.md), quyết định theo [07](07-design-decisions.md).

## 1. Hiện trạng và quy ước

Đã đọc Program.cs, ContractService.cs, Contract.cs, Qtkd.Api.csproj: lưu hợp đồng bằng ConcurrentDictionary; chưa có CSDL, ORM, migration, identity hoặc bảng thanh toán. Không thiết kế CRUD bảng nguồn. contract_id là tham chiếu int tương thích ID demo; service_id/price_list_ref/source refs là khóa ngoài logic opaque, không tự thêm FK xuyên module. actor_id lấy từ principal, không nhận client khai.

UUID và Instant/UTC là lựa chọn kỹ thuật; JSON là dữ liệu có cấu trúc, DBMS chưa chọn. `DECIMAL(p,s)` là placeholder: **Blocked by CREATE-07** trước DDL vật lý, không chốt p/s và không dùng float/double. `nullable` của notes là khả năng lưu trữ, chưa quyết định nghiệp vụ notes tùy chọn (CREATE-11a). Nullable của các trường nghiệp vụ khác có thể phải điều chỉnh sau xác nhận.

## 2. Entity và cardinality

| Bảng | Class | Quan hệ và mục đích | Căn cứ |
|---|---|---|---|
| payments | Payment | Root 1 — 0..* lines; 1 — 0..* audit/receipts; mỗi bảng tham chiếu đúng một snapshot. | US-PAY-01; DD-02, DD-03 |
| payment_lines | PaymentLine | Mỗi dòng thuộc một bảng; chứa giá trị đã áp dụng, không đọc giá động khi mở bảng. | PAY-03; DD-05 |
| payment_source_snapshots | PaymentSourceSnapshot | Snapshot có thể chưa được Payment tham chiếu khi đang preview, hoặc được 0..* Payment tham chiếu theo lịch sử. | CREATE-09; KT-02; DD-02 |
| payment_audit_entries | PaymentAuditEntry | Mỗi audit thuộc một Payment; không xóa do Cancelled. | §6; KT-04 |
| payment_save_receipts | PaymentSaveReceipt | Một kết quả thành công của actor/request; một Payment có nhiều lần lưu. | CREATE-12; DD-04 |

0..* lines không cho phép tự động lưu rỗng: **Blocked by CREATE-05, CREATE-11a**. Không tạo bảng PaymentPeriod riêng; value object được nhúng vào các cột kỳ.

## 3. Chi tiết schema logic

### payments

| Cột | Kiểu | Null | Khóa/Constraint | Mô tả | Nguồn/Nhãn | OQ |
|---|---|---|---|---|---|---|
| id | UUID | Không | PK | paymentId; server cấp khi tạo thành công. | US-PAY-01; DD-03 | — |
| contract_id | int | Không | External logical ref | Không đổi khi sửa Draft. | CREATE-08; DD-06 | — |
| period_type | text/enum | Không | Month hoặc Quarter | Không phải trạng thái bảng. | §2; CREATE-01 | CREATE-16 |
| period_year | integer | Không | Cùng kỳ gồm cả năm | Kỳ lịch theo cấu hình nguồn. | CREATE-01; USER-04 | CREATE-16 |
| period_number | integer | Không | Month: 1..12; Quarter: 1..4 | Khóa kỳ logic, không dùng riêng số kỳ. | CREATE-01; DD-03 | CREATE-16 |
| creator_id | text | Không | Identity logical ref | Người tạo, không đổi khi update. | CREATE-10; DD-06 | — |
| status | text/enum | Không | Draft/PendingApproval/Approved/Rejected/Cancelled | Chỉ tạo/sửa Draft trong UC này. | TA-SPEC §3; US-PAY-01 | UC khác ngoài phạm vi |
| notes | text | Có | Requiredness nghiệp vụ chưa chốt | Ghi chú được sửa. | CREATE-08, CREATE-11 | CREATE-11a |
| total_amount | DECIMAL(p,s) | Không | Bằng tổng amount các dòng sau chính sách tính | Không thêm thuế/chiết khấu. | PAY-03; DD-05 | CREATE-06, CREATE-07 |
| source_snapshot_id | UUID | Không | FK -> payment_source_snapshots.id | API gọi sourceBaseline. | DD-02; CREATE-09 | OQ-D-01 |
| version | bigint | Không | Bắt đầu 1, tăng mỗi commit sửa | API version/expectedVersion, không tăng khi replay. | BA E9; DD-03 | — |
| created_at / updated_at | UTC timestamp | Không | Server clock | Thời điểm tạo/lần sửa; không lấy từ client. | §6; AC-US01-07 | — |

### payment_lines

| Cột | Kiểu | Null | Khóa/Constraint | Mô tả | Nguồn/Nhãn | OQ |
|---|---|---|---|---|---|---|
| id | UUID | Không | PK | ID dòng lưu bền vững. | DD-03 | — |
| payment_id | UUID | Không | FK -> payments.id | Composition; không tồn tại độc lập. | US-PAY-01 | — |
| line_key | text | Không | Unique(payment_id,line_key) | Key kỹ thuật phân biệt dòng trong preview/lệnh lưu. | DD-02 | CREATE-06 cho cách sinh key khi gom |
| service_id | text | Không | Logical ref | Dịch vụ, không tạo CRUD nguồn. | §2; CREATE-08 | CREATE-19 |
| source_line_refs | JSON array | Không | Không mặc định unique toàn module | Danh sách nguồn đã dùng; không chốt phải có bao nhiêu. | PAY-02; DD-02 | CREATE-05, CREATE-06, CREATE-19 |
| quantity | DECIMAL(p,s) | Không | Chưa tự cấm âm/zero | Lượng cuối được chấp nhận, khác rawSource nếu được phép. | PAY-03; CREATE-08 | CREATE-07, CREATE-19 |
| unit_price | DECIMAL(p,s) | Không | Chỉ server xác định | Giá tại mốc tính, không nhận client tự chọn. | PAY-03; CREATE-04 | CREATE-07 |
| amount | DECIMAL(p,s) | Không | Theo quantity×unitPrice và chính sách làm tròn | Không dùng float. | PAY-03; DD-05 | CREATE-07 |

### payment_source_snapshots

| Cột | Kiểu | Null | Khóa/Constraint | Mô tả | Nguồn/Nhãn | OQ |
|---|---|---|---|---|---|---|
| id | UUID | Không | PK | Server cấp; input sourceBaseline/acceptedSource chỉ là ID này. | DD-02 | — |
| actor_id | text | Không | Principal logical ref | Chặn sử dụng snapshot người khác. | CREATE-10; DD-06 | — |
| contract_id | int | Không | External logical ref | Phải khớp input. | PAY-01 | — |
| period_type / period_year / period_number | Như payments | Không | Khớp kỳ request | Đổi kỳ phải lấy baseline tương ứng, không tự tái dùng snapshot kỳ cũ. | CREATE-01, CREATE-08 | CREATE-16 |
| price_list_ref | text | Không | External logical ref | Bảng giá hiệu lực đã đọc; phiên bản nguồn nếu có nằm trong raw_source. | CREATE-04; DD-02 | OQ-D-01 |
| raw_source | JSON | Không | Immutable | Hợp đồng/hiệu lực/cấu hình kỳ, sản lượng gốc/đối soát, giá/đơn vị tính, source IDs và version nếu có. Không chứa chỉnh sửa giả làm nguồn. | PAY-01..03; DD-02 | CREATE-06, OQ-D-01 |
| source_fingerprint | text | Không | Digest chuẩn hóa raw_source | So sánh nguồn độc lập dữ liệu nhập. Không phải input được tin từ client. | CREATE-09; DD-02 | OQ-D-01 |
| captured_at | UTC timestamp | Không | Server clock | Mốc đọc nguồn, không khẳng định nguồn bị khóa tới commit. | PAY-03; DD-02 | OQ-D-01 |

Snapshot giữ bất biến để giải thích số tiền đã lưu. Khi nguồn đổi, **Draft được cập nhật lại qua A9 sau xác nhận**, không tự đổi dữ liệu đã commit do module nguồn thay đổi. Thời điểm tính mới thay source_snapshot_id của Payment và audit ghi before/after; snapshot cũ vẫn tồn tại. Không chốt snapshot vĩnh viễn cho Draft trái CREATE-09.

### payment_audit_entries

| Cột | Kiểu | Null | Khóa/Constraint | Mô tả | Nguồn/Nhãn | OQ |
|---|---|---|---|---|---|---|
| id | UUID | Không | PK | Audit append-only. | §6; DD-03 | — |
| payment_id | UUID | Không | FK -> payments.id | Không cascade xóa theo Cancelled. | KT-03, KT-04 | — |
| actor_id / occurred_at | text / UTC timestamp | Không | Server context | Ai, lúc nào. | §6 | — |
| action | text | Không | create hoặc update trong UC này | Không thiết kế các action duyệt/hủy ở đây. | US-PAY-01; DD-04 | CREATE-18 ngoài Draft |
| before_data | JSON | Có | Null khi tạo | Dữ liệu trước, bao gồm version và trạng thái nếu có. | §6; DD-03 | — |
| after_data | JSON | Không | Giá trị sau | ID, kỳ, dòng, tổng, snapshot, status, version để biết thay đổi gì. | §6; DD-03 | CREATE-07 với tiền |
| request_id | UUID | Không | Unique(actor_id,request_id) cho audit create/update này | Liên kết thao tác thành công; retry không thêm audit. | CREATE-12; DD-04 | — |

### payment_save_receipts

| Cột | Kiểu | Null | Khóa/Constraint | Mô tả | Nguồn/Nhãn | OQ |
|---|---|---|---|---|---|---|
| actor_id / request_id | text / UUID | Không | PK kép(actor_id,request_id) | Khóa toàn bộ thao tác save của người gọi, tránh va chạm route. | DD-04 | — |
| request_hash | text | Không | Hash canonical method+path+body+expectedVersion | Không hash trạng thái nguồn hiện tại vì retry có thể đến sau. | DD-04 | — |
| payment_id | UUID | Không | FK -> payments.id | Bảng đã commit; không tìm theo kỳ để giả làm retry. | CREATE-12 | — |
| response_status | integer | Không | 201 tạo / 200 cập nhật | Replay giữ original status. | API; DD-04 | — |
| response_data | JSON | Không | Immutable | Bản PaymentView sau lần commit; không bị ghi đè bởi các lần sửa sau. | DD-04 | — |
| completed_at | UTC timestamp | Không | Server clock | Chỉ visible cùng commit với dữ liệu nghiệp vụ. | KT-04 | — |

Không lưu access token trong receipt/audit. Replay chỉ trả kết quả đã commit của người gọi; response có thể là lịch sử, không khẳng định trạng thái hiện tại. Thời hạn lưu/dọn receipt chưa chọn, không tự hết hạn rồi cho thao tác cũ thực hiện lần nữa.

## 4. Constraint và index

| Ràng buộc/index logic | Mục đích / nguồn | Trạng thái |
|---|---|---|
| Unique(contract_id,period_type,period_year,period_number) **WHERE status <> Cancelled** | Chặn mọi bảng còn tồn tại cùng kỳ, kể cả Draft; CREATE-01, CREATE-02, CREATE-12, USER-04; DD-03. | Quy tắc đã xác nhận. Cú pháp vật lý phụ thuộc DBMS, không chốt tháng-only. |
| PK receipt(actor_id,request_id) | Chỉ một kết quả cho cùng thao tác; DD-04. | Thiết kế kỹ thuật; xử lý unique conflict bằng rollback rồi đọc receipt, so hash. |
| FK nội bộ payment_id và source_snapshot_id | Không có dòng/audit/receipt mồ côi; KT-04. | Không thêm FK xuyên module. |
| Unique(payment_id,line_key) | Không trùng key kỹ thuật trong một bảng. | Không ngăn các dòng khác giá cùng dịch vụ trước CREATE-06. |
| Index audit(payment_id,occurred_at,id) | Đọc lịch sử giải thích thay đổi; §6. | Không thiết kế endpoint audit ngoài phạm vi. |
| Index snapshot(actor_id,contract_id,period_*) | Xác minh chủ thể/ngữ cảnh preview; DD-02, DD-06. | Không thay ownership bằng ID khó đoán. |

Không có constraint total_amount>=0, VAT, ngưỡng duyệt hoặc dịch vụ bắt buộc khi lưu vì PAY-04 áp dụng ở trình duyệt, CREATE-11a chưa chốt. Unique cùng kỳ **không** giải quyết tháng 1/quý I chồng lấn: Blocked by CREATE-16.

## 5. Transaction và cập nhật đồng thời

1. Ngoài transaction: đọc lại nguồn, kiểm tra điều kiện và fingerprint; đối chiếu A9. Kiểm tra sơ bộ không thay ràng buộc tại ghi.
2. Trong transaction: kiểm tra receipt trước; khóa/so version khi sửa; kiểm tra hiệu lực theo dữ liệu nguồn vừa đọc và clock server; INSERT/UPDATE aggregate, thay tập dòng, tăng version; ghi audit và receipt.
3. Unique live-period bảo vệ hai INSERT hoặc hai UPDATE đổi kỳ. Unique receipt bảo vệ hai lần cùng mã. Có unique conflict: rollback transaction, đọc receipt cùng actor/request; cùng hash thì replay, khác hash báo REQUEST_ID_REUSED; không có receipt tương ứng thì DUPLICATE_PERIOD hoặc VERSION_CONFLICT theo nguyên nhân. Không trả lỗi trùng nhầm cho retry vừa hoàn tất.
4. Bất kỳ ghi/audit/receipt lỗi -> rollback; lỗi trước khi mở transaction không tạo Payment. Snapshot preview có thể tồn tại kỹ thuật, không được gọi là bảng nghiệp vụ lưu dở dang.
5. Update kiểm tra status=Draft, creator_id=actor, version=expectedVersion ngay tại ghi. Điều kiện sai không ghi đè. Toàn bộ source snapshot/version không đồng nghĩa transaction xuyên nguồn; **Blocked by OQ-D-01**.

## 6. API ↔ class ↔ cột

| JSON API | Class / cột | Ghi chú |
|---|---|---|
| paymentId, contractId, creatorId, status, version | Payment.id/contract_id/creator_id/status/version | Các trường do server quyết định trừ contractId khi tạo. |
| period.type/year/periodNumber | PaymentPeriod -> period_type/year/number | Snapshot dùng cùng cấu trúc. |
| notes, totalAmount | Payment.notes/total_amount | Tổng chỉ output. |
| lines[].lineKey/serviceId/sourceLineRefs/quantity/unitPrice/amount | PaymentLine -> cột snake_case tương ứng | Input không có unitPrice/amount; decimal output/input là chuỗi. |
| lines[].lineId | PaymentLine.id | Chỉ có sau lưu; input dùng lineKey. |
| sourceBaseline, acceptedSource | PaymentSourceSnapshot.id | Baseline lưu trên Payment; acceptedSource là tham số refresh, không cột Payment riêng. |
| priceListRef | Snapshot.price_list_ref | Output; không cho client chọn giá lịch sử. |
| expectedVersion | So với Payment.version | Input-only, không cột riêng. |
| Idempotency-Key | PaymentSaveReceipt.request_id; audit.request_id | Metadata HTTP, không thuộc DraftInput. |
| diff, code/message/details/traceId | DTO tạm hoặc error envelope | Không là entity nghiệp vụ. |

## 7. Liên quan các US/PAY khác và migration

US-PAY-02/PAY-04 cần validation trình và thông báo, US-PAY-03/PAY-06..08 cần quyết định duyệt/lý do/thẩm quyền: **chưa thiết kế schema riêng trong lần này**. Chỉ giữ creator_id và enum để không mâu thuẫn tên. PAY-05 được bảo vệ bằng việc chỉ sửa Draft; điều chỉnh US-PAY-04 ↔ PAY-05 còn OQ-P03-10 ở BA US-03, không tự thêm bảng biên bản hoặc phiên bản điều chỉnh. US-PAY-05 chỉ dùng tác động loại Cancelled khỏi unique theo quyết định đã chốt; không có endpoint hủy tại 04.

Migration đề xuất: chọn DBMS giao dịch, giải quyết p/s và các OQ, tạo schema/index/FK bằng migration mới, kiểm thử unique/rollback/replay bằng hai kết nối, rồi mới đưa vào ứng dụng. Không giả định dữ liệu Payment cũ cần migrate từ demo hợp đồng; không sửa bảng hợp đồng demo. Chưa viết hoặc chạy migration, chưa benchmark.

## 8. Open Questions và kiểm chứng

Danh sách đầy đủ tại [01 Mục 4](01-requirements-summary.md). Blocked by CREATE-05, CREATE-06, CREATE-07, CREATE-11a, CREATE-16, CREATE-17, CREATE-18, CREATE-19, CREATE-20, OQ-D-01. Không có giả định nghiệp vụ mới được đánh dấu đã duyệt. Bản này là schema logic, chưa phải DDL thực thi; không tuyên bố unique/transaction đã được kiểm thử.
