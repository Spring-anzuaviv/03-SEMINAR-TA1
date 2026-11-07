# Open Questions US-PAY-04 (v1)

> Phiên bản: v1 · Ngày nhập: 07/11/2026 · Người phụ trách: Lộc
> Đầu vào: Bộ US-PAY-04 Before Review · [TA-SPEC §4.4, §5 PAY-05, §6](../../../../requirements/payment-management/spec.md) · TA-PDF tr.2–3
> AI: Codex · Prompt nhập bản v1: [P-02](../../../../workflow/prompt-log.md#p-02--nhập-bộ-us-pay-04-v1)
> Trạng thái: Bản lần chạy đầu – Design Pending Approval

Cả ba câu hỏi đang ở trạng thái **Cần xác nhận**. Các mã OQ là mã nội bộ.

| Mã trong bộ Before Review | Mã trong workspace v1 |
| --- | --- |
| OQ-01 | OQ-03 |
| OQ-02 | OQ-US04-01 |
| OQ-03 | OQ-US04-02 |

| Mã             | Vị trí trong đề              | Loại                             | Điểm chưa hợp lý hoặc cần kiểm tra                                                                                                                                                                                                  | Cần khách hàng xác nhận                                                                                                                                                                | Ảnh hưởng đến thiết kế                                                                  |
| --------------- | -------------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| **OQ-03** | §4.4 US-PAY-04 và PAY-05 (§5) | Mâu thuẫn nếu sửa trực tiếp | §4.4 cho phép Kế toán trưởng điều chỉnh bảng `Approved` khi có biên bản, còn PAY-05 cấm sửa bảng `Approved`. Từ “điều chỉnh” chưa chỉ rõ có được sửa bảng gốc hay chỉ ghi nhận điều chỉnh riêng. | Giữ bảng gốc và lập hồ sơ điều chỉnh riêng (A), hay phê chuẩn ngoại lệ cho phép cập nhật bảng gốc (B)?                                                                  | Quyết định nơi ghi thay đổi và việc có cần bổ sung ngoại lệ vào PAY-05.          |
| **OQ-US04-01** | §4.4 US-PAY-04                  | Thiếu                            | Đề yêu cầu đính kèm biên bản xác nhận nhưng chưa nêu tiêu chí chấp nhận biên bản và phạm vi nội dung được điều chỉnh.                                                                                          | Hướng A cần những thông tin nào trong hồ sơ? Hướng B cho sửa trường nào? Biên bản cần đáp ứng tiêu chí gì?                                                           | Quyết định dữ liệu nhập và điều kiện hệ thống kiểm tra trước khi lưu.          |
| **OQ-US04-02** | §1, §3 và §4.4 US-PAY-04     | Thiếu                            | Đề yêu cầu bảng được duyệt trước khi chuyển kế toán xuất hóa đơn, nhưng chưa mô tả quy trình áp dụng số liệu đã điều chỉnh.                                                                                 | Có phải duyệt lại không và ai duyệt? Với B, bảng ở trạng thái nào sau khi sửa? Khi nào kế toán được dùng số mới và xử lý ra sao nếu đã phát hành hóa đơn? | Quyết định trạng thái, quy trình sau khi ghi nhận và thời điểm áp dụng số liệu. |

## Ví dụ để trao đổi về OQ-03

Giả sử bảng đã duyệt ghi **120 triệu** và biên bản xác nhận số đúng là **115 triệu**.

- **A:** Bảng gốc vẫn ghi **120 triệu** và giữ `Approved`. Hệ thống lưu hồ sơ riêng ghi **giảm 5 triệu**, liên kết với bảng gốc. Kế toán chỉ dùng số **115 triệu** khi khoản điều chỉnh được phép áp dụng theo OQ-US04-02.
- **B:** Hệ thống cập nhật trực tiếp bảng gốc từ **120 triệu xuống 115 triệu** và lưu vết trước/sau. B chỉ thực hiện được sau khi ngoại lệ PAY-05 được phê chuẩn và yêu cầu đáp ứng điều kiện đã chốt.
