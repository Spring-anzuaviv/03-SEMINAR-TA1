# Review lại US-PAY-01 và đối chiếu mâu thuẫn nghiệp vụ (v1)

> Phiên bản được review: v1 · Ngày: 08/11/2026 · Người phụ trách: Chờ nhóm điền
> Đầu vào: TA-SPEC §1–6; SYS-US-01 v1; sequence/OQ v1; nhật ký P-17.
> AI: Codex / GPT-6 · Prompt thực tế và kiểm chứng: §7 bên dưới.
> Bản kiểm tra: HEAD `8913b86`, nhánh `v2-us-01`; nội dung ba file US-01 khớp commit `ea10323`.
> Kết luận: **Cần chỉnh sửa / Chờ xác nhận nghiệp vụ**. Design Pending Approval.

## 1. Phạm vi, nguồn và giới hạn

Review chức năng **lập bảng và sửa Draft của US-PAY-01**, gồm tính nhất quán spec/sequence/OQ và các mâu thuẫn của đề TA ảnh hưởng chức năng này. Tên nhánh `v2-us-01` không làm các tài liệu v1 thành v2. Không tạo thiết kế v2 hoặc tự phê duyệt câu trả lời nghiệp vụ.

| Mã nguồn | File / phần đã đọc | Dùng để |
|---|---|---|
| TA-SPEC | [spec.md](../../requirements/payment-management/spec.md), §1–6, d.1–84 | Căn cứ nghiệp vụ. Nội dung người dùng dán trong yêu cầu phù hợp phần nghiệp vụ này. |
| SYS01 | [sys-us-01-v1.md](../../analysis/payment-management/v1/sys-us-01-v1.md), toàn bộ 167 dòng | Đặc tả được review: bước 1–16, U1–U6, nhánh lỗi và 26 AC. |
| SEQ01 | [seq-us-01-v1.puml](../../design/payment-management/v1/diagrams/seq-us-01-v1.puml), toàn bộ 373 dòng; SVG và PNG kết xuất lại từ cùng nội dung | Tương tác, guard, vòng lặp và giao dịch. |
| OQ1 | [open-questions-v1.md](../../analysis/payment-management/v1/open-questions-v1.md), toàn bộ 52 dòng | Tình trạng câu hỏi chung và 11 OQ liên quan US-01. |
| P17 | [prompt-log.md](../../workflow/prompt-log.md), mục P-17 | Người dùng đã yêu cầu bắt đầu khi bấm nút, chọn dữ liệu sau đó và tiếp tục ở v1. Đây là xác nhận về trình tự tương tác, không phải xác nhận giá/thuế/quyền/kỳ. |
| AS-IS | [Program.cs](../../../src/Qtkd.Api/Program.cs), [ContractService.cs](../../../src/Qtkd.Api/Services/ContractService.cs), [Contract.cs](../../../src/Qtkd.Api/Models/Contract.cs), [Qtkd.Api.csproj](../../../src/Qtkd.Api/Qtkd.Api.csproj) | Bốn file hiện có của ứng dụng: demo hợp đồng .NET 8/in-memory; chưa có phần triển khai payment trong thư mục này. Không dùng logic hợp đồng làm quy tắc thanh toán. |
| PROC | [AGENTS.md](../../../AGENTS.md); [naming-versioning](../../../skills/naming-versioning/SKILL.md); [workflow](../../workflow/README.md); [sources.md](../../requirements/payment-management/sources.md) | Phạm vi review, đặt tên, nguồn và bằng chứng. |
| PUML | [PlantUML Sequence Diagram](https://plantuml.com/sequence-diagram), Grouping message / Message to Self / Declaring participant | [THAM KHẢO] Cú pháp và cách thể hiện tương tác, không bổ sung nghiệp vụ. |

`git diff 5d5161e HEAD -- src` không có thay đổi. Thay đổi US-01 đang review nằm ở tài liệu/PlantUML/SVG/OQ/nhật ký, không phải mã thực thi payment. Không suy luận các lỗi tài liệu dưới đây đã xảy ra trong ứng dụng.

TA-PDF chưa được đọc trực tiếp trong lần này; lần thử trước không có thư viện `pypdf`. Dẫn nguồn nghiệp vụ bằng TA-SPEC; ánh xạ trang TA-PDF (tr.1: §1–3; tr.2: §4–5; tr.3: §6) chỉ theo sổ nguồn. Chưa có HLD/LLD, class/state, hợp đồng API, thiết kế dữ liệu và ma trận truy vết v1 đầy đủ; **chưa đủ đầu vào review toàn bộ module**, nhưng đủ để review US-01 theo yêu cầu. Không coi những tài liệu ngoài phạm vi chưa được làm là lỗi mới của US-01.

Báo cáo R02 của lượt trước không có trong checkout hiện tại; nội dung nhận xét vẫn có trong lịch sử chat và P-17 nhắc báo cáo đó. Dùng số 03 để không tái sử dụng R02. Đối chiếu thay đổi với commit `5d5161e` (bản US-01 trước sửa), không tuyên bố đã đọc lại một file R02 không tồn tại tại HEAD.

## 2. Các điểm thiết kế cần chỉnh tiếp

| ID | Vị trí file/mục/dòng | Loại | Mức độ | Nhận xét và tác động | Đề xuất / cách kiểm chứng | Căn cứ | OQ |
|---|---|---|---|---|---|---|---|
| R03-01 | SEQ01 d.112–203, 228–231, 276–279, 302–321; SYS01 A14 d.87 và AU4 d.107 | Thiếu đường quay lại trong tương tác | TB | Vòng chọn dữ liệu kết thúc ở d.203, trước yêu cầu lưu. Khi lưu báo A14/A10, sơ đồ chỉ ghi “quay bước chọn tương ứng” rồi kết thúc nhánh; không có vòng lặp bao ngoài để thực hiện lại lựa chọn và lưu trong cùng use case. Luồng sửa cũng chỉ có một lượt U3/U4, dù AU4 quy định quay U3. Chưa biểu diễn trọn hành vi phục hồi đã mô tả trong spec. | Bao phần nhập/xem trước/lưu bằng vòng lặp thích hợp, hoặc chỉ rõ tương tác được gọi lại và điều kiện kết thúc. Khi lỗi đầu vào thì quay nhập; khi commit thành công thì kết thúc; khi kết quả commit chưa rõ phải dừng gửi lại để xác minh. Kiểm chứng bằng hai trace: A14 → đổi kỳ → xem trước → lưu thành công; AU4 → sửa nội dung → lưu thành công. Không biến mọi lỗi thành retry tự động. | [ĐẶC TẢ] TA-SPEC §4.1. [ĐỀ XUẤT KỸ THUẬT] Vòng phục hồi theo SYS01 A14/AU4, AC-US01-04/17/24. [THAM KHẢO] PUML Grouping message: thông báo không tự tạo vòng lặp. | Nội dung sửa theo OQ-US01-02; cấu trúc quay lại có thể chỉnh độc lập |
| R03-02 | SEQ01 d.138, 164–166, 192–195; SYS01 A10 d.84 | Guard thử lại chưa bao phủ giữ nguyên lựa chọn | TB | `preview` nằm trong `opt` chỉ khi chưa chọn hoặc đổi bảng giá. Ví dụ đã chọn bảng giá A, reader bị lỗi tạm thời, form giữ nguyên lựa chọn theo A10; khi thử lại cùng A thì cả “chưa chọn” và “đổi” đều sai. Sequence chưa có sự kiện gửi lại cho lựa chọn không đổi. Guard nhập kỳ cũng có cùng giới hạn nếu lỗi tải giá và thử lại cùng kỳ. | Mô tả sự kiện thử lại chủ động hoặc điều kiện cần tải/tính lại, không buộc người dùng đổi dữ liệu đúng để vượt guard. Lựa chọn đơn giản: nhận yêu cầu xem trước/thử lại với selection hiện tại và kiểm tra đủ dữ liệu. Kiểm chứng: lần đầu SOURCE_UNAVAILABLE, nguồn hoạt động lại, người dùng thử lại cùng hợp đồng/kỳ/giá và nhận preview. | [ĐỀ XUẤT KỸ THUẬT] Không có căn cứ trong TA về nút thử lại cụ thể; yêu cầu giữ lựa chọn/gửi lại do SYS01 A10, AC-US01-13 và tương tác hiện tại đặt ra để thực hiện US-PAY-01 [TA-SPEC §4.1]. | Không cần OQ nghiệp vụ mới |
| R03-03 | SEQ01 d.112, 186–190, 203–209; SYS01 bước 12–13 d.69–70, A13 d.86 | Chưa rõ sự kiện điều khiển giao diện | TB | UI tự gán `previewAccepted=true` theo nhánh “NVKD chấp nhận dữ liệu hiển thị”, nhưng chưa có thông điệp thao tác cụ thể để UI biết việc đó. “Kiểm tra kết quả” chưa chỉ rõ là đọc màn hình hay một sự kiện gửi vào hệ thống. Cờ này kết thúc vòng nhập trước khi bấm Lưu nháp; từ đó không còn nhánh đóng/đổi lựa chọn trong khoảng trước khi lưu, dù A13 cho phép đóng trước lưu. | Gắn điều kiện thoát với sự kiện UI cụ thể. Phương án đơn giản: cho đổi/đóng form cho đến khi NVKD bấm Lưu nháp; sự kiện này chuyển sang kiểm tra lưu. Nếu thật sự cần nút chấp nhận riêng, phải mô tả rõ như đề xuất tương tác, không mặc định đó là nghiệp vụ gốc. Kiểm chứng: xem preview → chưa bấm lưu → đổi giá hoặc đóng form, không tạo Draft. | [ĐẶC TẢ] TA-SPEC §4.1 không có thao tác xác nhận riêng. [QUYẾT ĐỊNH ĐÃ XÁC NHẬN – tương tác] P-17: bắt đầu từ nút lập. [ĐỀ XUẤT KỸ THUẬT] SYS01 A12/A13, AC-US01-24/25; PUML Message to Self. | Không cần OQ nghiệp vụ mới |
| R03-04 | SEQ01 d.318–321; SYS01 AU1/AU2/AU4 d.105–107 | Gộp phản hồi lỗi có cách xử lý khác nhau | TB | NOT_FOUND, FORBIDDEN, INVALID_STATE, lỗi lưu trữ, lỗi nội dung và thiếu version cùng đi tới “Giữ form, sửa dữ liệu hoặc tải lại version [AU4]”. Nếu bảng vừa bị hủy/trình duyệt hoặc người dùng mất quyền, sửa trường hay chỉ lấy token mới không làm bảng đủ điều kiện sửa Draft. Spec đã phân biệt AU1/AU2/AU4 nhưng UI trong sequence chưa phân biệt. | Tách phản hồi theo nhóm: lỗi trường → cho sửa; thiếu token → tải representation; không có bảng/không quyền/không Draft → thông báo không thể tiếp tục lưu sửa theo điều kiện hiện tại. Có thể giữ nội dung nhập cục bộ để người dùng xem, nhưng không mô tả là tiếp tục sửa bảng hợp lệ. Kiểm chứng: mở Draft → giao dịch khác hủy/trình → bấm lưu → bị từ chối và UI phản ánh trạng thái hiện tại. | [ĐẶC TẢ] TA-SPEC §3, §4.1, §4.5; SYS01 P4, AU1/AU2. [ĐỀ XUẤT KỸ THUẬT] Cách phản hồi UI cụ thể; không tự chốt mở sửa Rejected. | OQ-04/OQ-US03-07 vẫn mở cho Rejected |

Các nhận xét này là thiếu rõ/thiếu nhất quán trong mô hình tương tác, không phải lỗi cú pháp PlantUML. Không có nhận xét mức Cao mới được chứng minh trong phạm vi tài liệu đã đọc.

Gợi ý kỹ thuật bổ sung, không phải điều kiện nghiệp vụ mới:

- SEQ01 d.250 và 340 không nêu `paymentId` trong lời gọi audit, khác chữ ký ở bản trước. Khi lập hợp đồng audit, nên chỉ rõ định danh bảng trong tham số hoặc payload để truy ngược sự kiện về đúng bảng. Hiện chưa có hợp đồng dữ liệu audit nên không kết luận bản triển khai làm mất định danh [TA-SPEC §6 gạch 1; ĐỀ XUẤT KỸ THUẬT].
- Sơ đồ giảm lồng từ 15 xuống 8 mức nhưng tăng từ 2180 × 6140 lên 2559 × 7988 px. Có thể tách create/update hoặc phân trang khi xuất; đây là cải tiến khả năng đọc, không phải lỗi UML hay nghiệp vụ [naming-versioning §3; ĐỀ XUẤT KỸ THUẬT].

## 3. Đối chiếu các nội dung của lượt review trước

Bảng ghi **thay đổi quan sát được**, không thay nhóm đánh giá Đúng/Sai/Thừa cho các nhận xét R02.

| Nội dung đã nêu | Thay đổi trong bản hiện tại | Phần còn lại |
|---|---|---|
| R02-01: ảnh hưởng OQ thuế/làm tròn mâu thuẫn | OQ1 d.20 và SYS01 d.119 hiện cùng ghi đề xuất chưa xác nhận, chặn công thức cuối, không chặn mở form/công thức nhân. | Chưa có câu trả lời nghiệp vụ OQ-US03-03; không phải đã duyệt VAT. |
| R02-02: dữ liệu tính lại đem lưu/audit | SYS01 U4/U5 và SEQ01 d.313–340 dùng `validatedCandidate` để lưu/audit/response. | Chính sách trường sửa/tính lại chờ OQ-US01-02/OQ-US03-03. |
| R02-03: nguồn lấy version | Create/openDraft/update đều trả version; AU4 có thiếu token; AC-US01-19 cập nhật. | Chưa có API contract thực thi; không cần tiếp tục báo thiếu token như bản trước. |
| R02-04: guard lỗi có thể chồng nhau | Auth dùng điều kiện loại trừ; các kết quả dùng một `result.code`; chú thích d.38–40 nói rõ ưu tiên lỗi. | Vòng lặp/sự kiện thử lại là vấn đề khác tại R03-01..03. |
| R02-05: `ref` dùng làm ghi chú | Bản hiện tại dùng note cho phần OQ; không còn `ref` đó. | Không yêu cầu tạo Interaction giả chỉ để dùng `ref`. |
| R02-06: nguồn đổi giữa đọc và lưu | Có bước 14 tái kiểm tra; OQ-US01-01/04/05 và AC-US01-26 đã bổ sung chính sách nguồn đổi. | Đã ghi nhận đúng là OQ; chưa được tự chọn giữ số cũ/tính lại. |
| R02-07: commit không rõ kết quả | Tách committed/definitelyNotCommitted/unknown cho cả create/update; A15.2 không tự retry. | Cơ chế xác minh cụ thể chờ lựa chọn DB/driver, là phần kỹ thuật còn phải thiết kế. |
| R02-08: sơ đồ khó đọc | Có UI và các giai đoạn, giảm độ lồng. | Hình vẫn dài hơn; gợi ý tách/phân trang, không coi là lỗi chặn nghiệp vụ. |

## 4. Conflict và điểm chưa rõ của đề TA ảnh hưởng lập bảng

Các phương án sau là **đề nghị để người phụ trách chọn/xác nhận**, không phải business rule đã duyệt. Giữ ID OQ đang có; reviewer không sửa bảng OQ hoặc đóng câu hỏi.

| OQ / loại | Căn cứ mọi phía | Vấn đề cần giải quyết cho US-01 | Lựa chọn cần xác nhận và ảnh hưởng |
|---|---|---|---|
| **OQ-01 — Mâu thuẫn trực tiếp** | TA-SPEC §2 d.27: kỳ tháng hoặc quý ↔ §5 PAY-01 d.71: mỗi hợp đồng một bảng mỗi tháng | Không thể chốt một bảng quý có vi phạm quy tắc theo tháng không; phạm vi trùng/chồng lấn là gì. | A: duy nhất theo kỳ cấu hình và quy định cách xử lý chồng lấn; B: duy nhất theo tháng và xác định quý biểu diễn ra sao. Hỏi thêm khi đổi cấu hình kỳ đã có bảng. Chặn bước 7/14/15, khóa duy nhất, AC-US01-06/14. Không tự chọn A hoặc B. |
| **OQ-04 + OQ-US03-07 — Mâu thuẫn trực tiếp và thiếu bước chuyển** | TA-SPEC §3 d.36–37: từ chối → Rejected ↔ §5 PAY-08 d.78: từ chối → Draft | Tác động mở sửa bảng từng bị từ chối, không chặn lập mới. | A: từ chối trả Draft; B: có Rejected rồi chuyển Draft qua một sự kiện cần xác nhận. Nếu B: ai kích hoạt, mở form hay lưu thành công, lỗi/thoát thì trạng thái gì? Audit chuyển trạng thái theo §6. Chặn U2 đối với Rejected, AC-US01-18. |
| **OQ-US05-02 — Mơ hồ giữa duy nhất và lập lại** | TA-SPEC §4.5 d.64–65: Cancelled không dùng lại ↔ PAY-01 d.71: một bảng mỗi tháng | Không dùng lại bảng đã hủy không tự trả lời có được tạo bảng khác cùng kỳ không. | A: Cancelled vẫn chiếm kỳ; B: cho bảng mới, bảng cũ giữ Cancelled. Chọn nhất quán với OQ-01; ảnh hưởng phạm vi duy nhất và AC-US01-07/14. Chưa chốt một loại index cụ thể. |
| **OQ-US01-02 — Thiếu phạm vi sửa, chưa đủ để gọi là mâu thuẫn** | TA-SPEC §1 d.16–18: nguồn chỉ đọc; §4.1 d.43–45: tự sinh và cho sửa Draft; PAY-02/PAY-03 d.72–73 | Tự sinh dòng và cho sửa Draft có thể cùng tồn tại. Điều thiếu là được sửa gì và bảo toàn công thức/đối soát ra sao. | Cần ma trận trường: hợp đồng/kỳ/bảng giá, thêm/xóa dòng, sản lượng, đơn giá, thành tiền/tổng và thông tin khác; mỗi trường nêu có được sửa không, có đọc lại nguồn/tính lại không. Phân biệt sửa dữ liệu lưu trên bảng với ghi vào module nguồn. Không tự cấm mọi sửa hoặc cho sửa mọi trường. Chặn U3/U4, AC-US01-17. |
| **OQ-US01-01 — Mơ hồ chọn giá/thời điểm tính** | TA-SPEC §4.1 d.43–44; PAY-01 d.71: giá phù hợp; PAY-03 d.73: giá tại thời điểm tính; P-17 xác nhận tương tác chọn bảng giá | Được chọn bảng giá không có nghĩa mọi bảng giá đều phù hợp. Chưa rõ giá thay trong kỳ hoặc trong khoảng xem trước → lưu. | Cần tiêu chí theo hợp đồng/dịch vụ/mốc hiệu lực; chọn giá lúc tính hay theo giai đoạn kỳ, thiếu/trùng giá xử lý thế nào; đổi giá sau preview có giữ lần tính, tính lại hay xác nhận lại? Chặn 7/10/14, AC-US01-08/09/11/26. |
| **OQ-US01-04 — Thiếu quy tắc sinh dòng và phạm vi đối soát** | TA-SPEC §2 d.28–29; §4.1 d.43–44; PAY-02/PAY-03 d.72–73 | Tập rỗng khác sản lượng 0; nhiều bản ghi một dịch vụ; có phần chưa đối soát thì chưa biết “sản lượng kỳ” được kiểm tra ở cấp nào. | Cần xác nhận không có dữ liệu có được lập không; cách gộp/tách; kiểm tra đối soát toàn kỳ hay tập dữ liệu theo chính sách nào. Không tự lọc bỏ phần chưa đối soát để coi kỳ đã hợp lệ, không mặc định thiếu=0. Bổ sung mốc khi nguồn đổi trước lưu. Chặn 10/14, AC-US01-10/26. |
| **OQ-US01-05 — Mơ hồ mốc Active** | TA-SPEC §2 d.27 về kỳ; PAY-01 d.71 về đang hiệu lực | Chưa giải quyết hợp đồng Active lúc lập nhưng không phủ hết kỳ hoặc hết hiệu lực sau kỳ cần lập bù. | Xác nhận mốc đánh giá và xử lý hiệu lực một phần kỳ/nguồn đổi. Không tự đặt giới hạn kỳ quá khứ/tương lai. Chặn guard 5/14, AC-US01-05/26. |
| **OQ-US01-03 — Thiếu phạm vi quyền** | TA-SPEC §2 d.24 và §4.1 d.43–45; PAY-07 d.77 chỉ nói cấm tự duyệt | Vai trò NVKD rõ, phạm vi hợp đồng được lập và Draft của ai được sửa chưa rõ. | Tách quyền lập theo hợp đồng và quyền sửa theo bảng/người tạo/phân công. PAY-07 không cho phép suy ra chỉ người tạo được sửa. Chặn danh sách/quyền 2/5/14/U2, AC-US01-03. |
| **OQ-US03-03 — Thiếu chính sách tiền** | TA-SPEC §4.1 d.44: tính tổng; PAY-03 d.73; OQ1 d.20 ghi đề xuất nhóm | Đề không nêu VAT hay làm tròn. Chưa có căn cứ chốt cách xử lý số thập phân hoặc biến đề xuất nhóm thành công thức. | Xác nhận có thuế không; nếu có, cơ sở/loại/giá trị và cách tính; độ chính xác/thứ tự/cách làm tròn dòng và tổng; khi sửa lấy tổng mới thế nào. Đề nghị có ví dụ số để kiểm chứng. Chặn kết quả tiền cuối, AC-US01-12/17; công thức nhân PAY-03 vẫn có nguồn độc lập. |
| **OQ-US01-06 — Thiếu phạm vi đo NFR** | TA-SPEC §6 d.84: ≤3 giây với hợp đồng <200 dòng | Luồng nhiều lượt request khiến “phản hồi lập bảng” chưa có điểm đo thống nhất; “dòng” tính theo hợp đồng/nguồn hay kết quả chưa rõ. | Xác nhận thao tác/điểm bắt đầu-kết thúc, cách đếm và môi trường đo. Giữ nguyên ≤3 giây, <200 dòng; không tự thêm percentile/tải đồng thời. Chặn kết luận đạt AC-US01-20, không chặn vẽ luồng. |

**Các mâu thuẫn có trong đề nhưng không dùng để chốt luồng lập mới:**

- OQ-02: “từ 500 triệu” tại §4.3 ↔ “trên 500 triệu” tại PAY-06, ảnh hưởng đúng 500.000.000 đồng khi duyệt. Không biến ngưỡng thành điều kiện tạo Draft.
- OQ-03: KTT được điều chỉnh Approved tại §4.4 ↔ cấm mọi sửa Approved tại PAY-05. Không áp dụng luồng sửa Draft như cách giải mâu thuẫn Approved.
- OQ-05: tập dòng bắt buộc của PAY-04 chưa liệt kê. PAY-04 kiểm tra tổng âm/thiếu dòng khi trình duyệt; chưa có căn cứ mang nguyên các điều kiện đó sang bước lập. Thiếu dữ liệu để tính PAY-03 là vấn đề khác, đã có OQ-US01-01/04.

Không coi việc các OQ trên còn mở là lỗi suy diễn của bản thiết kế: bản hiện tại đã ghi Blocked. Phần cần sửa độc lập là tương tác tại §2; phần nghiệp vụ ở bảng này cần người phụ trách trả lời với người/ngày/nội dung/tham chiếu.

## 5. Bao phủ và thứ tự xử lý

| Yêu cầu / AC | Đánh giá trong phạm vi US-01 |
|---|---|
| US-PAY-01; AC-US01-01/21..25 | Có mở form → chọn hợp đồng/kỳ/giá → xem trước → lưu; chưa tạo Draft khi chỉ xem/đóng. Cần hoàn thiện vòng sự kiện/lỗi R03-01..03. |
| Vai trò/quyền/đầu vào; AC-US01-02..04 | Có vai trò và kiểm tra server; quyền theo OQ-US01-03. R03-04 cần phân loại phản hồi lỗi sửa. |
| PAY-01; AC-US01-05..07/14 | Có Active, giá, tra trùng sơ bộ và bảo đảm duy nhất khi ghi; kỳ/Cancelled/mốc Active còn OQ. Chưa triển khai constraint. |
| PAY-02; AC-US01-08/10 | Có Đã đối soát; dữ liệu rỗng/đối soát một phần và ánh xạ chờ OQ-US01-04. |
| PAY-03; AC-US01-09/11/12/17/26 | Có q × p, candidate phía server và không tin tổng client; giá/tiền/sửa/mốc nguồn vẫn chờ xác nhận. |
| Lỗi; AC-US01-13/16/19 | Có lỗi nguồn/giao dịch/token và phân biệt commit unknown; cần đường thử lại có chủ đích, không retry create khi chưa rõ kết quả. |
| NFR-PAY-01; AC-US01-15/17 | Audit create/update cùng giao dịch, before/after và actor/time đã mô tả. Chưa có kiểm thử hoặc hợp đồng dữ liệu audit đầy đủ. |
| Trạng thái; AC-US01-18/19 | Có Draft/version khi sửa; Rejected được đánh dấu chặn. Cần UI phản ánh không còn quyền/trạng thái hợp lệ theo R03-04. |
| NFR-PAY-02; AC-US01-20 | Giữ đúng ≤3 giây, <200 dòng; chưa đo, OQ-US01-06 mở. |
| US-PAY-02..05, PAY-04..08 | Chỉ kiểm tra ảnh hưởng/ràng buộc liên quan; không xác nhận đáp ứng toàn bộ các US ngoài phạm vi. |

Thứ tự đề nghị:

1. Chỉnh vòng tương tác/guard/phản hồi tại §2; việc này không yêu cầu tự trả lời nghiệp vụ.
2. Người phụ trách chốt ưu tiên OQ-01 + OQ-US05-02 (phạm vi kỳ/duy nhất), OQ-US01-01/04/05 (nguồn và phép tính), OQ-US01-02/03 (sửa/quyền), OQ-US03-03 (tiền). Ghi phương án chưa được chọn là Cần xác nhận.
3. OQ-04/OQ-US03-07 chỉ chặn mở sửa Rejected; tiếp tục phần tạo mới và sửa bảng đã là Draft. OQ-US01-06 cần chốt trước khi kết luận đo NFR.
4. Sau câu trả lời, đồng bộ spec → sequence → API/data/class/state/truy vết cùng version theo nhiệm vụ được giao; không sửa hồi tố TA-SPEC.

## 6. Kiểm chứng và kết luận

- `git diff ea10323 HEAD -- <SYS01> <OQ1> <SEQ01>` → không có khác biệt; bản đọc bằng Git ở lượt bị ngắt đúng với nội dung hiện tại.
- `git diff 5d5161e HEAD -- src` → rỗng. Đã đọc thực tế bốn file trong src/Qtkd.Api; không chạy test payment vì chưa có phần triển khai payment để kiểm thử.
- `java -jar C:/Users/phong/.vscode/extensions/jebbs.plantuml-2.18.1/plantuml.jar -charset UTF-8 -checkonly <TEMP>/qtkd-us01-rereview-ea10323/seq-us-01-v1.puml` → exit 0.
- `java -DPLANTUML_LIMIT_SIZE=22000 -jar C:/Users/phong/.vscode/extensions/jebbs.plantuml-2.18.1/plantuml.jar -charset UTF-8 -tpng <TEMP>/qtkd-us01-rereview-ea10323/seq-us-01-v1.puml` → exit 0; đã xem PNG bằng view_image. Bản TEMP được trích nguyên byte bằng `git show ea10323:<path>`, không ghi đè nguồn/SVG v1.
- Python 3.12.15 kiểm tra: SVG hiện tại là XML hợp lệ, 2559 × 7988 px; combined fragment alt/opt/loop/group/break lồng tối đa 8, đóng đầy đủ; 26 AC duy nhất. Git blob TA-SPEC tại HEAD và baseline `67dc495` giống nhau.
- `& C:/Users/phong/AppData/Roaming/uv/python/cpython-3.12.15-windows-x86_64-none/python.exe -X utf8 scripts/verify_agent_config.py` trước khi ghi báo cáo → `RESULT: PASS (0 failed checks)`.
- Chạy lại kiểm tra workspace sau tạo báo cáo → `RESULT: PASS (0 failed checks)`. Kiểm tra báo cáo qua Python: 4 R-ID duy nhất, bảng nhận xét đủ 8 cột, liên kết cục bộ tồn tại; nội dung sequence đã render khớp nguồn hiện tại sau chuẩn hóa CRLF/LF. Script kiểm tra đầu tiên đặt nhầm số dấu phân cột; sửa điều kiện đếm theo 8 cột rồi chạy lại PASS, không sửa nội dung nguồn vì lỗi kiểm tra này. `git diff --check` → exit 0 (không kiểm tra nội dung file chưa track); `git status --short` chỉ có báo cáo mới, không có file tracked bị sửa.
- Các tình huống ở §2 là cách kiểm chứng đề nghị, chưa phải kiểm thử UI tự động/ứng dụng đã chạy. Không đo hiệu năng, không xác nhận nghiệp vụ, không tuyên bố dùng Cursor/Antigravity: công cụ thực tế của lần này là Codex.

Kết luận: **Cần chỉnh sửa / Chờ xác nhận nghiệp vụ** cho US-01. Phần đã sửa giải quyết nhiều thiếu rõ của bản trước; còn bốn điểm tương tác tại §2 và các OQ nghiệp vụ tại §4. Chưa đủ đầu vào đánh giá toàn bộ thiết kế module. Reviewer không sửa thiết kế/OQ, không chốt nghiệp vụ hoặc thay nhóm đánh giá nhận xét AI.

## 7. Nhật ký và prompt thực tế

Ngày theo ngữ cảnh người dùng: 08/11/2026, Asia/Saigon. Công cụ: Codex / GPT-6, PowerShell, Git, Python 3.12.15, Java/PlantUML 1.2024.3, web để tra cú pháp PlantUML chính thức. Skill graphify đã đọc ở lượt trước; không có graphify-out/graph.json nên đọc tài liệu trực tiếp, không tạo graph/subagent. Đã đọc AGENTS.md và naming-versioning trước ghi báo cáo.

Lượt trước bị người dùng ngắt sau khi đọc nhánh v1-us-01-new và kết xuất PNG vào TEMP; chưa ghi báo cáo. Lượt tiếp tục kiểm tra HEAD đã merge cùng nội dung nên sử dụng kết quả đó sau khi xác minh không có khác biệt. Không chuyển nhánh hoặc sửa file người dùng.

AI viết báo cáo này; chưa có phần nhóm sửa/chưa tạo commit. Chỉ tạo báo cáo mới trong thư mục review, giữ nguyên thiết kế/spec/OQ/src và báo cáo cũ. Nhật ký được đặt trong báo cáo để tuân thủ phạm vi reviewer chỉ ghi báo cáo; không sửa prompt-log.md.

Prompt nguyên văn của lượt tiếp tục:

```text
tôi đã thay đổi code, hãy review lại.

đồng thời kiểm tra: Thiết kế module bảng thanh toán bằng AI Agent 
Công cụ: Cursor hoặc Antigravity 
ĐẶC TẢ NGHIỆP VỤ  
1. Mục đích và phạm vi 
Công ty cung cấp dịch vụ cho khách hàng theo hợp đồng. Định kỳ, nhân viên kinh doanh lập 
bảng thanh toán dựa trên sản lượng thực tế nhân đơn giá trong bảng giá. Bảng thanh toán 
phải được duyệt trước khi chuyển kế toán xuất hóa đơn. 
Module này chỉ bao gồm: lập, trình duyệt, duyệt/từ chối, điều chỉnh và hủy bảng thanh toán. 
Quản lý hợp đồng, bảng giá và sản lượng là module khác; module này chỉ đọc dữ liệu từ 
chúng. 
2. Thuật ngữ và vai trò 
Ý nghĩa 
Thuật ngữ / vai trò 
NVKD 
Nhân viên kinh doanh, lập và trình duyệt bảng 
KTT 
Kế toán trưởng 
GĐKD 
Giám đốc kinh doanh 
Kỳ thanh toán 
Khoảng thời gian tính tiền, là tháng hoặc quý tùy cấu hình của 
từng hợp đồng 
Sản lượng đã đối soát Sản lượng đã được hai bên xác nhận 
Dòng thanh toán 
Một dịch vụ trong bảng: sản lượng, đơn giá, thành tiền 
3. Trạng thái bảng thanh toán 
Bảng thanh toán có các trạng thái: Draft, PendingApproval, Approved, Rejected, 
Cancelled. 
Luồng chính: Draft → PendingApproval → Approved. Khi bị từ chối, bảng chuyển sang 
Rejected. Draft có thể chuyển sang Cancelled. 
4. Yêu cầu chức năng 
4.1 US-PAY-01: Lập bảng thanh toán (NVKD) 
NVKD chọn hợp đồng và kỳ thanh toán. Hệ thống tự sinh các dòng thanh toán từ sản lượng 
và bảng giá, tính tổng tiền, lưu ở trạng thái Draft. NVKD được phép chỉnh sửa bảng khi còn 
ở Draft. 
4.2 US-PAY-02: Trình duyệt (NVKD) 
NVKD chọn "Trình duyệt". Hệ thống kiểm tra hợp lệ theo PAY-04; nếu đạt, chuyển sang 
PendingApproval và gửi thông báo cho người duyệt. 
4.3 US-PAY-03: Duyệt hoặc từ chối 
Bảng có tổng tiền từ 500 triệu đồng trở lên do GĐKD duyệt; bảng dưới mức đó do KTT 
duyệt. Người duyệt có thể duyệt (→ Approved) hoặc từ chối kèm lý do (xem PAY-08). 
4.4 US-PAY-04: Điều chỉnh bảng đã duyệt (KTT) 
Khi phát hiện sai sót sau khi duyệt, KTT có thể điều chỉnh bảng đã Approved nếu có biên 
bản xác nhận đính kèm. Mọi điều chỉnh phải được ghi log. 
4.5 US-PAY-05: Hủy bảng nháp 
Bảng ở trạng thái Draft có thể bị hủy khi không còn cần thiết. Sau khi hủy, bảng chuyển sang 
Cancelled và không dùng lại được. 
5. Quy tắc nghiệp vụ 
Mã 
Nội dung 
PAY-01 
Chỉ lập bảng thanh toán cho hợp đồng đang hiệu lực (Active) và có bảng 
giá phù hợp. Mỗi hợp đồng chỉ có một bảng thanh toán cho mỗi tháng. 
PAY-02 
Sản lượng của kỳ phải ở trạng thái "Đã đối soát" trước khi lập bảng. 
PAY-03 
Thành tiền mỗi dòng = sản lượng × đơn giá tại thời điểm tính. 
PAY-04 
Khi trình duyệt, hệ thống chặn nếu tổng tiền âm hoặc thiếu dòng dịch vụ 
bắt buộc. Hệ thống chống thao tác trình duyệt trùng. 
PAY-05 
Bảng thanh toán đã Approved không được sửa dưới bất kỳ hình thức nào. 
PAY-06 
Bảng có tổng tiền trên 500 triệu đồng phải do GĐKD duyệt; các bảng còn 
lại do KTT duyệt. 
PAY-07 
Người lập bảng không được duyệt bảng do chính mình lập. 
PAY-08 
Khi từ chối phải nhập lý do; sau khi bị từ chối, bảng quay về trạng thái 
Draft để NVKD chỉnh sửa và trình lại. 
6. Yêu cầu phi chức năng 
• Mọi thay đổi trạng thái và mọi điều chỉnh phải được ghi audit log (ai, lúc nào, thay 
đổi gì). 
• Chức năng lập bảng phải phản hồi trong vòng 3 giây với hợp đồng có dưới 200 dòng. 

để tìm ra các điểm conflict đối với việc lập bảng thanh toán để giải quyết cho chức năng lập bảng thanh toán
```
