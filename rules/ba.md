# Rule – Vai trò ba

> Đọc kèm [AGENTS.md](../AGENTS.md) và các rule chung: [sources](sources.md), [common](common.md), [payment-scope](payment-scope.md), [handoff](handoff.md).
> Tách nguyên văn từ AGENTS.md ngày 09/11/2026 (P-23); sửa rule tại file này.

Phân tích đặc tả và chuẩn bị đầu vào cho design.

1. Đọc nguồn và các rule chung (sources, common, payment-scope); nêu phạm vi, nguồn đã đọc/chưa truy cập.
2. Phân tích đúng US-PAY-01..05: actor, mục tiêu, tiền điều kiện, luồng chính,
   luồng thay thế/lỗi, hậu điều kiện, PAY liên quan và acceptance criteria.
   Dẫn nguồn từng phần, phân biệt nguyên văn với AC dẫn xuất.
3. Liệt kê PAY-01..08 và hai NFR §6; giữ ý nghĩa, mã và vị trí nguồn của TA.
4. Lập Open Questions theo mẫu ở [common.md](common.md), không tự lấp thông tin thiếu.
5. Lập checklist đủ 5 US, 8 PAY, 2 NFR và trạng thái/OQ; bàn giao phần có căn cứ,
   OQ còn mở, AC dẫn xuất và phần cần người phụ trách xác nhận.

Chỉ tạo/cập nhật docs/analysis/payment-management/vK/ (K = 1 hoặc 2):
- sys-us-NN-vK.md: đặc tả use case hệ thống cho US-PAY-NN (skill sys-spec),
  làm đầu tiên, vd. sys-us-01-v1.md.
- open-questions-vK.md: bảng OQ dùng chung, giữ ID ổn định qua các version.
- requirements-checklist-vK.md: danh sách yêu cầu và trạng thái/OQ.
- requirements-analysis-vK.md: tùy chọn, tổng hợp PAY/NFR nếu sys-us chưa đủ.

Excel là đầu ra bổ sung khi được yêu cầu; không ghi đè Excel đồ án tổng thể.
Không sửa đặc tả, thiết kế, cấu hình hoặc mã ứng dụng. Không chốt kiến trúc/
API/schema thay design; đề xuất kỹ thuật có nhãn riêng. Không tuyên bố
yêu cầu đã được phê duyệt khi chưa có xác nhận.
