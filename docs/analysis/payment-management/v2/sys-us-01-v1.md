# Đặc tả Use Case hệ thống – SYS-PAY-01: Lập bảng thanh toán – v01

> **Nguồn:** TA-SPEC ([spec.md](../../requirements/payment-management/spec.md)), §1–6; vị trí trang TA-PDF theo [sổ nguồn](../../requirements/payment-management/sources.md); các xác nhận trực tiếp của người dùng ghi tại Phần 1–2 dưới đây.
> **Bản hiện hành:** Nội dung sau xác nhận được lưu trong file v01. Phần 1–2 giữ căn cứ và quyết định; Phần 3 chỉ trình bày đặc tả thao tác; Phần 5 tách riêng truy vết nguồn.
> **Trạng thái:** Bản tổng hợp sau xác nhận luồng và phương án đã trao đổi. Các nội dung được xác nhận không còn coi là giả định; các câu hỏi chưa có câu trả lời cụ thể vẫn được giữ ở Phần 4. Không tuyên bố mọi câu hỏi đã đóng hoặc đã kiểm thử hệ thống.
>
> **Nhãn dùng trong phần căn cứ, ngoài bảng Use Case:**
> - `[ĐẶC TẢ]`: có trong TA-SPEC.
> - `[AC dẫn xuất]`: suy ra trực tiếp từ yêu cầu có căn cứ.
> - `[QUYẾT ĐỊNH ĐÃ XÁC NHẬN]`: người dùng đã trả lời hoặc đồng ý phương án trong cuộc trao đổi này.
> - `[ĐỀ XUẤT KỸ THUẬT – ĐÃ ĐỒNG Ý]`: phương án bổ sung được người dùng chấp nhận; không phải câu nguyên văn trong đề.

## Phần 1. Nội dung đã xác nhận

### 1.1. Căn cứ xác nhận

- **USER-01:** Tin nhắn người dùng trả lời trực tiếp CREATE-01, 02, 03, 04, 08, 09, 10, 11, 12, 13. Nội dung từng câu trả lời được trích tại bảng 1.2.
- **USER-02:** Tin nhắn bắt đầu bằng “tôi đồng ý với thiết kế của bạn.”, tiếp theo yêu cầu viết đặc tả chức năng hệ thống theo mẫu Use Case. Xác nhận này áp dụng cho luồng và các phương án đã trình bày trước đó; không tự thay thế câu trả lời còn thiếu về dữ liệu rỗng, cách gom dòng hoặc làm tròn.
- **USER-03:** Yêu cầu lưu v01 là phân tích từ đề và v02 là bản sau xác nhận, trình bày nội dung xác nhận/đề xuất trước đặc tả hệ thống.
- **USER-04:** Yêu cầu kiểm tra bảng trùng ngay ở bước lưu, bao gồm Draft; làm rõ trùng tháng/quý; thay khung opt lịch sử Cancelled bằng ghi chú; bỏ interaction ref và bỏ nhãn xác nhận khỏi các bước đặc tả. Quy tắc áp dụng cho cùng hợp đồng/kỳ; khi cập nhật loại chính bảng đang sửa.
- **Người xác nhận:** người dùng trong cuộc trao đổi này; không tự gán tên hoặc vai trò phê duyệt khác. **Ngày ghi nhận vào tài liệu:** 07/11/2026 (Asia/Saigon). Các mã USER là tham chiếu nội bộ cho lời xác nhận, không phải mã trong đề.

### 1.2. Quy tắc nghiệp vụ sau xác nhận

Tất cả các dòng sau mang nhãn `[QUYẾT ĐỊNH ĐÃ XÁC NHẬN]`. TA-SPEC được giữ nguyên; bảng này ghi cách làm rõ/bổ sung khi thiết kế chức năng, không coi là nội dung nguyên văn của đề.

| ID trao đổi | Câu trả lời của người dùng (USER-01) | Quy tắc áp dụng | Căn cứ gốc / ảnh hưởng |
|---|---|---|---|
| CREATE-01 | “cho phép theo tháng hoặc theo quý.” | Kỳ thanh toán hỗ trợ tháng hoặc quý theo cấu hình hợp đồng. Kiểm tra trùng theo hợp đồng/kỳ; bảng khác kỳ nhưng chồng lấn còn CREATE-16. | TA-SPEC §2; PAY-01. Giải quyết khác biệt tháng/quý trong v01 ở mức loại kỳ được phép. |
| CREATE-02 | “khi đã cancelled thì xem như bảng không còn tồn tại, do đó có thể tạo lại bảng mới” | Bảng Cancelled không ngăn lập bảng mới cho cùng hợp đồng/kỳ; không khôi phục để dùng lại bảng cũ. Việc giữ lịch sử được chấp nhận tại KT-03. | PAY-01; US-PAY-05. |
| CREATE-03 | “khi hợp đồng hết hiệu lực, không cho phép thao tác. bắt buộc phải lập bảng trước khi hết hiệu lực” | Trong SYS-PAY-01, không cho lập hoặc sửa Draft khi hợp đồng hết hiệu lực; kiểm tra lại trước khi lưu. Phạm vi ảnh hưởng sang chức năng khác còn CREATE-18. | PAY-01; ảnh hưởng bước chọn hợp đồng, lưu và A1. |
| CREATE-04 | “áp dụng mức giá theo bảng giá đang có hiệu lực cho hợp đồng. chỉ có một bảng giá hiệu lực tại 1 thời điểm.” | Sử dụng bảng giá hiện hành cho hợp đồng; tại một thời điểm chỉ có một bảng giá hiệu lực. Không tự chọn bảng hết hiệu lực. | PAY-01, PAY-03; xem KT-01. |
| CREATE-08 | “được chỉnh sửa các trường kỳ, sản lượng, bảng giá, dịch vụ, ghi chú” | Khi còn Draft, cho sửa kỳ, sản lượng, bảng giá, dịch vụ, ghi chú; áp dụng đồng thời giới hạn giá hiện hành và KT-01. Chưa có quyền sửa trực tiếp đơn giá hoặc thành tiền. | US-PAY-01; phạm vi sửa dữ liệu trên bản nháp, không sửa module nguồn. |
| CREATE-09 | “cập nhật lại. như create-04, chỉ một bảng giá có hiệu lực tại một thời điểm.” | Dữ liệu nguồn thay đổi thì cập nhật lại cho bản nháp; nếu ảnh hưởng phần đã sửa, thực hiện KT-02 trước khi ghi đè. | TA-SPEC §1; US-PAY-01; PAY-03. |
| CREATE-10 | “chỉ sửa bảng cho mình lập.” | NVKD chỉ được sửa Draft do chính mình lập. | US-PAY-01; ảnh hưởng kiểm tra quyền khi mở và khi lưu. |
| CREATE-11 | “khi lưu nháp, đảm bảo các trường bắt buộc phải được fill” | Lưu nháp phải điền đủ trường bắt buộc. Danh sách trường cụ thể còn CREATE-11a. | US-PAY-01; không tự chuyển toàn bộ PAY-04 thành điều kiện lưu nháp. |
| CREATE-12 | “khi nhấn lưu lại, chỉ lưu một bảng, tránh trùng.” | Gửi lại cùng yêu cầu không tạo bảng mới. Chỉ tạo khi không có bảng khác cùng hợp đồng, cùng tháng/năm hoặc quý/năm ở trạng thái khác Cancelled, kể cả Draft. Kiểm tra lại trước lưu và tại điểm ghi để chống tạo đồng thời; khi sửa loại chính bảng đang sửa. [USER-04] | PAY-01; US-PAY-01; KT-04. |
| CREATE-13 | “dòng thanh toán. tính từ khi bấm lưu” | Điều kiện hiệu năng áp dụng với dưới 200 dòng thanh toán; bắt đầu đo khi bấm Lưu. Điểm kết thúc được làm rõ tại KT-05. | TA-SPEC §6; giữ ngưỡng dưới 200, không đổi thành 200 hoặc ít hơn. |

## Phần 2. Các đề xuất đã được đồng ý

Các phương án dưới đây được trình bày trước tin nhắn USER-02 và được người dùng đồng ý. Đây là quyết định bổ sung cho bản v02, không sửa hồi tố TA-SPEC. Chi tiết triển khai cụ thể chưa được thiết kế trong tài liệu Use Case này.

| ID | Phương án đã đồng ý | Mục đích và yêu cầu liên quan | Lựa chọn khác đã cân nhắc / lý do chọn | Tác động |
|---|---|---|---|---|
| KT-01 | Hệ thống tự xác định bảng giá đang hiệu lực; trường bảng giá chỉ phản ánh/cập nhật lựa chọn hợp lệ, không mở quyền chọn giá lịch sử trái CREATE-04. [USER-02; CREATE-04, CREATE-08] | Giữ giá áp dụng nhất quán với quy tắc một bảng giá hiệu lực. | Cho chọn tùy ý dễ trái CREATE-04; tự xác định phù hợp quy tắc hiện hành. | Làm rõ nghĩa “sửa bảng giá”; không cho sửa bảng giá ở module nguồn. Không mặc định được sửa trực tiếp đơn giá. |
| KT-02 | Khi phát hiện nguồn thay đổi lúc lưu, hiển thị phần thay đổi ảnh hưởng đến dữ liệu NVKD đã sửa trước khi áp dụng; sau xác nhận cập nhật, tính lại và cho kiểm tra bản nháp trước khi lưu. [USER-02; CREATE-08, CREATE-09] | Tránh âm thầm mất chỉnh sửa hoặc thay đổi số tiền ngoài dự kiến. | Ghi đè ngay đơn giản hơn nhưng có thể làm mất dữ liệu; giữ nguyên mãi không đáp ứng CREATE-09. | Không lưu âm thầm theo dữ liệu cũ khi nguồn đã thay đổi; chưa xác nhận áp dụng thì giữ phần nhập trên màn hình. |
| KT-03 | Giữ bảng Cancelled và audit log để truy vết, nhưng loại khỏi kiểm tra trùng; tạo lại là tạo một bảng mới. [USER-02; CREATE-02; US-PAY-05; TA-SPEC §6] | Cho lập lại mà vẫn có lịch sử. | Xóa vật lý làm mất dấu vết; khôi phục bảng cũ trái yêu cầu không dùng lại. | Có thể có nhiều bản ghi lịch sử cùng hợp đồng/kỳ, nhưng không có nhiều bảng chưa Cancelled trùng kỳ. |
| KT-04 | Lưu bảng, toàn bộ dòng và audit liên quan cùng thành công hoặc cùng thất bại; kiểm soát lưu lặp và tạo đồng thời. [USER-02; CREATE-12; PAY-01; TA-SPEC §6] | Tránh dữ liệu dở dang, trùng bảng và thiếu audit. | Chỉ vô hiệu hóa nút Lưu không ngăn được yêu cầu gửi lại hoặc hai người tạo đồng thời. | Kiểm soát phía hệ thống; cơ chế giao dịch/chống lặp cụ thể thuộc thiết kế chi tiết, không mặc định một công nghệ. |
| KT-05 | Kết thúc đo thời gian khi NVKD nhận kết quả lưu thành công sau khi dữ liệu đã được lưu. [USER-02; CREATE-13; TA-SPEC §6] | Làm rõ tiêu chí phản hồi trong 3 giây. | Chỉ đo xử lý nội bộ có thể bỏ qua thời gian người dùng chờ; đo từ bấm Lưu đến kết quả phản ánh trải nghiệm đã thống nhất. | Đây là yêu cầu kiểm thử, chưa phải bằng chứng hệ thống đã đạt. Không tự thêm percentile hoặc tải đồng thời. |

## Phần 3. Đặc tả Use Case hệ thống

| Mục | Nội dung |
|---|---|
| **Tên Use Case (SYS-PAY-01)** | Lập bảng thanh toán. |
| **Tác nhân** | **Chính:** Nhân viên kinh doanh (NVKD).<br>**Hỗ trợ:** Các module cung cấp dữ liệu hợp đồng, bảng giá và sản lượng. |
| **Mục tiêu** | Lập bảng thanh toán cho hợp đồng và kỳ thanh toán; hệ thống tự sinh dòng, tính tiền và lưu ở trạng thái `Draft`. Cho phép NVKD sửa bản nháp do mình lập. |
| **Kích hoạt** | NVKD chọn **Lập bảng thanh toán** hoặc mở bản nháp do mình lập để chỉnh sửa. |
| **Tiền điều kiện** | **P1.** Người thực hiện có vai trò NVKD.<br>**P2.** Hợp đồng đang Active, chưa hết hiệu lực.<br>**P3.** Có đúng một bảng giá đang hiệu lực cho hợp đồng.<br>**P4.** Sản lượng sử dụng để lập đã đối soát.<br>**P5.** Khi tạo mới, không có bảng khác cùng hợp đồng và cùng kỳ tháng/năm hoặc quý/năm ở bất kỳ trạng thái nào ngoài Cancelled, bao gồm Draft. Khi sửa, kiểm tra này loại chính bảng đang sửa.<br>**P6.** Khi sửa, bảng còn Draft và người sửa là người lập. |
| **Hậu điều kiện** | **Thành công:** Bảng và toàn bộ dòng được lưu ở Draft; hệ thống đã tính thành tiền và tổng tiền. Ghi nhận người lập, thời điểm lập; khi sửa giữ người lập và ghi audit nội dung điều chỉnh. Không tạo thêm bảng khi gửi lại cùng yêu cầu hoặc khi có yêu cầu tạo trùng đồng thời. Không sửa dữ liệu của module nguồn.<br>**Thất bại:** Không lưu dữ liệu dở dang; nếu đang sửa, dữ liệu đã lưu trước đó không bị cập nhật một phần. |
| **Dòng cơ bản** | **1.** NVKD mở chức năng lập bảng.<br>**2.** Hệ thống hiển thị biểu mẫu và lựa chọn hợp đồng.<br>**3.** NVKD chọn hợp đồng và kỳ tháng/quý theo cấu hình hợp đồng.<br>**4.** Hệ thống kiểm tra hợp đồng còn hiệu lực và tìm bảng khác cùng hợp đồng, cùng tháng/năm hoặc quý/năm, có trạng thái khác Cancelled, kể cả Draft. Nếu có bảng trùng hoặc hợp đồng không hợp lệ, xử lý E4.<br>**5.** Hệ thống đọc sản lượng của kỳ, xác định bảng giá đang hiệu lực và kiểm tra điều kiện đối soát. Không đạt thì xử lý E5; lỗi đọc dữ liệu thì xử lý E10.<br>**6.** Hệ thống sinh các dòng, tính thành tiền mỗi dòng bằng sản lượng × đơn giá và tính tổng tiền.<br>**7.** Hệ thống hiển thị bản xem trước. NVKD kiểm tra, chỉnh sửa kỳ, sản lượng, dịch vụ, ghi chú; bảng giá áp dụng do hệ thống xác định theo hiệu lực. Nếu đổi kỳ hoặc dịch vụ, hệ thống đọc lại dữ liệu liên quan, kiểm tra trùng theo kỳ mới và tính lại.<br>**8.** NVKD nhấn **Lưu**.<br>**9.** Hệ thống kiểm tra yêu cầu lưu theo thứ tự:<br>**9.1.** Nhận diện cùng yêu cầu đã lưu thành công; nếu có, xử lý A10.<br>**9.2.** Kiểm tra trường bắt buộc, kỳ theo cấu hình, hiệu lực hợp đồng, bảng giá và sản lượng; nếu sửa, kiểm tra thêm người lập, Draft và phiên bản dữ liệu.<br>**9.3.** Kiểm tra lại có bảng khác cùng hợp đồng, cùng tháng/năm hoặc quý/năm, trạng thái khác Cancelled, kể cả Draft hay không. Khi sửa, loại chính bảng đang sửa. Nếu có bảng trùng, từ chối lưu theo E9. Nếu cùng yêu cầu vừa hoàn tất, trả kết quả theo A10.<br>**9.4.** Đối chiếu nguồn hiện tại với mốc nguồn của bản xem trước; nguồn thay đổi thì xử lý A9.<br>**10.** Hệ thống tính lại tiền và thực hiện giao dịch lưu. Trong giao dịch, hệ thống kiểm tra lại kết quả yêu cầu, bảng trùng cùng hợp đồng/kỳ, thời hạn hợp đồng và điều kiện cập nhật trước khi ghi. Chỉ khi không có bảng khác chưa Cancelled cùng kỳ, hệ thống mới lưu bảng Draft, các dòng, audit và kết quả thao tác. Gặp xung đột thì xử lý E9; lỗi ghi thì xử lý E10.<br>**11.** Hệ thống trả kết quả lưu thành công và hiển thị bảng đã lưu. |
| **Dòng thay thế** | **A1 – Chỉnh sửa Draft:**<br>(1) NVKD mở bảng do mình lập.<br>(2) Hệ thống kiểm tra vai trò, người lập, trạng thái Draft và hiệu lực hợp đồng.<br>(3) NVKD chỉnh sửa các trường được phép; hệ thống kiểm tra dữ liệu phụ thuộc và tính lại.<br>(4) NVKD nhấn Lưu và tiếp tục từ bước 9. Kiểm tra trùng loại chính bảng đang sửa; lưu thành công cập nhật bảng hiện có, giữ Draft và giữ người lập.<br><br>**A9 – Nguồn thay đổi khi lưu:**<br>(1) Hệ thống hiển thị phần nguồn thay đổi và tác động lên dữ liệu NVKD đã chỉnh sửa; chưa ghi dữ liệu.<br>(2) NVKD xác nhận áp dụng; hệ thống cập nhật phần được chấp nhận, tính lại và hiển thị bản xem trước.<br>(3) NVKD kiểm tra và nhấn Lưu lại; hệ thống thực hiện lại bước 9. Nếu NVKD chưa xác nhận thì giữ phần nhập, chưa ghi đè và chưa lưu theo nguồn cũ.<br><br>**A10 – Gửi lại cùng yêu cầu đã thành công:** Hệ thống trả kết quả của lần lưu đã hoàn tất; không tạo thêm bảng, dòng, audit hoặc áp dụng điều chỉnh lần nữa. Yêu cầu tạo khác trùng hợp đồng/kỳ vẫn bị từ chối. |
| **Dòng lỗi** | **E4 – Không đủ điều kiện lập:** Hợp đồng không còn hiệu lực hoặc đã có bảng khác chưa Cancelled cùng hợp đồng, cùng tháng/năm hoặc quý/năm, kể cả Draft. Hệ thống không lập thêm và thông báo nguyên nhân.<br><br>**E5 – Bảng giá hoặc sản lượng không hợp lệ:** Không xác định được đúng một bảng giá hiệu lực, hoặc sản lượng sử dụng chưa đối soát. Hệ thống không lưu và thông báo nguyên nhân.<br><br>**E9 – Kiểm tra trước lưu hoặc tại điểm ghi không đạt:**<br>• Thiếu trường bắt buộc hoặc kỳ không phù hợp: chỉ rõ điều kiện cần sửa, giữ phần nhập.<br>• Có bảng khác chưa Cancelled cùng hợp đồng/kỳ, kể cả Draft: từ chối tạo hoặc đổi kỳ gây trùng.<br>• Hợp đồng hết hiệu lực, người sửa không phải người lập, bảng không còn Draft, phiên bản đã thay đổi hoặc mã yêu cầu được dùng cho nội dung khác: từ chối ghi thay đổi và thông báo nguyên nhân.<br>• Xung đột phát sinh khi ghi: hủy giao dịch; không lưu bảng hoặc dòng dở dang.<br><br>**E10 – Lỗi đọc nguồn/kho, tính toán hoặc ghi dữ liệu:** Thông báo lỗi. Nếu lỗi trong giao dịch, hủy toàn bộ phần ghi bảng, dòng, audit và kết quả thao tác. Nếu mất phản hồi sau khi đã lưu thành công, gửi lại cùng yêu cầu được xử lý theo A10. |
| **Yêu cầu phi chức năng** | **Audit:** Mọi thay đổi trạng thái và điều chỉnh ghi ai, lúc nào, thay đổi gì. Bảng, dòng, audit và kết quả thao tác cùng thành công hoặc cùng thất bại.<br>**Hiệu năng:** Với dưới 200 dòng thanh toán, thời gian từ khi bấm Lưu đến khi nhận kết quả thành công sau khi dữ liệu đã được lưu không quá 3 giây.<br>**Toàn vẹn:** Kiểm tra quyền, trạng thái, thời hạn hợp đồng và trùng kỳ ở phía hệ thống; kiểm soát trùng tại thời điểm ghi để hai yêu cầu đồng thời không tạo được hai bảng. |

Bảng Cancelled không ngăn lập lại: tạo một bảng mới, giữ bảng cũ và lịch sử. Kiểm tra cùng kỳ bao gồm năm và tháng hoặc năm và quý; không áp dụng giới hạn một bảng cho toàn bộ lịch sử hợp đồng.

## Phần 4. Chi tiết chưa có quyết định cụ thể

Các chi tiết dưới đây vẫn cần câu trả lời cụ thể trước khi triển khai đầy đủ. Phần 3 chỉ trình bày các bước; phạm vi bị chặn và căn cứ được tách tại phần này và Phần 5.

| ID | Vị trí mọi nguồn | Loại | Vấn đề | Lý do cần xác nhận | Lựa chọn nếu có | Ảnh hưởng | Trạng thái | Người/ngày/câu trả lời và tham chiếu |
|---|---|---|---|---|---|---|---|---|
| CREATE-05 | TA-SPEC §4.1; PAY-02; TA-PDF tr.2; v01 CREATE-05 | Thiếu | Không có sản lượng hoặc chỉ một phần đã đối soát. | Chưa xác định được bảng rỗng hoặc phạm vi dữ liệu được lập. | Chặn / lập phần đủ điều kiện / phương án khác. | P4, bước 5, E5. | Cần xác nhận | Chưa có câu trả lời cụ thể; USER-02 không chọn phương án. |
| CREATE-06 | TA-SPEC §4.1; PAY-03; TA-PDF tr.2; v01 CREATE-06 | Thiếu | Cách gộp/tách dòng theo dịch vụ, đơn giá, đơn vị tính. | Quyết định cấu trúc dòng, số dòng và kết quả tính. | Gom theo dịch vụ / tách theo tổ hợp dữ liệu tính tiền. | Bước 6, phép tính, số dòng để đo hiệu năng. | Cần xác nhận | Chưa có câu trả lời cụ thể. |
| CREATE-07 | PAY-03; TA-PDF tr.2; v01 CREATE-07 | Thiếu | Độ chính xác và quy tắc làm tròn. | Không thể chốt kết quả số tiền kỳ vọng. | Làm tròn dòng / tổng; số chữ số và cách làm tròn cần chọn. | Bước 6, 10. | Cần xác nhận | Chưa có câu trả lời cụ thể. |
| CREATE-11a | US-PAY-01; PAY-04; USER-01 CREATE-11; v01 CREATE-11 | Thiếu | Danh sách trường bắt buộc; ghi chú có bắt buộc và có yêu cầu ít nhất một dòng không? | CREATE-11 đã chốt nguyên tắc điền đủ nhưng chưa nêu danh sách kiểm tra. | Liệt kê rõ trường/điều kiện; phối hợp CREATE-05. | Bước 9, E9. | Cần xác nhận | Người dùng mới xác nhận “các trường bắt buộc phải được fill”. |
| CREATE-16 | TA-SPEC §2; PAY-01; USER-01 CREATE-01 | Thiếu | Quý I và tháng 1 cùng hợp đồng có được cùng tồn tại không, nhất là khi cấu hình kỳ thay đổi? | Khác mã kỳ vẫn có thể trùng sản lượng được tính tiền. | Cấm kỳ chồng lấn / quy tắc chuyển đổi kỳ được xác nhận. | P5, bước 4, 9. | Cần xác nhận | Chưa có câu trả lời cụ thể. |
| CREATE-17 | PAY-02; USER-01 CREATE-03 | Thiếu | Đối soát hoàn tất sau khi hợp đồng hết hiệu lực. | Quy tắc hiện tại đồng thời yêu cầu đối soát trước khi lập và lập trước hết hạn, nên trường hợp này không có đường xử lý. Không tự thêm ngoại lệ. | Xác nhận chấp nhận hạn chế / quy trình xử lý riêng có nguồn. | Điều kiện hoàn thành nghiệp vụ; P2, P4. | Cần xác nhận | CREATE-03 vẫn áp dụng đúng như đã chốt. |
| CREATE-18 | USER-01 CREATE-03, CREATE-09; TA-SPEC §4.2–4.4; PAY-05 | Mơ hồ | Phạm vi cấm thao tác sau hết hạn và cập nhật nguồn khi bảng không còn Draft. | Không được tự lan quyền sửa Draft sang PendingApproval/Approved; ảnh hưởng các UC khác và xung đột điều chỉnh Approved vốn còn mở. | Xác định riêng trong SYS-PAY-02, 03, 04, 05. | Không chặn luồng tạo/sửa Draft đã mô tả; cần đồng bộ vòng đời toàn module. | Cần xác nhận | Tài liệu này chỉ chốt phạm vi SYS-PAY-01. |

**Ánh xạ sau xác nhận:** CREATE-01, 02, 03, 04, 08, 09, 10, 12, 13 đã có quyết định cho phạm vi chức năng này; CREATE-11 chốt nguyên tắc, phần danh sách chuyển tiếp sang CREATE-11a. CREATE-14 (nghĩa sửa bảng giá) được làm rõ bằng KT-01; CREATE-15 (cập nhật nguồn trước khi ghi đè chỉnh sửa) bằng KT-02. Giữ các ID CREATE-05, 06, 07 còn mở từ v01 và các câu hỏi phát sinh nêu trên.


## Phần 5. Truy vết nguồn và giới hạn của đặc tả

Phần này giữ căn cứ ngoài bảng Use Case để các bước không bị xen nhãn xác nhận hoặc chú thích nguồn.

| Phần đặc tả | Phân loại và căn cứ |
|---|---|
| Tên, tác nhân, mục tiêu, kích hoạt; bước 1–3 | Đặc tả và AC dẫn xuất từ TA-SPEC §1, §2, §4.1, US-PAY-01; TA-PDF tr.1–2. |
| P2–P5; bước 4, 5, 9.2, 9.3; E4, E5 | PAY-01, PAY-02; CREATE-01..04; USER-01. USER-04 làm rõ kiểm tra cả Draft, thực hiện lại khi lưu và tại điểm ghi, loại chính bảng đang sửa. |
| Sinh dòng/tính tiền; bước 6, 7, 10 | US-PAY-01; PAY-03; CREATE-08, CREATE-09; KT-01. Chi tiết Blocked by CREATE-06, CREATE-07. Dữ liệu rỗng/đối soát một phần Blocked by CREATE-05. |
| Quyền sửa, P6, A1, E9 | US-PAY-01; CREATE-03, CREATE-08, CREATE-10. Kiểm tra phiên bản là đề xuất kỹ thuật để phát hiện xung đột sửa, không phải trạng thái mới. |
| Trường bắt buộc, bước 9.2, E9 | CREATE-11; danh sách cụ thể Blocked by CREATE-11a. |
| A9 và bước 9.4 | CREATE-09; KT-02, được USER-02 đồng ý. Việc NVKD xác nhận cập nhật là thao tác nghiệp vụ, khác với nhãn ghi nhận phê duyệt trong phần căn cứ. |
| A10, bước 9.1, 9.3, 10 | CREATE-12; KT-04. Nhận diện yêu cầu lặp trước kiểm tra dành cho ghi mới; nếu chưa có kết quả, kiểm tra trùng vẫn áp dụng. Truy vấn kết quả yêu cầu và xung đột trước lưu cần nhất quán để không báo trùng nhầm cho cùng yêu cầu vừa hoàn tất. |
| Lưu bảng/dòng/audit/kết quả; hậu điều kiện; E9, E10 | Đề xuất kỹ thuật KT-04 đã được đồng ý; TA-SPEC §6; CREATE-12. Không tự thêm công nghệ lưu trữ hoặc tuyên bố có giao dịch xuyên module nguồn. |
| Cancelled chỉ là ghi chú, được lập lại | US-PAY-05; CREATE-02; KT-03; USER-04. |
| Hiệu năng và audit | TA-SPEC §6; TA-PDF tr.3; CREATE-13; KT-04, KT-05. Chưa có bằng chứng đo hiệu năng hoặc kiểm thử ứng dụng. |
| Kiểm tra tháng/quý | CREATE-01, CREATE-12; USER-04. Chỉ chốt trùng cùng kỳ; các kỳ khác nhau nhưng chồng lấn còn Blocked by CREATE-16. CREATE-17 và CREATE-18 tiếp tục giữ nguyên. |

PAY-04 kiểm tra tổng tiền âm hoặc thiếu dịch vụ bắt buộc khi trình duyệt, thuộc SYS-PAY-02; không tự bổ sung các điều kiện này thành lệnh cấm lưu mọi bản nháp.
