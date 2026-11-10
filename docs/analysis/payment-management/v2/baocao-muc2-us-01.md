# Báo cáo mục 2 – Tổng hợp vấn đề phát triển US-PAY-01

> Ngày: 08/11/2026 · Bản đối chiếu: v1 và v2
> AI: Codex / GPT-6 · Prompt: P-20 trong [nhật ký](../../../workflow/prompt-log.md)
> Bổ sung ngày 09/11/2026: review class/state/API theo R05-01..09 · Prompt: P-27.
> Phạm vi: yêu cầu, quy tắc nghiệp vụ, dữ liệu, phân quyền và xử lý lỗi của US-PAY-01.

Báo cáo tổng hợp các vấn đề ảnh hưởng đến phát triển chức năng, phân tích và hướng xử lý từ các lượt review/câu trả lời của người dùng. Cột đánh giá là phần AI tự đối chiếu theo yêu cầu người dùng; chưa thay thế việc nhóm đánh giá, xác nhận hoặc phê duyệt nghiệp vụ.

Phần tự đánh giá đã có được giữ tại mục 1–2. Mục 3 bổ sung nhận xét từ review 05 và để chờ người dùng nhận xét; hướng xử lý tại đó là đề xuất của AI, chưa được ghi thành quyết định của người dùng.

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
- `ai-review-04-v2.md`: nguồn lịch sử của hai thiếu sót tại mục 2, hiện không có trong workspace; lượt bổ sung này giữ nội dung đã tổng hợp, chưa đối chiếu lại được báo cáo nguồn.
- [Review 05 – class, state và API](../../../review/payment-management/ai-review-05-v1.md): nguồn bổ sung tại mục 3.

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

## 3. Bổ sung từ review class, state diagram và API liên quan US-01

Nguồn: [ai-review-05-v1.md](../../../review/payment-management/ai-review-05-v1.md), §4. Giữ ID để người dùng có thể nhận xét từng vấn đề. Ba nhận xét đầu thuộc chính thiết kế v1; sáu nhận xét sau là phần chưa có thiết kế class/state/API v2 tương ứng với yêu cầu mới, không phải kết luận v1 đã sai vì chưa biết thay đổi về sau.

| Vấn đề phát hiện | Vị trí, căn cứ | Loại vấn đề | Hướng xử lý AI đề xuất; tình trạng ý kiến người dùng | Đánh giá của người dùng |
|---|---|---|---|---|
| R05-01 — Chưa đủ căn cứ xác minh kết quả tạo khi mất phản hồi | API v1 E5/E7; class v1 FindByContractPeriod; SYS v1 A15.2; TA-SPEC §4.1, PAY-01, §6 | Thiếu hợp đồng xử lý kết quả lưu; Cao | Gắn lần tạo với định danh có thể tra cứu; phân biệt đã lưu/chắc chắn chưa lưu/còn chưa rõ. Danh sách theo hợp đồng/kỳ chưa đủ nhận diện đúng lần tạo; đọc thấy rỗng chưa chứng minh giao dịch cũ đã kết thúc. Đây là đề xuất kỹ thuật, chưa có ý kiến mới của người dùng. | Chờ bạn nhận xét |
| R05-02 — Chưa có cách xác minh riêng kết quả sửa Draft | API v1 E8/E7/E6; sequence v1 U5/AU5.1; TA-SPEC §4.1, §6 | Thiếu luồng phục hồi cập nhật; TB | Xác minh đúng lần update, gắn bảng, version đầu vào và kết quả thao tác. Không chỉ dựa vào version hiện tại vì có thể đã có lần sửa khác. Liên quan mục 2 về dữ liệu trả sau K1, nhưng đây là khoảng trống của contract API v1. Chưa có ý kiến mới của người dùng. | Chờ bạn nhận xét |
| R05-03 — Chữ ký mở giao dịch chưa thống nhất với sequence | Class v1 IUnitOfWork.Begin dòng 199; sequence v1 dòng 235–239, 325–329 | Không nhất quán contract kỹ thuật; Thấp | Class dùng Begin(): void trong khi sequence nhận beginResult để rẽ lỗi/thành công. Chọn trả kết quả hoặc mô tả bắt/chuyển exception tại service; không mặc định cách dùng exception là sai. Chưa có ý kiến mới của người dùng. | Chờ bạn nhận xét |
| R05-04 — Class/API chưa theo ngữ cảnh chi tiết hợp đồng | Class v1 OpenCreateForm/SelectContract; API v1 E1–E3 ↔ SYS v2 bước 1–4, AC-US01-21; P-18.1 | Chưa chuyển yêu cầu vào thiết kế v2; TB | Người dùng đã xác nhận lập từ chi tiết hợp đồng, không chọn lại. Cần class/API v2 mở form với hợp đồng đang xem và kiểm tra quyền phía server. Bổ sung mức thiết kế cho vấn đề điểm bắt đầu ở mục 1; chưa coi thiết kế đã hoàn thành. | Chờ bạn nhận xét |
| R05-05 — Thiếu contract lấy giá Active, bằng chứng nguồn và phản hồi tính lại | Class v1 IPriceReader; API v1 E3–E5; state v1 T1 ↔ SYS v2 bước 7/11, A7.3/A11.1, AC-US01-09/26/34; PAY-01/03 | Chưa chuyển quy tắc giá vào class/state/API v2; TB | Người dùng đã chốt tự lấy Active gắn hợp đồng, giá đổi trước lưu thì dùng Active, bảng giá được tạo khi hợp đồng còn hiệu lực. Reader/DTO cần dữ liệu kiểm chứng và phản hồi preview mới khi tính lại; không cho giữ giá cũ. Thuế/làm tròn và đồng bộ nền vẫn theo OQ. Chưa có đánh giá của người dùng về nhận xét review này. | Chờ bạn nhận xét |
| R05-06 — Chưa chốt thiết kế ngăn tháng/quý chồng lấn | Class v1 BillingPeriod/FindConflict; state v1 T1; API v1 E3/E5; thiết kế dữ liệu v1 §8 ↔ SYS v2 §1.5, AC-US01-14/30 | Thiếu thiết kế ràng buộc theo quyết định v2; TB | Người dùng đã xác nhận không chồng lấn. Unique theo cùng start/end chỉ chặn khoảng giống nhau, chưa tự chặn tháng 1 với quý I. Cần cơ chế kiểm tra/bảo vệ nguyên tử và phản hồi lỗi trường kỳ, kiểm chứng cả đồng thời. Không tự chốt cách đổi kỳ Draft hoặc chính sách Cancelled từ lượt này. | Chờ bạn nhận xét |
| R05-07 — Ghi chú chưa có đường đi tới lưu trữ và đọc lại | Class v1 PaymentSheet; API v1 PaymentSheetDto/E4/E5 ↔ SYS v2 bước 5/12, AC-US01-27; P-18.2 | Thiếu ánh xạ dữ liệu cho yêu cầu bổ sung; TB | Người dùng đã yêu cầu ghi chú tùy chọn. Cần field tương ứng trong model/request/response/lưu trữ v2; để trống vẫn hợp lệ, không tự đặt giới hạn ký tự. Bổ sung chi tiết thiết kế cho vấn đề ghi chú ở mục 1. | Chờ bạn nhận xét |
| R05-08 — Chưa tách trường nguồn đã khóa khỏi phần changes còn mở | API v1 E8; class v1 PaymentService.Update/PaymentLine ↔ SYS v2 A11.2/AU4.2, AC-US01-32/33; TA-SPEC §1/PAY-03; P-19 | Chưa chuyển phần yêu cầu đã rõ vào contract v2; TB | Người dùng đã khóa sản lượng, đơn giá, hợp đồng, khách hàng và kết quả tính; cần contract từ chối request nhập đè. Các trường khác vẫn OQ-US01-02, không tự cho đổi kỳ. Hệ thống cập nhật đơn giá từ Active không phải sửa tay. Chưa có đánh giá mới về nhận xét review này. | Chờ bạn nhận xét |
| R05-09 — Chưa có contract cho đề xuất quyền theo một người thực hiện | Class v1 IContractReader; API v1 §1/E5/E8 ↔ SYS v2 P1/P4, A6.1, AC-US01-03/31; OQ-US01-03; P-19 | Thiếu thiết kế chi tiết cho phương án quyền; TB | Người dùng yêu cầu ghi rõ đây là đề xuất: chỉ lập hợp đồng được giao, chỉ sửa Draft do mình tạo. Cần chỉ ra dữ liệu kiểm tra quyền và phản hồi khi quyền bị thu hồi; không coi vai trò NVKD là đủ và không tuyên bố khách hàng đã phê duyệt. | Chờ bạn nhận xét |

Mục 3 có 9 nhận xét: 1 Cao, 7 TB, 1 Thấp theo review 05. Các hàng R05-04..09 nối tiếp vấn đề nghiệp vụ tại mục 1 ở mức thiết kế, không được cộng thành sáu vấn đề nghiệp vụ mới độc lập. Chưa sửa class/state/API hay đánh dấu các nhận xét là đã xử lý.
