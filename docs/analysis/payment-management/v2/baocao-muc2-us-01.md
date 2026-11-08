# Báo cáo mục 2 – Tổng hợp vấn đề phát triển US-PAY-01

> Ngày: 08/11/2026 · Bản đối chiếu: v1 và v2
> AI: Codex / GPT-6 · Prompt: P-20 trong [nhật ký](../../../workflow/prompt-log.md)
> Phạm vi: yêu cầu, quy tắc nghiệp vụ, dữ liệu, phân quyền và xử lý lỗi của US-PAY-01.

Báo cáo tổng hợp các vấn đề ảnh hưởng đến phát triển chức năng, phân tích và hướng xử lý từ các lượt review/câu trả lời của người dùng. Cột đánh giá là phần AI tự đối chiếu theo yêu cầu người dùng; chưa thay thế việc nhóm đánh giá, xác nhận hoặc phê duyệt nghiệp vụ.

Cột **Đánh giá AI** nhận xét bản phân tích/thiết kế trước khi điều chỉnh:

- **Thiếu:** chưa mô tả hoặc chưa bao phủ đầy đủ.
- **Sai:** cách hiểu hoặc luồng không phù hợp nội dung người dùng xác nhận.
- **Thừa:** thêm thao tác không cần thiết cho chức năng.
- **Đủ:** đã nhận diện hoặc giữ câu hỏi mở phù hợp; không đồng nghĩa nghiệp vụ đã được chốt.

Các yêu cầu được người dùng bổ sung sau được ghi rõ là phần bổ sung. Đánh giá “Thiếu” phản ánh mức bao phủ trước bổ sung, không mặc định AI đã đọc sai đề gốc.

Nguồn đối chiếu:

- [TA-SPEC](../../../requirements/payment-management/spec.md): §1–6; các quy tắc PAY thuộc §5.
- [Đặc tả v1](../v1/sys-us-01-v1.md) và [đặc tả v2](sys-us-01-v2.md).
- [OQ v2](open-questions-v2.md), [sequence v2](../../../design/payment-management/v2/diagrams/seq-us-01-v2.puml).
- Các xác nhận của người dùng tại P-18/P-19 trong [nhật ký](../../../workflow/prompt-log.md).
- [Review v2](../../../review/payment-management/ai-review-04-v2.md) cho các thiếu sót kỹ thuật cuối báo cáo.

Vị trí V2 trong bảng là nơi xử lý hoặc tiếp tục ghi nhận vấn đề trong sys-us-01-v2.md.

## 1. Các vấn đề yêu cầu, phân tích và xử lý

| Vấn đề phát hiện | Vị trí, căn cứ | Loại vấn đề | Phân tích và cách xử lý theo ý kiến của người dùng | Đánh giá phân tích, thiết kế của AI |
|---|---|---|---|---|
| Chưa xác định đúng điểm bắt đầu và ngữ cảnh hợp đồng | TA-SPEC §4.1; V2 §1.3 bước 1–3 | Mơ hồ luồng nghiệp vụ | Bắt đầu khi NVKD bấm Lập bảng thanh toán tại chi tiết hợp đồng. Hợp đồng được lấy từ màn hình hiện tại. | **Sai** — bản đầu bắt đầu quá muộn và bố trí bước chọn hợp đồng không phù hợp quy trình được xác nhận. |
| Kỳ tháng/quý mâu thuẫn với duy nhất theo tháng | TA-SPEC §2 ↔ PAY-01; OQ-01; V2 §1.5 | Mâu thuẫn nghiệp vụ | Kiểm tra khoảng thời gian thanh toán: có tháng 1 thì không lập quý I; có quý II thì không lập tháng 4–6. Kỳ cụ thể vẫn theo cấu hình hợp đồng. | **Đủ** — đã phát hiện đúng mâu thuẫn; quy tắc kiểm tra được hoàn thiện từ câu trả lời của người dùng. |
| Chưa rõ cách xác định bảng giá áp dụng | PAY-01, PAY-03; OQ-US01-01; V2 bước 7 | Mơ hồ dữ liệu đầu vào | Chỉ có một bảng giá hiệu lực tại một thời điểm, gắn với hợp đồng. Hệ thống tự lấy, NVKD không chọn thủ công. | **Thừa** — thao tác chọn bảng giá trong thiết kế trước không cần thiết. |
| Bảng giá đổi giữa xem trước và lưu | PAY-03; OQ-US01-01; V2 bước 11, A11.1 | Mơ hồ thời điểm tính giá | Giá mới đã Active thì dùng giá mới; chưa Active thì dùng giá đang Active. Tính lại và thông báo khi kết quả thay đổi. | **Đủ** — nhận diện đúng điểm cần xác nhận, không tự quyết giữ giá cũ. |
| Chưa có điều kiện về thời điểm tạo bảng giá | V2 bước 7, A7.3, AU4.3; xác nhận P-19 | Thiếu yêu cầu nguồn | Bảng giá phải được lập khi hợp đồng còn hiệu lực. Module thanh toán đọc và xác minh điều kiện nguồn này. | **Thiếu** — bản trước chưa bao phủ điều kiện được người dùng bổ sung. |
| Phạm vi quyền lập và sửa Draft chưa rõ | TA-SPEC §2, §4.1; OQ-US01-03; V2 P1/P4, U2 | Thiếu chính sách phân quyền | NVKD chỉ lập trên hợp đồng được giao, chỉ sửa Draft do mình tạo. Ghi rõ đây là đề xuất theo hướng một người thực hiện. | **Đủ** — phù hợp khi giữ thành OQ/đề xuất, chưa coi là chính sách khách hàng đã duyệt. |
| Chưa xác định đầy đủ trường được sửa | TA-SPEC §1, §4.1; OQ-US01-02; V2 §1.2, U3 | Thiếu ma trận trường | Khóa sản lượng, đơn giá, thông tin hợp đồng và khách hàng. Các trường còn lại chưa mặc định đều được sửa. | **Thiếu** — mô tả chung “được sửa Draft” chưa đủ để thiết kế form và kiểm tra request. |
| Chưa làm rõ việc nhập hay ánh xạ sản lượng, đơn giá | TA-SPEC §4.1, PAY-03; OQ-US01-04; V2 bước 7–8 | Mơ hồ nguồn dữ liệu | Sản lượng và đơn giá lấy từ bảng sản lượng và bảng giá, không nhập thủ công. Hệ thống tính thành tiền. | **Đủ** — hướng đọc nguồn và tính q × p đã có; câu trả lời làm rõ thêm việc cấm nhập đè. |
| Chưa thể hiện rõ điều kiện đủ trường bắt buộc | V2 bước 6, 10–11; AC-US01-33 | Thiếu điều kiện lập bảng | Chỉ cho phép lập khi đủ trường bắt buộc. UI kiểm soát thao tác; server vẫn kiểm tra lại nếu request bỏ qua UI. | **Thiếu** — cần cụ thể hóa điều kiện cho phép thao tác, không chỉ kiểm tra sau khi gửi yêu cầu. |
| Thiếu trường ghi chú | V2 bước 5; AC-US01-27 | Thiếu thông tin biểu mẫu | Bổ sung ghi chú tùy chọn; bỏ trống vẫn hợp lệ. | **Thiếu** — bản trước chưa có nội dung được bổ sung. |
| Phản hồi thành công/thất bại và lỗi trường chưa đầy đủ | V2 bước 13, A4, A11, AU4 | Thiếu phản hồi người dùng | Luôn thông báo kết quả; tô đỏ đúng trường thiếu hoặc vi phạm, nêu lý do và giữ dữ liệu để sửa. Ghi chú trống không bị báo lỗi. | **Thiếu** — trả mã lỗi hoặc thông báo chung chưa đủ giúp người dùng xử lý. |
| Hết phiên hoặc mất quyền trong lúc xem trước | V2 bước 6, A6.1; AC-US01-31 | Thiếu tình huống phân quyền | Trả 401 hoặc 403, thông báo tương ứng, khóa/kết thúc form; không tiếp tục đọc giá/sản lượng sau khi từ chối. | **Thiếu** — trước đó có kiểm tra nhưng thiếu đường phản hồi và kết thúc cho UI. |
| Dòng lỗi chưa chỉ rõ cách tiếp tục | V2 §1.4, §1.6 | Thiếu luồng phục hồi | Mỗi nhánh phải chỉ rõ quay bước nhập nào, thử lại bước nào hoặc kết thúc. | **Thiếu** — “quay lại bước tương ứng” chưa đủ cụ thể để phát triển và kiểm thử. |
| Thuế và làm tròn chưa có quy tắc thống nhất | PAY-03; OQ-US03-03; V2 bước 8/11/U4 | Thiếu quy tắc tính tiền | Người dùng yêu cầu giữ thuế ở OQ để hỏi lại khách hàng. Làm tròn và độ chính xác chưa có câu trả lời mới. | **Đủ** — chưa được tự thêm thuế suất, công thức VAT hoặc cách làm tròn. |
| Chưa rõ dữ liệu rỗng, nhiều bản ghi và đối soát một phần | TA-SPEC §4.1, PAY-02; OQ-US01-04; V2 A8 | Thiếu quy tắc xử lý dữ liệu | Đã xác nhận lấy dữ liệu từ nguồn; cách gộp/tách, phân biệt thiếu với 0 và cấp kiểm tra đối soát vẫn còn mở. | **Đủ** — đã nhận diện đúng phần thiếu; không tự coi dữ liệu thiếu là 0. |
| Chưa rõ hiệu lực đối với kỳ quá khứ hoặc một phần kỳ | PAY-01; OQ-US01-05; V2 bước 2/11 | Mơ hồ điều kiện hiệu lực | Đã rõ kiểm tra trạng thái Active. Điều kiện lập bù hoặc hiệu lực một phần kỳ chưa được trả lời. | **Đủ** — giữ đúng phần chưa rõ, không tự thêm điều kiện cấm lập kỳ quá khứ. |
| Trạng thái sau từ chối không thống nhất | TA-SPEC §3 ↔ PAY-08; OQ-04, OQ-US03-07; V2 U2 | Mâu thuẫn trạng thái | Chưa chốt về Draft ngay hay qua Rejected, ai chuyển và khi nào. Chỉ chặn mở sửa bảng bị từ chối. | **Đủ** — phát hiện đúng mâu thuẫn và không dùng nó để chặn toàn bộ lập mới. |
| Chưa rõ có được lập mới sau khi hủy | TA-SPEC §4.5 ↔ PAY-01; OQ-US05-02; V2 §1.5 | Mơ hồ quy tắc duy nhất | V2 tham chiếu quyết định US-05 đã có: được tạo bảng mới, giữ bảng cũ Cancelled và không dùng lại bảng cũ. | **Đủ** — phân biệt được tạo bảng mới với tái sử dụng bảng đã hủy, có ghi nguồn quyết định. |
| Chưa rõ thời điểm cập nhật Draft khi giá đổi | OQ-US01-01; V2 §1.5 | Thiếu quy tắc đồng bộ | Đã chốt dùng Active khi tính/lưu; chưa chốt có cập nhật ngay mọi Draft đang không được mở hay không. | **Đủ** — không tự thêm cơ chế cập nhật hàng loạt khi chưa được xác nhận. |
| Yêu cầu hiệu năng chưa đủ điều kiện đo | TA-SPEC §6; OQ-US01-06; V2 §4 | Thiếu điều kiện nghiệm thu | Giữ ≤3 giây với <200 dòng; điểm đo, cách đếm dòng và môi trường vẫn cần xác nhận. | **Đủ** — không tự thay ngưỡng hoặc tuyên bố đạt hiệu năng khi chưa đo. |

## 2. Các vấn đề thiết kế kỹ thuật còn cần hoàn thiện

Hai vấn đề dưới đây được phát hiện trong review v2, chưa có quyết định bổ sung riêng của người dùng và chưa được xem là đã xử lý đầy đủ.

| Vấn đề phát hiện | Vị trí | Loại vấn đề | Hướng xử lý cần hoàn thiện | Đánh giá phân tích, thiết kế của AI |
|---|---|---|---|---|
| Thiếu đường tải lại dữ liệu/version sau lỗi thiếu token | V2 AU4; sequence nhánh VERSION_REQUIRED; R04-02 | Thiếu tương tác phục hồi | Phải đóng form để mở lại U1 hoặc có thao tác tải lại representation/version thực sự; không chỉ hiển thị lời nhắc. | **Thiếu** — luồng hiện tại chưa biểu diễn đầy đủ việc lấy token mới. |
| Xác minh đã lưu nhưng chưa mô tả đủ dữ liệu trả về | V2 K1, bước 13/U6; R04-03 | Thiếu luồng dữ liệu | Khi xác minh committed, phải trả id, dữ liệu và version đã lưu, hoặc đọc lại bảng đã xác minh trước khi hiển thị. | **Thiếu** — chỉ trả trạng thái kết quả chưa đủ để hoàn thành phục hồi trên UI. |

Kiểm tra cú pháp hoặc kết xuất PlantUML thành công không chứng minh hai vấn đề kỹ thuật này đã được giải quyết. Báo cáo không kết luận ứng dụng đã được triển khai, kiểm thử tích hợp hoặc đạt hiệu năng.
