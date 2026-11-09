# Rule – Phạm vi Bảng thanh toán

> Áp dụng cho mọi vai trò.
> Tách nguyên văn từ AGENTS.md ngày 09/11/2026 (P-23); sửa rule tại file này.

- Chỉ phân tích/thiết kế lập và sửa Draft, trình duyệt, duyệt/từ chối, điều chỉnh,
  hủy bảng thanh toán [TA-SPEC §1, §4]. Hợp đồng, bảng giá, sản lượng chỉ được
  đọc qua interface; không thiết kế CRUD cho các module đó.
- Vai trò theo §2: NVKD, KTT, GĐKD. Trạng thái liệt kê trong §3: Draft,
  PendingApproval, Approved, Rejected, Cancelled. Không thêm trạng thái hoặc
  chốt luồng cuối cùng khi mâu thuẫn liên quan chưa được xác nhận.
- Bao phủ đủ US-PAY-01..05, PAY-01..08 và hai NFR §6.
  NFR-PAY-01 (audit) và NFR-PAY-02 (lập bảng ≤3 giây với <200 dòng) là mã nội bộ;
  đề không đặt mã NFR. Không đổi thành ≤200 dòng hoặc tự thêm percentile/
  tải đồng thời như tiêu chuẩn gốc.
- Audit mọi thay đổi trạng thái và mọi điều chỉnh: ai, lúc nào, thay đổi gì
  [TA-SPEC §6]. Giữ OQ về điều chỉnh Approved.
- PAY-04 yêu cầu chống trình duyệt trùng; Idempotency-Key, unique constraint
  hoặc transaction là phương án kỹ thuật cần giải thích. PAY-07 cấm tự duyệt.
- Quyền hủy, phạm vi sửa Draft, làm tròn, VAT, lập lại sau hủy hoặc kênh thông báo
  chưa rõ thì ghi OQ, không tự thêm thành rule.
- Tên trạng thái, class, thao tác và endpoint phải nhất quán giữa tài liệu,
  class/sequence/state diagram, API và mô hình dữ liệu.

Các tình huống cần nhận diện dưới đây chưa phải đáp án nghiệp vụ và không
thay việc đọc toàn bộ đặc tả:

| Vị trí TA-SPEC | Vấn đề | Lý do cần xác nhận |
|---|---|---|
| §2 ↔ PAY-01 | Kỳ tháng/quý nhưng duy nhất theo tháng | Ảnh hưởng khóa duy nhất và kỳ được lập |
| §4.3 ↔ PAY-06 | Từ 500 triệu / trên 500 triệu | Chưa thống nhất ai duyệt đúng 500.000.000 đồng |
| §4.4 ↔ PAY-05 | KTT điều chỉnh Approved / cấm mọi sửa đổi | Chưa thể chốt sửa trực tiếp hay bản điều chỉnh |
| §3 ↔ PAY-08 | Sau từ chối ở Rejected / quay Draft | Chưa chốt đích chuyển trạng thái/bước trung gian |
| PAY-04 | Chưa liệt kê dòng dịch vụ bắt buộc | Chưa đủ căn cứ tạo validation chi tiết |
