# Danh mục sequence và tên dùng cho US-PAY-01 (v2)

> Phiên bản: v2 · Ngày: 08/11/2026 · Người phụ trách: Chờ nhóm điền
> Đầu vào: sys-us-01-v2.md; open-questions-v2.md; P-18, P-19
> AI: Codex / GPT-6 · Prompt: P-18, P-19 trong docs/workflow/prompt-log.md
> Trạng thái: Bản sau review – Design Pending Approval

Tài liệu này chỉ là danh mục và giải thích phương án cho sequence được giao; chưa phải toàn bộ LLD/class/API/schema của module.

## Sơ đồ sequence

| File | Mục đích / phạm vi | US / PAY / AC | OQ / kết xuất |
|---|---|---|---|
| [seq-us-01-v2.puml](diagrams/seq-us-01-v2.puml), [SVG](diagrams/seq-us-01-v2.svg) | Lập từ chi tiết hợp đồng; vòng nhập kỳ/ghi chú, xem trước, lưu/phục hồi; sửa Draft | US-PAY-01; PAY-01..03; AC-US01-01..34; audit §6 | OQ đang mở theo SYS §2; kết quả kiểm chứng P-19 ghi trong prompt-log |

## Đối chiếu bước hệ thống

| Bước / nhánh SYS | Đoạn sequence | AC |
|---|---|---|
| 1–3, A2 | openCreateForm, kiểm tra phiên/quyền/Active, form cố định hợp đồng | 02, 03, 05, 21 |
| 4–6, A4, A6 | Nhập kỳ theo cấu hình, ghi chú tùy chọn, findOverlap | 04, 06, 22, 27, 30 |
| 7–9, A7, A7.1, A7.2, A8, A9 | Đọc nguồn, Active price, loop PAY-03, lỗi dữ liệu/thử lại/đổi kỳ | 08, 10, 11, 12, 13, 23, 24 |
| 10–11, A11, A11.1 | Validation đỏ trường, giá Active khác preview thì quay 9 trong cùng vòng lặp | 09, 26, 28 |
| 12–13, A12, A12.1, A12.2, K1 | Giao dịch, overlap nguyên tử, audit, commit và xác minh | 01, 07, 14, 15, 16, 29 |
| A10, AU3 | Đóng form, thông báo, không tạo Cancelled | 25, 29 |
| U1–U6, AU1, AU4, AU4.1, AU5, AU5.1, AU5.2 | Đọc version, candidate server, loop sửa/lưu/tra cứu | 17, 18, 19, 26, 28, 29 |
| 6/A6.1 | Auth trước toàn bộ xem trước: 401 hết phiên, 403 mất quyền, ngừng đọc giá/sản lượng, khóa form và thông báo | 02, 03, 31 |
| 11/A11.2/U3/U4/AU4.2 | Khóa trường nguồn ở UI; server từ chối ghi đè khi lập hoặc sửa; q/p ánh xạ từ nguồn | 17, 32 |
| 6/10/11 | Chỉ cho lập/lưu khi đủ trường bắt buộc; request bỏ qua UI vẫn bị từ chối | 04, 28, 33 |
| 7/11/A7.3/AU4.3 | Xác minh bảng giá được lập khi hợp đồng còn hiệu lực qua bằng chứng nguồn | 34 |

AC trong bảng viết tắt phần số, ví dụ 02 = AC-US01-02. Nguồn nghiệp vụ và review: SYS-US-01 v2 §1.1/§3, TA-SPEC §4.1, PAY-01..03, §6, P-18.1..3.

## Tên dùng tạm – cần đồng bộ vào class/API

| Thành phần | Thông điệp / dữ liệu |
|---|---|
| PaymentForm | Ngữ cảnh contractId từ chi tiết; thông tin khách hàng chỉ đọc; kỳ; note tùy chọn; preview; fieldErrors; version; mã tra cứu. Sản lượng/đơn giá/hợp đồng/khách hàng chỉ đọc; canSave chỉ đúng khi đủ trường bắt buộc |
| PaymentService | openCreateForm, preview, create, openDraft, update, checkSaveOutcome; validateAndCalculate / validateAndRecalculate trả candidate; authenticateAndCheckRole / authorizeCreateByAssignment. Quyền theo phân công/người tạo là đề xuất P-19 |
| IContractReader | getContract (Active, cấu hình kỳ, thông tin khách hàng liên quan); getContractAuthorization (thông tin phân công/quyền chỉ đọc phục vụ đề xuất). Không tự coi các trường này đã có trong AS-IS |
| IPriceReader | getActiveForContract(contractId, now); đọc bảng giá gắn hợp đồng, giá/phiên bản và creationEvidence xác minh hợp đồng còn hiệu lực khi tạo giá |
| IQuantityReader | getQuantities; chỉ đọc sản lượng và trạng thái đối soát |
| PaymentRepository | findOverlap, lockContractScopeAndCreate, getById, update, findSaveOutcome |
| AuditLog / PaymentDatabase | append / begin, commit, rollback; bảng/dòng/audit dùng cùng giao dịch |

UI→Service mô tả lời gọi ứng dụng phía server; chưa chốt controller, endpoint hoặc schema. Mọi request xác thực/phân quyền độc lập và dừng ngay khi không đạt; việc kiểm tra đã thể hiện ở lần mở không cấp quyền vô thời hạn. Nguồn chỉ được đọc sau khi có quyền. Các nhóm kiểm tra trả một result.code loại trừ nhau, không dùng thứ tự nhãn alt để ngầm chọn lỗi.

Mã/HTTP dùng tạm khi làm API: UNAUTHENTICATED 401, FORBIDDEN 403, NOT_FOUND 404; INVALID_INPUT/VERSION_REQUIRED 400; CONTRACT_NOT_ACTIVE/PERIOD_OVERLAP/QUANTITY_NOT_RECONCILED/ACTIVE_PRICE_INVALID/INVALID_STATE/CONCURRENT_MODIFICATION/PRICE_CHANGED 409; SOURCE_UNAVAILABLE/RESULT_UNKNOWN 503; PERSISTENCE_ERROR 500. Create thành công 201; đọc/sửa thành công 200. POLICY_DEPENDENT trong sequence chỉ đánh dấu phần nguồn/tính tiền chưa có quyết định, không phải mã API cuối cùng. formOpen/saved/outcomeUnknown là điều khiển UI, không thêm trạng thái bảng.

P-19 bổ sung READ_ONLY_FIELD 400 khi cố ghi đè trường nguồn và PRICE_ORIGIN_INVALID 409 khi điều kiện lúc tạo giá chưa đạt/chưa xác minh. Đây là mã kỹ thuật tạm. create vẫn nhận contractId làm tham chiếu ngữ cảnh; không nhận thay đổi thông tin hợp đồng/khách hàng. update chỉ nhận các trường được phép theo ma trận; không lấy q/p hoặc tổng do client gửi làm dữ liệu quyết định.

Đề xuất một người thực hiện: create cần vai trò NVKD và hợp đồng được giao; update cần NVKD và currentUser.id = payment.createdBy. Chưa suy ra quyền sửa khi hợp đồng đổi người phụ trách, chưa giả định hợp đồng chỉ có một người được giao, và chưa coi đề xuất là quyết định đã được khách hàng duyệt. Kiểm tra lại mỗi request, đặc biệt lúc xem trước sau khi form đã mở. Thuế vẫn giữ OQ-US03-03 để xác nhận lại khách hàng; không bổ sung trường thuế bắt buộc hay công thức VAT.

Điều kiện giá được tạo khi hợp đồng còn hiệu lực do người dùng xác nhận ở P-19. Module nguồn phải cung cấp bằng chứng lịch sử hoặc kết quả xác minh có căn cứ; Active hiện tại không chứng minh trạng thái lúc tạo giá. creationEvidence là yêu cầu tích hợp TO-BE, chưa có trường/API tương ứng được khảo sát trong mã hiện tại; không thiết kế tạo/sửa bảng giá trong module thanh toán.

## Phương án kỹ thuật trong phạm vi sequence

| Mục đích / yêu cầu | Phương án đề xuất | Thay thế / lý do / tác động |
|---|---|---|
| Chống chồng lấn, PAY-01 và P-18.3 | Khi lưu, khóa phạm vi thanh toán của hợp đồng trong DB thanh toán, kiểm tra lại toàn khoảng rồi ghi trong cùng giao dịch; Cancelled loại khỏi kiểm tra theo quyết định US05 v2 | Chỉ tra trước khi ghi có race. Unique theo mã kỳ không chặn tháng/quý. Có thể dùng constraint phân bổ từng tháng nếu chọn schema phù hợp; chưa chốt DB/index. Khóa làm các lần lưu cùng hợp đồng chờ nhau |
| Audit §6 | Candidate hợp lệ, bảng/dòng và audit cùng transaction; audit before/after dùng đúng dữ liệu được ghi | Audit sau commit có thể mất vết. Lỗi audit phải rollback dữ liệu; đây là đề xuất, chưa có phép thử DB |
| Giữ đúng sửa Draft §4.1 | getById trả version; update có điều kiện Draft/version, trả version mới | Ghi đè không version có thể mất sửa đổi; khóa bi quan là phương án khác. Thiếu token tải lại; xung đột thông báo, không tự ghi đè |
| Dùng giá Active, P-18.3 | Đọc giá Active lúc tính và lúc lưu, so phiên bản với preview; giá đổi thì tính lại và thông báo, không có lựa chọn giữ giá cũ | Giữ snapshot cũ để lưu trái xác nhận. Phát hiện đổi giữa lần đọc cuối và commit cần phối hợp interface nguồn/phiên bản khi chọn công nghệ; transaction cục bộ không bảo đảm khóa được nguồn ngoài |
| Kết quả commit chưa rõ | Giữ id/mã tra cứu thao tác; K1 xác minh đã lưu/chắc chắn chưa lưu/chưa rõ; chưa rõ không gửi lại create/update | Rollback sau mất phản hồi không chứng minh chưa commit. DB/driver phải cung cấp cách xác định kết quả; một lần đọc không thấy bản ghi chưa đủ kết luận nếu commit còn đang xử lý. Chưa chọn giao thức cụ thể |

Các phương án kỹ thuật không bổ sung business rule; nguồn liên quan được ghi trong từng hàng. Cần đưa vào 07-design-decisions khi lập bộ thiết kế tổng thể. Chưa có kiến trúc/API/data đầy đủ để kết luận có thể triển khai toàn bộ module.

## Thay đổi so với v1

V1 chưa có tài liệu danh mục này. Bổ sung để liên kết sequence v2 với SYS/AC/OQ, thống nhất tên và ghi giới hạn kỹ thuật; không bổ sung HLD/class/API/schema ngoài phạm vi. Căn cứ P-18 và quy tắc sequence-diagram/naming-versioning.
