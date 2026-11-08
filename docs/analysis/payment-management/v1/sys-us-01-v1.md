# SYS-US-01 – Lập bảng thanh toán (v1)

> Phiên bản: v1 · Ngày: 08/11/2026 · Người phụ trách: Chờ nhóm điền
> Đầu vào: [TA-SPEC](../../../requirements/payment-management/spec.md) §1–6; [sổ nguồn](../../../requirements/payment-management/sources.md); [open-questions-v1.md](open-questions-v1.md); sys-us-03/04/05-v1.md để đối chiếu OQ
> AI: Codex / GPT-6 · Prompt: P-15, P-16 trong [prompt-log](../../../workflow/prompt-log.md)
> Trạng thái: Bản lần chạy đầu – BA Pending Review / Design Pending Approval

Đã đọc TA-SPEC §1–6. Chưa đọc trực tiếp TA-PDF trong lần chạy này; căn cứ nghiệp vụ dưới đây dẫn TA-SPEC, không tuyên bố đã đối chiếu PDF. Nội dung người dùng trích trong chat phù hợp phần US-PAY-01 và PAY liên quan trong TA-SPEC. Phân tích chỉ bao gồm lập bảng và quyền sửa Draft của US-PAY-01; không thực hiện toàn bộ năm US. Các đề xuất trong OQ của US-PAY-03 chưa được coi là quyết định nghiệp vụ đã xác nhận.

`SYS-US-01`, `AC-US01-kk`, `OQ-US01-kk` là mã nội bộ. `NFR-PAY-01/02` là mã nội bộ cho hai gạch đầu dòng §6. Nhãn: [ĐẶC TẢ] = nội dung nguồn; [AC dẫn xuất] = tiêu chí suy ra và nối nguồn; [ĐỀ XUẤT KỸ THUẬT] = cách đáp ứng; [GIẢ ĐỊNH – Cần xác nhận] = phần chưa được chốt.

## 1. Use case

### 1.1. Phạm vi và căn cứ

| Yêu cầu | Áp dụng cho SYS-US-01 | Căn cứ |
|---|---|---|
| US-PAY-01 | NVKD chọn hợp đồng/kỳ; tự sinh dòng, tính tổng, lưu Draft; cho phép sửa khi Draft. | [ĐẶC TẢ] TA-SPEC §4.1 |
| Ranh giới module | Chỉ đọc hợp đồng, bảng giá, sản lượng; không quản lý hay sửa dữ liệu nguồn. | [ĐẶC TẢ] TA-SPEC §1 |
| PAY-01 | Hợp đồng Active, bảng giá phù hợp; mỗi hợp đồng một bảng mỗi tháng. Kỳ tháng/quý: Blocked by OQ-01; lập lại sau hủy: Blocked by OQ-US05-02. | [ĐẶC TẢ] TA-SPEC §2, §5 PAY-01, §4.5 |
| PAY-02 | Sản lượng kỳ phải ở trạng thái “Đã đối soát”, tức đã được hai bên xác nhận. | [ĐẶC TẢ] TA-SPEC §2, §5 PAY-02 |
| PAY-03 | Thành tiền mỗi dòng = sản lượng × đơn giá tại thời điểm tính. Cách chọn giá: Blocked by OQ-US01-01; thuế/làm tròn: Blocked by OQ-US03-03. | [ĐẶC TẢ] TA-SPEC §5 PAY-03; §4.1 |
| PAY-04 | Áp dụng khi trình duyệt, thuộc US-PAY-02. Không chuyển việc chặn tổng âm/thiếu dòng bắt buộc hay chống trình duyệt trùng thành điều kiện lập Draft. | [ĐẶC TẢ] TA-SPEC §4.2, §5 PAY-04 |
| PAY-05 | Quy định cấm sửa Approved; mâu thuẫn với §4.4 đã có OQ-03, thuộc US-PAY-04. Sửa Draft ở đây không phải điều chỉnh Approved. | [ĐẶC TẢ] TA-SPEC §4.1, §4.4, §5 PAY-05 |
| PAY-06, PAY-07 | Phân công người duyệt và cấm tự duyệt thuộc US-PAY-03; không dùng làm điều kiện tạo Draft. | [ĐẶC TẢ] TA-SPEC §4.3, §5 PAY-06, PAY-07 |
| PAY-08 | Có liên quan khi sửa bảng từng bị từ chối. Không tự đưa Rejected về Draft: Blocked by OQ-04, OQ-US03-07. | [ĐẶC TẢ] TA-SPEC §3, §4.1, §5 PAY-08 |
| NFR-PAY-01 | Audit mọi thay đổi trạng thái và mọi điều chỉnh: ai, lúc nào, thay đổi gì. | [ĐẶC TẢ] TA-SPEC §6 gạch 1 |
| NFR-PAY-02 | Lập bảng phản hồi trong vòng 3 giây với hợp đồng có dưới 200 dòng; không suy rộng SLA cho sửa Draft. | [ĐẶC TẢ] TA-SPEC §6 gạch 2 |

### 1.2. Thông tin chung

| Mục | Đặc tả |
|---|---|
| Tên | SYS-US-01 – Lập bảng thanh toán. [ĐẶC TẢ] [TA-SPEC §4.1] |
| Tác nhân chính | NVKD lập bảng và sửa khi Draft. Phạm vi hợp đồng/bảng được thao tác: Blocked by OQ-US01-03. [ĐẶC TẢ] [TA-SPEC §2, §4.1] |
| Tác nhân liên quan | Các module hợp đồng, bảng giá, sản lượng cung cấp dữ liệu chỉ đọc. Không bổ sung vai trò vận hành các module đó vào use case này. [ĐẶC TẢ] [TA-SPEC §1] |
| Mục tiêu | Sinh bảng thanh toán từ sản lượng thực tế và bảng giá, tính tiền, lưu Draft để tiếp tục quy trình duyệt sau này. [ĐẶC TẢ] [TA-SPEC §1, §4.1] |
| Kích hoạt | NVKD chọn hợp đồng, kỳ và yêu cầu lập; hoặc gửi nội dung sửa bảng Draft. Tên nút và bố cục UI là [ĐỀ XUẤT KỸ THUẬT], không được đề quy định. [ĐẶC TẢ] [TA-SPEC §4.1] |
| P1 – Người thực hiện | NVKD; đề xuất lấy định danh/vai trò từ phiên đã xác thực phía server. Phạm vi quyền trên từng hợp đồng/bảng: Blocked by OQ-US01-03. [ĐẶC TẢ] / [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §2, §4.1] |
| P2 – Hợp đồng/kỳ | Chọn hợp đồng Active và kỳ theo cấu hình hợp đồng; thời điểm đánh giá Active: Blocked by OQ-US01-05; kỳ và duy nhất: Blocked by OQ-01, OQ-US05-02. [ĐẶC TẢ] [TA-SPEC §2, §5 PAY-01, §4.5] |
| P3 – Dữ liệu nguồn | Có bảng giá phù hợp và sản lượng kỳ Đã đối soát. Tiêu chí giá: Blocked by OQ-US01-01; dữ liệu rỗng/ánh xạ dòng: Blocked by OQ-US01-04. [ĐẶC TẢ] [TA-SPEC §4.1, §5 PAY-01..03] |
| P4 – Sửa bảng | Bảng tồn tại và đang Draft. Trường được sửa/tính lại: Blocked by OQ-US01-02. Nhánh bảng bị từ chối: Blocked by OQ-04, OQ-US03-07. [ĐẶC TẢ] [TA-SPEC §3, §4.1, §5 PAY-08] |
| Hậu điều kiện thành công | Lập: bảng có các dòng sản lượng/đơn giá/thành tiền, tổng tiền và trạng thái Draft. Sửa: lưu nội dung đã được phép, giữ Draft. [ĐẶC TẢ] [TA-SPEC §2, §4.1, §5 PAY-03]. Đề xuất ghi sự kiện create (chưa có bảng → Draft), người tạo, thời điểm, dữ liệu tại thời điểm tính; update ghi trước/sau cùng audit. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §6 gạch 1; §5 PAY-03] |
| Hậu điều kiện thất bại | Không tạo bảng/dòng dở dang; sửa thất bại không ghi một phần, không có audit thành công lệch dữ liệu. Lỗi của yêu cầu này không hoàn tác thay đổi hợp lệ của giao dịch khác. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1, §5 PAY-01, §6 gạch 1] |
| NFR-PAY-01 | Áp dụng audit đối với sửa Draft; đề xuất ghi cả khởi tạo Draft và lưu audit trong cùng giao dịch với bảng/dòng. [ĐẶC TẢ] / [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §6 gạch 1] |
| NFR-PAY-02 | Áp dụng lập: ≤3 giây với <200 dòng; hợp đồng 200 dòng không thuộc điều kiện này. Cách đo: Blocked by OQ-US01-06. Chưa có kết quả đo. [ĐẶC TẢ] [TA-SPEC §6 gạch 2] |

### 1.3. Dòng cơ bản – lập bảng (`create`)

Luồng mô tả phần có căn cứ. Các chính sách phụ thuộc OQ dưới đây chưa phải thiết kế cuối cùng; không biến OQ thành lỗi nghiệp vụ khi chạy hệ thống.

| Bước | NVKD / Hệ thống | Nội dung và căn cứ |
|---|---|---|
| 1 | NVKD | Gửi hợp đồng và kỳ thanh toán đã chọn. [ĐẶC TẢ] [TA-SPEC §4.1] |
| 2 | Hệ thống | Kiểm tra định danh, vai trò NVKD phía server; kiểm tra đủ dữ liệu hợp đồng/kỳ. Kiểm tra phạm vi quyền: Blocked by OQ-US01-03. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §2, §4.1] |
| 3 | Hệ thống | Đọc hợp đồng, kiểm tra tồn tại và Active. Mốc đánh giá hiệu lực: Blocked by OQ-US01-05. Không đổi trạng thái hợp đồng. [ĐẶC TẢ] / [AC dẫn xuất] [TA-SPEC §1, §5 PAY-01] |
| 4 | Hệ thống | Kiểm tra kỳ theo cấu hình và tra bảng đã có để thực hiện PAY-01. Quy tắc kỳ tháng/quý và bảng Cancelled có chiếm kỳ hay không: Blocked by OQ-01, OQ-US05-02. Không chốt khóa duy nhất trong đặc tả này. [ĐẶC TẢ] / [AC dẫn xuất] [TA-SPEC §2, §5 PAY-01, §4.5] |
| 5 | Hệ thống | Đọc bảng giá phù hợp và sản lượng kỳ; kiểm tra Đã đối soát trước khi lập. Mốc chọn giá, ánh xạ dịch vụ và dữ liệu rỗng: Blocked by OQ-US01-01, OQ-US01-04. [ĐẶC TẢ] [TA-SPEC §1, §4.1, §5 PAY-01..03] |
| 6 | Hệ thống | Với mỗi dòng dịch vụ được xác định từ dữ liệu nguồn, lấy sản lượng và đơn giá tại thời điểm tính, tính thành tiền = sản lượng × đơn giá, tổng hợp tổng tiền. Tổng từ các thành tiền là AC dẫn xuất; không tự thêm VAT/quy tắc làm tròn. Blocked by OQ-US01-01, OQ-US01-04, OQ-US03-03 đối với phần chưa rõ. [ĐẶC TẢ] / [AC dẫn xuất] [TA-SPEC §2, §4.1, §5 PAY-03] |
| 7 | Hệ thống | Đề xuất mở giao dịch, bảo đảm không có bảng khác chiếm cùng phạm vi kỳ theo PAY-01 đã được xác nhận, lưu bảng và dòng ở Draft cùng dữ liệu tại thời điểm tính. Kiểm tra trùng có hiệu lực cả khi hai yêu cầu đến đồng thời; Blocked by OQ-01, OQ-US05-02 về phạm vi duy nhất. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1, §5 PAY-01, PAY-03] |
| 8 | Hệ thống | Đề xuất ghi audit action=create, ai, lúc nào, trước=chưa có bảng, sau=Draft cùng dữ liệu đã tạo trong cùng giao dịch; commit chỉ khi cả bảng/dòng và audit thành công. “Chưa có bảng” không phải trạng thái bổ sung. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §3, §6 gạch 1] |
| 9 | Hệ thống | Trả bảng đã lưu gồm định danh, hợp đồng/kỳ, các dòng, tổng và Draft. Hình thức response là đề xuất kỹ thuật. [ĐẶC TẢ] / [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1] |

### 1.4. Dòng thay thế – lập bảng

Mọi nhánh lỗi kết thúc yêu cầu hiện tại, không tiếp tục tính/lưu sau khi đã từ chối.

| Nhánh | Rẽ từ | Xử lý và căn cứ |
|---|---|---|
| A2 | 2 | Chưa xác thực hoặc không phải NVKD: từ chối. Phạm vi hợp đồng được phép: Blocked by OQ-US01-03. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §2, §4.1] |
| A2.1 | 2 | Thiếu hợp đồng/kỳ hoặc sai định dạng: yêu cầu bổ sung/sửa, không ghi bảng. Không tự thêm giới hạn kỳ quá khứ/tương lai. [AC dẫn xuất] / [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §2, §4.1] |
| A3 | 3 | Không tìm thấy hợp đồng hoặc không Active: không lập, trả lý do. Tiêu chí thời điểm: Blocked by OQ-US01-05. [AC dẫn xuất] [TA-SPEC §5 PAY-01] |
| A4 | 4 | Kỳ không khớp cấu hình hoặc đã có bảng chiếm kỳ theo quy tắc được xác nhận: không lập thêm. Kỳ quý và Cancelled: Blocked by OQ-01, OQ-US05-02. [AC dẫn xuất] [TA-SPEC §2, §5 PAY-01, §4.5] |
| A4.1 | 4 | Lỗi tra bảng đã có: trả lỗi, không coi việc chưa đọc được là kỳ còn trống. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §5 PAY-01] |
| A5 | 5 | Không có bảng giá phù hợp hoặc sản lượng chưa Đã đối soát: không lập. Giá thiếu/mâu thuẫn theo dịch vụ và tập sản lượng rỗng: Blocked by OQ-US01-01, OQ-US01-04; không tự coi rỗng là đã đối soát hay thay bằng 0. [AC dẫn xuất] [TA-SPEC §4.1, §5 PAY-01..03] |
| A5.1 | 3 hoặc 5 | Interface đọc hợp đồng/bảng giá/sản lượng gặp lỗi: trả lỗi, không lưu bảng từ dữ liệu thiếu hoặc giá mặc định. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §1, §4.1, §5 PAY-01..03] |
| A6 | 6 | Dữ liệu không đủ để tính theo PAY-03 hoặc không đạt chính sách tính đã được xác nhận: không ghi kết quả tính thiếu. Không thêm chặn tổng âm ở bước lập; PAY-04 kiểm tra khi trình duyệt. Blocked by OQ-US01-01, OQ-US01-04, OQ-US03-03 cho tiêu chí còn thiếu. [AC dẫn xuất] [TA-SPEC §4.1, §5 PAY-03, PAY-04] |
| A7 | 7 | Hai yêu cầu cùng lập cho một phạm vi duy nhất: giao dịch thua xung đột không tạo bảng thứ hai. Không đồng nhất yêu cầu này với chống trình duyệt trùng PAY-04. Blocked by OQ-01, OQ-US05-02 về phạm vi duy nhất. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §5 PAY-01] |
| A7.1 | 7–8 | Không mở được giao dịch: trả lỗi trước khi ghi. Lỗi lưu bảng/dòng, ghi audit hoặc commit: rollback toàn bộ giao dịch, trả lỗi; không trả thành công khi audit thất bại. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1, §6 gạch 1] |

### 1.5. Dòng sửa Draft (`update`)

Đây là phần quyền sửa thuộc US-PAY-01; không tự thiết kế thêm chuyển Rejected → Draft. Các trường nhập và trường tính lại chưa được chốt.

| Bước | Nội dung và căn cứ |
|---|---|
| U1 | NVKD gửi định danh bảng và nội dung muốn sửa; đề xuất kèm version đã đọc để phát hiện ghi đè. Blocked by OQ-US01-02 về trường được sửa. [ĐẶC TẢ] / [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1] |
| U2 | Hệ thống kiểm tra định danh/vai trò, tra bảng và kiểm tra quyền trên bảng; Blocked by OQ-US01-03. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §2, §4.1] |
| U3 | Kiểm tra trạng thái hiện tại là Draft. Với Rejected: Blocked by OQ-04, OQ-US03-07; không tự thực hiện chuyển trạng thái. [ĐẶC TẢ] / [AC dẫn xuất] [TA-SPEC §3, §4.1, §5 PAY-08] |
| U4 | Kiểm tra nội dung thuộc phạm vi cho sửa và tính lại tiền nếu thay đổi ảnh hưởng tính tiền theo chính sách được xác nhận. Nếu cho đổi hợp đồng/kỳ hoặc đọc lại nguồn, phải xác định cách tái kiểm tra PAY-01..03 trước khi thiết kế chi tiết. Blocked by OQ-US01-02, OQ-US03-03; giá/dòng/hiệu lực theo OQ-US01-01, OQ-US01-04, OQ-US01-05 khi có liên quan. [GIẢ ĐỊNH – Cần xác nhận] [TA-SPEC §4.1, §5 PAY-01..03] |
| U5 | Đề xuất giao dịch cập nhật có điều kiện trạng thái vẫn Draft và version không đổi; lưu audit action=update, người, thời điểm, trước/sau ngay cả khi trạng thái vẫn Draft; commit cùng dữ liệu. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1, §6 gạch 1] |
| U6 | Trả bảng sau sửa, trạng thái Draft. [ĐẶC TẢ] / [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1] |

| Nhánh | Rẽ từ | Xử lý và căn cứ |
|---|---|---|
| AU2 | U2 | Chưa xác thực, không phải NVKD hoặc không đủ quyền trên bảng: từ chối; Blocked by OQ-US01-03 cho phạm vi quyền. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §2, §4.1] |
| AU2.1 | U2 | Bảng không tồn tại: trả không tìm thấy, không tạo mới bằng thao tác update. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1] |
| AU2.2 | U2 | Lỗi đọc bảng: trả lỗi, không tiếp tục cập nhật khi chưa lấy được dữ liệu/trạng thái hiện tại. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1] |
| AU3 | U3 | Bảng hiện tại không Draft: không chạy luồng sửa Draft. Rejected chờ OQ-04/OQ-US03-07; điều chỉnh Approved thuộc US-PAY-04/OQ-03, ngoài phạm vi. [AC dẫn xuất] [TA-SPEC §3, §4.1, §4.4, §5 PAY-05, PAY-08] |
| AU4 | U4 | Nội dung không hợp lệ theo phạm vi/chính sách đã xác nhận: từ chối, giữ bản đã lưu; không tự cấm/cho sửa một trường cụ thể. Blocked by OQ-US01-02, OQ-US03-03. [GIẢ ĐỊNH – Cần xác nhận] [TA-SPEC §4.1, §5 PAY-03] |
| AU5 | U5 | Version/trạng thái thay đổi sau khi đọc (ví dụ đã trình duyệt hoặc hủy): rollback, trả xung đột; không ghi đè thay đổi của giao dịch khác. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §3, §4.1, §4.2, §4.5] |
| AU5.1 | U5 | Không mở được giao dịch: trả lỗi trước khi ghi. Lỗi lưu, audit hoặc commit: rollback cả dữ liệu và audit của yêu cầu sửa; trả lỗi. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §6 gạch 1] |

## 2. Điểm cần xác nhận

Bảng dùng đúng các cột của [OQ chung](open-questions-v1.md). Cột cuối nêu lý do và ảnh hưởng. Các ID có sẵn được tái sử dụng; đề xuất cũ vẫn chờ xác nhận, không được truyền sang sequence như quy tắc đã duyệt.

Trong cột **Vị trí mọi nguồn**, **Vị trí trong quy trình** chỉ rõ mục, tiền điều kiện/bước/nhánh và AC của chính đặc tả này; phần TA-SPEC phía trước là căn cứ phát sinh vấn đề. Mã bước giúp tra cứu ổn định khi số dòng thay đổi.

| ID | Vị trí mọi nguồn | Loại | Mô tả | Đề xuất / Lựa chọn | Trạng thái | Người/ngày/tham chiếu | Còn mở / ảnh hưởng |
|---|---|---|---|---|---|---|---|
| OQ-01 | TA-SPEC §2 “tháng hoặc quý tùy cấu hình” ↔ §5 PAY-01 “mỗi tháng”<br>**Vị trí trong quy trình:** [sys-us-01-v1.md](sys-us-01-v1.md), §1.2 P2; §1.3 bước 4, 7; §1.4 A4, A7; §3 AC-US01-06, AC-US01-14. | Mâu thuẫn | Với hợp đồng cấu hình quý, lập một bảng quý hay các bảng tháng? Có cho chồng lấn tháng/quý không? | A: duy nhất theo kỳ cấu hình; B: duy nhất theo tháng và cần làm rõ cách biểu diễn quý; chờ người phụ trách. | Cần xác nhận | – | Chặn bước 4, 7, A4, A7; chưa thể chốt định danh kỳ, phạm vi kiểm tra trùng và constraint. |
| OQ-US05-02 | TA-SPEC §4.5 “Cancelled và không dùng lại được” ↔ §5 PAY-01 “một bảng… mỗi tháng”<br>**Vị trí trong quy trình:** [sys-us-01-v1.md](sys-us-01-v1.md), §1.2 P2; §1.3 bước 4, 7; §1.4 A4, A7; §3 AC-US01-07, AC-US01-14. | Mơ hồ | Đã có trong OQ chung: có được tạo bảng mới cùng kỳ sau khi hủy không? | A: được lập mới, bảng cũ vẫn Cancelled; B: không được lập lại. | Cần xác nhận | – | Chặn xử lý bảng đã hủy ở bước 4/7; không lấy câu trả lời v2 của US-PAY-05 áp sang v1. |
| OQ-US03-03 | TA-SPEC §4.1 “tính tổng tiền”; §5 PAY-03; §4.3/PAY-06; OQ chung, đề xuất Đan Anh P-04..P-07<br>**Vị trí trong quy trình:** [sys-us-01-v1.md](sys-us-01-v1.md), §1.3 bước 6; §1.4 A6; §1.5 U4, AU4; §3 AC-US01-11, AC-US01-12, AC-US01-17. | Thiếu | Tổng tiền, VAT, mốc tính và làm tròn đã có OQ liên US. | Giữ đề xuất Đan Anh trong OQ chung; cần xác nhận có thuế hay không, giá trị/cách tính và làm tròn, không tự thêm công thức. | Đề xuất của Đan Anh – chờ khách hàng xác nhận | Đan Anh / 07/11/2026 / P-04..P-07 | Chặn hoàn thiện kết quả tiền và U4; công thức nhân PAY-03 vẫn có căn cứ độc lập. |
| OQ-04 | TA-SPEC §3 “Rejected” ↔ §5 PAY-08 “quay về… Draft”; OQ chung P-04<br>**Vị trí trong quy trình:** [sys-us-01-v1.md](sys-us-01-v1.md), §1.2 P4; §1.5 U3, AU3; §3 AC-US01-18. | Mâu thuẫn | Bảng bị từ chối ở Rejected hay trở lại Draft, có bước trung gian không? | Đề xuất cũ: Rejected rồi Draft; chưa coi là luồng đã duyệt. | Đề xuất của Đan Anh – chờ khách hàng xác nhận | Đan Anh / 07/11/2026 / P-04 | Chặn phần U3 mở sửa bảng bị từ chối; không chặn sửa bảng đã ở Draft hợp lệ. |
| OQ-US03-07 | TA-SPEC §3; §5 PAY-08; OQ-04; OQ chung P-05, P-06<br>**Vị trí trong quy trình:** [sys-us-01-v1.md](sys-us-01-v1.md), §1.2 P4; §1.5 U3, AU3; §3 AC-US01-18. | Thiếu | Nếu có Rejected → Draft, ai kích hoạt và khi nào? | Đề xuất cũ: NVKD thực hiện chỉnh sửa thì chuyển; chờ xác nhận. | Đề xuất của Đan Anh – chờ khách hàng xác nhận | Đan Anh / 07/11/2026 / P-05, P-06 | Chặn thao tác mở sửa Rejected ở U3/AU3; chưa thiết kế chuyển này. |
| OQ-US01-01 | TA-SPEC §4.1 “từ sản lượng và bảng giá”; §5 PAY-01 “bảng giá phù hợp”, PAY-03 “đơn giá tại thời điểm tính”<br>**Vị trí trong quy trình:** [sys-us-01-v1.md](sys-us-01-v1.md), §1.2 P3; §1.3 bước 5, 6; §1.4 A5, A6; §1.5 U4; §3 AC-US01-08, AC-US01-09, AC-US01-11. | Mơ hồ | “Phù hợp” được xác định theo dịch vụ/hợp đồng và mốc thời gian nào? Nếu giá đổi trong kỳ, nhiều giá cùng phù hợp hoặc thiếu giá cho dịch vụ thì xử lý ra sao? | Giá tại lúc lập / theo hiệu lực trong kỳ, có thể tách theo giai đoạn; người phụ trách cần chỉ rõ tiêu chí và xử lý thiếu/trùng giá. | Cần xác nhận | – | Cần chọn được giá duy nhất đúng căn cứ trước khi tính. Chặn phần chọn giá ở bước 5–6/A5/A6 và U4 nếu đọc lại giá; không tự chọn giá mới nhất hay thay giá thiếu bằng 0. |
| OQ-US01-02 | TA-SPEC §4.1 “được phép chỉnh sửa… Draft”; §5 PAY-01..03<br>**Vị trí trong quy trình:** [sys-us-01-v1.md](sys-us-01-v1.md), §1.2 P4; §1.5 U1, U4, AU4; §3 AC-US01-17. | Thiếu | Draft được sửa trường nào: hợp đồng/kỳ, thêm/xóa dòng, sản lượng/đơn giá hay chỉ thông tin khác? Khi lưu có lấy lại nguồn/tính lại không? | Giữ dữ liệu nguồn chỉ đọc / cho phép ghi đè một số trường của bảng với giới hạn cần xác nhận. | Cần xác nhận | – | Chặn U1/U4/AU4 và thiết kế request update; ảnh hưởng tái kiểm tra hiệu lực, duy nhất kỳ, đối soát và PAY-03. Không tự coi NVKD được sửa sản lượng nguồn. |
| OQ-US01-03 | TA-SPEC §2 “NVKD… lập”; §4.1 “NVKD… chỉnh sửa”; §5 PAY-07 chỉ nói cấm tự duyệt<br>**Vị trí trong quy trình:** [sys-us-01-v1.md](sys-us-01-v1.md), §1.2 P1; §1.3 bước 2; §1.4 A2; §1.5 U2, AU2; §3 AC-US01-03, AC-US01-17. | Thiếu | NVKD được lập trên mọi hợp đồng hay chỉ hợp đồng được giao? Được sửa Draft do NVKD khác tạo không? | A: theo hợp đồng được giao/người tạo; B: mọi NVKD; cần xác nhận từng thao tác. | Cần xác nhận | – | Chặn phạm vi quyền ở bước 2/U2, không chặn nhận diện vai trò NVKD. PAY-07 không đủ căn cứ để suy ra quyền sở hữu Draft. |
| OQ-US01-04 | TA-SPEC §2 “một dịch vụ trong bảng”; §4.1 “tự sinh… từ sản lượng”; §5 PAY-02, PAY-03<br>**Vị trí trong quy trình:** [sys-us-01-v1.md](sys-us-01-v1.md), §1.2 P3; §1.3 bước 5, 6; §1.4 A5, A6; §1.5 U4; §3 AC-US01-10. | Thiếu | Không có bản ghi sản lượng có khác sản lượng 0 đã đối soát không? Nhiều bản ghi cùng dịch vụ gộp/tách thế nào, dịch vụ nào được đưa vào bảng? | Không lập khi không có dữ liệu / cho lập bảng rỗng; gộp theo dịch vụ / tách theo dữ liệu nguồn hoặc giai đoạn giá; chờ xác nhận. | Cần xác nhận | – | Chặn ánh xạ dòng bước 5–6/A5/A6; tránh tự coi thiếu dữ liệu là 0 hoặc tự tạo danh sách dịch vụ bắt buộc của PAY-04. |
| OQ-US01-05 | TA-SPEC §5 PAY-01 “đang hiệu lực (Active)”; §2 kỳ thanh toán<br>**Vị trí trong quy trình:** [sys-us-01-v1.md](sys-us-01-v1.md), §1.2 P2; §1.3 bước 3; §1.4 A3; §1.5 U4; §3 AC-US01-05. | Mơ hồ | Đánh giá Active ở thời điểm gửi yêu cầu hay cần hiệu lực trong toàn bộ/một phần kỳ? Hợp đồng hết hiệu lực sau kỳ có được lập cho kỳ đã qua không? | Active tại lúc lập / theo hiệu lực của kỳ; cần chỉ rõ mốc đánh giá và kiểm tra lại khi nguồn thay đổi. | Cần xác nhận | – | Chặn hoàn thiện guard bước 3/A3 và U4 nếu đổi hợp đồng/kỳ; không tự thêm cấm lập kỳ quá khứ/tương lai. |
| OQ-US01-06 | TA-SPEC §6 gạch 2 “phản hồi trong vòng 3 giây… dưới 200 dòng”<br>**Vị trí trong quy trình:** [sys-us-01-v1.md](sys-us-01-v1.md), §1.2 hàng NFR-PAY-02; §3 AC-US01-20. | Thiếu | Đo từ thao tác UI tới hiển thị hay từ server nhận yêu cầu tới phản hồi? Số dòng tính theo dữ liệu nguồn hay dòng bảng sau sinh, môi trường đo nào? | Xác nhận điểm bắt đầu/kết thúc, cách đếm dòng và môi trường; giữ nguyên ≤3 giây, <200 dòng. | Cần xác nhận | – | Chặn kết luận đạt NFR-PAY-02, không chặn thiết kế luồng. Không tự thêm percentile hoặc mức tải đồng thời thành tiêu chuẩn gốc. |

## 3. Acceptance criteria

Các mã AC dưới đây do phân tích đặt, không có trong đề. Các AC kỹ thuật kiểm chứng phương án được đề xuất, không bổ sung business rule. AC phụ thuộc OQ chưa thể đánh dấu đã đáp ứng.

| ID | Given / When / Then | Nhãn | Nguồn | OQ |
|---|---|---|---|---|
| AC-US01-01 | Given hợp đồng/kỳ và nguồn hợp lệ; When NVKD lập (1–9); Then sinh dòng, tính tiền và lưu Draft, trả bảng đã lưu. | [AC dẫn xuất] | TA-SPEC §4.1, PAY-01..03 | Phần kỳ/giá/tổng phụ thuộc các AC dưới đây. |
| AC-US01-02 | Given chưa xác thực hoặc không có vai trò NVKD; When create/update (2/U2); Then từ chối trước khi ghi (A2/AU2). | [ĐỀ XUẤT KỸ THUẬT] | TA-SPEC §2, §4.1 | – |
| AC-US01-03 | Given NVKD và hợp đồng/bảng cụ thể; When kiểm tra quyền (2/U2); Then cho phép/từ chối đúng phạm vi được xác nhận. | [AC dẫn xuất] | TA-SPEC §2, §4.1 | Blocked by OQ-US01-03 |
| AC-US01-04 | Given thiếu/sai định dạng hợp đồng hoặc kỳ; When lập (2); Then không ghi bảng, trả lỗi (A2.1). | [AC dẫn xuất] | TA-SPEC §4.1 | – |
| AC-US01-05 | Given hợp đồng không tồn tại hoặc không Active theo tiêu chí đã xác nhận; When lập (3); Then không lập (A3). | [AC dẫn xuất] | TA-SPEC §5 PAY-01 | Blocked by OQ-US01-05 đối với mốc hiệu lực |
| AC-US01-06 | Given kỳ không phù hợp cấu hình hoặc đã bị chiếm; When kiểm tra (4); Then không tạo thêm (A4), bao gồm tình huống kỳ quý. | [AC dẫn xuất] | TA-SPEC §2, §5 PAY-01 | Blocked by OQ-01 |
| AC-US01-07 | Given bảng cùng kỳ đã Cancelled; When lập bảng mới (4/7); Then xử lý đúng quyết định về lập lại, giữ bảng cũ Cancelled. | [AC dẫn xuất] | TA-SPEC §4.5, §5 PAY-01 | Blocked by OQ-US05-02 |
| AC-US01-08 | Given không có bảng giá phù hợp hoặc sản lượng chưa Đã đối soát; When lập (5); Then không tạo bảng (A5). | [AC dẫn xuất] | TA-SPEC §5 PAY-01, PAY-02 | Blocked by OQ-US01-01 cho tiêu chí phù hợp |
| AC-US01-09 | Given giá đổi trong kỳ/nhiều giá/thiếu giá; When chọn giá cho từng dịch vụ (5–6); Then dùng chính sách đã xác nhận, không thay giá thiếu bằng 0 (A5/A6). | [AC dẫn xuất] | TA-SPEC §4.1, §5 PAY-01, PAY-03 | Blocked by OQ-US01-01 |
| AC-US01-10 | Given tập sản lượng rỗng, giá trị 0 hoặc nhiều bản ghi một dịch vụ; When sinh dòng (5–6); Then ánh xạ/từ chối theo chính sách đã xác nhận (A5/A6). | [AC dẫn xuất] | TA-SPEC §2, §4.1, §5 PAY-02, PAY-03 | Blocked by OQ-US01-04 |
| AC-US01-11 | Given dòng có sản lượng q và đơn giá p xác định; When tính (6); Then thành tiền trước xử lý còn mở bằng q × p; không lấy giá do client tự gửi khi lập mới. | [AC dẫn xuất] / [ĐỀ XUẤT KỸ THUẬT] | TA-SPEC §4.1, §5 PAY-03 | Chọn p: OQ-US01-01; xử lý tiền: OQ-US03-03 |
| AC-US01-12 | Given các thành tiền đã tính; When tổng hợp (6/U4); Then tổng nhất quán với dòng và chính sách tiền được xác nhận; không tự cộng VAT/làm tròn lên (A6/AU4). | [AC dẫn xuất] | TA-SPEC §4.1, §5 PAY-03 | Blocked by OQ-US03-03 |
| AC-US01-13 | Given interface nguồn bị lỗi; When đọc (3/5); Then trả lỗi, không ghi bảng từ dữ liệu thiếu (A5.1). | [ĐỀ XUẤT KỸ THUẬT] | TA-SPEC §1, §4.1, §5 PAY-01..03 | – |
| AC-US01-14 | Given hai yêu cầu cùng chiếm một phạm vi duy nhất; When lưu đồng thời (7); Then nhiều nhất một bảng được tạo, yêu cầu thua trả xung đột (A7). | [AC dẫn xuất] / [ĐỀ XUẤT KỸ THUẬT] | TA-SPEC §5 PAY-01 | Blocked by OQ-01, OQ-US05-02 về phạm vi duy nhất |
| AC-US01-15 | Given lập hợp lệ; When commit (7–9); Then bảng/dòng và audit create cùng tồn tại, audit có ai/lúc nào/thay đổi gì. | [ĐỀ XUẤT KỸ THUẬT] | TA-SPEC §4.1, §6 gạch 1 | – |
| AC-US01-16 | Given lỗi đọc dữ liệu thanh toán hoặc mở giao dịch/ghi bảng, dòng, audit/commit; When create/update (4/7–8/U2/U5); Then trả lỗi, không tiếp tục sau lỗi đọc/mở giao dịch và không có dữ liệu/audit ghi một phần (A4.1/A7.1/AU2.2/AU5.1). | [ĐỀ XUẤT KỸ THUẬT] | TA-SPEC §4.1, §5 PAY-01, §6 gạch 1 | – |
| AC-US01-17 | Given Draft và NVKD đủ quyền; When sửa trường được phép (U1–U6); Then lưu nội dung hợp lệ, giữ Draft và ghi audit update trước/sau. Nội dung sai bị từ chối (AU4). | [AC dẫn xuất] / [ĐỀ XUẤT KỸ THUẬT] | TA-SPEC §4.1, §5 PAY-03, §6 gạch 1 | Blocked by OQ-US01-02, OQ-US01-03, OQ-US03-03; nguồn đọc lại theo U4 |
| AC-US01-18 | Given bảng không tồn tại hoặc không Draft; When update (U2/U3); Then không chạy sửa Draft, trả lý do (AU2.1/AU3). | [AC dẫn xuất] | TA-SPEC §3, §4.1 | Rejected: Blocked by OQ-04, OQ-US03-07; không quyết định ngoại lệ Approved. |
| AC-US01-19 | Given bảng đã đổi version/trạng thái sau khi đọc; When update (U5); Then không ghi đè thay đổi mới, rollback và trả xung đột (AU5). | [ĐỀ XUẤT KỸ THUẬT] | TA-SPEC §3, §4.1, §4.2, §4.5 | – |
| AC-US01-20 | Given hợp đồng có dưới 200 dòng; When lập; Then phản hồi trong vòng 3 giây theo cách đo được xác nhận. Dữ liệu 199 dòng là ca biên thuộc điều kiện; 200 dòng không có SLA này trong đề. | [AC dẫn xuất] | TA-SPEC §6 gạch 2 | Blocked by OQ-US01-06; chưa đo |

## 4. Bàn giao thiết kế và kiểm chứng

- Đầu vào sequence: chính file này và OQ v1. Đường dẫn đầu ra: [seq-us-01-v1.puml](../../../design/payment-management/v1/diagrams/seq-us-01-v1.puml). Danh mục bước, tên tạm và đề xuất kỹ thuật nằm trong chú thích đầu `.puml`, theo cách tổ chức các sequence hiện có của workspace.
- Phần độc lập có thể thiết kế: actor NVKD, đọc nguồn, kiểm tra Active/có giá/đối soát ở mức nguyên tắc, PAY-03, lưu Draft, audit và nhánh thất bại. Những phần phụ thuộc OQ ở mục 2 chưa đủ điều kiện chốt request, constraint kỳ hay công thức tiền cuối cùng.
- Không viết API/schema hay mã ứng dụng trong đặc tả BA này. Đây là phân tích và thiết kế đề xuất, chưa phải kết quả triển khai, đo hiệu năng hay phê duyệt nghiệp vụ.
- Lệnh/kết quả kiểm chứng thực tế được ghi tại P-15 của prompt-log; không dùng kiểm tra định dạng làm bằng chứng nội dung đã được duyệt.
