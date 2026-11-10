# AI Review 05 – Class, state diagram và API của US-PAY-01 (v1)

> Phiên bản được review: v1; đối chiếu bổ sung với yêu cầu US-PAY-01 v2 · Ngày: 09/11/2026
> Vai trò: reviewer · AI: Codex / GPT-6 · Prompt: P-26 trong [prompt-log](../../workflow/prompt-log.md)
> Trạng thái: Báo cáo AI, chưa được nhóm đánh giá; không phải phê duyệt nghiệp vụ hoặc thiết kế.

## 1. Phạm vi và giới hạn

Review phần lập bảng và sửa Draft của US-PAY-01 trong class diagram, state diagram và hợp đồng API. Sequence, đặc tả hệ thống và thiết kế dữ liệu được đọc ở phần liên quan để kiểm tra tính nhất quán. Không review lại toàn bộ US-PAY-02..05, không sửa thiết kế, không ghi thêm vào báo cáo mục 2 của người dùng.

Tại HEAD `a396b32`, class, state và API chỉ có bản v1. Vì vậy, báo cáo tách hai nhóm:

- R05-01..03: khoảng trống kỹ thuật trong chính bộ v1.
- R05-04..09: phần thiết kế chưa có bản v2 để đáp ứng các thay đổi đã ghi trong SYS-US-01 v2. Đây là khoảng trống chuyển tiếp phiên bản, không phải kết luận v1 đã sai vì chưa biết yêu cầu bổ sung về sau.

Kết luận: **Cần chỉnh sửa đối với các khoảng trống kỹ thuật v1; Chưa đủ đầu vào để kết luận class/state/API v2 đáp ứng US-01.** Các sửa đổi tiếp theo thuộc v2; giữ nguyên v1 đã đóng băng.

Báo cáo dùng số 05 vì lịch sử Git còn tên các báo cáo 03-v1 và 04-v2 đã bị xóa; không tái sử dụng số hoặc ghi đè báo cáo 01 đang tồn tại. Chỉ dùng danh sách tên trong lịch sử để chọn số, không coi nội dung báo cáo đã xóa là đầu vào đã đọc.

## 2. Nguồn đã đọc

| Mã | Tài liệu và phần đã đọc | Dùng để |
|---|---|---|
| TA-SPEC | [spec.md](../../requirements/payment-management/spec.md), §1–6 | Căn cứ nghiệp vụ: US-PAY-01, PAY-01..03, giới hạn trạng thái và hai NFR |
| SYS1 | [sys-us-01-v1.md](../../analysis/payment-management/v1/sys-us-01-v1.md), quy trình, nhánh lỗi, OQ và AC liên quan lập/sửa | Kiểm tra thiết kế cùng version |
| SYS2 | [sys-us-01-v2.md](../../analysis/payment-management/v2/sys-us-01-v2.md), §1–4 và mục thay đổi | Nhận diện phần đã thay đổi sau review, không dùng để sửa hồi tố v1 |
| OQ2 | [open-questions-v2.md](../../analysis/payment-management/v2/open-questions-v2.md), OQ-01 và OQ ảnh hưởng US-01 | Phân biệt phần đã rõ với phần còn mở, đặc biệt quyền là đề xuất |
| CLASS1 | [class-v1.puml](../../design/payment-management/v1/diagrams/class-v1.puml), toàn bộ | Entity, service, interface, quan hệ, chữ ký thao tác |
| STATE1 | [state-machine-v1.puml](../../design/payment-management/v1/diagrams/state-machine-v1.puml), toàn bộ; trọng tâm T1/T2 và nhánh mở sửa | Vòng đời, điều kiện tạo và sửa Draft |
| API1 | [04-api-contract-v1.md](../../design/payment-management/v1/04-api-contract-v1.md), §1–3 E1–E8, §5 | Request/response, quyền, lỗi, phục hồi kết quả lưu |
| DD1 | [03-detailed-design-v1.md](../../design/payment-management/v1/03-detailed-design-v1.md), §1–6 | Danh mục tên, mã lỗi, mô tả class và bảng chuyển trạng thái |
| DATA1 | [05-data-design-v1.md](../../design/payment-management/v1/05-data-design-v1.md), §6–14 | Khóa kỳ, snapshot, audit, giao dịch và ánh xạ API |
| SEQ1 | [seq-us-01-v1.puml](../../design/payment-management/v1/diagrams/seq-us-01-v1.puml), các phần mở form, tạo và sửa Draft | Đối chiếu lời gọi, kết quả giao dịch, lỗi lưu |
| SEQ2 | [seq-us-01-v2.puml](../../design/payment-management/v2/diagrams/seq-us-01-v2.puml), phần xem trước và K1 tạo/sửa | Kiểm tra hướng xử lý đã được mô tả ở v2; không coi đây là API contract hoàn chỉnh |
| R01 | [ai-review-01-v1.md](ai-review-01-v1.md), phạm vi, bảng nhận xét và kết luận | Tránh ghi nhận lại cùng một vấn đề như phát hiện mới |
| LOG | [prompt-log.md](../../workflow/prompt-log.md), P-18/P-19 và các mục kiểm chứng P-21..P-25 | Truy vết thay đổi của người dùng và bằng chứng đã ghi |

Đã đọc AGENTS.md, các rule chung và reviewer, skill naming-versioning, ngữ cảnh payment và quy trình minh chứng. Không đọc trực tiếp TA-PDF trong lượt này; các căn cứ nghiệp vụ dưới đây dẫn TA-SPEC. Không dùng nguồn nghiệp vụ trực tuyến, không khảo sát lại mã ứng dụng và không khẳng định thành phần TO-BE đã triển khai.

Đầu vào v2 còn thiếu: `class-v2.puml`, `state-machine-v2.puml`, `03-detailed-design-v2.md`, `04-api-contract-v2.md` và thiết kế dữ liệu v2 để kiểm tra ràng buộc/lưu ghi chú. SYS2 còn dẫn `user-review-us-05.md` hiện không tồn tại; lượt này không xác minh lại quyết định lập sau hủy và không lấy dẫn chiếu thiếu đó làm quyết định mới.

## 3. Bao phủ phần liên quan US-01

| Nội dung | Class/state/API hiện có | Kết quả đối chiếu |
|---|---|---|
| NVKD lập bảng Draft | CLASS1 có controller/service, PaymentSheet; STATE1 T1; API1 E5 | Có mô hình cơ bản; điểm vào màn hình cần chuyển tiếp theo SYS2, R05-04 |
| Active, giá phù hợp, sản lượng Đã đối soát | STATE1 T1; reader chỉ đọc; API1 E4/E5 | Có theo TA-SPEC PAY-01..03; chưa có hợp đồng giá Active và bằng chứng lịch sử theo SYS2, R05-05 |
| Thành tiền = sản lượng × đơn giá, tổng phía server | PaymentLine, RecalculateTotal; API1 E4/E5 không tin tổng từ client | Có; thuế/làm tròn vẫn phụ thuộc OQ-US03-03, không kết luận công thức tiền cuối đã đủ |
| Duy nhất kỳ tháng/quý | BillingPeriod, FindConflict; STATE1 T1; E3/E5 | v1 giữ OQ đúng; chưa có thiết kế v2 chứng minh chống chồng lấn theo quyết định mới, R05-06 |
| Sửa khi Draft, kiểm soát version | Repository.Update có expectedStatus/expectedVersion; STATE1 T2; API1 E8 | Có nền tảng; phạm vi sửa còn OQ-US01-02; phần trường nguồn đã chốt ở SYS2 chưa thành contract v2, R05-08 |
| Quyền theo hợp đồng/người tạo | API1 có xác thực/vai trò, phạm vi quyền để OQ | Không phải thiếu kiểm tra vai trò; còn thiếu thiết kế v2 cho đề xuất được giao/người tạo, R05-09 |
| Ghi chú tùy chọn | Chưa có field trong PaymentSheet và E4/E5/PaymentSheetDto | Chưa chuyển tiếp yêu cầu SYS2, R05-07 |
| Thông báo và lỗi trường | ApiError có message/details; SEQ1 có phản hồi UI | Có khung phản hồi; API1 E2–E4 không liệt kê lại 401/403 nhưng đã có quy ước xác thực chung, không kết luận là không xác thực |
| Audit và lưu nguyên tử | IAuditLog, IUnitOfWork; T1/T2 ghi audit; API1 E5/E8 | Có phương án đáp ứng TA-SPEC §6; chưa có bằng chứng chạy giao dịch thực |
| Kết quả commit chưa rõ | CommitOutcome, RESULT_UNKNOWN; API1 E7 | Chưa đủ contract xác minh tạo/sửa, R05-01/02 |
| Lập ≤3 giây với <200 dòng | Giữ NFR trong SYS1/SYS2, OQ-US01-06 | Chưa đo; render sơ đồ không chứng minh hiệu năng |

### State diagram

STATE1 giữ đúng Draft, PendingApproval, Approved, Rejected, Cancelled theo TA-SPEC §3; T1 có Active/giá/đối soát và audit; T2 có version và trường được phép. Rejected → Draft và điều chỉnh Approved được đánh dấu chờ OQ, không tự coi là luồng đã chốt. Những nhận xét về reject của US-03 đã nằm trong R01-05/06, không ghi lại thành lỗi mới của US-01.

Không yêu cầu thêm trạng thái nghiệp vụ cho mở form, xem trước, lỗi validation hoặc đóng form chưa lưu. Khi có state v2, cần cập nhật điều kiện T1/T2 theo các phần đã rõ trong R05-05/06/08/09; thao tác chỉ tính lại để xem trước chưa được coi là tạo Draft hay ghi audit thay đổi bảng. Căn cứ: TA-SPEC §3, §4.1; SYS2 §1.3, A10/A11.1 và AC-US01-23/25/26.

## 4. Nhận xét bổ sung

Vị trí dòng theo bản đọc ngày 09/11/2026. Mức độ đánh giá ảnh hưởng nếu dùng tài liệu hiện có để triển khai. Các đề nghị về mã thao tác, DTO, lỗi và cơ chế giao dịch là **đề xuất kỹ thuật**, không phải business rule mới của TA-SPEC. Không tự đánh giá nhận xét là Đúng/Sai/Thừa thay nhóm.

### 4.1. Khoảng trống kỹ thuật trong bộ v1

| ID | Vị trí file/mục/dòng | Loại | Mức độ Cao/TB/Thấp | Nhận xét và tác động | Đề xuất/cách kiểm chứng | Căn cứ trang/mục/US/PAY | OQ |
|---|---|---|---|---|---|---|---|
| R05-01 | API1 E5 dòng 102–104, E7 dòng 113–116; CLASS1 dòng 135, 177; SYS1 A15.2 | Thiếu contract phục hồi kết quả tạo | Cao | E5 trả RESULT_UNKNOWN rồi yêu cầu gọi E7, nhưng E7 chỉ trả danh sách theo hợp đồng/kỳ, có thể gồm Cancelled. Chưa có định danh gắn kết với lần create và chưa có kết quả phân biệt đã commit/chắc chắn chưa commit/còn chưa rõ. Danh sách rỗng tại một thời điểm chưa chứng minh giao dịch cũ đã kết thúc; một bảng cùng kỳ cũng chưa chứng minh do request đang kiểm tra tạo ra. Tài liệu chưa đủ để UI quyết định báo thành công hoặc cho gửi lại. Không khẳng định implementation đã xử lý sai vì chưa có implementation. | Bổ sung contract nhận diện lần lưu và điều kiện kết luận ba kết quả; trả id/version/representation của đúng lần tạo hoặc chỉ rõ bước đọc tiếp. Có thể dùng id bảng cấp trước hoặc mã thao tác, tùy DB/driver; không bắt buộc một công nghệ cụ thể. Kiểm chứng: commit xong mất response; đọc khi giao dịch còn đang xử lý; có bảng cũ Cancelled; một request khác cùng kỳ thắng. Không được suy từ danh sách rỗng thành chắc chắn chưa lưu. | SYS1 §1.4 A15.2 và AC-US01-16; TA-SPEC §4.1, §5 PAY-01, §6. Cơ chế nhận diện thao tác: không có căn cứ bắt buộc trong đặc tả, là đề xuất kỹ thuật hoàn thiện phục hồi đã chọn. | OQ-01/OQ-US05-02 ảnh hưởng tập kết quả; xác minh commit là quyết định kỹ thuật cần hoàn thiện |
| R05-02 | API1 E8 dòng 123–126, E7 dòng 115–116; SEQ1 dòng 349–364; SYS1 AU5.1 | Thiếu contract phục hồi kết quả sửa | TB | E8 có RESULT_UNKNOWN; SYS1 yêu cầu xử lý như A15.2. Tuy nhiên E7 được mô tả chỉ phục vụ xác minh tạo, còn E6 chỉ đọc representation hiện tại. Chưa có cách xác định lần update đang kiểm tra đã commit hay bị một lần sửa khác thay thế. Chỉ thấy version tăng chưa đủ để gán kết quả cho đúng request; UI thiếu căn cứ cho phép lưu lại hoặc báo U6. | Định nghĩa riêng hoặc dùng chung cơ chế kiểm tra kết quả cho update, gắn paymentId, lần thao tác và version đầu vào/kết quả; cho biết dữ liệu trả là kết quả thao tác hay dữ liệu hiện tại. Kiểm chứng mất response sau commit, không commit và có cập nhật kế tiếp bởi một phiên khác. Chưa xác định thì giữ trạng thái chưa rõ. | TA-SPEC §4.1, §6; SYS1 §1.5 AU5.1; API1 E8. Đây là đề xuất kỹ thuật, không thêm yêu cầu dùng Idempotency-Key từ PAY-04. | Không phụ thuộc việc chốt trường nào được sửa; nội dung changes vẫn OQ-US01-02 |
| R05-03 | CLASS1 IUnitOfWork.Begin dòng 199; SEQ1 dòng 235–239 và 325–329 | Không nhất quán chữ ký và kết quả lỗi | Thấp | Class khai báo Begin(): void, nhưng sequence chờ beginResult rồi rẽ error/OK. Chưa mô tả adapter bắt exception để tạo beginResult. Vì vậy hai tài liệu chưa chỉ cùng một contract lỗi mở giao dịch; không đủ căn cứ nói phương án dùng exception là sai. | Chọn trả kết quả hoặc giữ void và mô tả bắt/chuyển exception tại service; đồng bộ class/sequence và PERSISTENCE_ERROR. Kiểm chứng khi không mở được giao dịch: trả lỗi, không ghi dữ liệu/audit, không commit. | SEQ1 A15.1/AU5.1; TA-SPEC §4.1, §6 là yêu cầu liên quan. Kiểu trả về/exception không có căn cứ trong đặc tả, là đề xuất kỹ thuật. | – |

### 4.2. Khoảng trống chuyển tiếp từ yêu cầu v2 sang class/state/API

Các hàng dưới không kết luận bản v1 phải chứa quyết định v2. Chúng chỉ rõ phần còn thiếu trước khi dùng bộ thiết kế để triển khai chức năng đã được người dùng sửa.

| ID | Vị trí file/mục/dòng | Loại | Mức độ Cao/TB/Thấp | Nhận xét và tác động | Đề xuất/cách kiểm chứng | Căn cứ trang/mục/US/PAY | OQ |
|---|---|---|---|---|---|---|---|
| R05-04 | CLASS1 dòng 127–129, 144–146, 215–217; API1 E1–E3 dòng 61–63, 86–88 ↔ SYS2 bước 1–4, AC-US01-21 | Chưa chuyển tiếp điểm vào và ngữ cảnh hợp đồng | TB | Class/API hiện bắt đầu bằng danh sách rồi chọn hợp đồng; yêu cầu hiện tại bắt đầu từ chi tiết hợp đồng và tự lấy contractId. Chưa có class/API v2 cho form theo ngữ cảnh này. Dùng nguyên E1–E3 cho luồng mới sẽ buộc chọn lại hoặc để trống thông tin hợp đồng. | Trong v2, mô tả mở form với contractId từ ngữ cảnh, trả hợp đồng/khách hàng cố định và cấu hình kỳ. Giữ xác minh phía server; không coi contractId do UI gửi là bằng chứng quyền. Không bắt buộc xóa endpoint v1. Kiểm chứng mở từ hợp đồng A: form của A, không có bước chọn hợp đồng B. | SYS2 §1.1, §1.3 bước 1–4; P-18.1. TA-SPEC §4.1 xác lập lập theo hợp đồng/kỳ; cách vào từ chi tiết là thay đổi của người dùng. | OQ-US01-03 cho phạm vi quyền; không chặn việc bỏ chọn lại hợp đồng |
| R05-05 | CLASS1 IPriceReader dòng 219–221; API1 E3/E4/E5 dòng 88–104; STATE1 T1 dòng 19 ↔ SYS2 bước 7/11, A7.3/A11.1, AC-US01-09/26/34 | Chưa chuyển tiếp contract giá Active và bằng chứng nguồn | TB | Reader hiện liệt kê/đọc bảng giá theo id do request chọn. Chưa có contract v2 trả đúng bảng giá Active gắn hợp đồng, phiên bản và bằng chứng bảng giá được tạo khi hợp đồng còn hiệu lực. E5 cũng chưa định nghĩa phản hồi tính lại/xem trước mới khi Active đổi. Dùng contract cũ có thể lấy lại id giá cũ hoặc không thể kiểm tra điều kiện lịch sử đã bổ sung. R01-03 đã nêu chuyện chọn giá; hàng này bổ sung thiếu hụt tích hợp và phản hồi sau khi SYS2 đã làm rõ. | Thiết kế reader chỉ đọc với dữ liệu kiểm chứng, thống nhất request không có quyền chọn giữ giá cũ. Giá Active đổi trước lưu: chưa ghi, trả preview/ngữ cảnh mới và thông báo để người dùng kiểm tra rồi lưu lại. Sai/thiếu bằng chứng lịch sử phải có kết quả rõ; không suy từ Active hiện tại. Đồng bộ điều kiện tạo/sửa trong state v2. Kiểm chứng giá mới Active/chưa Active, không có/nhiều giá Active và không đủ bằng chứng nguồn. | TA-SPEC §1, PAY-01/PAY-03; SYS2 §1.3 bước 7/11, A7.3/A11.1; P-18.1/3, P-19. Hình dạng DTO/mã lỗi là đề xuất kỹ thuật. | OQ-US01-01 còn đồng bộ nền; OQ-US03-03 còn thuế/làm tròn; không tự mở CRUD giá |
| R05-06 | CLASS1 BillingPeriod/FindConflict dòng 33–41, 178; STATE1 T1 dòng 19; API1 E3/E5; DATA1 §8 dòng 149–156 ↔ SYS2 §1.5, AC-US01-14/30 | Chưa có thiết kế v2 chống kỳ chồng lấn | TB | Bộ v1 giữ OQ-01 là đúng theo đầu vào v1. Sau xác nhận không chồng lấn, chưa có class/API/data v2 chốt cách nhận diện khoảng thanh toán và bảo đảm nguyên tử. Hai phương án unique theo bộ start/end trong DATA1 chỉ chặn hai khoảng giống nhau, không tự chặn tháng 1 với quý I. Không kết luận v1 đã chọn sai phương án vì §8 vẫn là các lựa chọn chờ xác nhận. | V2 cần mô tả kiểm tra giao nhau theo cùng hợp đồng, kết quả lỗi trả cho trường kỳ và cơ chế bảo vệ khi hai request đồng thời. Có thể chọn chiếm tháng hoặc cơ chế khoảng thời gian tương đương, giải thích lựa chọn. Đồng bộ guard tạo và trường hợp đổi kỳ nếu sau này được cho phép. Kiểm chứng tháng 1/quý I và quý II/tháng 5 cả tuần tự lẫn đồng thời; tháng 1/tháng 2 không bị chặn nếu đúng cấu hình. | TA-SPEC §2 ↔ PAY-01; quyết định P-18.3 tại SYS2 §1.1/1.5 và OQ2 OQ-01; cơ chế nguyên tử là đề xuất kỹ thuật. | OQ-01 đã có quyết định v2; thay đổi kỳ sau lưu còn OQ-US01-02; không xác nhận lại chính sách Cancelled trong lượt này |
| R05-07 | CLASS1 PaymentSheet dòng 48–68; API1 PaymentSheetDto dòng 29–45, E4/E5 dòng 89/99 ↔ SYS2 bước 5/12, AC-US01-27 | Chưa có ánh xạ dữ liệu ghi chú tùy chọn ở v2 | TB | Chưa có thuộc tính lưu ghi chú trong model, request và response hiện có; cũng chưa có thiết kế dữ liệu v2. Do đó chưa có đường đi đầy đủ từ nhập ghi chú tới lưu/đọc lại. Đây là thiếu chuyển tiếp yêu cầu bổ sung, không phải yêu cầu gốc TA-SPEC đã bị bỏ sót. | Bổ sung ánh xạ field tương ứng trong model/DTO/lưu trữ v2, ghi rõ tùy chọn; phản hồi đọc và lưu trả lại nội dung đã lưu. Không tự đặt giới hạn ký tự như quy tắc đã duyệt. Kiểm chứng bỏ trống vẫn tạo được; có nội dung thì lưu, đọc lại và audit phản ánh dữ liệu thực. | SYS2 §1.2 biểu mẫu, §1.3 bước 5/12, AC-US01-27; P-18.2. TA-SPEC §4.1/§6 là yêu cầu liên quan. | Không lấy ghi chú làm trường bắt buộc; các trường khác còn OQ-US01-02 |
| R05-08 | API1 E8 dòng 123–126; CLASS1 PaymentService.Update dòng 150 và PaymentLine; SYS2 A11.2/AU4.2, AC-US01-32/33 | Chưa chuyển tiếp phần trường nguồn đã được khóa | TB | E8 để toàn bộ changes là Blocked by OQ-US01-02; request tạo không nhận tổng/dòng đã là điểm đúng. Tuy nhiên SYS2 đã làm rõ sản lượng, đơn giá, hợp đồng, khách hàng và kết quả tính không cho nhập đè, trong khi các trường còn lại vẫn mở. Chưa có contract v2 tách phần đã rõ khỏi phần chưa rõ, hay phản hồi khi request cố ghi đè. Không được hiểu khóa sửa tay là cấm hệ thống cập nhật từ giá Active. | Trong v2, mô tả allowlist cho phần đã chốt và xử lý payload chứa field chỉ đọc, kèm mã lỗi/message/field khi cần. Các trường chưa rõ tiếp tục Blocked, không tự cho phép đổi kỳ hoặc sửa dòng. Kiểm chứng bypass UI để gửi q/p/hợp đồng/khách hàng/tổng khác nguồn: bị từ chối, không ghi; server đồng bộ giá Active vẫn hợp lệ. | TA-SPEC §1, §4.1, PAY-03; SYS2 §1.2, A11.2/AU4.2, AC-US01-32/33; P-19. Mã lỗi/schema cụ thể là đề xuất kỹ thuật. | OQ-US01-02 đã rõ khóa trường nguồn, còn ma trận trường khác; OQ-US01-04 còn ánh xạ dữ liệu |
| R05-09 | CLASS1 IContractReader dòng 215–217; API1 §1 dòng 18/24, E5 dòng 98, E8 dòng 122 ↔ SYS2 P1/P4, A6.1, AC-US01-03/31 | Chưa có contract v2 cho đề xuất quyền theo một người thực hiện | TB | API1 đã yêu cầu xác thực/vai trò và để quyền đối tượng ở OQ; không có căn cứ nói toàn bộ API bỏ phân quyền. Phần v2 đề xuất chỉ lập trên hợp đồng được giao, chỉ sửa Draft do mình tạo chưa có contract class/API tương ứng về dữ liệu kiểm tra quyền và phản hồi khi quyền bị thu hồi lúc preview/lưu. Nếu dùng vai trò NVKD như điều kiện duy nhất thì chưa thực hiện đề xuất đang trình xác nhận. | Thiết kế v2 cần chỉ rõ nguồn chứng minh được giao, CreatedBy cho sửa và kiểm tra lại mỗi request; 401/403 có thông báo như SYS2. Gắn nhãn đề xuất/cần xác nhận cho phạm vi quyền, không tuyên bố khách hàng đã duyệt hoặc mỗi hợp đồng chỉ có một người được giao. Kiểm chứng mất phiên/mất quyền khi preview: dừng, không tiếp tục đọc giá/sản lượng; thử sửa Draft người khác theo phương án được đề xuất. | TA-SPEC §2/§4.1 xác lập NVKD; SYS2 §1.1/1.2, A6.1, AC-US01-03/31; P-19. Quyền được giao/người tạo là đề xuất của người dùng, chưa phải quy tắc gốc. | OQ-US01-03 vẫn cần xác nhận đề xuất |

Tổng cộng **9 nhận xét: 1 Cao, 7 TB, 1 Thấp**. Không đưa vấn đề tạo version sớm, đặt tên báo cáo hay cách trình bày vào bảng lỗi phát triển.

## 5. Những điểm còn mở, không tự kết luận là lỗi thiết kế

- Thuế, độ chính xác và làm tròn: OQ-US03-03. Giữ phần tính tiền cuối chờ khách hàng; không thêm VAT mặc định. TA-SPEC PAY-03 chỉ xác lập phép nhân.
- Cách gộp/tách dòng, nguồn rỗng khác 0, đối soát một phần và sản lượng đổi giữa preview/lưu: OQ-US01-04. Cấu trúc tham chiếu nguồn đơn trị đã được nêu trong R01-15; không ghi lại như phát hiện mới.
- Rejected về Draft, ai chuyển và khi nào: OQ-04/OQ-US03-07. Chỉ chặn nhánh mở sửa bảng bị từ chối, không chặn toàn bộ tạo mới.
- Hiệu lực với kỳ quá khứ/một phần kỳ: OQ-US01-05; cách đo ≤3 giây với <200 dòng: OQ-US01-06.

Căn cứ và trạng thái các câu hỏi trên: SYS2 §2, OQ2; không đóng OQ trong lượt review này.

## 6. Kiểm chứng và phần chưa kiểm được

| Kiểm tra | Lệnh/cách thực hiện | Kết quả |
|---|---|---|
| Cú pháp class/state v1 | `java -jar C:/Users/phong/.vscode/extensions/jebbs.plantuml-2.18.1/plantuml.jar -charset UTF-8 -checkonly docs/design/payment-management/v1/diagrams/class-v1.puml docs/design/payment-management/v1/diagrams/state-machine-v1.puml` | Exit 0; PlantUML 1.2024.3, Java 27.0.1.0.3 |
| Render lại class/state | Cùng jar và hai file, dùng `-tsvg -o <TEMP>/codex-us01-review05` | Exit 0; tạo 2 SVG trong TEMP, không ghi lại SVG v1 |
| SVG trong repo so với nguồn hiện tại | Python 3.12.15, parse XML, so danh sách nội dung phần tử text với SVG vừa render | Class 175/175 và state 48/48 text giống nhau; chưa xem bằng mắt bố cục |
| Cấu hình workspace | Python 3.12.15 `-X utf8 scripts/verify_agent_config.py` | FAIL 4 checks có sẵn: README dẫn thiếu README review; prompt-log dẫn thiếu 03 v2; README review không tồn tại; hai tên file analysis/v2 không theo quy ước. Không sửa ngoài phạm vi review |
| Mã ứng dụng, kiểm thử API/giao dịch, hiệu năng | Không thực hiện | Không có kết luận đạt chức năng, atomicity hoặc NFR từ kiểm tra tài liệu |

Kiểm tra cú pháp/render chỉ chứng minh nguồn PlantUML xử lý được. Không chứng minh các khoảng trống contract đã được xử lý. Sau khi ghi báo cáo, kiểm tra liên kết/bảng Markdown, ID, diff và hash các đầu vào được ghi tại P-26.

## 7. Bàn giao

Người phụ trách đánh giá từng R05-kk trước khi đưa thay đổi vào v2. Chưa có đánh giá của nhóm hoặc xác nhận khách hàng trong báo cáo này. Lượt này chỉ tạo báo cáo mới và bổ sung nhật ký; giữ nguyên class, state, API, sequence, OQ và báo cáo mục 2.

Ưu tiên hoàn thiện contract xác minh kết quả tạo/sửa; sau đó lập class/state/API v2 cùng version với SYS2 và SEQ2, bảo đảm truy vết được giá Active, chồng lấn kỳ, ghi chú, trường chỉ đọc và đề xuất quyền. Chỉ phần OQ đã được trả lời mới chuyển thành quyết định; các phần còn mở tiếp tục được đánh dấu.
