# Danh mục thiết kế chi tiết US-PAY-02 (v1)

> Phiên bản: v1 · Ngày: 08/11/2026 · Người phụ trách: Chưa chỉ định
> Đầu vào: [sys-us-02-v1.md](../../../analysis/payment-management/v1/sys-us-02-v1.md), [OQ v1](../../../analysis/payment-management/v1/open-questions-v1.md)
> AI: Codex / GPT-6 · Prompt: P-16 trong [prompt-log](../../../workflow/prompt-log.md)
> Trạng thái: Bản lần chạy đầu – Design Pending Approval

Chỉ lập danh mục sequence US-PAY-02 theo skill; chưa thực hiện toàn bộ LLD/class/state/API/data. Không khẳng định thành phần trong sơ đồ đã tồn tại ở AS-IS.

## Sơ đồ sequence

| File | Mục đích / phạm vi | Truy vết | OQ / trạng thái |
|---|---|---|---|
| [seq-us-02-v1.puml](diagrams/seq-us-02-v1.puml) | Submit từ Draft, kiểm tra phía hệ thống, chống lặp/đồng thời, audit, thông báo | US-PAY-02; PAY-04/06; NFR-PAY-01; AC-US02-01..13; TA-SPEC §2–4.3, PAY-04..08, §6; TA-PDF tr.1–3 | Blocked by OQ-02, OQ-05, OQ-US02-01, OQ-US02-02, OQ-US03-02, OQ-US03-03, OQ-04, OQ-US03-07; Design Pending Approval |

PAY-05/08 chỉ tác động guard trạng thái/trình lại; PAY-07 thuộc US-PAY-03, không thêm kiểm tra cấm người lập submit. Không gọi ghi tới các module hợp đồng/bảng giá/sản lượng. NFR-PAY-02 chỉ áp dụng lập bảng, chưa đo hiệu năng. [TA-SPEC §1, §3–4, §5 PAY-05/07/08, §6; TA-PDF tr.1–3]

### Đối chiếu SYS ↔ sequence

| Bước/nhánh SYS-US-02 | Đoạn sequence | AC |
|---|---|---|
| 1–2, A2 | submit, checkSubmitPermission; break lỗi nhận diện/quyền | AC-US02-01/06 |
| 3, A3 | getById; break không tìm thấy | AC-US02-07 |
| 3, A3.1 | break PendingApproval / Approved hoặc Cancelled / Rejected | AC-US02-05/08/09 |
| 4, A4, A4.1 | validateSubmission; tổng âm, note tổng 0, thiếu dòng bắt buộc | AC-US02-02/03/04 |
| 5, A5 | resolveRequiredApprover; alt dưới/trên/đúng ngưỡng; break chưa chốt người nhận | AC-US02-10 |
| 6, A6 | Transaction; transition có điều kiện Draft + expectedVersion, alt conflict; note hai request cùng version | AC-US02-05/13 |
| 6, A6.1 | alt lỗi lưu / lỗi audit / lỗi commit, rollback; nhánh thành công append audit + commit | AC-US02-01/11 |
| 7–8, A7 | notifySubmission, alt gửi thành công/thất bại; note OQ lỗi gửi | AC-US02-01/12 |

`break` là combined fragment UML cho nhánh kết thúc sớm; phần phụ thuộc OQ kết thúc mô tả tại điểm chưa xác định, không biểu diễn chính sách lỗi runtime đã duyệt. Nhánh đồng thời giả định mỗi request kiểm tra đầu vào riêng rồi tranh chấp ở lần ghi có điều kiện; request thắng commit cả trạng thái và audit, request thua rollback. [ĐỀ XUẤT KỸ THUẬT] [SYS-US-02 §1.3–1.5; DD-01]

## Tên dùng tạm – cần đồng bộ vào 03

Chưa có danh mục lớp/API/state chính thức. Bảng dưới chỉ dành cho sequence US-PAY-02; không chuẩn hóa hay sửa tên các US khác.

| Trách nhiệm | Tên tạm / thao tác |
|---|---|
| Điều phối yêu cầu | PaymentController.submit(id); PaymentService.submit(id, currentUser) |
| Quyền, dữ liệu, người nhận | checkSubmitPermission; validateSubmission; resolveRequiredApprover |
| Lưu bảng và giao dịch | PaymentRepository.getById / begin / transition / rollback / commit; Database conditionalUpdate(id, Draft, expectedVersion) |
| Audit trong cùng giao dịch | AuditLog.append(actor, time, id, Draft, PendingApproval, submit, transaction) |
| Thông báo | Notification.notifySubmission(id, recipient); kênh và kết quả lỗi Blocked by OQ-US02-02 |
| Lỗi tạm, chưa phải API contract | UNAUTHENTICATED 401; FORBIDDEN 403; NOT_FOUND 404; INVALID_STATE 409; DUPLICATE_SUBMIT 409; CONCURRENT_CHANGE 409; NEGATIVE_TOTAL 400; REQUIRED_SERVICE_MISSING 400; PERSISTENCE_ERROR 500 |
| Trạng thái / action | Draft, PendingApproval, Approved, Rejected, Cancelled; action submit (TA-SPEC §3, §4.2) |

[ĐỀ XUẤT KỸ THUẬT] Mã lỗi tạm giúp phân biệt lỗi cho client, thay thế có thể dùng một mã chung kèm lý do; tách mã giúp kiểm chứng từng nhánh, không tạo quyền hoặc validation mới. Không chốt endpoint/schema. Giao dịch và đồng thời: [DD-01](07-design-decisions-v1.md). Căn cứ hành vi: SYS-US-02 A2..A7, AC-US02-01..13.

## Kiểm chứng

PlantUML 1.2025.2, Java 1.8.0_251: chạy `-charset UTF-8 -checkonly`, `-tsvg`, `-tpng` cho `diagrams/seq-us-02-v1.puml`, cả ba lệnh exit 0. Đã tạo [SVG](diagrams/seq-us-02-v1.svg) (82.584 byte) và [PNG](diagrams/seq-us-02-v1.png) (343.409 byte), kích thước 1941 × 3863. Đã mở PNG kiểm tra: hiển thị đủ tiêu đề, các nhánh, transaction/audit và thông báo; không thấy lỗi chữ hoặc cắt nội dung.

Kiểm tra bổ sung bằng Python: giữ nguyên 18 dòng OQ cũ trong bảng chung, đồng bộ đủ 8 ID trong bảng câu hỏi sys spec với OQ/sequence, tên `@startuml` đúng file, cặp start/end cân bằng, SVG XML hợp lệ và không có “Syntax Error”. `python -X utf8 scripts/verify_agent_config.py` → PASS (0 failed checks). Chi tiết lệnh và các lần thử lỗi ở P-16. Đây là kiểm chứng tài liệu/kết xuất, chưa có kiểm thử ứng dụng, đo hiệu năng hoặc phê duyệt thiết kế/nghiệp vụ.
