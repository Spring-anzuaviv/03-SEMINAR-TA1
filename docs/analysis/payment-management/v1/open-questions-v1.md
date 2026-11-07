# Open Questions – Bảng thanh toán (v1)

> Phiên bản: v1 · Ngày: 07/11/2026 · Người phụ trách: Đan Anh (US-PAY-03); Lộc (US-PAY-04, nhập từ bộ "Before Review")
> Đầu vào: [sys-us-03-v1.md](sys-us-03-v1.md); [sys-us-04-v1.md](sys-us-04-v1.md); TA-SPEC §1, §3, §4.3, §4.4, §5, §6; đề xuất của Đan Anh ngày 07/11/2026
> AI: Claude Code / Claude Sonnet 5.5 (US-PAY-03), Codex (US-PAY-04) · Prompt: P-02, P-03, P-04, P-05, P-06, P-07 trong [prompt-log](../../../workflow/prompt-log.md)
> Trạng thái: Bản lần chạy đầu – Design Pending Approval
>
> Bảng OQ dùng chung, gồm OQ phát sinh từ US-PAY-03 và US-PAY-04. OQ-01, OQ-05 và OQ của US-PAY-01/02/05 do người viết sys-us tương ứng bổ sung.
> `OQ-USNN-kk` là mã tự đặt. Đặc tả TA không bị sửa hồi tố.
> **Nguồn các đề xuất (US-PAY-03):** các lượt trao đổi trong chat Claude Code ngày 07/11/2026 (prompt P-04..P-07), người đề xuất: Đan Anh (tài khoản git `danwanh`). Đây là **đề xuất của nhóm, chưa được khách hàng xác nhận**; trạng thái chỉ chuyển sang xác nhận khi có người/ngày/tham chiếu từ phía khách hàng. Các OQ của US-PAY-04 chưa có đề xuất.

| ID | Vị trí mọi nguồn | Loại | Mô tả | Đề xuất / trả lời của Đan Anh (nguyên ý) | Trạng thái | Người/ngày/tham chiếu | Còn mở / ảnh hưởng |
|---|---|---|---|---|---|---|---|
| OQ-02 | TA-SPEC §4.3 "từ 500 triệu trở lên" ↔ PAY-06 "trên 500 triệu" (tr.2) | Mâu thuẫn | Đúng 500.000.000 đ ai duyệt | "từ ... trở lên" → Giám đốc kinh doanh | **Đề xuất của Đan Anh – chờ khách hàng xác nhận** | Đan Anh / 07/11/2026 / P-04 | Không còn. Ảnh hưởng US-PAY-02 (người nhận thông báo). Chữ "trên" của PAY-06 vẫn nằm trong đề. |
| OQ-04 | TA-SPEC §3 ↔ PAY-08 (tr.1–2) | Mâu thuẫn | Đích sau từ chối | "rejected rồi draft" | **Đề xuất của Đan Anh – chờ khách hàng xác nhận** | Đan Anh / 07/11/2026 / P-04 | Bước sau xem OQ-US03-07. |
| OQ-US03-01 | PAY-07; §2; §4.3 | Mơ hồ | Người lập; PAY-07 với từ chối; nhiều vai trò | Người lập là người tạo Draft; PAY-07 có áp dụng (với từ chối); một người một vai trò | **Đề xuất của Đan Anh – chờ khách hàng xác nhận** | Đan Anh / 07/11/2026 / P-04 | Không còn. Cần lưu người tạo Draft. |
| OQ-US03-02 | §4.3; PAY-06; §2 | Mơ hồ | Theo vai trò hay cá nhân; thay thế chéo | Theo vai trò; không duyệt thay nhau | **Đề xuất của Đan Anh – chờ khách hàng xác nhận** | Đan Anh / 07/11/2026 / P-04 | Không còn. |
| OQ-US03-03 | §4.3; PAY-06; PAY-03; §4.1 | Thiếu | Tổng tiền so ngưỡng: thời điểm, VAT, làm tròn; sửa khi `PendingApproval` | P-04: "có tính VAT". P-05: "tổng tiền lấy tại thời điểm lập"; "làm tròn theo tiền Việt"; "thuế mặc định để tôi xác nhận với khách hàng sau"; "chỉ được sửa ở trạng thái Draft". P-06: "Cần xác nhận, chỉ cần biết là thuế"; "làm tròn dòng tổng, làm tròn lên". P-07: "giá trị thuế là 1 giá trị x hoặc % trên tổng" | **Đề xuất của Đan Anh – chờ khách hàng xác nhận; giá trị thuế mặc định còn Cần xác nhận (không chặn)** | Đan Anh / 07/11/2026 / P-04..P-07 | Còn: giá trị thuế mặc định và dùng loại nào (x hay %), người phụ trách xác nhận với khách hàng; không chặn thiết kế. Đã rõ: thuế là một giá trị x hoặc một tỷ lệ % trên tổng. Cách hiểu: làm tròn từng dòng và tổng, làm tròn lên theo đồng (dấu phẩy trong "dòng tổng" đọc là "dòng và tổng"). Ảnh hưởng US-PAY-01. |
| OQ-US03-04 | §4.3; PAY-08 | Thiếu | Ràng buộc lý do, nơi lưu, Nhân viên kinh doanh thấy không | P-04: "có thấy". P-05: "text có giới hạn 500 từ" | **Đề xuất của Đan Anh – chờ khách hàng xác nhận** | Đan Anh / 07/11/2026 / P-04, P-05 | Không còn. Ghi chú: "500 từ" hiểu là 500 từ (words), không phải ký tự; cách đếm từ là đề xuất kỹ thuật. |
| OQ-US03-05 | §4.2; §4.3; §3 | Thiếu | Có thông báo kết quả không; ai; kênh | P-04: "có thông báo". P-05: "thông báo trong hệ thống". P-06: "có kèm lý do". P-07: "phải" (trả lời câu hỏi người nhận có phải Nhân viên kinh doanh người tạo Draft) | **Đề xuất của Đan Anh – chờ khách hàng xác nhận** | Đan Anh / 07/11/2026 / P-04..P-07 | Không còn. Người nhận: Nhân viên kinh doanh người tạo Draft; thông báo trong hệ thống, kèm lý do khi từ chối, cho cả duyệt và từ chối. |
| OQ-US03-06 | §1 | Mơ hồ | Chuyển kế toán sau `Approved` | "module bên kế toán là ngoài phạm vi" | **Đề xuất của Đan Anh – chờ khách hàng xác nhận** | Đan Anh / 07/11/2026 / P-04 | Không còn. |
| OQ-US03-07 | §3 "Rejected"; PAY-08 "quay về Draft để Nhân viên kinh doanh chỉnh sửa" (tr.1–2); trả lời OQ-04 | Thiếu | Bước `Rejected` → `Draft` do ai, khi nào | P-05: "khu Nhân viên kinh doanh thực hiện chỉnh sửa bảng reject" | **Đề xuất của Đan Anh – chờ khách hàng xác nhận** | Đan Anh / 07/11/2026 / P-05, P-06 | Đan Anh đồng ý cách hiểu của AI (P-06: "bạn hiểu đúng") – `Rejected` → `Draft` khi Nhân viên kinh doanh chỉnh sửa; hệ thống không tự chuyển lúc từ chối. Ảnh hưởng US-PAY-01/02 (thao tác mở sửa bảng `Rejected` chưa có trong đề). |
| OQ-03 | TA-SPEC §4.4 US-PAY-04 "Kế toán trưởng có thể điều chỉnh bảng đã Approved nếu có biên bản" ↔ PAY-05 "đã Approved không được sửa dưới bất kỳ hình thức nào" (tr.2) | Mâu thuẫn | "Điều chỉnh" chưa chỉ rõ có được sửa bảng gốc hay chỉ ghi nhận điều chỉnh riêng. | – | Cần xác nhận | – | Giữ bảng gốc và lập hồ sơ điều chỉnh riêng (A), hay phê chuẩn ngoại lệ cho sửa bảng gốc (B)? Quyết định nơi ghi thay đổi và việc bổ sung ngoại lệ vào PAY-05. US-PAY-04. |
| OQ-US04-01 | TA-SPEC §4.4 US-PAY-04 (tr.2) | Thiếu | Đề yêu cầu đính kèm biên bản xác nhận nhưng chưa nêu tiêu chí chấp nhận biên bản và phạm vi nội dung được điều chỉnh. | – | Cần xác nhận | – | Hướng A cần thông tin gì trong hồ sơ? Hướng B cho sửa trường nào? Biên bản cần tiêu chí gì? Quyết định dữ liệu nhập và điều kiện kiểm tra trước khi lưu. |
| OQ-US04-02 | TA-SPEC §1, §3, §4.4 US-PAY-04 (tr.1–2) | Thiếu | Đề yêu cầu bảng được duyệt trước khi chuyển kế toán xuất hóa đơn, nhưng chưa mô tả quy trình áp dụng số liệu đã điều chỉnh. | – | Cần xác nhận | – | Có phải duyệt lại không và ai duyệt? Với B, bảng ở trạng thái nào sau khi sửa? Khi nào kế toán dùng số mới, xử lý ra sao nếu đã phát hành hóa đơn? Quyết định trạng thái, quy trình sau ghi nhận và thời điểm áp dụng. |

## Ví dụ để trao đổi về OQ-03 (từ bộ US-PAY-04)

Giả sử bảng đã duyệt ghi **120 triệu** và biên bản xác nhận số đúng là **115 triệu**.

- **A:** Bảng gốc vẫn ghi **120 triệu** và giữ `Approved`. Hệ thống lưu hồ sơ riêng ghi **giảm 5 triệu**, liên kết với bảng gốc. Kế toán chỉ dùng số **115 triệu** khi khoản điều chỉnh được phép áp dụng theo OQ-US04-02.
- **B:** Hệ thống cập nhật trực tiếp bảng gốc từ **120 triệu xuống 115 triệu** và lưu vết trước/sau. B chỉ thực hiện được sau khi ngoại lệ PAY-05 được phê chuẩn và yêu cầu đáp ứng điều kiện đã chốt.

## Đối chiếu mã trong bộ Before Review

| Mã trong bộ Before Review | Mã trong workspace v1 |
|---|---|
| OQ-01 | OQ-03 |
| OQ-02 | OQ-US04-01 |
| OQ-03 | OQ-US04-02 |
