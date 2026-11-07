# Quyết định kỹ thuật US-PAY-02 (v1)

> Phiên bản: v1 · Ngày: 08/11/2026 · Người phụ trách: Chưa chỉ định
> Đầu vào: [sys-us-02-v1.md](../../../analysis/payment-management/v1/sys-us-02-v1.md) §1.3–1.5; [OQ v1](../../../analysis/payment-management/v1/open-questions-v1.md)
> AI: Codex / GPT-6 · Prompt: P-16 trong [prompt-log](../../../workflow/prompt-log.md)
> Trạng thái: Bản lần chạy đầu – Design Pending Approval

## DD-01 – Ghi có điều kiện và audit trong một giao dịch

[ĐỀ XUẤT KỸ THUẬT] Phạm vi chỉ submit US-PAY-02. Mục đích đáp ứng PAY-04 và NFR-PAY-01: không trình trùng, không lưu chuyển trạng thái thiếu audit. [TA-SPEC §4.2, §5 PAY-04, §6; TA-PDF tr.2–3; SYS-US-02 bước 6, A6/A6.1, AC-US02-05/11/13]

Phương án minh họa: đọc trạng thái và version, cập nhật chỉ khi vẫn `Draft` và version bằng giá trị đã đọc; mỗi lần cập nhật làm thay đổi version. Ghi trạng thái và audit dùng cùng giao dịch. Không có dòng cập nhật thì rollback, trả xung đột; lỗi lưu/audit/commit trước khi commit thì rollback, không gọi thông báo. Hai request đọc cùng version chỉ một request có thể commit, request kia không tạo thêm audit chuyển trạng thái. Version là cơ chế kỹ thuật chống dùng dữ liệu cũ, chưa chốt trường/schema. Dùng version tránh ghi dựa trên dữ liệu Draft đã bị sửa sau bước kiểm tra.

Thay thế: khóa bảng trong thời gian kiểm tra và ghi, đơn giản về điều phối nhưng có thể giữ khóa lâu; chỉ kiểm tra trạng thái trước rồi ghi riêng không đủ vì có thể tranh chấp. Idempotency-Key có thể giúp gửi lại sau mất phản hồi nhưng chưa cần chốt hợp đồng hoặc thời gian lưu khóa. Chọn minh họa cập nhật có điều kiện vì vừa đủ cho bài tập và không giữ khóa trong lúc gửi thông báo.

Hệ quả: thao tác thua không ghi đè trạng thái hiện có; phải có lưu trữ hỗ trợ giao dịch chung với audit. Không khẳng định code AS-IS đã có cơ chế này. Không thêm điều kiện nghiệp vụ hoặc trạng thái. Các tên `version`, `transition`, `append` là tên tạm cần đồng bộ khi có LLD/API/data.

Thông báo được minh họa sau commit theo thứ tự SYS bước 6–7. Đây chưa phải quyết định hoàn chỉnh về tính nguyên tử giữa lưu trạng thái và gửi thông báo: **Blocked by OQ-US02-02**. Không tự chốt giữ trạng thái, hoàn tác, thử lại hay cơ chế outbox; sau xác nhận phải cập nhật sequence và audit mọi chuyển trạng thái bổ sung. Rủi ro hiện còn: chính sách lỗi gửi, người nhận, dòng bắt buộc, quyền và luồng trình lại đều phụ thuộc OQ trong sys spec.
