# SYS-PAY-01 — Ma trận truy vết

08/11/2026 — **Design Pending Approval**. Chỉ bổ sung thiết kế SYS-PAY-01; các US khác được liệt kê để thấy giới hạn bao phủ, không nhận là đã hoàn tất toàn module. AC-US01-01..15 tự đặt, định nghĩa tại [01](01-requirements-summary.md), không phải nguyên văn đề.

## 1. Nguồn và bản đã đọc

| Nguồn | Bản đọc / giới hạn |
|---|---|
| [TA-SPEC](../../requirements/payment-management/spec.md) §1–6 | TA-PDF theo sổ nguồn: §1–3 tr.1, §4–5 tr.2, §6 tr.3; chưa đọc lại PDF. |
| [BA SYS-PAY-01 v01](../../analysis/payment-management/sys-pay-01-lap-bang-thanh-toan-v01.md) | Working copy hiện hành, commit gần nhất của đường dẫn 184f006, có thay đổi chưa commit; commit không đại diện toàn bộ nội dung đang làm. |
| Ba sequence SYS-PAY-01 và [README](diagrams/README.md) | Sequence lập mới commit gần nhất 184f006, có thay đổi cục bộ; không tự coi là bản đã duyệt. |
| [01](01-requirements-summary.md), [03](03-detailed-design.md), [04](04-api-contract.md), [05](05-data-design.md), [07](07-design-decisions.md), [class.puml](diagrams/class.puml) | File mới của lần này, chưa commit, các thành phần là đề xuất TO-BE. |
| 02-architecture-design.md, 08-handoff-to-developer.md | Chưa có; không tạo/nhận đã đọc tài liệu không tồn tại. |

Cột thành phần ghi vai trò đã mô tả ở 03, đồng thời đánh dấu thiếu 02. Do chưa có bộ kiến trúc đầy đủ, các dòng làm được vẫn dùng **Thiết kế một phần** thay vì nhận đã thiết kế toàn diện. Các marker Blocked trong cột cuối giữ ID CREATE của BA, không đổi tên để khớp một mẫu mã OQ khác. Mọi cách kiểm chứng dưới đây là **kế hoạch chưa chạy**, không phải kết quả test.

## 2. Ma trận chính

| ID | Loại | Nguồn | Nội dung rút gọn | Thành phần (02) | UML / phần tử | API (04) | Class/method (03) | Dữ liệu (05) | Cách kiểm chứng đề xuất | Trạng thái | OQ/DD |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US-PAY-01 | US | TA-SPEC §4.1; tr.2; BA SYS-PAY-01 | Tạo/sửa Draft | PaymentApplicationService / Store; chưa có 02 | class.puml: Payment; sequence-sys-pay-01-lap-bang-thanh-toan.puml: prepareDraft/saveDraft | API-01..06 | prepareDraft/openDraft/previewChanges/refreshPreview/saveDraft | payments, lines, snapshots, audit, receipts | Kiểm thử chuỗi preview→create→open→update và lỗi; chưa chạy | Thiết kế một phần | Blocked by CREATE-05/06/07/11a/19/20; OQ-D-01; thiếu 02 |
| US-PAY-02 | US | TA-SPEC §4.2; tr.2 | Trình duyệt và thông báo | Ngoài phạm vi bản này | Chưa thiết kế sequence submit trong bộ bổ sung | Chưa thiết kế | Chưa thiết kế submit | Chưa có yêu cầu trình/thông báo | Bàn giao UC02; không gọi create là submit | Chưa thiết kế | PAY-04; không gán thông báo đã tồn tại |
| US-PAY-03 | US | TA-SPEC §4.3; tr.2 | Duyệt/từ chối | Ngoài phạm vi | Enum chỉ giữ tên, không mô tả quyết định | Chưa thiết kế | Không approve/reject trong service | Chưa có dữ liệu quyết định duyệt | Cần thiết kế UC03 độc lập theo BA tương ứng | Chưa thiết kế | OQ-P03-01, OQ-P03-02 trong BA US03; không chọn ngưỡng/đích trạng thái |
| US-PAY-04 | US | TA-SPEC §4.4; tr.2 | Điều chỉnh Approved | Ngoài phạm vi | Không vẽ lớp điều chỉnh/biên bản | Chưa thiết kế | Không adjust | Chưa có bảng biên bản/điều chỉnh | Cần chốt PAY-05↔US04 trước thiết kế | Chưa thiết kế | OQ-P03-10; CREATE-18 |
| US-PAY-05 | US | TA-SPEC §4.5; tr.2; BA CREATE-02 | Hủy và lập lại | PaymentApplicationService / Store; chưa có 02 | sequence-sys-pay-01-lap-bang-thanh-toan.puml: ghi chú Cancelled; class.puml: PaymentStatus | API-05 chỉ lập lại | prepareDraft/saveDraft | Unique loại Cancelled; không xóa lịch sử | Lập lại sau fixture Cancelled có ID mới; cancel chưa có test | Thiết kế một phần | Chưa thiết kế endpoint/quyền cancel; DD-03 |
| PAY-01 | PAY | TA-SPEC §5; tr.2; BA CREATE-01..04,12; USER-04 | Active, giá hợp lệ, duy nhất kỳ | PaymentApplicationService / Store; chưa có 02 | sequence-sys-pay-01-lap-bang-thanh-toan.puml: guard hợp đồng/trùng trước ghi và transaction | API-01,03,05,06 | lookupConflict/executeAtomicSave | Unique live-period, snapshots | Hai kết nối create cùng kỳ→một commit; khác năm không trùng | Thiết kế một phần | Blocked by CREATE-16/17; OQ-D-01; DD-01/03 |
| PAY-02 | PAY | TA-SPEC §5; tr.2 | Sản lượng đã đối soát | PaymentApplicationService / Store; chưa có 02 | sequence-sys-pay-01-lap-bang-thanh-toan.puml: guard sản lượng; class.puml: rawSource | API-01,03..06 | readCurrentSources | raw_source và source_line_refs | Nguồn chưa đối soát chặn; sửa quantity phải theo policy chốt | Thiết kế một phần | Blocked by CREATE-05, CREATE-19 |
| PAY-03 | PAY | TA-SPEC §5; tr.2 | Lượng×giá tại thời điểm tính | PaymentApplicationService / Store; chưa có 02 | class.puml: calculateAmount/recalculate; sequence-sys-pay-01-lap-bang-thanh-toan.puml: tính lại | Preview/PaymentView; API-01,03..06 | PaymentLine.calculateAmount, Payment.recalculate | quantity/unit_price/amount/total_amount/snapshot | Ví dụ số nguyên; kiểm thử làm tròn sau khi chốt | Thiết kế một phần | Blocked by CREATE-06, CREATE-07; DD-02/05 |
| PAY-04 | PAY | TA-SPEC §5; tr.2 | Tổng âm, dịch vụ bắt buộc, chống trình trùng | Ngoài phạm vi | Không vẽ submit; create receipt không phải chống trình trùng | Không submit | Chưa có validation submit | Không thêm constraint total>=0 cho Draft | Cần kiểm thử trình duyệt riêng | Chưa thiết kế | Danh sách dịch vụ bắt buộc chưa rõ; không tự áp dụng khi lưu |
| PAY-05 | PAY | TA-SPEC §5; tr.2 | Approved không được sửa | PaymentApplicationService / Store; chưa có 02 | class.puml: reviseDraft; sequence-sys-pay-01-sua-draft.puml: guard Draft | API-02,03,04,06 | reviseDraft / executeAtomicSave | status/version kiểm tra tại ghi | Gọi sửa Approved→INVALID_STATE, không thay dữ liệu | Thiết kế một phần | Ngoại lệ điều chỉnh US04 còn OQ-P03-10; phạm vi này chỉ Draft |
| PAY-06 | PAY | TA-SPEC §5 ↔ §4.3; tr.2 | Thẩm quyền theo ngưỡng | Ngoài phạm vi | Không mô hình ngưỡng | Chưa thiết kế | Không quyết định approver | Không hardcode threshold constraint | Cần chốt điểm đúng 500 triệu | Chưa thiết kế | OQ-P03-01; không áp dụng đề xuất US03 vào US01 |
| PAY-07 | PAY | TA-SPEC §5; tr.2 | Không tự duyệt bảng mình lập | PaymentApplicationService / Store; chưa có 02 | class.puml: creatorId | API-05 ghi người lập; chưa API duyệt | saveDraft lưu creatorId | payments.creator_id bất biến | Kiểm tra creator lấy principal; test cấm tự duyệt thuộc UC03 | Thiết kế một phần | Chưa có approve/reject enforcement; không đánh dấu đã đáp ứng |
| PAY-08 | PAY | TA-SPEC §5 ↔ §3; tr.1–2 | Lý do từ chối và quay về sửa | Ngoài phạm vi | Enum Rejected không quyết định bước mở lại | Chưa thiết kế | Không reject/reopen | Chưa có lý do từ chối | Cần chốt Rejected/Draft và mở lại | Chưa thiết kế | OQ-P03-02 |
| NFR-PAY-01 | NFR | TA-SPEC §6 gạch 1; tr.3 | Audit mọi đổi trạng thái/điều chỉnh | PaymentApplicationService / Store; chưa có 02 | class.puml: PaymentAuditEntry; sequence lưu: rollback/commit | API-05,06; replay không thêm audit | executeAtomicSave | payment_audit_entries cùng transaction | Inject lỗi audit→không Payment/dòng/receipt mới; đếm audit retry | Thiết kế một phần | Chỉ create→Draft và sửa Draft đã thiết kế; submit/approve/reject/adjust/cancel/reopen chưa có |
| NFR-PAY-02 | NFR | TA-SPEC §6 gạch 2; tr.3; CREATE-13; KT-05 | ≤3 giây khi <200 dòng | PaymentApplicationService / Store; chưa có 02 | sequence-sys-pay-01-lap-bang-thanh-toan.puml: bấm Lưu→kết quả sau commit | API-05,06 trong ngữ cảnh lập/lưu Draft | saveDraft | Index kỳ/receipt, batch lưu dòng | Đo từ UI click đến response sau commit với 199 dòng, ghi dữ liệu và thời gian; không tự gán SLA cho 200 dòng | Thiết kế một phần | Blocked by CREATE-06/07 cho dataset; chưa benchmark, chưa có 02 |
| AC-US01-01 | AC dẫn xuất | 01 Mục 3; PAY-01; CREATE-03 | Hợp đồng còn hiệu lực | PaymentApplicationService / Store; chưa có 02 | class.puml: readContract/saveDraft; ba sequence SYS-PAY-01 | API-01..06 | readContract/saveDraft | source snapshot/thời hạn | Đổi hiệu lực trước ghi, chặn lưu | Thiết kế một phần | Blocked by CREATE-17; OQ-D-01; thiếu 02 |
| AC-US01-02 | AC dẫn xuất | 01 Mục 3; §2; CREATE-01 | Kỳ tháng/quý/năm | PaymentApplicationService / Store; chưa có 02 | class.puml: PaymentPeriod; ba sequence SYS-PAY-01 | API-01,03,05,06 | PaymentPeriod | period_* | Thử tháng/quý không đúng cấu hình và cùng số kỳ khác năm | Thiết kế một phần | Blocked by CREATE-16 với chồng lấn; thiếu 02 |
| AC-US01-03 | AC dẫn xuất | 01 Mục 3; PAY-01; CREATE-12; USER-04 | Unique kể cả Draft / concurrent | PaymentApplicationService / Store; chưa có 02 | class.puml: lookupConflict/executeAtomicSave; ba sequence SYS-PAY-01 | API-01,03,05,06 | lookupConflict/executeAtomicSave | unique live-period | Hai request khác nhau cùng kỳ, một commit | Thiết kế một phần | DD-03; thiếu 02 |
| AC-US01-04 | AC dẫn xuất | 01 Mục 3; CREATE-02; KT-03 | Lập lại sau Cancelled | PaymentApplicationService / Store; chưa có 02 | class.puml: prepareDraft/saveDraft; ba sequence SYS-PAY-01 | API-01,05 | prepareDraft/saveDraft | unique loại Cancelled; audit cũ | ID mới, lịch sử cũ giữ nguyên | Thiết kế một phần | DD-03; thiếu 02 |
| AC-US01-05 | AC dẫn xuất | 01 Mục 3; PAY-01/02; CREATE-04 | Giá duy nhất và đối soát | PaymentApplicationService / Store; chưa có 02 | class.puml: readCurrentSources; ba sequence SYS-PAY-01 | API-01,03..06 | readCurrentSources | raw_source/source_line_refs | 0 hoặc 2 bảng giá hiệu lực; nguồn chưa đối soát | Thiết kế một phần | Blocked by CREATE-05/19; thiếu 02 |
| AC-US01-06 | AC dẫn xuất | 01 Mục 3; US-PAY-01; PAY-03 | Sinh dòng và tính tiền | PaymentApplicationService / Store; chưa có 02 | class.puml: calculateAmount/recalculate; ba sequence SYS-PAY-01 | API-01,03..06 | calculateAmount/recalculate | quantity/unit_price/amount/total_amount | Tính tiền và tổng, test làm tròn sau xác nhận | Thiết kế một phần | Blocked by CREATE-06/07; thiếu 02 |
| AC-US01-07 | AC dẫn xuất | 01 Mục 3; US-PAY-01; BA bước 6–10 | Draft sau commit, preview chưa có Payment | PaymentApplicationService / Store; chưa có 02 | class.puml: prepareDraft/saveDraft; ba sequence SYS-PAY-01 | API-01,05 | prepareDraft/saveDraft | Payment vs snapshot kỹ thuật | Đếm Payment trước/sau preview/save; status Draft | Thiết kế một phần | DD-02/03; thiếu 02 |
| AC-US01-08 | AC dẫn xuất | 01 Mục 3; CREATE-10; US-PAY-01 | Owner-only Draft | PaymentApplicationService / Store; chưa có 02 | class.puml: openDraft/reviseDraft; ba sequence SYS-PAY-01 | API-02..04,06 | openDraft/reviseDraft | creator_id/status/version | Người khác hoặc Approved không sửa được | Thiết kế một phần | DD-06; thiếu 02 |
| AC-US01-09 | AC dẫn xuất | 01 Mục 3; CREATE-08; BA A1 | Đổi trường phải kiểm tra lại | PaymentApplicationService / Store; chưa có 02 | class.puml: previewChanges/saveDraft; ba sequence SYS-PAY-01 | API-03,06 | previewChanges/saveDraft | period/lines và snapshot | Đổi kỳ sang kỳ đã có Draft; không đổi creator/contract | Thiết kế một phần | Blocked by CREATE-19/20; thiếu 02 |
| AC-US01-10 | AC dẫn xuất | 01 Mục 3; CREATE-11 | Trường bắt buộc | PaymentApplicationService / Store; chưa có 02 | class.puml: saveDraft; ba sequence SYS-PAY-01 | API-05,06 | saveDraft | nullability/validation | Thiếu từng trường phải báo đúng path | Thiết kế một phần | Blocked by CREATE-11a; thiếu 02 |
| AC-US01-11 | AC dẫn xuất | 01 Mục 3; CREATE-09; KT-02 | Nguồn đổi cần xác nhận | PaymentApplicationService / Store; chưa có 02 | class.puml: refreshPreview; ba sequence SYS-PAY-01 | API-03..06 | refreshPreview | snapshot rawSource độc lập input | Đổi nguồn sau preview→SOURCE_CHANGED, không ghi Payment | Thiết kế một phần | Blocked by CREATE-20; OQ-D-01; thiếu 02 |
| AC-US01-12 | AC dẫn xuất | 01 Mục 3; CREATE-12; KT-04 | Replay cùng request | PaymentApplicationService / Store; chưa có 02 | class.puml: getSaveReceipt/executeAtomicSave; ba sequence SYS-PAY-01 | API-05,06 | getSaveReceipt/executeAtomicSave | PK receipt và request_hash | Mất response rồi retry→original status/body, một audit; mã/body khác→409 | Thiết kế một phần | DD-04; thiếu 02 |
| AC-US01-13 | AC dẫn xuất | 01 Mục 3; §6; KT-04 | Atomicity bảng/dòng/audit/receipt | PaymentApplicationService / Store; chưa có 02 | class.puml: executeAtomicSave; ba sequence SYS-PAY-01 | API-05,06 | executeAtomicSave | giao dịch nội bộ | Inject lỗi từng bước, rollback không mồ côi | Thiết kế một phần | DD-03/04; thiếu 02 |
| AC-US01-14 | AC dẫn xuất | 01 Mục 3; BA E9; README sequence | Không ghi đè version cũ | PaymentApplicationService / Store; chưa có 02 | class.puml: reviseDraft/executeAtomicSave; ba sequence SYS-PAY-01 | API-06 | reviseDraft/executeAtomicSave | version | Hai phiên sửa cùng version chỉ một thành công | Thiết kế một phần | DD-03; thiếu 02 |
| AC-US01-15 | AC dẫn xuất | 01 Mục 3; §6; CREATE-13 | Đo thời gian save | PaymentApplicationService / Store; chưa có 02 | class.puml: saveDraft; ba sequence SYS-PAY-01 | API-05,06 | saveDraft | lưu dòng/index | 199 dòng, đo UI→response sau commit; không tính thời gian xác nhận giữa lần lưu | Thiết kế một phần | Blocked by CREATE-06/07; KT-05; thiếu 02 |

## 3. Quyết định và câu hỏi nối tới yêu cầu

| Quyết định / câu hỏi | Yêu cầu, AC | Thiết kế chịu ảnh hưởng |
|---|---|---|
| CREATE-01..04, USER-04 | US-PAY-01, PAY-01, AC-US01-01..05 | period, unique cả Draft, loại Cancelled; readContract/readCurrentSources. |
| CREATE-08..10; KT-01, KT-02 | US-PAY-01, PAY-02/03, AC-US01-08/09/11 | DraftInput, owner, snapshot, API-02..04/06. |
| CREATE-11 / CREATE-11a | AC-US01-10 | Requiredness nghiệp vụ còn Blocked by CREATE-11a; không tự bắt buộc notes. |
| CREATE-12; KT-03, KT-04; DD-03, DD-04 | PAY-01; NFR-PAY-01; AC-US01-03/04/12/13/14 | Unique live-period, version, receipt và transaction; khác chống trình trùng PAY-04. |
| CREATE-13; KT-05 | NFR-PAY-02; AC-US01-15 | Phép đo end-to-end 199 dòng; chưa có kết quả. |
| CREATE-05, CREATE-06, CREATE-07 | PAY-02/03; AC-US01-05/06/15 | Dòng rỗng/đối soát một phần, grouping, decimal và làm tròn. |
| CREATE-16, CREATE-17, CREATE-18 | PAY-01/02; AC-US01-01/02; UC khác | Unique không giải quyết chồng lấn; hết hạn không tự ngoại lệ; ngoài Draft chưa được mở sửa. |
| CREATE-19, CREATE-20, OQ-D-01 | PAY-02/03; AC-US01-05/09/11 | Quyền sửa lượng, hợp nhất nguồn, mức nhất quán nguồn trước commit. |
| DD-01, DD-02, DD-05, DD-06 | US-PAY-01; PAY-01..03; AC-US01-01/05/06/08/11 | Adapter chỉ đọc, snapshot độc lập input, số chính xác, principal/ownership. |

## 4. Ma trận ngược

| Thành phần / endpoint / entity | Yêu cầu truy về | Giải thích phạm vi |
|---|---|---|
| PaymentForm, PaymentApplicationService | US-PAY-01, AC-US01-01..15 | Chỉ lập/sửa Draft; không approve/submit. |
| PaymentSourceReader | PAY-01..03; AC-US01-01/05/06/11 | Chỉ đọc; không CRUD module khác. |
| API-01 prepareDraft | AC-US01-01..07 | Preview không tạo Payment. |
| API-02 openDraft | AC-US01-08 | Chỉ đọc Draft của mình. |
| API-03 previewChanges | AC-US01-09 | Xem trước, không thay dữ liệu nguồn. |
| API-04 refreshPreview | AC-US01-11 | A9 đã có trong BA; không tạo chức năng ngoài UC. |
| API-05 create / API-06 update | AC-US01-03/07..15 | Receipt và version là cơ chế kỹ thuật, không thêm trạng thái nghiệp vụ. |
| Payment / PaymentPeriod / PaymentLine | US-PAY-01; PAY-01..03 | Dữ liệu bảng, kỳ và dòng. |
| PaymentSourceSnapshot | PAY-03; CREATE-09; AC-US01-11 | Bằng chứng nguồn tính tiền và phát hiện thay đổi. |
| PaymentAuditEntry | NFR-PAY-01; AC-US01-13 | Chỉ audit các thao tác được thiết kế tại bản này. |
| PaymentSaveReceipt | CREATE-12; AC-US01-12 | Replay cùng yêu cầu, cùng transaction. |
| DraftInput, LineInput, SaveDraftCommand, DTO view | US-PAY-01; DD-02/04/06 | Hợp đồng in/out, không entity/CRUD riêng. |

## 5. Tổng hợp và kiểm chứng

- Ma trận có **30 dòng chính**: 5 US, 8 PAY, 2 NFR, 15 AC dẫn xuất. Không được suy số lượng dòng thành số yêu cầu đã đáp ứng.
- Các câu hỏi chưa trả lời được ghi tại 01; không đưa dòng bị chặn thành “Đã thiết kế – chưa kiểm thử”. Phần ngoài UC này dùng “Chưa thiết kế” hoặc “Thiết kế một phần” nếu chỉ có tác động gián tiếp.
- Audit đã mô tả cho tạo Draft và sửa Draft. Draft→PendingApproval, PendingApproval→Approved/Rejected/Draft, mở lại Rejected→Draft, Approved điều chỉnh và Draft→Cancelled chưa có thiết kế transaction/audit trong bản này; đích chuyển mâu thuẫn phải được xác nhận trước.
- PAY-06 và PAY-08 không được tự chọn một phía. Điều chỉnh Approved (US04/PAY-05) không được coi đã giải quyết bằng cách cấm sửa trong UC01.
- Thống kê trạng thái: **24 dòng Thiết kế một phần**, **6 dòng Chưa thiết kế**; 0 dòng nhận đã thiết kế đầy đủ. Các phụ thuộc Blocked giữ ở cột OQ/DD và mục 01, không đổi ID CREATE thành mã OQ giả.
- Đã chạy kiểm tra cấu trúc ngày 08/11/2026: đủ 30 ID chính, mỗi ID đúng một dòng; 15 AC có định nghĩa tại 01; 5 ví dụ JSON parse được; bảng Markdown, fence, link cục bộ, UTF-8 và khoảng trắng **PASS**. Các marker Blocked trỏ tới câu hỏi có định nghĩa tại 01; enum PaymentStatus đúng 5 giá trị, đủ 5 phương thức service nối tới 6 endpoint.
- Class đã chạy `-checkonly` và render PNG bằng PlantUML 1.2024.3, Java 27.0.1.0.3: **PASS**. Đã xem ảnh kiểm tra bố cục/chữ, không thấy chồng chữ; ảnh preview ở thư mục tạm, không thêm ảnh sinh tự động vào repo.
- Chưa có API/CSDL thực để integration test; NFR-PAY-02 chưa được đo. Kiểm tra đủ ID/JSON/cú pháp không chứng minh nghiệp vụ đã đúng hoặc các OQ đã được giải quyết.

Lệnh tối thiểu để kiểm tra lại độ phủ (PowerShell thay cho Python không có trong PATH):

```powershell
$taskMatrix = Get-Content -Raw -Encoding UTF8 docs/design/payment-management/06-traceability-matrix.md
$taskIds = @(1..5 | ForEach-Object { 'US-PAY-0' + $_ }) + @(1..8 | ForEach-Object { 'PAY-0' + $_ }) + @('NFR-PAY-01','NFR-PAY-02') + @(1..15 | ForEach-Object { 'AC-US01-' + $_.ToString('00') })
$taskMissing = @($taskIds | Where-Object { [regex]::Matches($taskMatrix, '(?m)^\| ' + [regex]::Escape($_) + ' \|').Count -ne 1 })
if ($taskMissing.Count) { throw ($taskMissing -join ', ') }
Write-Output '30 IDs, exactly once: PASS'
```

Kết quả lần này: `30 IDs, exactly once: PASS`. Chi tiết kiểm tra liên kết/JSON và lệnh render ghi tại prompt-log và chỉ mục sơ đồ; tất cả là kiểm chứng tài liệu, không phải thực thi chức năng.
