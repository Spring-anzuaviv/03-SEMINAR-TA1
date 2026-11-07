# Open Questions – Bảng thanh toán (v1)

> Phiên bản: v1 · Ngày: 07/11/2026 · Người phụ trách: Đan Anh (US-PAY-03); Lộc (US-PAY-04, nhập từ bộ "Before Review"); Tuấn (US-PAY-05)
> Đầu vào: [sys-us-03-v1.md](sys-us-03-v1.md); [sys-us-04-v1.md](sys-us-04-v1.md); [sys-us-05-v1.md](sys-us-05-v1.md); TA-SPEC §1, §3, §4.3, §4.4, §4.5, §5, §6; đề xuất của Đan Anh ngày 07/11/2026
> AI: Claude Code / Claude Sonnet 5.5 (US-PAY-03), Codex (US-PAY-04), Gemini 3.8 Flash (US-PAY-05) · Prompt: P-02..P-10, P-11..P-14 trong [prompt-log](../../../workflow/prompt-log.md)
> Trạng thái: Bản lần chạy đầu – Design Pending Approval
>
> Bảng OQ dùng chung, gồm OQ phát sinh từ US-PAY-03, US-PAY-04 và US-PAY-05. OQ-01, OQ-05 và OQ của US-PAY-01/02 do người viết sys-us tương ứng bổ sung.
> `OQ-USNN-kk` là mã tự đặt. Đặc tả TA không bị sửa hồi tố.
> **Nguồn các đề xuất (US-PAY-03):** các lượt trao đổi trong chat Claude Code ngày 07/11/2026 (prompt P-04..P-07), người đề xuất: Đan Anh (tài khoản git `danwanh`). Đây là **đề xuất của nhóm, chưa được khách hàng xác nhận**; trạng thái chỉ chuyển sang xác nhận khi có người/ngày/tham chiếu từ phía khách hàng. Các OQ của US-PAY-04 và US-PAY-05 (bản v1) chưa có đề xuất từ khách hàng.

| ID | Vị trí mọi nguồn | Loại | Mô tả | Đề xuất / Lựa chọn | Trạng thái | Người/ngày/tham chiếu | Còn mở / ảnh hưởng |
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
| **OQ-US05-01** | TA-SPEC §4.5 tr.2 ("Bảng ở trạng thái Draft có thể bị hủy khi không còn cần thiết"); §2 tr.1; TA-PDF tr.1, tr.2 | Mơ hồ | Đặc tả dùng thể bị động ("có thể bị hủy") mà không nêu rõ tác nhân nào được phép hủy bảng thanh toán Draft: chỉ NVKD tạo bảng (owner), bất kỳ NVKD nào, hay cả KTT / GĐKD? | **Lựa chọn A**: Chỉ NVKD tạo bảng (Creator / Owner).<br>**Lựa chọn B**: Bất kỳ NVKD nào quản lý hợp đồng đó đều có quyền hủy.<br>**Lựa chọn C**: NVKD tạo bảng hoặc KTT / GĐKD có quyền hủy. | Cần xác nhận | – | Cần căn cứ chính xác để thiết kế phân quyền (Authorization). Ảnh hưởng SYS-US-05 (P1, Bước 2, Nhánh A2, AC-US05-01, AC-US05-04). |
| **OQ-US05-02** | TA-SPEC §4.5 tr.2 ("Sau khi hủy, bảng chuyển sang Cancelled và không dùng lại được"); §5 PAY-01 tr.2 ("Mỗi hợp đồng chỉ có một bảng thanh toán cho mỗi tháng"); TA-PDF tr.2 | Mơ hồ | Sau khi một bảng thanh toán của kỳ tháng M bị hủy sang `Cancelled`, hợp đồng đó có được phép lập một bảng thanh toán mới cho cùng kỳ tháng M đó nữa không? | **Lựa chọn A**: Được phép lập bảng thanh toán mới cho kỳ đó (bảng Cancelled chỉ lưu vết audit, không tính vào ràng buộc duy nhất của kỳ).<br>**Lựa chọn B**: Không được phép lập lại trong cùng kỳ. | Cần xác nhận | – | PAY-01 quy định mỗi hợp đồng chỉ có một bảng cho mỗi tháng. Quyết định ràng buộc duy nhất của kỳ (Filtered Unique Index). Ảnh hưởng SYS-US-05 (S4, AC-US05-08), US-PAY-01 (PAY-01). |
| **OQ-US05-03** | TA-SPEC §4.5 tr.2 ("Bảng ở trạng thái Draft có thể bị hủy khi không còn cần thiết"); §6 tr.3 ("Mọi thay đổi trạng thái và mọi điều chỉnh phải được ghi audit log (ai, lúc nào, thay đổi gì)"); TA-PDF tr.2, tr.3 | Thiếu | Thao tác hủy bảng thanh toán Draft có bắt buộc người dùng nhập "Lý do hủy" (Cancellation Reason) hay không? Và lý do này được lưu trên bảng thanh toán hay chỉ lưu trong Audit Log? | **Lựa chọn A**: Bắt buộc nhập lý do hủy.<br>**Lựa chọn B**: Tùy chọn nhập lý do hủy (optional).<br>**Lựa chọn C**: Không yêu cầu lý do hủy. | Cần xác nhận | – | §4.5 không quy định rõ trường lý do hủy. Quyết định API contract và schema lưu trữ. Ảnh hưởng SYS-US-05 (Bước 1, 4, Nhánh A4, S3, AC-US05-01, AC-US05-07). |

## Bổ sung US-PAY-02 ngày 08/11/2026 (P-16)

Đầu vào: [sys-us-02-v1.md](sys-us-02-v1.md), TA-SPEC §2–4.3, PAY-04, PAY-06, PAY-08; TA-PDF tr.1–2 (dẫn trang theo sổ nguồn). Các dòng của US khác ở trên được giữ nguyên. OQ-05 là ID giữ chỗ được điền nội dung, OQ-US02-01/02 giữ nguyên ID đã có trong sys spec. Tất cả chưa có câu trả lời xác nhận.

| ID | Vị trí mọi nguồn | Loại Mâu thuẫn/Mơ hồ/Thiếu | Mô tả | Lý do cần xác nhận | Lựa chọn | Ảnh hưởng | Trạng thái | Người/ngày/câu trả lời và tham chiếu |
|---|---|---|---|---|---|---|---|---|
| OQ-05 | TA-SPEC §5 PAY-04 “thiếu dòng dịch vụ bắt buộc”; TA-PDF tr.2 | Thiếu | Danh sách dòng bắt buộc và tiêu chí xác định thiếu? | Chưa đủ căn cứ xây dựng kiểm tra đầy đủ dòng | Người phụ trách cung cấp danh sách/quy tắc theo hợp đồng hoặc dịch vụ | SYS-US-02 P3, bước 4, A4.1; AC-US02-01/04 | Cần xác nhận | Chưa có |
| OQ-US02-01 | TA-SPEC §2 và §4.2 “NVKD”; TA-PDF tr.1–2 | Mơ hồ | NVKD được trình bảng nào? | Vai trò chưa xác định quyền trên từng bảng | Chỉ bảng mình lập / phạm vi được phân công / mọi bảng; chưa chọn | SYS-US-02 P1, bước 2, A2; AC-US02-01/06 | Cần xác nhận | Chưa có |
| OQ-US02-02 | TA-SPEC §4.2 “gửi thông báo cho người duyệt”; TA-PDF tr.2 | Thiếu | Kênh/nội dung thông báo; gửi lỗi thì trạng thái và kết quả trình ra sao? | Tránh tự coi trình hoàn tất hoặc gửi trùng khi thông báo lỗi | Giữ chờ và gửi lại / hoàn tác trình; cần xác nhận cả kênh và nội dung | SYS-US-02 bước 7–8, A7, hậu điều kiện; AC-US02-01/12 | Cần xác nhận | Chưa có; OQ-US03-05 về thông báo kết quả duyệt không thay câu hỏi này |

### Đối chiếu phụ thuộc dùng chung của US-PAY-02

Đây là ghi nhận ảnh hưởng bổ sung, không thay thế đề xuất/câu hỏi US-PAY-03 trong bảng gốc. Khi dùng cho US-PAY-02, trạng thái là **Cần xác nhận**; “Không còn” hoặc “không chặn” trong cột ảnh hưởng cũ không phải bằng chứng khách hàng đã trả lời. [TA-SPEC §3, §4.2–4.3, PAY-06, PAY-08; TA-PDF tr.1–2; bảng đề xuất P-04..P-07 ở trên]

| ID hiện có | Căn cứ và điều chưa chốt | Ảnh hưởng US-PAY-02 | Trạng thái / xác nhận |
|---|---|---|---|
| OQ-02 | §4.3 “từ” ↔ PAY-06 “trên”, TA-PDF tr.2: ai duyệt đúng 500 triệu | Bước 5/A5, AC-US02-01/10; Blocked by OQ-02 | Cần xác nhận; giữ đề xuất Đan Anh, chưa có xác nhận khách hàng |
| OQ-US03-02 | §2, §4.3, PAY-06, TA-PDF tr.1–2: ánh xạ vai trò sang người nhận | Bước 5/A5, AC-US02-01/10; Blocked by OQ-US03-02 | Cần xác nhận; không chốt vai trò/cá nhân hoặc thay thế chéo |
| OQ-US03-03 | §4.1, §4.3, PAY-03, PAY-06, TA-PDF tr.2: cơ sở tổng tiền so ngưỡng | Bước 5/A5, AC-US02-01/10; Blocked by OQ-US03-03 | Cần xác nhận; không tự thêm VAT/làm tròn từ đề xuất nhóm |
| OQ-04 | §3 ↔ PAY-08, TA-PDF tr.1–2: đích sau từ chối | A3.1, AC-US02-09; Blocked by OQ-04 | Cần xác nhận; không tự chốt Rejected/Draft |
| OQ-US03-07 | §3, PAY-08, TA-PDF tr.1–2: ai/khi nào đưa Rejected về Draft | A3.1, AC-US02-09; Blocked by OQ-US03-07 | Cần xác nhận; không tự chốt thao tác trở về Draft |

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
