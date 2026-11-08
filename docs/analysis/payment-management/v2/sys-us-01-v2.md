# SYS-US-01 – Lập bảng thanh toán (v2)

> Phiên bản: v2 · Ngày: 08/11/2026 · Người phụ trách: Chờ nhóm điền họ tên
> Đầu vào: TA-SPEC §1–6; review và xác nhận của người dùng tại P-18; open-questions-v2.md
> AI: Codex / GPT-6 · Nhật ký: [P-18, P-19](../../../workflow/prompt-log.md)
> Trạng thái: Bản sau review – Design Pending Approval

## 1. Use case

### 1.1. Phạm vi, nguồn và xác nhận

US-PAY-01 bao gồm lập bảng và sửa Draft. Hợp đồng, bảng giá và sản lượng chỉ được đọc qua interface; không thiết kế CRUD các module đó. Căn cứ: TA-SPEC §1, §4.1.

Đã đọc TA-SPEC §1–6, chưa đọc trực tiếp TA-PDF trong lần này. SYS-US-01, AC-US01-kk, OQ và NFR là mã nội bộ. Các AC là tiêu chí dẫn xuất hoặc kiểm chứng phương án kỹ thuật; không phải mã AC của đề. Nội dung quy trình dùng câu trực tiếp theo yêu cầu người dùng; nguồn và phân loại đặt trong cột riêng, không chèn nhãn ngoặc vuông vào từng hành động.

| Nội dung | Phân loại | Nguồn |
|---|---|---|
| NVKD lập bảng, tự sinh dòng/tổng và lưu Draft; sửa khi Draft | Đặc tả | TA-SPEC §2, §4.1 |
| Active; bảng giá phù hợp; duy nhất theo tháng | Đặc tả gốc, giữ nguyên câu trong nguồn | TA-SPEC §5 PAY-01 |
| Tháng/quý theo cấu hình hợp đồng | Đặc tả | TA-SPEC §2 |
| Không cho bảng tháng và bảng quý chồng lấn cùng khoảng thanh toán; bảng cùng tháng/quý cũng không trùng | Xác nhận sau review | P-18.3, người dùng trong chat, 08/11/2026; OQ-01 |
| Bấm Lập bảng từ chi tiết hợp đồng; tự lấy hợp đồng, không chọn lại | Xác nhận sau review | P-18.1, người dùng trong chat, 08/11/2026 |
| Một bảng giá có hiệu lực tại một thời điểm, gắn với hợp đồng; tự lấy bảng giá Active, không cho chọn thủ công | Xác nhận sau review | P-18.1 và P-18.3; OQ-US01-01 |
| Giá mới đã Active trước khi lưu thì dùng giá mới; chưa Active thì tiếp tục dùng bảng giá Active hiện tại | Xác nhận sau review | P-18.3; OQ-US01-01 |
| Ghi chú tùy chọn; thông báo kết quả; tô đỏ trường thiếu bắt buộc/vi phạm và nêu lỗi | Xác nhận sau review | P-18.1, P-18.2 |
| NVKD chỉ lập trên hợp đồng được giao, chỉ sửa Draft do mình tạo | Đề xuất của người dùng theo hướng một người thực hiện; chưa coi là chính sách đã được khách hàng phê duyệt | P-19, 08/11/2026; OQ-US01-03 |
| Sản lượng, đơn giá, thông tin hợp đồng và khách hàng không cho sửa thủ công; sản lượng/đơn giá ánh xạ từ bảng sản lượng/bảng giá | Xác nhận phạm vi trường nguồn | P-19; OQ-US01-02, OQ-US01-04; TA-SPEC §1, PAY-03 |
| Chỉ lập khi trường bắt buộc đã đầy đủ; thuế tiếp tục để mở xác nhận khách hàng | Xác nhận điều kiện nhập; thuế chưa được chốt | P-19; OQ-US03-03 |
| Bảng giá phải được lập khi hợp đồng còn hiệu lực | Xác nhận điều kiện tạo dữ liệu nguồn; không giao module thanh toán CRUD bảng giá | P-19; OQ-US01-01; TA-SPEC §1 |
| Sản lượng Đã đối soát; thành tiền = sản lượng × đơn giá tại thời điểm tính | Đặc tả | TA-SPEC §2, §5 PAY-02, PAY-03 |
| Audit mọi thay đổi trạng thái/điều chỉnh; lập ≤3 giây với <200 dòng | Đặc tả; NFR-PAY-01/02 là mã nội bộ | TA-SPEC §6 |
| Cho phép lập bảng mới sau hủy, giữ bảng cũ Cancelled và không tính bảng đó vào duy nhất | Quyết định v2 đã có của US-PAY-05, không phải xác nhận mới trong lượt chat này | [OQ-US05-02](open-questions-v2.md), [user-review-us-05.md](../../../review/payment-management/user-review-us-05.md) §2.1, người phụ trách 07/11/2026 |
| PAY-04 kiểm tra khi trình duyệt, PAY-06/07 khi duyệt; PAY-05/08 ảnh hưởng nhánh sửa nhưng chưa giải quyết điều chỉnh Approved/Rejected | Ranh giới, không thực hiện US-PAY-02..05 trong tài liệu này | TA-SPEC §3, §4.2–4.5, §5 PAY-04..08 |

### 1.2. Thông tin chung và biểu mẫu

| Mục | Nội dung | Căn cứ |
|---|---|---|
| Tác nhân / mục tiêu | NVKD lập bảng thanh toán Draft cho hợp đồng đang xem | TA-SPEC §2, §4.1; P-18.1 |
| Kích hoạt | Bấm Lập bảng thanh toán tại màn hình chi tiết hợp đồng | P-18.1 |
| P1 | Có ngữ cảnh hợp đồng; server kiểm tra phiên/vai trò và quyền trên từng yêu cầu, kể cả xem trước. Đề xuất một người thực hiện: chỉ lập trên hợp đồng được giao; không suy ra một hợp đồng chỉ được giao cho duy nhất một NVKD | P-19; TA-SPEC §2; OQ-US01-03 |
| P2 | Để tính/lưu: hợp đồng có trạng thái Active (Có hiệu lực), kỳ hợp lệ và không chồng lấn kỳ đã có | TA-SPEC §5 PAY-01; P-18.3 |
| P3 | Đọc được sản lượng Đã đối soát và một bảng giá Active gắn với hợp đồng; nguồn phải chứng minh bảng giá được lập khi hợp đồng còn hiệu lực | TA-SPEC §5 PAY-01..03; P-18.1/3; P-19 |
| P4 | Khi sửa: bảng tồn tại, đang Draft; theo đề xuất một người thực hiện, người sửa phải là người tạo Draft. Các trường nguồn bị khóa; ma trận trường khác còn OQ-US01-02, Rejected còn OQ-04/OQ-US03-07 | P-19; TA-SPEC §3, §4.1, §5 PAY-08 |
| Thành công | Lưu bảng/dòng/tổng/ghi chú ở Draft cùng audit; hiển thị thông báo thành công và bảng vừa lưu | TA-SPEC §4.1, §6; P-18.1/2 |
| Thất bại | Thông báo nguyên nhân, giữ dữ liệu nhập khi còn ở form, đánh dấu đúng trường lỗi; không lưu một phần. Kết quả commit chưa rõ phải được xác minh trước khi gửi lại | P-18.1/2; phương án kỹ thuật đáp ứng TA-SPEC §4.1, §6 |

| Thông tin | Nguồn và thao tác | Bắt buộc / khả năng sửa |
|---|---|---|
| Hợp đồng / khách hàng | Tự đọc thông tin gắn với hợp đồng đang xem | Chỉ đọc, không cho sửa thủ công ở lập hoặc sửa Draft |
| Loại kỳ | Đọc cấu hình hợp đồng, hiển thị Tháng hoặc Quý | Không tự cho đổi loại trái cấu hình; cấu hình module hợp đồng ngoài phạm vi |
| Kỳ cụ thể | NVKD chọn tháng/năm hoặc quý/năm tương ứng cấu hình | Bắt buộc; thiếu/sai thì tô đỏ trường và nêu lỗi |
| Bảng giá | Hệ thống lấy bảng giá Active gắn với hợp đồng | Chỉ hiển thị; không cho chọn hoặc nhập đè giá |
| Sản lượng / đơn giá | Ánh xạ từ bảng sản lượng của kỳ và bảng giá Active gắn hợp đồng | Chỉ đọc ở cả lập và sửa Draft; không gửi giá trị nhập đè từ form |
| Thành tiền dòng / tổng | Hệ thống tính từ dữ liệu nguồn | Không nhập đè kết quả tính; thuế/làm tròn còn OQ-US03-03 |
| Ghi chú | NVKD nhập ở bước 5 | Tùy chọn, để trống không báo lỗi; chưa tự đặt giới hạn ký tự |

Căn cứ của biểu mẫu: TA-SPEC §2, §4.1, PAY-01..03 và P-18.1/2. Cấu hình có thể khác giữa các kỳ; kiểm tra chồng lấn vẫn áp dụng khi cấu hình hợp đồng đổi. Không thiết kế chức năng thay đổi cấu hình hợp đồng.

P-19 xác nhận khóa trường nguồn ở cả UI và server: request cố sửa sản lượng, đơn giá, hợp đồng hoặc khách hàng bị từ chối; không chỉ ẩn ô nhập. Hệ thống cập nhật đơn giá từ bảng giá Active là đồng bộ nguồn, không phải cho NVKD sửa thủ công. Chỉ bật Lưu nháp khi kỳ và các trường bắt buộc hiện có đã đầy đủ; ghi chú vẫn tùy chọn, không thêm trường thuế bắt buộc khi thuế chưa được xác nhận. Server kiểm tra lại kể cả request bỏ qua UI. Ma trận quyền sửa các trường còn lại, gồm đổi kỳ sau khi đã lưu, vẫn cần OQ-US01-02.

### 1.3. Dòng cơ bản – lập bảng

| Bước | Tác nhân | Hành động và phản hồi | Căn cứ |
|---|---|---|---|
| 1 | NVKD | Bấm Lập bảng thanh toán tại chi tiết hợp đồng | P-18.1 |
| 2 | Hệ thống | Lấy định danh hợp đồng từ ngữ cảnh; kiểm tra phiên, vai trò, quyền lập, tồn tại và Active. Kiểm tra hợp đồng được giao theo đề xuất một người thực hiện | TA-SPEC §2, PAY-01; P-18.1; P-19/OQ-US01-03 |
| 3 | Hệ thống | Mở biểu mẫu với thông tin hợp đồng cố định, loại kỳ theo cấu hình, vùng chọn kỳ và ghi chú tùy chọn | TA-SPEC §2; P-18.1/2 |
| 4 | NVKD | Chọn tháng/năm hoặc quý/năm theo loại kỳ của hợp đồng | TA-SPEC §2; P-18.2 |
| 5 | NVKD | Nhập ghi chú nếu cần; có thể bỏ qua | P-18.2 |
| 6 | Hệ thống | Trước mỗi yêu cầu xem trước, kiểm tra lại phiên/quyền; không đạt thì A6.1 và dừng request. Nếu đạt, kiểm tra trường bắt buộc đầy đủ, kỳ đúng cấu hình và không chồng lấn | P-19; TA-SPEC PAY-01; P-18.3 |
| 7 | Hệ thống | Ánh xạ sản lượng từ bảng sản lượng của kỳ, kiểm tra Đã đối soát; lấy đơn giá từ bảng giá Active gắn hợp đồng và kiểm tra bằng chứng bảng giá được lập lúc hợp đồng còn hiệu lực | P-19; TA-SPEC PAY-01..03; P-18.1/3 |
| 8 | Hệ thống | Sinh dòng, tính thành tiền = sản lượng × đơn giá Active và tổng hợp tổng; chưa lưu bảng | TA-SPEC §4.1, PAY-03 |
| 9 | Hệ thống | Hiển thị kỳ, bảng giá áp dụng, dòng/tổng và ghi chú để NVKD kiểm tra | P-18.1/2; cách trình bày kỹ thuật của TA-SPEC §4.1 |
| 10 | NVKD | Kiểm tra và bấm Lưu nháp; thao tác chỉ được bật khi các trường bắt buộc đã điền đầy đủ | P-18.1/2; P-19 |
| 11 | Hệ thống | Kiểm tra lại phiên/quyền, Active, kỳ, trùng, đối soát và dữ liệu bắt buộc; đọc lại bảng giá Active. Nếu giá thay đổi từ lần xem trước, tính lại theo giá Active và thực hiện A11.1. Nếu sản lượng đổi, chính sách chọn bản nguồn còn Blocked by OQ-US01-04, không tự giữ cũ hoặc lấy mới | TA-SPEC PAY-01..03; P-18.3; OQ-US01-04 |
| 12 | Hệ thống | Lưu bảng/dòng/tổng/ghi chú ở Draft và audit create cùng giao dịch; kiểm tra chồng lấn nguyên tử khi ghi để chống hai yêu cầu cùng chiếm thời gian | TA-SPEC §4.1, §6; P-18.3; phương án kỹ thuật |
| 13 | Hệ thống | Thông báo Lập bảng thanh toán thành công, hiển thị bảng đã lưu cùng id/version và kết thúc | P-18.1; id/version là phương án kỹ thuật |

Nguồn sinh dòng rỗng/nhiều bản ghi/đối soát một phần và công thức tiền cuối cùng còn phụ thuộc OQ-US01-04/OQ-US03-03. Phép nhân PAY-03 và giao diện có thể thiết kế độc lập; không mặc định VAT, làm tròn hoặc dữ liệu thiếu bằng 0.

### 1.4. Dòng thay thế và lỗi

Mỗi thông báo dưới đây hiển thị trên màn hình. Không suy ra phải gửi email/SMS hay thông báo cho vai trò khác.

| Nhánh | Rẽ từ | Xử lý / thông báo | Điểm tiếp tục hoặc kết thúc |
|---|---|---|---|
| A2 | 2 hoặc kiểm tra quyền lại ở 11 | Sai phiên/quyền, mất ngữ cảnh hoặc hợp đồng không tồn tại/không Active: nêu rõ nguyên nhân | Về chi tiết hợp đồng, kết thúc lượt lập; khi đủ điều kiện thực hiện lại từ bước 1 |
| A4 | 4/6 hoặc 11 | Thiếu tháng/quý/năm, kỳ sai cấu hình: thông báo chưa thể lưu, tô đỏ đúng trường và nêu lý do; giữ ghi chú | Quay bước 4; sửa xong kiểm tra lại bước 6 |
| A6 | 6 hoặc 11 | Đã có bảng cùng kỳ hoặc chồng lấn tháng/quý: báo kỳ bị chiếm, đánh dấu trường kỳ | Quay bước 4 |
| A6.1 | 6, khi xem trước/thử lại | Phiên hết hạn: trả UNAUTHENTICATED, thông báo cần đăng nhập. Phiên còn hợp lệ nhưng mất quyền, gồm không còn được giao theo đề xuất: trả FORBIDDEN và thông báo không được phép. Không trả preview cũ thành kết quả mới, không đọc sản lượng/giá hoặc ghi bảng sau khi đã từ chối | Khóa xem trước/lưu và kết thúc lượt form. Hết phiên: đăng nhập xong mở lại từ bước 1; mất quyền: chỉ mở lại bước 1 khi được cấp quyền, không thử lại vòng xem trước hiện tại |
| A7 | 7 | Sản lượng chưa Đã đối soát: báo chưa thể lập cho kỳ này | Quay bước 4 chọn kỳ khác; hoặc đóng form theo A10 |
| A7.1 | 7 | Không có hoặc có nhiều hơn một bảng giá Active gắn với hợp đồng: báo lỗi dữ liệu bảng giá, không chọn giá thay thế | Giữ form; thử lại từ bước 7 sau khi nguồn được xử lý, hoặc A10 |
| A7.2 | 2/6/7/11 | Lỗi đọc nguồn/tra trùng: báo tải dữ liệu thất bại, không diễn giải là không tồn tại | Nếu lỗi mở: về chi tiết và thử bước 1; nếu form đã mở: thử lại chính bước 6, 7 hoặc 11 đã lỗi, kể cả không đổi kỳ |
| A7.3 | 7 hoặc 11 | Bảng giá được lập khi hợp đồng chưa hiệu lực, hoặc nguồn chưa cung cấp bằng chứng để xác minh: thông báo bảng giá chưa đáp ứng điều kiện nguồn, không tự suy từ Active hiện tại rằng lúc tạo cũng Active | Giữ form; thử lại từ bước 7 sau khi nguồn được xử lý, hoặc đóng theo A10. Không sửa/tạo bảng giá trong module này |
| A8 | 8 | Dữ liệu rỗng, thiếu giá dòng, gộp/tách hay đối soát một phần chưa đủ chính sách: phần này còn OQ-US01-04; cách tính tiền cuối cùng còn OQ-US03-03 | Khi đã có chính sách, lỗi dữ liệu thông báo và quay bước 4 hoặc thử lại bước 7; hiện chưa chốt nhánh nghiệp vụ cuối cùng |
| A9 | 9 | Đổi kỳ: xóa kết quả phụ thuộc và bảng giá hiển thị cũ; phản hồi cũ đến muộn không ghi đè kỳ mới. Chỉ đổi ghi chú: không cần tính lại tiền | Đổi kỳ quay bước 4 rồi 6–9; đổi ghi chú quay bước 5 rồi 9 |
| A10 | Trước lưu ở 3–10 | Đóng form: thông báo chưa lưu dữ liệu; không tạo Draft hay chuyển Cancelled | Về chi tiết hợp đồng, kết thúc |
| A11 | 11 | Lỗi trường nhập: thông báo, tô đỏ trường thiếu/vi phạm và nêu lý do. Ghi chú trống không bị coi là lỗi | Quay bước 4 nếu lỗi kỳ; nếu nguồn lỗi theo A7.2; nếu điều kiện quyền/Active không còn đạt theo A2 |
| A11.1 | 11 | Bảng giá Active khác lần xem trước: lấy giá mới, tính lại dòng/tổng và thông báo đã cập nhật. Không cho chọn giữ giá cũ | Quay bước 9 để NVKD kiểm tra rồi bấm lưu ở 10; chưa ghi bảng trong nhánh này |
| A11.2 | 11 | Request cố nhập đè sản lượng, đơn giá, hợp đồng, khách hàng hoặc kết quả tính: trả READ_ONLY_FIELD và thông báo trường không được phép thay đổi; không lập bảng từ dữ liệu nhập đè | Kết thúc form, về chi tiết và mở lại từ bước 1 để lấy dữ liệu nguồn |
| A12 | 12 | Yêu cầu đồng thời vừa chiếm kỳ: rollback, báo xung đột và đánh dấu trường kỳ | Quay bước 4 |
| A12.1 | 12 | Lỗi lưu bảng/dòng/audit hoặc commit được xác định chưa xảy ra: rollback giao dịch còn mở; thông báo lưu thất bại, giữ form; không tô đỏ trường hợp lệ vì lỗi hệ thống | NVKD chủ động thử lại từ bước 10, luôn qua kiểm tra bước 11 |
| A12.2 | 12 | Mất kết quả commit: thông báo chưa xác định kết quả, giữ mã tra cứu thao tác; không tự gửi create lại | Sang K1 để xác minh, không quay bước 10 khi chưa có kết luận |

Nhánh lỗi dựa vào TA-SPEC §4.1, PAY-01..03, §6 và review P-18.1/2/3. Giao dịch, version, mã tra cứu và cách phục hồi là đề xuất kỹ thuật.

K1: NVKD yêu cầu kiểm tra kết quả lưu. Hệ thống tra cứu thao tác/bảng đã cấp id và xác minh kết quả giao dịch. Đã lưu thì tiếp tục bước 13; xác định chưa lưu thì quay bước 10; còn chưa rõ thì thông báo và ở K1 hoặc về chi tiết để kết thúc. Cơ chế xác minh cụ thể còn phụ thuộc DB/driver, chưa phải bằng chứng đã triển khai.

### 1.5. Quy tắc tháng/quý và bảng giá

| Trường hợp cùng hợp đồng | Kết quả | Căn cứ |
|---|---|---|
| Đã có tháng 1, xin lập quý I | Từ chối vì quý I bao phủ tháng 1–3 | P-18.3; OQ-01 |
| Đã có tháng 1, xin lập tháng 2/3 | Không chồng lấn tháng 1; vẫn kiểm tra đúng cấu hình và chưa có bảng tháng 2/3 | P-18.3; TA-SPEC §2, PAY-01 |
| Đã có quý II, xin lập tháng 4/5/6 | Từ chối | P-18.3 |
| Đã có quý II, xin lập quý II lần nữa | Từ chối | TA-SPEC PAY-01; P-18.3 |
| Bảng cũ Cancelled | Không dùng lại bảng cũ; cho lập bảng mới theo quyết định US-PAY-05 v2 hiện có | OQ-US05-02 v2, nguồn ở §1.1 |
| Giá mới đã Active khi lưu | Dùng bảng giá mới; nếu khác lần xem trước, tính lại và thông báo A11.1 | P-18.3 |
| Giá mới chưa Active | Dùng bảng giá đang Active, không dùng bản chưa có hiệu lực | P-18.3 |

Việc lấy giá lúc lưu đã rõ. Cơ chế tự cập nhật hàng loạt Draft đang không được mở khi nguồn giá đổi chưa được xác nhận; giữ phần này trong OQ-US01-01, không triển khai tác vụ nền trong thiết kế hiện tại.

### 1.6. Sửa Draft đã lưu

| Bước | Nội dung | Căn cứ |
|---|---|---|
| U1 | NVKD mở bảng Draft và bấm Chỉnh sửa; hệ thống đọc dữ liệu đã lưu và version | TA-SPEC §4.1; cách mở và version là đề xuất kỹ thuật |
| U2 | Kiểm tra phiên/quyền, bảng tồn tại và đang Draft; theo đề xuất một người thực hiện, người gọi phải là người tạo Draft. Rejected không tự được chuyển về Draft để sửa | P-19/OQ-US01-03; TA-SPEC §3, §4.1; OQ-04/OQ-US03-07 |
| U3 | Hiện form; khóa sản lượng, đơn giá, hợp đồng, khách hàng và kết quả tính. NVKD chỉ sửa trường được phép; các trường khác còn OQ-US01-02. Khi hệ thống tính lại/lưu vẫn lấy đơn giá Active từ nguồn | P-19; P-18.1/3; OQ-US01-02 |
| U4 | NVKD bấm Lưu thay đổi; server đọc lại bản hiện tại, kiểm tra version/trạng thái/nội dung, đối chiếu giá Active và tạo candidate hợp lệ. Giá đổi thì thông báo và hiển thị kết quả tính mới trước khi lưu lại | TA-SPEC PAY-03; P-18.3; OQ-US01-02, OQ-US03-03 |
| U5 | Cập nhật có điều kiện Draft/version; lưu cùng candidate vào bảng/dòng và audit before/after trong một giao dịch | TA-SPEC §4.1, §6; phương án kỹ thuật |
| U6 | Hiển thị thông báo lưu thành công, Draft sau sửa và version mới | P-18.1 |

| Nhánh | Xử lý / thông báo | Tiếp tục |
|---|---|---|
| AU1 | Không tồn tại/lỗi đọc/sai quyền/không Draft: thông báo và không mở sửa sai trạng thái | Về bảng đang xem và kết thúc; khi đủ điều kiện mở lại từ U1 |
| AU3 | Đóng form sửa: thông báo thay đổi chưa lưu, giữ dữ liệu đã lưu trước đó | Về bảng đang xem, kết thúc |
| AU4 | Thiếu version, trường vi phạm: thông báo và tô đỏ đúng trường nhập; thiếu token là lỗi tải dữ liệu, không tô đỏ ghi chú trống | Sai nội dung quay U3; thiếu version tải lại từ U1 |
| AU4.1 | Giá Active thay đổi: tính lại, thông báo và hiển thị kết quả mới | Quay U3 để kiểm tra rồi U4; giá cũ không còn là lựa chọn |
| AU4.2 | Request cố ghi đè sản lượng, đơn giá, hợp đồng, khách hàng hoặc kết quả server tính: trả READ_ONLY_FIELD, nêu trường không được phép sửa; dữ liệu đã lưu không đổi | Quay U1 tải lại dữ liệu nguồn, rồi U3 chỉ sửa trường được phép |
| AU4.3 | Nguồn chưa đáp ứng/xác minh được điều kiện bảng giá được lập khi hợp đồng còn hiệu lực: thông báo, không lưu thay đổi | Giữ form ở U3; khi nguồn đã được xử lý, NVKD thử lại U4 |
| AU5 | Version/trạng thái đổi: rollback, thông báo xung đột, không ghi đè | Quay U1 tải lại |
| AU5.1 | Lỗi lưu/audit xác định chưa commit: rollback và thông báo | Quay U3 giữ nội dung; NVKD chủ động lưu lại U4 |
| AU5.2 | Kết quả commit chưa rõ: thông báo và ngăn gửi lại | Sang K1; xác định đã lưu thì U6, chưa lưu thì U3, còn chưa rõ ở K1 |

Ma trận trường sửa/tính lại và chính sách nguồn sản lượng thay đổi vẫn Blocked by OQ-US01-02, OQ-US01-04; không mặc định cho sửa sản lượng/đơn giá nguồn hoặc chốt cách điều chỉnh Approved.

## 2. Open Questions và quyết định

Bảng dưới dùng trạng thái v2. Các conflict trước xác nhận được giữ trong OQ v1 theo yêu cầu. Chi tiết nguồn/câu trả lời: [open-questions-v2.md](open-questions-v2.md); bằng chứng chat tại P-18, không sửa hồi tố TA-SPEC.

| ID | Trạng thái v2 | Phần đã rõ / còn mở | Vị trí quy trình | Nguồn câu trả lời |
|---|---|---|---|---|
| OQ-01 | Đã xác nhận | Đã rõ phạm vi chồng lấn thời gian; loại kỳ vẫn theo cấu hình hợp đồng. | §1.3 bước 6, 11, 12; A6/A12; AC-US01-06, AC-US01-14, AC-US01-30. | Người dùng trong chat / 08/11/2026 / P-18.3: không cho bảng tháng và quý chồng lấn; tháng 1 chặn quý I, quý II chặn tháng 4–6. |
| OQ-US05-02 | Đã xác nhận trong bộ US-PAY-05 v2 hiện có | Giữ quyết định đã có; không suy ra unique index tháng đơn lẻ đủ chống chồng lấn quý/tháng. | §1.3 bước 6, 11, 12; §1.5; AC-US01-07, AC-US01-14. | Người phụ trách / 07/11/2026 / user-review-us-05.md §2.1 và OQ v2: cho lập bảng mới sau hủy; không dùng lại bảng Cancelled. |
| OQ-US03-03 | Cần xác nhận với khách hàng | Thuế vẫn mở; chưa có công thức/thuế suất, chưa thêm trường thuế bắt buộc. Độ chính xác và làm tròn cũng chưa có câu trả lời trong P-19. | §1.3 bước 8/11; §1.6 U4; AC-US01-11, AC-US01-12, AC-US01-17, AC-US01-33. | Người dùng / 08/11/2026 / P-19: thuế phải tiếp tục giữ ở câu hỏi mở để xác nhận lại khách hàng. Đề xuất P-04..P-07 chưa phải phê duyệt. |
| OQ-04 | Cần xác nhận | Chỉ chặn mở sửa bảng bị từ chối; không chặn lập mới/sửa bảng đã Draft. | §1.6 U2/AU1; AC-US01-18. | Giữ đề xuất P-04, chưa coi là phê duyệt. |
| OQ-US03-07 | Cần xác nhận | Chưa rõ người/thời điểm chuyển Rejected về Draft. | §1.6 U2/AU1; AC-US01-18. | Giữ đề xuất P-05/P-06, chưa có xác nhận mới. |
| OQ-US01-01 | Đã rõ chọn giá/lúc tạo giá; còn mở đồng bộ Draft đang không mở | Đã rõ điều kiện nghiệp vụ khi tạo bảng giá; không suy ra từ Active hiện tại sang lịch sử. Còn cách đồng bộ mọi Draft đang không mở; interface nguồn phải cung cấp bằng chứng lúc lập giá. | §1.3 bước 7/11, A7.3/A11.1; §1.6 U4/AU4.1; AC-US01-09, AC-US01-26, AC-US01-34. | Người dùng / 08/11/2026 / P-18.1, P-18.3, P-19: dùng giá Active gắn hợp đồng; bảng giá phải được lập lúc hợp đồng còn hiệu lực. Cần dữ liệu nguồn xác minh điều kiện lúc tạo. |
| OQ-US01-02 | Đã xác nhận khóa trường nguồn; còn ma trận trường khác | UI và server khóa trường nguồn, kể cả sửa Draft; cập nhật đơn giá do hệ thống từ giá Active vẫn hợp lệ. Quyền sửa trường khác, gồm đổi kỳ sau lưu, còn cần xác nhận. | §1.2 biểu mẫu; §1.6 U3/U4/AU4.2; AC-US01-17, AC-US01-32. | Người dùng / 08/11/2026 / P-19: không cho đổi sản lượng, đơn giá, thông tin hợp đồng, khách hàng; q/p ánh xạ từ nguồn, không nhập tay. |
| OQ-US01-03 | Đề xuất theo hướng một người thực hiện – cần xác nhận | Dùng giả định thiết kế có nhãn đề xuất: lập cần được giao hợp đồng; sửa cần đúng người tạo. Không tuyên bố khách hàng đã phê duyệt; không suy ra mỗi hợp đồng chỉ có một NVKD được giao. | §1.2 P1/P4; §1.3 bước 2/6/11/A6.1; §1.6 U2; AC-US01-03, AC-US01-31. | Người dùng / 08/11/2026 / P-19: NVKD chỉ lập trên hợp đồng được giao, không sửa Draft người khác; yêu cầu ghi rõ đây là đề xuất theo hướng một người thực hiện. |
| OQ-US01-04 | Đã rõ ánh xạ nguồn; còn gộp/tách/rỗng/đối soát một phần | Lấy q/p từ nguồn đã rõ. Còn cách ánh xạ nhiều bản ghi, cấp đối soát, rỗng/0 và xử lý thay đổi sản lượng giữa xem trước/lưu; không tự lấp các phần này. | §1.3 bước 7/8/11, A8; §1.6 U4; AC-US01-10, AC-US01-26, AC-US01-32. | Người dùng / 08/11/2026 / P-19: sản lượng và đơn giá ánh xạ từ bảng sản lượng và bảng giá, không nhập thủ công. Chưa trả lời gộp/tách, dữ liệu rỗng/0, đối soát một phần hoặc nguồn đổi. |
| OQ-US01-05 | Đã rõ kiểm tra trạng thái Active; còn mở hiệu lực đối với kỳ | Kiểm tra trạng thái Active thực hiện được; chính sách hiệu lực của kỳ quá khứ/một phần kỳ còn cần xác nhận. | §1.3 bước 2/11; AC-US01-05. | Người dùng trong chat / 08/11/2026 / P-18.1: kiểm tra Active (Có hiệu lực); chưa trả lời lập bù/hiệu lực một phần kỳ. |
| OQ-US01-06 | Cần xác nhận | Chưa kết luận đạt ≤3 giây với <200 dòng; không thêm SLA cho sửa Draft. | §4; AC-US01-20. | Chưa có câu trả lời về điểm đo, cách đếm dòng và môi trường. |

## 3. Acceptance criteria và truy vết

Giữ ID AC-US01-01..26, cập nhật theo quyết định mới; P-18 thêm AC-US01-27..30 và P-19 thêm AC-US01-31..34. Cột “Phân loại” phân biệt AC dẫn xuất, đề xuất chưa duyệt và kiểm chứng kỹ thuật.

| ID | Given / When / Then | Phân loại | Nguồn | OQ |
|---|---|---|---|---|
| AC-US01-01 | Dữ liệu hợp lệ; NVKD thực hiện 1–13; bảng/dòng/tổng/ghi chú được lưu Draft và có thông báo thành công. | AC dẫn xuất | TA-SPEC §4.1; P-18.1/2 | Các phần còn mở xem AC tương ứng |
| AC-US01-02 | Sai phiên/không có vai trò NVKD; mở/xem trước/lưu (2/6/11/U2); trả thông báo từ chối và không ghi, xem trước không gọi giá/sản lượng sau khi từ chối (A2/A6.1/AU1). | Kiểm chứng kỹ thuật | TA-SPEC §2, §4.1; P-18.1; P-19 | – |
| AC-US01-03 | Theo đề xuất một người thực hiện: NVKD lập trên hợp đồng được giao; sửa Draft chỉ khi createdBy là chính mình; kiểm tra lại mỗi request. Không coi đề xuất này là phê duyệt khách hàng. | Giả định theo đề xuất | P-19; TA-SPEC §2, §4.1 | OQ-US01-03 còn chờ xác nhận đề xuất |
| AC-US01-04 | Thiếu/sai kỳ ở 6/11; thông báo chưa lưu, tô đỏ trường tháng/quý/năm vi phạm, giữ ghi chú và quay 4 (A4/A11). | AC dẫn xuất | P-18.2; TA-SPEC §2 | – |
| AC-US01-05 | Hợp đồng không tồn tại/không Active tại 2/11; thông báo và kết thúc về chi tiết (A2); không tự thêm cấm kỳ quá khứ. | AC dẫn xuất | TA-SPEC PAY-01; P-18.1 | OQ-US01-05 còn phần hiệu lực theo kỳ |
| AC-US01-06 | Kỳ sai cấu hình hoặc chồng lấn ở 6/11; từ chối, đánh dấu kỳ và quay 4 (A6). | AC dẫn xuất | TA-SPEC §2/PAY-01; P-18.3 | OQ-01 đã xác nhận |
| AC-US01-07 | Bảng cũ Cancelled; kiểm tra trùng; được tạo bảng mới, giữ bảng cũ và bỏ bảng cũ khỏi phạm vi chiếm kỳ. | AC dẫn xuất | OQ-US05-02 v2; user-review-us-05.md §2.1 | Quyết định US05 v2 đã có |
| AC-US01-08 | Không có giá Active phù hợp hoặc sản lượng chưa đối soát ở 7; thông báo, không lưu; thử lại 7 hoặc đổi kỳ 4 (A7/A7.1). | AC dẫn xuất | TA-SPEC PAY-01/02; P-18.1/3 | Ánh xạ nguồn theo OQ-US01-04 |
| AC-US01-09 | Lúc lưu có giá mới đã Active; dùng giá mới. Giá mới chưa Active thì dùng Active hiện tại. Không cho chọn giữ giá cũ (A11.1). | AC dẫn xuất | P-18.1/3; TA-SPEC PAY-03 | OQ-US01-01 đã rõ phần lúc lưu |
| AC-US01-10 | Nguồn rỗng/0/nhiều bản ghi/đối soát một phần tại 7/8/11; xử lý theo chính sách được xác nhận (A8). | AC dẫn xuất | TA-SPEC §4.1, PAY-02/03 | Blocked by OQ-US01-04 |
| AC-US01-11 | q/p xác định từ nguồn; khi sinh dòng 8/11; thành tiền trước xử lý tiền còn mở bằng q × p. | AC dẫn xuất | TA-SPEC PAY-03 | OQ-US03-03 cho xử lý tiền cuối |
| AC-US01-12 | Các dòng đã tính; tính tổng tại 8/11/U4; dùng chính sách tiền được xác nhận, không tự thêm VAT/làm tròn. | AC dẫn xuất | TA-SPEC §4.1/PAY-03 | Blocked by OQ-US03-03 |
| AC-US01-13 | Lỗi đọc nguồn ở 2/6/7/11/U1; thông báo, không coi là dữ liệu rỗng, cho thử lại cùng kỳ từ bước lỗi (A7.2/AU1). | Kiểm chứng kỹ thuật | TA-SPEC §1/§4.1; P-18.1 | – |
| AC-US01-14 | Hai yêu cầu tháng/quý chồng lấn tới 12; kiểm tra nguyên tử chỉ cho một yêu cầu chiếm thời gian, yêu cầu thua báo và quay 4 (A12). | AC dẫn xuất / kỹ thuật | TA-SPEC PAY-01; P-18.3 | – |
| AC-US01-15 | Lưu thành công 12–13; dữ liệu và audit cùng tồn tại, audit có ai/lúc nào/thay đổi gì. | Kiểm chứng kỹ thuật | TA-SPEC §6 gạch 1 | – |
| AC-US01-16 | Lỗi lưu/audit (A12.1/AU5.1) không ghi một phần. Kết quả commit chưa rõ (A12.2/AU5.2) thông báo và vào K1; chỉ quay lưu khi xác minh chưa lưu. | Kiểm chứng kỹ thuật | TA-SPEC §4.1/§6; P-18.1 | – |
| AC-US01-17 | Draft đủ quyền theo đề xuất người tạo, chỉ sửa trường được phép; sửa U1–U6; cùng candidate được lưu, audit và response; lỗi nội dung quay U3 (AU4), cố ghi đè nguồn bị từ chối (AU4.2). | AC dẫn xuất / kỹ thuật, quyền là đề xuất | TA-SPEC §4.1/PAY-03/§6; P-19 | OQ-US01-02 còn trường khác, OQ-US01-03 là đề xuất, OQ-US03-03 còn thuế/làm tròn |
| AC-US01-18 | Bảng không tồn tại/không Draft; mở sửa U1/U2; thông báo và kết thúc (AU1), không tự chuyển Rejected về Draft. | AC dẫn xuất | TA-SPEC §3/§4.1/PAY-08 | Blocked by OQ-04, OQ-US03-07 với bảng bị từ chối |
| AC-US01-19 | Tạo/đọc/sửa trả version; thiếu version khi sửa tải lại U1; token/trạng thái cũ báo xung đột, quay U1 (AU4/AU5). | Kiểm chứng kỹ thuật | TA-SPEC §4.1 | – |
| AC-US01-20 | Hợp đồng <200 dòng; lập bảng phản hồi ≤3 giây theo cách đo được xác nhận; 200 dòng không thuộc điều kiện gốc. | AC dẫn xuất | TA-SPEC §6 gạch 2 | Blocked by OQ-US01-06; chưa đo |
| AC-US01-21 | Từ chi tiết hợp đồng bấm Lập bảng (1–3); form tự điền đúng hợp đồng, không tải danh sách/chọn lại; chưa ghi Draft. | AC dẫn xuất | P-18.1 | – |
| AC-US01-22 | Hợp đồng cấu hình tháng hoặc quý; bước 4 cho chọn tháng/năm hoặc quý/năm tương ứng; không cho nhập loại trái cấu hình. | AC dẫn xuất | TA-SPEC §2; P-18.2 | – |
| AC-US01-23 | Xem trước 8–9 chưa ghi Draft; chỉ sau bấm Lưu nháp 10 và kiểm tra 11 mới ghi 12. | Kiểm chứng kỹ thuật | P-18.1/2; TA-SPEC §4.1 | – |
| AC-US01-24 | Đổi kỳ ở A9 phải quay 4, tính lại từ 6; đổi ghi chú quay 5 rồi 9 không đổi tiền; phản hồi cũ không ghi đè kỳ mới. | Kiểm chứng kỹ thuật | TA-SPEC §4.1/PAY-03; P-18.2 | – |
| AC-US01-25 | Đóng form trước lưu (A10/AU3); thông báo chưa lưu, về chi tiết/bảng; không tạo bảng hay chuyển Cancelled. | Kiểm chứng kỹ thuật | P-18.1; TA-SPEC §4.1/§4.5 | – |
| AC-US01-26 | Nguồn giá đổi giữa xem trước và lưu; lấy Active, tính lại và thông báo, quay 9 rồi 10 (A11.1/AU4.1). Nguồn sản lượng thay đổi còn chờ chính sách. | AC dẫn xuất | P-18.3; TA-SPEC PAY-03 | OQ-US01-04 cho sản lượng; OQ-US01-01 chỉ còn đồng bộ nền |
| AC-US01-27 | Ghi chú bỏ trống hoặc có nội dung; lập bảng; cả hai hợp lệ, lưu ghi chú nếu có, không tự đặt giới hạn ký tự. | AC dẫn xuất | P-18.2 | – |
| AC-US01-28 | Lưu lỗi trường bắt buộc/vi phạm; tô đỏ đúng trường, nêu lý do, giữ dữ liệu. Lỗi hệ thống không tô đỏ trường hợp lệ; ghi chú trống không báo thiếu. | AC dẫn xuất | P-18.2 | – |
| AC-US01-29 | Kết thúc thao tác thành công/thất bại/đóng trước lưu; hiển thị thông báo phù hợp. K1 có ba đường: đã lưu→13/U6, chưa lưu→10/U3, chưa rõ→K1 hoặc kết thúc. | AC dẫn xuất / kỹ thuật | P-18.1; §1.4 K1 | – |
| AC-US01-30 | Có tháng 1 thì không lập quý I; có quý II thì không lập tháng 4/5/6; tháng 2 không trùng tháng 1 nếu đúng cấu hình và chưa bị chiếm. | AC dẫn xuất | P-18.3; OQ-01 | – |
| AC-US01-31 | Form đang mở, phiên hết hạn hoặc bị thu quyền; yêu cầu xem trước/thử lại; nhận 401 UNAUTHENTICATED hoặc 403 FORBIDDEN, có thông báo tương ứng, đóng/khóa form và chỉ mở lại bước 1 sau khi đủ điều kiện (A6.1). | Kiểm chứng kỹ thuật | P-19 | Quyền được giao theo đề xuất OQ-US01-03 |
| AC-US01-32 | UI không cho sửa sản lượng/đơn giá/hợp đồng/khách hàng; request ghi đè thủ công khi lập hoặc sửa bị server từ chối, không lưu (A11.2/AU4.2). q/p lấy từ bảng sản lượng/bảng giá; đồng bộ giá Active của hệ thống vẫn hợp lệ. | AC dẫn xuất | P-19; TA-SPEC §1, PAY-03 | Các trường khác còn OQ-US01-02 |
| AC-US01-33 | Thiếu trường bắt buộc: Lưu nháp không được bật, preview không sinh bảng từ dữ liệu thiếu. Request bỏ qua UI vẫn bị server từ chối, có lỗi trường; đủ dữ liệu mới qua bước 6/11, ghi chú trống không chặn. | AC dẫn xuất / kỹ thuật | P-19; P-18.2 | Thuế chưa phải trường bắt buộc do OQ-US03-03 |
| AC-US01-34 | Bảng giá phải được tạo khi hợp đồng còn hiệu lực. Reader cung cấp bằng chứng nguồn; sai hoặc chưa xác minh được thì thông báo A7.3/AU4.3 và không lưu. Không lấy Active hiện tại làm bằng chứng lịch sử. | AC dẫn xuất / tích hợp đề xuất | P-19 | Interface nguồn phải cung cấp dữ liệu xác minh, chưa có bằng chứng triển khai |

## 4. NFR và giới hạn thiết kế

NFR-PAY-01 áp dụng audit mọi thay đổi trạng thái/điều chỉnh, kể cả sửa vẫn Draft; tạo Draft được đề xuất ghi audit cùng dữ liệu. NFR-PAY-02 giữ đúng ≤3 giây với hợp đồng có <200 dòng; chưa chốt cách đo theo OQ-US01-06 và chưa đo. Không tự thêm tải đồng thời/percentile hay SLA cho sửa Draft. Nguồn: TA-SPEC §6.

Thiết kế transaction bảo đảm duy nhất phạm vi thời gian và audit trong module thanh toán, không khóa được nguồn hợp đồng/giá/sản lượng bằng transaction cục bộ. Phương án đề xuất: đọc giá Active khi tính/lưu, dùng phiên bản nguồn để phát hiện thay đổi; phối hợp kiểm tra giá tại thời điểm chốt lưu cần được hoàn thiện khi chọn interface nguồn. Chưa tuyên bố bảo đảm nguyên tử liên module hoặc đã đo NFR.

## Thay đổi so với v1

| Vị trí | Thay đổi | Căn cứ |
|---|---|---|
| Điểm vào / bước 1–3 | Từ chi tiết hợp đồng; bỏ danh sách/chọn lại hợp đồng | P-18.1 |
| Bước 4–5 / biểu mẫu | Chọn tháng/năm hoặc quý/năm theo cấu hình; ghi chú tùy chọn | P-18.2 |
| Bước 6, 12 | Chặn chồng lấn tháng/quý, không chỉ so mã kỳ | P-18.3, OQ-01 |
| Bước 7, 11 / U4 | Tự lấy giá Active gắn với hợp đồng, giá đổi tính lại; bỏ chọn giá thủ công | P-18.1/3, OQ-US01-01 |
| Các nhánh lỗi | Có thông báo, đánh dấu trường vi phạm, điểm quay lại cụ thể và vòng thử lại | P-18.1/2 |
| AC / OQ | Giữ ID; tách quyết định đã rõ và phần còn mở; không coi đề xuất VAT là phê duyệt | P-18, TA-SPEC §4.1/PAY-03 |
| Bổ sung sau P-18 | P-19 thêm phản hồi hết phiên/mất quyền lúc xem trước; ghi rõ đề xuất một người thực hiện; khóa trường nguồn, bắt buộc đủ dữ liệu; giữ thuế mở; kiểm tra điều kiện lúc tạo bảng giá. Thêm AC-US01-31..34, A6.1/A7.3/AU4.2/AU4.3 | P-19 |
| Bản đối chiếu | [SYS-US-01 v1](../v1/sys-us-01-v1.md) | Chỉ liên kết v1 trong mục so sánh này |

Sequence: [seq-us-01-v2.puml](../../../design/payment-management/v2/diagrams/seq-us-01-v2.puml). Bản v2 là tài liệu thiết kế, không phải triển khai mã ứng dụng hay phê duyệt toàn bộ nghiệp vụ.
