# SYS-US-01 – Lập bảng thanh toán (v1)

> Phiên bản: v1 · Cập nhật: 08/11/2026 · Người phụ trách: Chờ nhóm điền
> Đầu vào: [TA-SPEC](../../../requirements/payment-management/spec.md) §1–6; [OQ chung](open-questions-v1.md); hướng dẫn quy trình của người dùng tại P-17
> AI: Codex / GPT-6 · Prompt: P-15, P-16, P-17 trong [prompt-log](../../../workflow/prompt-log.md)
> Trạng thái: Bản lần chạy đầu – BA Pending Review / Design Pending Approval
> Người dùng yêu cầu tiếp tục sửa trong v1; chưa chuyển sang v2. Báo cáo review cũ vẫn phản ánh bản trước lần sửa này.

Đã đọc TA-SPEC §1–6; chưa đọc trực tiếp TA-PDF trong lần sửa này. Mã SYS/AC/OQ/NFR là mã nội bộ, trừ US-PAY/PAY do đề đặt. Phạm vi: lập bảng và sửa Draft của US-PAY-01. Hợp đồng, bảng giá, sản lượng chỉ được đọc [ĐẶC TẢ] [TA-SPEC §1, §4.1].

**Điểm bắt đầu của use case là NVKD bấm “Lập bảng thanh toán”, khi chưa chọn hợp đồng, kỳ và bảng giá.** Hệ thống mở biểu mẫu, hỗ trợ nhập/chọn dữ liệu và kiểm tra theo từng bước. Bảng Draft chỉ được tạo sau thao tác lưu thành công. Mở biểu mẫu và xem dữ liệu tính thử không tạo bảng trong CSDL. Điểm bắt đầu và thao tác chọn bảng giá theo hướng dẫn người dùng; cách mở form, xem trước và nút “Lưu nháp” là đề xuất tương tác để thực hiện hướng dẫn đó [QUYẾT ĐỊNH ĐÃ XÁC NHẬN – về trình tự tương tác] [P-17, người dùng trong chat, 08/11/2026]; [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1].

## 1. Use case

### 1.1. Phạm vi và căn cứ

| Yêu cầu | Áp dụng | Căn cứ |
|---|---|---|
| US-PAY-01 | NVKD lập bảng; tự sinh dòng/tổng, lưu Draft; sửa khi Draft. | [ĐẶC TẢ] TA-SPEC §4.1 |
| PAY-01 | Kiểm tra hợp đồng Active, bảng giá phù hợp và duy nhất theo tháng. Kỳ tháng/quý chưa thống nhất: Blocked by OQ-01. Lập lại sau hủy: Blocked by OQ-US05-02. | [ĐẶC TẢ] TA-SPEC §2, §5 PAY-01, §4.5 |
| PAY-02 | Sản lượng kỳ phải Đã đối soát. | [ĐẶC TẢ] TA-SPEC §2, §5 PAY-02 |
| PAY-03 | Thành tiền dòng = sản lượng × đơn giá tại thời điểm tính. Tổng hợp thành tiền là AC dẫn xuất từ yêu cầu tính tổng. Giá/dòng/tổng cuối cùng: Blocked by OQ-US01-01, OQ-US01-04, OQ-US03-03. | [ĐẶC TẢ] / [AC dẫn xuất] TA-SPEC §4.1, §5 PAY-03 |
| PAY-04 | Kiểm tra tổng âm, dòng bắt buộc và chống trình duyệt trùng ở US-PAY-02; không chuyển thành điều kiện lập Draft. | [ĐẶC TẢ] TA-SPEC §4.2, §5 PAY-04 |
| PAY-05 | Approved không sửa theo PAY-05; mâu thuẫn với điều chỉnh §4.4 nằm ở OQ-03/US-PAY-04, ngoài luồng sửa Draft này. | [ĐẶC TẢ] TA-SPEC §4.1, §4.4, §5 PAY-05 |
| PAY-06, PAY-07 | Phân công người duyệt/cấm tự duyệt thuộc US-PAY-03. | [ĐẶC TẢ] TA-SPEC §4.3, §5 PAY-06, PAY-07 |
| PAY-08 | Mở sửa bảng bị từ chối còn Blocked by OQ-04, OQ-US03-07; không tự chuyển Rejected → Draft. | [ĐẶC TẢ] TA-SPEC §3, §5 PAY-08 |
| NFR-PAY-01 | Audit mọi thay đổi trạng thái và điều chỉnh: ai, lúc nào, thay đổi gì. | [ĐẶC TẢ] TA-SPEC §6 gạch 1 |
| NFR-PAY-02 | Lập bảng ≤3 giây với hợp đồng <200 dòng. Phạm vi đo: Blocked by OQ-US01-06; không tính thời gian NVKD suy nghĩ/nhập liệu thành một cam kết mới. | [ĐẶC TẢ] TA-SPEC §6 gạch 2 |

### 1.2. Thông tin chung và dữ liệu trên biểu mẫu

| Mục | Đặc tả |
|---|---|
| Tên / tác nhân / mục tiêu | SYS-US-01 – Lập bảng thanh toán; NVKD thực hiện để có bảng Draft từ nguồn chỉ đọc. [ĐẶC TẢ] [TA-SPEC §1, §2, §4.1] |
| Kích hoạt | NVKD bấm nút “Lập bảng thanh toán”. Chưa yêu cầu NVKD đã chọn hợp đồng/kỳ/bảng giá trước khi bắt đầu. [QUYẾT ĐỊNH ĐÃ XÁC NHẬN – về tương tác] [P-17, người dùng, 08/11/2026] |
| P1 – Trước khi mở | NVKD đang truy cập ứng dụng; server kiểm tra phiên/vai trò khi mở và khi nhận yêu cầu tiếp theo. Cách xác thực là đề xuất kỹ thuật. Phạm vi hợp đồng/bảng được thao tác: Blocked by OQ-US01-03. [ĐẶC TẢ] / [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §2, §4.1] |
| P2 – Điều kiện để lưu | Hợp đồng Active, kỳ hợp lệ và chưa bị chiếm theo chính sách đã xác nhận; đây là kiểm tra trong quy trình sau khi chọn, không phải dữ liệu phải có sẵn trước bước 1. Blocked by OQ-01, OQ-US01-05, OQ-US05-02. [ĐẶC TẢ] [TA-SPEC §2, §5 PAY-01, §4.5] |
| P3 – Điều kiện tính | Bảng giá được chọn phải phù hợp; sản lượng kỳ Đã đối soát. Không ghi vào module nguồn. Blocked by OQ-US01-01, OQ-US01-04 cho tiêu chí còn thiếu. [ĐẶC TẢ] [TA-SPEC §1, §5 PAY-01..03] |
| P4 – Điều kiện sửa | Bảng đã lưu tồn tại, hiện Draft; phạm vi trường được sửa: Blocked by OQ-US01-02; quyền: Blocked by OQ-US01-03. Rejected chờ OQ-04/OQ-US03-07. [ĐẶC TẢ] [TA-SPEC §4.1, §5 PAY-08] |
| Hậu điều kiện thành công | Bảng, dòng và tổng đã lưu ở Draft; đề xuất trả cả id và version để dùng khi sửa, ghi audit create/update trong cùng giao dịch. [ĐẶC TẢ] / [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1, §6 gạch 1] |
| Hậu điều kiện lỗi | Lỗi kiểm tra: giữ biểu mẫu và chỉ rõ trường/điều kiện cần sửa. Lỗi ghi xác định chưa commit: không có dữ liệu/audit lưu một phần. Nếu mất kết quả commit, chưa được kết luận bảng chưa tồn tại; cần kiểm tra kết quả theo cơ chế DB sẽ chọn. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1, §6 gạch 1] |
| NFR-PAY-01 | Áp dụng audit sửa Draft; đề xuất ghi cả sự kiện tạo Draft. Mở form/xem trước chưa làm thay đổi bảng nên không ghi audit thay đổi bảng thành công. [ĐẶC TẢ] / [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §6 gạch 1] |
| NFR-PAY-02 | Giữ nguyên ≤3 giây, <200 dòng; điểm bắt đầu/kết thúc phép đo và cách đếm dòng chờ OQ-US01-06. Chưa đo; không tự áp SLA cho sửa Draft. [ĐẶC TẢ] [TA-SPEC §6 gạch 2] |

| Thông tin | NVKD thao tác | Hệ thống cung cấp / kiểm tra | Căn cứ |
|---|---|---|---|
| Hợp đồng | Chọn trên biểu mẫu sau khi mở. | Đọc danh sách, chi tiết, trạng thái và cấu hình kỳ; phạm vi danh sách chờ OQ-US01-03. | [ĐẶC TẢ] TA-SPEC §4.1, PAY-01 |
| Kỳ thanh toán | Nhập/chọn sau khi chọn hợp đồng. | Hiển thị kiểu kỳ theo cấu hình; kiểm tra kỳ và trùng; chưa tự chốt khóa tháng/quý. | [ĐẶC TẢ] TA-SPEC §2, PAY-01 |
| Bảng giá | Chọn từ dữ liệu được tải theo hợp đồng/kỳ. | Xác minh bảng giá được chọn phù hợp, không tin id/giá client gửi; tiêu chí phù hợp chờ OQ-US01-01. | [QUYẾT ĐỊNH ĐÃ XÁC NHẬN – về tương tác] P-17; [ĐẶC TẢ] PAY-01, PAY-03 |
| Dòng: dịch vụ, sản lượng, đơn giá, thành tiền; tổng | Xem và kiểm tra kết quả được sinh. | Đọc nguồn và tính; không mặc định cho nhập đè sản lượng/đơn giá/thành tiền. Quyền sửa sau lưu chờ OQ-US01-02. | [ĐẶC TẢ] TA-SPEC §2, §4.1, PAY-02, PAY-03 |

“Nhập thông tin” ở luồng này là nhập/chọn hợp đồng, kỳ và bảng giá nêu trên. Chưa bổ sung mã tự nhập, ngày lập, ghi chú hay trường bắt buộc khác khi chưa được yêu cầu.

### 1.3. Dòng cơ bản – lập bảng từ màn hình

| Bước | Tác nhân | Hành động và phản hồi |
|---|---|---|
| 1 | NVKD | Bấm “Lập bảng thanh toán” để bắt đầu use case. [QUYẾT ĐỊNH ĐÃ XÁC NHẬN – tương tác] [P-17] |
| 2 | Hệ thống | Nhận yêu cầu mở chức năng, kiểm tra phiên/vai trò NVKD; đọc danh sách hợp đồng được phép chọn. Phạm vi danh sách: Blocked by OQ-US01-03. Chưa ghi bảng. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §2, §4.1] |
| 3 | Hệ thống | Hiển thị biểu mẫu lập mới với vùng chọn hợp đồng; vùng kỳ, bảng giá và kết quả tính chờ lựa chọn tương ứng. [ĐỀ XUẤT KỸ THUẬT] [P-17; TA-SPEC §4.1] |
| 4 | NVKD | Chọn hợp đồng trên biểu mẫu. [ĐẶC TẢ] [TA-SPEC §4.1] |
| 5 | Hệ thống | Đọc và kiểm tra hợp đồng tồn tại, quyền và Active; trả thông tin hợp đồng/cấu hình kỳ để nhập kỳ. Mốc Active: Blocked by OQ-US01-05; phạm vi quyền: Blocked by OQ-US01-03. [ĐẶC TẢ] / [AC dẫn xuất] [TA-SPEC §2, PAY-01] |
| 6 | NVKD | Nhập/chọn kỳ theo thông tin hợp đồng vừa tải. [ĐẶC TẢ] [TA-SPEC §2, §4.1] |
| 7 | Hệ thống | Kiểm tra kỳ, tra trùng sơ bộ, đọc các bảng giá phù hợp với hợp đồng/kỳ. Blocked by OQ-01, OQ-US05-02, OQ-US01-01 về các chính sách còn mở. [ĐẶC TẢ] / [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §2, PAY-01] |
| 8 | Hệ thống | Hiển thị các bảng giá có thể chọn; người dùng xem thông tin nguồn để lựa chọn. Đọc danh sách không tự sửa hay tạo bảng giá. [ĐỀ XUẤT KỸ THUẬT] [P-17; TA-SPEC §1, PAY-01] |
| 9 | NVKD | Chọn bảng giá trên biểu mẫu. [QUYẾT ĐỊNH ĐÃ XÁC NHẬN – tương tác] [P-17] |
| 10 | Hệ thống | Kiểm tra lựa chọn đủ và hợp lệ; đọc bảng giá được chọn và sản lượng kỳ, kiểm tra giá phù hợp/Đã đối soát, sinh dòng, tính mỗi dòng = sản lượng × đơn giá và tổng. Đây là dữ liệu xem trước, chưa lưu Draft. Blocked by OQ-US01-01, OQ-US01-04, OQ-US03-03 về chọn giá/ánh xạ dòng/xử lý tiền cuối cùng. [ĐẶC TẢ] / [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1, PAY-01..03] |
| 11 | Hệ thống | Hiển thị dịch vụ, sản lượng, đơn giá, thành tiền và tổng để NVKD kiểm tra; giữ thông tin hợp đồng/kỳ/bảng giá đã chọn. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §2, §4.1] |
| 12 | NVKD | Kiểm tra thông tin. Nếu đổi hợp đồng/kỳ/bảng giá, quay bước tương ứng theo A12 để tải/tính lại; không dùng kết quả cũ cho lựa chọn mới. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1, PAY-03] |
| 13 | NVKD | Bấm “Lưu nháp” sau khi kiểm tra; giao diện gửi các định danh đã chọn và ngữ cảnh lần tính, không dùng tổng do client nhập làm số liệu quyết định. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1, PAY-03] |
| 14 | Hệ thống | Kiểm tra lại phía server: phiên/quyền, hợp đồng, kỳ, trùng, bảng giá và đối soát; tạo kết quả tính hợp lệ để lưu từ nguồn theo chính sách thời điểm được xác nhận. Nếu nguồn đổi sau xem trước: Blocked by OQ-US01-01, OQ-US01-04, OQ-US01-05, OQ-US01-02; không tự quyết giữ số cũ hay thay số mới. Các kiểm tra ở form không thay kiểm tra lúc lưu. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §1, §4.1, PAY-01..03] |
| 15 | Hệ thống | Mở giao dịch, bảo đảm duy nhất nguyên tử theo phạm vi kỳ được xác nhận, lưu bảng/dòng/tổng ở Draft và audit create: ai, lúc nào, trước=chưa có bảng, sau=dữ liệu đã lưu; commit cùng nhau. “Chưa có bảng” không phải trạng thái bổ sung. Blocked by OQ-01, OQ-US05-02 về phạm vi duy nhất. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §3, §4.1, PAY-01, §6 gạch 1] |
| 16 | Hệ thống | Sau khi xác nhận commit thành công, hiển thị bảng Draft đã lưu cùng id/version, dữ liệu dòng/tổng. Chưa trình duyệt. [ĐẶC TẢ] / [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1] |

### 1.4. Dòng thay thế và vòng quay lại

| Nhánh | Rẽ từ | Xử lý và điểm quay lại |
|---|---|---|
| A2 | 2; mọi yêu cầu sau đó | Chưa xác thực: yêu cầu đăng nhập; đã xác thực nhưng không có vai trò/quyền: báo không được phép. Không tải dữ liệu ngoài quyền, không ghi bảng. Phạm vi quyền: Blocked by OQ-US01-03. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §2, §4.1] |
| A3 | 2–3 | Lỗi tải danh sách: báo lỗi và cho thử lại bước 2. Danh sách hợp lệ nhưng rỗng: thông báo chưa có hợp đồng để chọn, không tạo Draft rỗng. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1, PAY-01] |
| A5 | 5 | Hợp đồng không tồn tại/không Active/không được phép: báo lý do tại biểu mẫu, quay bước 4; mốc hiệu lực và quyền chờ OQ-US01-05/OQ-US01-03. [AC dẫn xuất] [TA-SPEC §5 PAY-01, §4.1] |
| A7 | 7 | Kỳ thiếu/sai cấu hình hoặc đã bị chiếm: báo tại trường kỳ, quay bước 6. Không có bảng giá phù hợp: báo và cho đổi hợp đồng/kỳ; không cho chọn bảng giá bất kỳ để bỏ kiểm tra. Blocked by OQ-01, OQ-US05-02, OQ-US01-01. [AC dẫn xuất] [TA-SPEC §2, PAY-01] |
| A9 | 9–10 | Chưa chọn bảng giá hoặc lựa chọn không còn phù hợp: báo và quay bước 9/7. Sản lượng chưa Đã đối soát: báo không thể sinh bảng, cho đổi kỳ ở bước 6 hoặc dừng; không thiết kế thao tác đối soát. Dữ liệu rỗng/thiếu/trùng giá/không đủ tính: Blocked by OQ-US01-01/OQ-US01-04/OQ-US03-03 cho tiêu chí; không thay dữ liệu thiếu bằng 0. [AC dẫn xuất] [TA-SPEC §1, PAY-01..03] |
| A10 | 5, 7, 10, 14 | Lỗi đọc hợp đồng/giá/sản lượng hoặc tra trùng: trả lỗi, giữ lựa chọn, cho gửi lại bước tương ứng; không coi lỗi đọc là dữ liệu không tồn tại. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §1, §4.1, PAY-01..03] |
| A12 | 12 | Đổi hợp đồng: xóa lựa chọn kỳ/giá và kết quả phụ thuộc, quay bước 5. Đổi kỳ: tải lại giá, xóa giá/kết quả cũ, quay bước 7. Đổi bảng giá: tính lại bước 10. Phản hồi của yêu cầu lựa chọn cũ không được ghi đè lựa chọn mới. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1, PAY-03] |
| A13 | 1–13, trước khi lưu | NVKD đóng biểu mẫu: kết thúc, không tạo bảng/audit thay đổi bảng. Đây là thoát màn hình, không phải hủy một bảng Draft sang Cancelled của US-PAY-05. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §3, §4.1, §4.5] |
| A14 | 14 | Dữ liệu chọn không đủ/điều kiện không còn hợp lệ: báo lỗi tại biểu mẫu và quay bước chọn tương ứng, không ghi bảng. Chính sách khi nguồn đổi giữa xem trước/lưu còn Blocked by OQ-US01-01/OQ-US01-04/OQ-US01-05; xử lý cuối cùng chưa được chốt. [AC dẫn xuất] / [GIẢ ĐỊNH – Cần xác nhận] [TA-SPEC §5 PAY-01..03] |
| A15 | 15 | Yêu cầu khác vừa chiếm kỳ: rollback yêu cầu thua, báo xung đột, giữ form để NVKD kiểm tra; không tạo bảng thứ hai. Phạm vi duy nhất: Blocked by OQ-01, OQ-US05-02. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §5 PAY-01] |
| A15.1 | 15 | Lỗi mở giao dịch/lưu bảng/dòng/audit, hoặc commit được xác định chưa xảy ra: không lưu một phần; rollback khi giao dịch còn mở, báo lỗi. Không tuyên bố rollback được một giao dịch đã commit. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1, §6 gạch 1] |
| A15.2 | 15 | Không biết kết quả commit do mất phản hồi: báo “Chưa xác định kết quả lưu”, không báo chắc chắn chưa tạo và không tự gửi create lại; cần cơ chế xác minh kết quả khi chọn DB/driver. Đây là tình trạng kết quả thao tác, không phải trạng thái bảng mới. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1, §6 gạch 1] |

### 1.5. Sửa một Draft đã lưu

| Bước | Hành động và phản hồi |
|---|---|
| U1 | NVKD mở bảng đã lưu và bấm “Chỉnh sửa”. Hệ thống đọc bảng gồm id, dữ liệu và version; version cũng có trong kết quả bước 16. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1] |
| U2 | Kiểm tra phiên, quyền và trạng thái hiện tại Draft; hiển thị dữ liệu đã lưu lên biểu mẫu sửa. Quyền: Blocked by OQ-US01-03; Rejected: Blocked by OQ-04/OQ-US03-07. [ĐẶC TẢ] / [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §3, §4.1, PAY-08] |
| U3 | NVKD sửa thông tin trong phạm vi được xác nhận. Không tự cho phép sửa từng trường hay nguồn dữ liệu: Blocked by OQ-US01-02; giá/dòng/hiệu lực theo OQ-US01-01/OQ-US01-04/OQ-US01-05 nếu phải đọc lại nguồn. [GIẢ ĐỊNH – Cần xác nhận] [TA-SPEC §1, §4.1, PAY-01..03] |
| U4 | NVKD bấm “Lưu thay đổi”; gửi nội dung sửa và expectedVersion đã nhận. Hệ thống đọc lại bản hiện tại, kiểm tra quyền/trạng thái/version, tính lại theo chính sách được xác nhận và tạo candidate gồm dữ liệu dòng/tổng hợp lệ phía server. Bản trước và candidate sau phải ứng với cùng version được cập nhật thành công. Blocked by OQ-US01-02, OQ-US03-03. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1, PAY-03] |
| U5 | Giao dịch cập nhật có điều kiện trạng thái vẫn Draft/version khớp. Repository lưu candidate, audit ghi before và chính candidate đã lưu làm after; cùng commit, không lưu riêng raw request khác với kết quả tính. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1, PAY-03, §6 gạch 1] |
| U6 | Trả và hiển thị cùng dữ liệu đã lưu, trạng thái Draft, version mới. [ĐẶC TẢ] / [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1] |

| Nhánh | Rẽ từ | Xử lý |
|---|---|---|
| AU1 | U1–U2 hoặc U4 | Bảng không tồn tại/lỗi đọc: thông báo, không mở form hoặc lưu sửa từ dữ liệu thiếu. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1] |
| AU2 | U2 hoặc U4 | Sai phiên/quyền hoặc bảng không Draft: từ chối sửa. Rejected chờ OQ-04/OQ-US03-07; điều chỉnh Approved thuộc US-PAY-04/OQ-03. [AC dẫn xuất] [TA-SPEC §3, §4.1, §4.4, PAY-05, PAY-08] |
| AU4 | U4 | Nội dung không hợp lệ: giữ form, nêu lỗi, quay U3; thiếu version: yêu cầu tải lại representation có version. Các trường sửa/tính lại còn Blocked by OQ-US01-02/OQ-US03-03. [ĐỀ XUẤT KỸ THUẬT] / [GIẢ ĐỊNH – Cần xác nhận] [TA-SPEC §4.1, PAY-03] |
| AU5 | U5 | Trạng thái/version đã đổi: rollback cập nhật, báo xung đột, cho tải lại; không ghi đè giao dịch khác. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §3, §4.1] |
| AU5.1 | U5 | Lỗi lưu/audit/commit xác định chưa commit: rollback dữ liệu và audit yêu cầu sửa. Kết quả commit chưa rõ xử lý như A15.2, không kết luận dữ liệu cũ còn nguyên. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §6 gạch 1] |

## 2. Điểm cần xác nhận

Cột **Vị trí mọi nguồn** gồm căn cứ TA-SPEC và vị trí cụ thể trong quy trình này. Các OQ giữ ID ổn định. Hướng dẫn bấm nút và chọn bảng giá P-17 chỉ xác nhận tương tác; chưa trả lời các chính sách giá, kỳ, quyền hay sửa Draft. Những đề xuất VAT/làm tròn của US-PAY-03 vẫn chờ xác nhận; công thức tiền cuối cùng bị chặn, phần mở form và chọn dữ liệu vẫn có thể thiết kế.

| ID | Vị trí mọi nguồn | Loại | Mô tả | Đề xuất / Lựa chọn | Trạng thái | Người/ngày/tham chiếu | Còn mở / ảnh hưởng |
|---|---|---|---|---|---|---|---|
| OQ-01 | TA-SPEC §2 “tháng hoặc quý tùy cấu hình” ↔ §5 PAY-01 “mỗi tháng”<br>**Vị trí trong quy trình:** [sys-us-01-v1.md](sys-us-01-v1.md), §1.2 P2; §1.3 bước 7, 14, 15; §1.4 A7, A14, A15; §3 AC-US01-06, AC-US01-14. | Mâu thuẫn | Với hợp đồng cấu hình quý, lập một bảng quý hay các bảng tháng? Có cho chồng lấn tháng/quý không? | A: duy nhất theo kỳ cấu hình; B: duy nhất theo tháng và cần làm rõ cách biểu diễn quý; chờ người phụ trách. | Cần xác nhận | – | Chặn hoàn thiện kiểm tra kỳ/trùng ở bước 7/14/15; phần mở biểu mẫu độc lập. Chưa chốt khóa tháng/quý. |
| **OQ-US05-02** | TA-SPEC §4.5 tr.2 ("Sau khi hủy, bảng chuyển sang Cancelled và không dùng lại được"); §5 PAY-01 tr.2 ("Mỗi hợp đồng chỉ có một bảng thanh toán cho mỗi tháng"); TA-PDF tr.2<br>**Vị trí trong quy trình:** [sys-us-01-v1.md](sys-us-01-v1.md), §1.2 P2; §1.3 bước 7, 14, 15; §1.4 A7, A14, A15; §3 AC-US01-07, AC-US01-14. | Mơ hồ | Sau khi một bảng thanh toán của kỳ tháng M bị hủy sang `Cancelled`, hợp đồng đó có được phép lập một bảng thanh toán mới cho cùng kỳ tháng M đó nữa không? | **Lựa chọn A**: Được phép lập bảng thanh toán mới cho kỳ đó (bảng Cancelled chỉ lưu vết audit, không tính vào ràng buộc duy nhất của kỳ).<br>**Lựa chọn B**: Không được phép lập lại trong cùng kỳ. | Cần xác nhận | – | Chặn xác định Cancelled có chiếm kỳ ở bước 7/14/15; giữ trạng thái Cần xác nhận của v1, không lấy quyết định từ v2 để chốt v1. |
| OQ-US03-03 | §4.3; PAY-06; PAY-03; §4.1<br>**Vị trí trong quy trình:** [sys-us-01-v1.md](sys-us-01-v1.md), §1.3 bước 10, 14; §1.4 A9; §1.5 U4, AU4; §3 AC-US01-11, AC-US01-12, AC-US01-17. | Thiếu | Tổng tiền so ngưỡng: thời điểm, VAT, làm tròn; sửa khi `PendingApproval` | P-04: "có tính VAT". P-05: "tổng tiền lấy tại thời điểm lập"; "làm tròn theo tiền Việt"; "thuế mặc định để tôi xác nhận với khách hàng sau"; "chỉ được sửa ở trạng thái Draft". P-06: "Cần xác nhận, chỉ cần biết là thuế"; "làm tròn dòng tổng, làm tròn lên". P-07: "giá trị thuế là 1 giá trị x hoặc % trên tổng" | **Đề xuất của Đan Anh – chờ khách hàng xác nhận** | Đan Anh / 07/11/2026 / P-04..P-07 | Các câu P-04..P-07 là đề xuất nhóm chưa được khách hàng xác nhận; chưa chốt có thuế, cơ sở/loại/giá trị thuế, thứ tự/độ chính xác/cách làm tròn. Chặn kết quả tiền cuối cùng và AC-US01-12/U4; không chặn mở form/chọn dữ liệu hay công thức nhân PAY-03 có căn cứ. |
| OQ-04 | TA-SPEC §3 ↔ PAY-08 (tr.1–2)<br>**Vị trí trong quy trình:** [sys-us-01-v1.md](sys-us-01-v1.md), §1.2 P4; §1.5 U2, AU2; §3 AC-US01-18. | Mâu thuẫn | Đích sau từ chối | "rejected rồi draft" | **Đề xuất của Đan Anh – chờ khách hàng xác nhận** | Đan Anh / 07/11/2026 / P-04 | Chặn mở sửa bảng Rejected ở U2/AU2; không chặn luồng lập mới hoặc sửa bảng đã là Draft. |
| OQ-US03-07 | §3 "Rejected"; PAY-08 "quay về Draft để Nhân viên kinh doanh chỉnh sửa" (tr.1–2); trả lời OQ-04<br>**Vị trí trong quy trình:** [sys-us-01-v1.md](sys-us-01-v1.md), §1.2 P4; §1.5 U2, AU2; §3 AC-US01-18. | Thiếu | Bước `Rejected` → `Draft` do ai, khi nào | P-05: "khu Nhân viên kinh doanh thực hiện chỉnh sửa bảng reject" | **Đề xuất của Đan Anh – chờ khách hàng xác nhận** | Đan Anh / 07/11/2026 / P-05, P-06 | Chặn xác định người/thời điểm đưa Rejected về Draft khi mở sửa; chưa bổ sung transition này vào U2. |
| OQ-US01-01 | TA-SPEC §4.1 “từ sản lượng và bảng giá”; §5 PAY-01 “bảng giá phù hợp”, PAY-03 “đơn giá tại thời điểm tính”<br>**Vị trí trong quy trình:** [sys-us-01-v1.md](sys-us-01-v1.md), §1.2 P3; §1.3 bước 7, 9, 10, 14; §1.4 A7, A9, A14; §3 AC-US01-08, AC-US01-09, AC-US01-11, AC-US01-26. | Mơ hồ | “Phù hợp” được xác định theo dịch vụ/hợp đồng và mốc thời gian nào? Nếu giá đổi trong kỳ, nhiều giá cùng phù hợp hoặc thiếu giá cho dịch vụ thì xử lý ra sao? | Giá tại lúc lập / theo hiệu lực trong kỳ, có thể tách theo giai đoạn; người phụ trách cần chỉ rõ tiêu chí và xử lý thiếu/trùng giá. | Cần xác nhận | – | P-17 xác nhận NVKD chọn bảng giá trên form; tiêu chí giá phù hợp vẫn Cần xác nhận. Cần làm rõ giá đổi giữa xem trước/lưu hoặc trước sửa Draft: giữ lần tính cũ, tính lại hay yêu cầu xác nhận kết quả mới? Chặn chọn giá/tính cuối tại 7/10/14; transaction cục bộ không khóa module giá. |
| OQ-US01-02 | TA-SPEC §4.1 “được phép chỉnh sửa… Draft”; §5 PAY-01..03<br>**Vị trí trong quy trình:** [sys-us-01-v1.md](sys-us-01-v1.md), §1.2 P4; §1.5 U3, U4, AU4; §3 AC-US01-17. | Thiếu | Draft được sửa trường nào: hợp đồng/kỳ, thêm/xóa dòng, sản lượng/đơn giá hay chỉ thông tin khác? Khi lưu có lấy lại nguồn/tính lại không? | Giữ dữ liệu nguồn chỉ đọc / cho phép ghi đè một số trường của bảng với giới hạn cần xác nhận. | Cần xác nhận | – | Chặn danh mục trường sửa và cách tính lại U3/U4; nếu cho đổi hợp đồng/kỳ/giá, cần chỉ rõ tái kiểm tra PAY-01..03 và đọc lại nguồn. Việc chọn bảng giá khi lập mới theo P-17 không tự mở quyền sửa đơn giá/sản lượng nguồn. |
| OQ-US01-03 | TA-SPEC §2 “NVKD… lập”; §4.1 “NVKD… chỉnh sửa”; §5 PAY-07 chỉ nói cấm tự duyệt<br>**Vị trí trong quy trình:** [sys-us-01-v1.md](sys-us-01-v1.md), §1.2 P1; §1.3 bước 2, 5, 14; §1.4 A2, A5; §1.5 U2, AU2; §3 AC-US01-03. | Thiếu | NVKD được lập trên mọi hợp đồng hay chỉ hợp đồng được giao? Được sửa Draft do NVKD khác tạo không? | A: theo hợp đồng được giao/người tạo; B: mọi NVKD; cần xác nhận từng thao tác. | Cần xác nhận | – | Chặn phạm vi danh sách hợp đồng và quyền tại bước 2/5/14/U2; vai trò NVKD có nguồn độc lập. PAY-07 không xác lập quyền sở hữu Draft. |
| OQ-US01-04 | TA-SPEC §2 “một dịch vụ trong bảng”; §4.1 “tự sinh… từ sản lượng”; §5 PAY-02, PAY-03<br>**Vị trí trong quy trình:** [sys-us-01-v1.md](sys-us-01-v1.md), §1.2 P3; §1.3 bước 10, 14; §1.4 A9, A14; §3 AC-US01-10, AC-US01-26. | Thiếu | Không có bản ghi sản lượng có khác sản lượng 0 đã đối soát không? Nhiều bản ghi cùng dịch vụ gộp/tách thế nào, dịch vụ nào được đưa vào bảng? | Không lập khi không có dữ liệu / cho lập bảng rỗng; gộp theo dịch vụ / tách theo dữ liệu nguồn hoặc giai đoạn giá; chờ xác nhận. | Cần xác nhận | – | Cần xác nhận dữ liệu rỗng/0, gộp/tách dịch vụ và đối soát một phần; nếu nguồn sản lượng đổi giữa xem trước/lưu thì giữ bản tính hay yêu cầu tính lại? Chặn ánh xạ dòng tại 10/14; không tự coi thiếu dữ liệu là 0. |
| OQ-US01-05 | TA-SPEC §5 PAY-01 “đang hiệu lực (Active)”; §2 kỳ thanh toán<br>**Vị trí trong quy trình:** [sys-us-01-v1.md](sys-us-01-v1.md), §1.2 P2; §1.3 bước 5, 14; §1.4 A5, A14; §3 AC-US01-05, AC-US01-26. | Mơ hồ | Đánh giá Active ở thời điểm gửi yêu cầu hay cần hiệu lực trong toàn bộ/một phần kỳ? Hợp đồng hết hiệu lực sau kỳ có được lập cho kỳ đã qua không? | Active tại lúc lập / theo hiệu lực của kỳ; cần chỉ rõ mốc đánh giá và kiểm tra lại khi nguồn thay đổi. | Cần xác nhận | – | Cần xác nhận mốc Active và cách xử lý hợp đồng/cấu hình đổi sau khi tải form hoặc giữa xem trước/lưu. Chặn guard hiệu lực bước 5/14; không tự cấm lập kỳ quá khứ/tương lai. |
| OQ-US01-06 | TA-SPEC §6 gạch 2 “phản hồi trong vòng 3 giây… dưới 200 dòng”<br>**Vị trí trong quy trình:** [sys-us-01-v1.md](sys-us-01-v1.md), §1.2 hàng NFR-PAY-02; §3 AC-US01-20. | Thiếu | Đo từ thao tác UI tới hiển thị hay từ server nhận yêu cầu tới phản hồi? Số dòng tính theo dữ liệu nguồn hay dòng bảng sau sinh, môi trường đo nào? | Xác nhận điểm bắt đầu/kết thúc, cách đếm dòng và môi trường; giữ nguyên ≤3 giây, <200 dòng. | Cần xác nhận | – | Quy trình mới có nhiều lượt tải và thời gian người dùng nhập/chọn. Cần xác nhận thao tác/điểm đo và cách đếm dòng; giữ ≤3 giây, <200 dòng, chưa đo và không tự áp SLA mới cho mỗi lượt hay cả thời gian nhập. |

## 3. Acceptance criteria

Mã AC-US01-kk do nhóm đặt; giữ AC-01..20 và bổ sung AC-21..26 cho phần tương tác trước lưu. Những AC có OQ chưa được coi là đã đáp ứng.

| ID | Given / When / Then | Nhãn | Nguồn | OQ |
|---|---|---|---|---|
| AC-US01-01 | Given dữ liệu hợp lệ; When NVKD đi từ bước 1 đến 16; Then bảng/dòng/tổng được lưu Draft và hiển thị sau commit, không tự trình duyệt. | [AC dẫn xuất] | TA-SPEC §4.1 | Phần kỳ/giá/tổng theo OQ bên dưới |
| AC-US01-02 | Given sai phiên hoặc không có vai trò NVKD; When mở/làm việc trên form (2,14/U2); Then từ chối trước ghi (A2/AU2). | [ĐỀ XUẤT KỸ THUẬT] | TA-SPEC §2, §4.1 | – |
| AC-US01-03 | Given NVKD và hợp đồng/bảng; When tải danh sách/chọn/sửa (2,5,14/U2); Then giới hạn theo quyền được xác nhận (A2/A5/AU2). | [AC dẫn xuất] | TA-SPEC §2, §4.1 | Blocked by OQ-US01-03 |
| AC-US01-04 | Given thiếu/sai hợp đồng/kỳ/bảng giá; When chọn hoặc lưu (5,7,10,14); Then hiển thị lỗi, cho sửa lựa chọn, không ghi Draft (A5/A7/A9/A14). | [AC dẫn xuất] | TA-SPEC §4.1; P-17 | – |
| AC-US01-05 | Given hợp đồng không tồn tại/không Active; When kiểm tra (5/14); Then báo tại form và không lập (A5/A14). | [AC dẫn xuất] | TA-SPEC §5 PAY-01 | Blocked by OQ-US01-05 cho mốc hiệu lực |
| AC-US01-06 | Given kỳ sai cấu hình/đã bị chiếm; When kiểm tra (7/14); Then báo và không tạo thêm (A7/A14). | [AC dẫn xuất] | TA-SPEC §2, PAY-01 | Blocked by OQ-01 |
| AC-US01-07 | Given bảng cùng kỳ đã Cancelled; When tra trùng/lưu (7/14/15); Then xử lý theo quyết định lập lại, giữ bảng cũ Cancelled. | [AC dẫn xuất] | TA-SPEC §4.5, PAY-01 | Blocked by OQ-US05-02 |
| AC-US01-08 | Given không có giá phù hợp hoặc sản lượng chưa đối soát; When tải giá/tính/lưu (7/10/14); Then báo lý do, không tạo bảng (A7/A9/A14). | [AC dẫn xuất] | TA-SPEC §5 PAY-01, PAY-02 | Blocked by OQ-US01-01 cho phù hợp |
| AC-US01-09 | Given giá thay đổi/thiếu/nhiều giá; When chọn và tính (7/10/14); Then áp chính sách đã xác nhận; id bảng giá được chọn phải được kiểm tra server. | [AC dẫn xuất] | TA-SPEC §4.1, PAY-01, PAY-03; P-17 | Blocked by OQ-US01-01 |
| AC-US01-10 | Given nguồn rỗng/0/nhiều bản ghi/đối soát một phần; When sinh dòng (10/14); Then xử lý theo chính sách đã xác nhận (A9/A14), không mặc định thiếu=0. | [AC dẫn xuất] | TA-SPEC §2, PAY-02, PAY-03 | Blocked by OQ-US01-04 |
| AC-US01-11 | Given q và p xác định; When sinh dòng (10/14); Then thành tiền trước xử lý tiền còn mở bằng q × p, đọc q/p từ nguồn. | [AC dẫn xuất] | TA-SPEC §5 PAY-03 | Chọn giá: OQ-US01-01; xử lý tiền: OQ-US03-03 |
| AC-US01-12 | Given các dòng đã tính; When tính tổng (10/14/U4); Then nhất quán với dòng và chính sách tiền được xác nhận, không tự thêm VAT/làm tròn. | [AC dẫn xuất] | TA-SPEC §4.1, PAY-03 | Blocked by OQ-US03-03 |
| AC-US01-13 | Given lỗi interface hoặc tra dữ liệu; When tải form/chọn/tính (2/5/7/10/14/U1); Then báo lỗi, giữ form khi đã mở, không ghi từ dữ liệu thiếu (A3/A10/AU1). | [ĐỀ XUẤT KỸ THUẬT] | TA-SPEC §1, §4.1, PAY-01..03 | – |
| AC-US01-14 | Given hai yêu cầu cùng chiếm một phạm vi kỳ; When ghi (15); Then nhiều nhất một bảng được tạo, yêu cầu thua báo xung đột (A15). | [AC dẫn xuất] / [ĐỀ XUẤT KỸ THUẬT] | TA-SPEC §5 PAY-01 | Blocked by OQ-01, OQ-US05-02 |
| AC-US01-15 | Given lưu hợp lệ; When commit (15–16); Then bảng/dòng và audit create cùng tồn tại, audit có ai/lúc nào/thay đổi gì. | [ĐỀ XUẤT KỸ THUẬT] | TA-SPEC §6 gạch 1 | – |
| AC-US01-16 | Given lỗi giao dịch; When lưu (15/U5); Then lỗi xác định chưa commit không lưu một phần (A15.1/AU5.1); kết quả commit chưa rõ không bị báo chắc chắn chưa lưu (A15.2). | [ĐỀ XUẤT KỸ THUẬT] | TA-SPEC §4.1, §6 gạch 1 | – |
| AC-US01-17 | Given Draft, đủ quyền và nội dung được phép; When sửa U1–U6; Then lưu cùng candidate đã tính/kiểm tra vào bảng, audit và response; sai nội dung giữ form (AU4). | [AC dẫn xuất] / [ĐỀ XUẤT KỸ THUẬT] | TA-SPEC §4.1, PAY-03, §6 | Blocked by OQ-US01-02, OQ-US01-03, OQ-US03-03 |
| AC-US01-18 | Given không có bảng/không Draft; When mở sửa U1/U2; Then không mở luồng sửa Draft từ dữ liệu sai (AU1/AU2). | [AC dẫn xuất] | TA-SPEC §3, §4.1 | Rejected: Blocked by OQ-04, OQ-US03-07 |
| AC-US01-19 | Given representation có version; When tạo/đọc/sửa; Then UI nhận version ở 16/U1/U6; thiếu token yêu cầu tải lại (AU4), token/trạng thái cũ không ghi đè (AU5). | [ĐỀ XUẤT KỸ THUẬT] | TA-SPEC §4.1 | – |
| AC-US01-20 | Given hợp đồng <200 dòng; When lập; Then phản hồi ≤3 giây theo cách đo được xác nhận, 200 dòng không nằm trong điều kiện này. | [AC dẫn xuất] | TA-SPEC §6 gạch 2 | Blocked by OQ-US01-06; chưa đo |
| AC-US01-21 | Given chưa chọn dữ liệu; When NVKD bấm Lập bảng (1–3); Then mở form trước khi yêu cầu chọn hợp đồng/kỳ/giá, chưa ghi Draft. Nếu không có hợp đồng, hiển thị rỗng (A3). | [AC dẫn xuất] / [ĐỀ XUẤT KỸ THUẬT] | P-17; TA-SPEC §4.1 | Danh sách theo OQ-US01-03 |
| AC-US01-22 | Given form mở; When chọn hợp đồng (4–5), nhập kỳ (6–8), chọn giá (9); Then tải dữ liệu phụ thuộc theo thứ tự, không yêu cầu chọn sẵn trước bước 1. | [AC dẫn xuất] / [ĐỀ XUẤT KỸ THUẬT] | P-17; TA-SPEC §2, §4.1, PAY-01 | Phù hợp/kỳ theo OQ-US01-01/OQ-01 |
| AC-US01-23 | Given đã chọn đủ; When tính xem trước (10–12); Then hiển thị dòng/tổng để kiểm tra; chỉ bấm Lưu nháp mới gửi yêu cầu ghi (13–16). | [ĐỀ XUẤT KỸ THUẬT] | P-17; TA-SPEC §4.1 | Tiền cuối theo OQ-US03-03 |
| AC-US01-24 | Given đã có kết quả; When đổi hợp đồng/kỳ/giá (A12); Then xóa dữ liệu phụ thuộc và tải/tính lại; bỏ phản hồi cũ đến muộn, không dùng tổng cũ cho lựa chọn mới. | [ĐỀ XUẤT KỸ THUẬT] | TA-SPEC §4.1, PAY-03 | – |
| AC-US01-25 | Given chưa lưu; When đóng form (A13); Then không có bảng hay chuyển Cancelled được tạo bởi thao tác đóng form. | [ĐỀ XUẤT KỸ THUẬT] | TA-SPEC §3, §4.1, §4.5 | – |
| AC-US01-26 | Given xem trước hợp lệ nhưng nguồn thay đổi; When bấm lưu (14/A14); Then xử lý theo chính sách thời điểm được xác nhận, không suy ra kiểm tra form bảo đảm mọi điều kiện còn đúng khi ghi. | [AC dẫn xuất] / [GIẢ ĐỊNH – Cần xác nhận] | TA-SPEC §1, PAY-01..03 | Blocked by OQ-US01-01, OQ-US01-04, OQ-US01-05 |

## 4. Bàn giao và phạm vi lần sửa

- Sequence cùng version: [seq-us-01-v1.puml](../../../design/payment-management/v1/diagrams/seq-us-01-v1.puml), có lifeline giao diện và các giai đoạn mở form, chọn dữ liệu, xem trước, lưu, sửa Draft.
- Lần sửa theo P-17 thay cách trình bày quy trình người dùng; giữ ID AC/OQ và bổ sung AC-21..26. Vị trí OQ được cập nhật theo số bước mới ở cả hai bảng.
- Hướng dẫn của người dùng chỉ xác nhận trình tự tương tác. Nghiệp vụ chưa rõ vẫn Blocked; chưa có phê duyệt toàn bộ thiết kế, triển khai hay đo hiệu năng.
- Nhật ký P-17 ghi cả yêu cầu thiết kế lại và yêu cầu tiếp tục ở v1. Báo cáo ai-review-02-v1.md không bị sửa và chưa phải kết quả review bản vừa thay đổi.
