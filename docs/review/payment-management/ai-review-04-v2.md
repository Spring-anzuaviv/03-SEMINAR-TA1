# Review US-PAY-01: đặc tả, sequence và OQ (v2)

> Phiên bản được review: v2 · Ngày: 08/11/2026 · Người phụ trách: Chờ nhóm điền
> Đầu vào: TA-SPEC §1–6; SYS-US-01 v2; sequence/OQ v2; 03-detailed-design-v2.md; xác nhận P-18.
> AI: Codex / GPT-6 · Prompt thực tế và kiểm chứng: §6 của báo cáo này.
> Bản kiểm tra: working tree trên nhánh v2-us-01, HEAD 8913b86; tài liệu US-01 v2 đang chưa commit.
> Kết luận: **Cần chỉnh sửa / Chờ xác nhận nghiệp vụ**. Design Pending Approval.

## 1. Nguồn và phạm vi

Review riêng **lập bảng và sửa Draft của US-PAY-01 v2** theo yêu cầu hiện tại. Tab v1 đang mở trong IDE không phải bản được review. Không sửa đặc tả, sequence, OQ, nhật ký hoặc src/.

| Mã | Tài liệu / phần đọc | Vai trò nguồn |
|---|---|---|
| TA-SPEC | [spec.md](../../requirements/payment-management/spec.md), §1–6 | Căn cứ nghiệp vụ gốc, giữ nguyên mâu thuẫn. |
| SYS2 | [sys-us-01-v2.md](../../analysis/payment-management/v2/sys-us-01-v2.md), toàn bộ 210 dòng | Đặc tả use case, 30 AC và phần thay đổi v1 → v2. |
| SEQ2 | [seq-us-01-v2.puml](../../design/payment-management/v2/diagrams/seq-us-01-v2.puml), toàn bộ 358 dòng; SVG cùng tên, PNG kết xuất lại | Thiết kế tương tác được kiểm tra. |
| OQ2 | [open-questions-v2.md](../../analysis/payment-management/v2/open-questions-v2.md), toàn bộ 47 dòng | Câu trả lời đã xác nhận, phần xác nhận một phần và câu hỏi còn mở. |
| DD2 | [03-detailed-design-v2.md](../../design/payment-management/v2/03-detailed-design-v2.md), toàn bộ 60 dòng | Danh mục sequence, tên tạm, nhóm lỗi, phương án kỹ thuật và giới hạn. Tài liệu tự xác định chưa phải LLD đầy đủ. |
| P18 | [prompt-log.md](../../workflow/prompt-log.md), P-18.1..4 và kiểm chứng P-18 | Căn cứ người dùng đã xác nhận điểm vào, kỳ, giá Active, ghi chú/thông báo và yêu cầu làm v2. |
| US05 | [user-review-us-05.md](user-review-us-05.md), §2.1; OQ2 dòng OQ-US05-02 | Kiểm tra căn cứ tái sử dụng quyết định v2 cho lập mới sau hủy; không suy ra quyền lập/sửa từ quyền hủy. |
| R03 | [ai-review-03-v1.md](ai-review-03-v1.md), §2 | Các vấn đề v1 để đối chiếu thay đổi; không dùng nhận xét AI làm xác nhận nghiệp vụ. |
| PROC | [AGENTS.md](../../../AGENTS.md); [naming-versioning](../../../skills/naming-versioning/SKILL.md); [workflow](../../workflow/README.md) | Phạm vi ghi file, số báo cáo/ID, nguồn và kiểm chứng. |

TA-PDF chưa được đọc trực tiếp trong lần này; căn cứ nội dung là TA-SPEC. Không sử dụng tài liệu nghiệp vụ trực tuyến. Không review lại các bộ US03/04/05 baseline được sao chép sang v2 ngoài phần quyết định hủy liên quan US-01.

Chưa có các tài liệu tổng thể v2 `01-requirements-summary`, `02-architecture-design`, API contract, data design, traceability matrix, design decisions, class/state/component đầy đủ. **Chưa đủ đầu vào review toàn bộ module**; không coi những tài liệu nằm ngoài phạm vi US-01 được giao là lỗi mới của lần này. Không khảo sát lại mã ứng dụng và không kết luận các vấn đề dưới đây là lỗi triển khai đã xảy ra.

## 2. Nhận xét cần xử lý

| ID | Vị trí file/mục/dòng | Loại | Mức độ | Nhận xét và tác động | Đề xuất / cách kiểm chứng | Căn cứ trang/mục/US/PAY/AC | OQ |
|---|---|---|---|---|---|---|---|
| R04-01 | SEQ2 d.67–106, đặc biệt kiểm tra d.68 và các nhánh kết quả d.80–105; DD2 d.42/44 | Chưa đủ ánh xạ lỗi → phản hồi trong sequence | TB | `preview` kiểm tra phiên/quyền, nhưng các operand kết quả chỉ bao phủ OK, FIELD_INVALID, PERIOD_OVERLAP, NOT_RECONCILED, ACTIVE_PRICE_INVALID, SOURCE_UNAVAILABLE và POLICY_DEPENDENT. Không có nhánh cho phiên hết hạn/mất quyền sau khi form đã mở. DD2 yêu cầu mọi request kiểm tra độc lập và dừng khi không có quyền, nhưng chưa chỉ rõ phản hồi/điểm kết thúc cho tình huống này trong preview. Nếu validation trả UNAUTHENTICATED/FORBIDDEN thì không operand hiện có nào mô tả phản hồi cho UI. Đây là thiếu trace, không phải bằng chứng server cho đọc trái quyền. | Thêm đường trả lỗi phiên/quyền và kết thúc hoặc yêu cầu xác thực lại theo chính sách UI; chỉ tiếp tục đọc nguồn khi kiểm tra thành công. Đồng bộ bảng ánh xạ mã lỗi/nhóm kiểm tra. Cũng cần nêu rõ ACTIVE_PRICE_INVALID khi sửa được ánh xạ vào đâu trong d.254–267, thay vì để người triển khai tự chọn nhóm. Kiểm chứng: mở form hợp lệ → phiên hết hạn/mất quyền → yêu cầu preview → nhận thông báo rõ, không đi vào đọc nguồn. | [ĐẶC TẢ] TA-SPEC §2, §4.1. [QUYẾT ĐỊNH ĐÃ XÁC NHẬN] P-18.1 yêu cầu thông báo cả thất bại. [ĐỀ XUẤT KỸ THUẬT] DD2 d.42/44; SYS2 AC-US01-02/03/29. | Phạm vi quyền cụ thể còn OQ-US01-03; việc phản hồi khi quyền không đạt có thể mô tả độc lập |
| R04-02 | SEQ2 d.229–240, 257–259, 326–348; SYS2 AU4 d.129, AC-US01-19 d.179 | Thiếu đường tải lại version trong vòng sửa | TB | VERSION_REQUIRED thông báo “quay U1”, nhưng U1/openDraft nằm ngoài vòng sửa. Nhánh này không kết thúc vòng/form và vòng hiện tại chỉ có lưu/thử lại, kiểm tra kết quả, đóng form; chưa có sự kiện tải lại để lấy version. Theo trace đang vẽ, bấm lưu tiếp vẫn có thể gửi cùng token thiếu. Nhánh CONCURRENT_MODIFICATION d.314–316 đã đóng form để mở lại, trong khi VERSION_REQUIRED chưa thể hiện cách tiếp tục tương đương. | Chọn một cách nhất quán: kết thúc form sửa để người dùng mở lại U1, hoặc thêm sự kiện tải lại gọi openDraft và thay dữ liệu/version trong UI. Nêu cách xử lý nội dung nhập chưa lưu khi tải lại. Kiểm chứng: mở sửa → request thiếu version → nhận VERSION_REQUIRED → tải lại representation có version → lưu thành công; không chỉ lặp lại request thiếu token. | [ĐẶC TẢ] TA-SPEC §4.1. [ĐỀ XUẤT KỸ THUẬT] Version là phương án thiết kế, không có trong đề; yêu cầu tải lại do SYS2 AU4/AC-US01-19 và DD2 d.52 xác lập. | Không cần OQ nghiệp vụ mới về đường tải lại; trường sửa vẫn theo OQ-US01-02 |
| R04-03 | SEQ2 K1 d.203–210 và 326–333; SYS2 K1 d.98, bước 13 d.71, U6 d.123 | Thiếu dữ liệu trả về để hoàn thành phục hồi | TB | K1 chỉ vẽ repository trả `committed / definitelyNotCommitted / unknown`, service trả `outcome`, sau đó UI hiển thị bảng/dữ liệu đã lưu. Với create trước đó chỉ nhận RESULT_UNKNOWN(lookupId), chưa có paymentId/version; với update cũng chưa nhận newVersion. Chưa mô tả dữ liệu lấy ở đâu để hiển thị đúng representation đã commit. Có thể giao thức dự kiến trả cả dữ liệu nhưng chữ ký hiện tại chưa nói rõ; không kết luận triển khai làm mất dữ liệu. | Định nghĩa kết quả committed mang định danh bảng, dữ liệu và version đã lưu, hoặc vẽ bước đọc representation theo id đã xác minh trước khi trả UI. Dùng dữ liệu đã commit, không mặc định preview trước lỗi bằng dữ liệu cuối cùng. Không cần chốt DB/schema để làm rõ luồng dữ liệu này. Kiểm chứng: mất phản hồi commit → K1 xác minh committed → UI nhận đúng id/dòng/tổng/version và kết thúc thành công. | [ĐẶC TẢ] TA-SPEC §4.1, PAY-03. [ĐỀ XUẤT KỸ THUẬT] SYS2 bước 13/U6/K1, AC-US01-19/29; DD2 d.54. Phương thức K1 và payload không phải yêu cầu gốc của TA. | Không cần OQ nghiệp vụ mới; cơ chế xác minh DB/driver vẫn là giới hạn kỹ thuật đã ghi |

Không phát hiện vấn đề mức Cao được chứng minh trong phạm vi lần này. Ba nhận xét là thiếu hoàn thiện mô tả tương tác/dữ liệu; không phải lỗi cú pháp PlantUML hoặc bằng chứng ứng dụng đã sai.

## 3. Thay đổi so với các điểm review v1

Bảng này ghi nhận nội dung v2 đang có; không thay nhóm đánh giá Đúng/Sai/Thừa cho các R-ID cũ.

| Điểm v1 | Nội dung v2 quan sát được | Đánh giá phạm vi |
|---|---|---|
| R03-01: vòng phục hồi nằm ngoài lưu | SEQ2 d.63–226 và d.240–348 có vòng bao cả nhập/lưu/thử lại/tra cứu kết quả. | Phần quay lại sau lỗi trường/lưu đã được thể hiện. Còn đường lấy version ở R04-02. |
| R03-02: thử lại phải đổi lựa chọn | SEQ2 d.65 cho sự kiện thử lại dữ liệu với cùng kỳ; SYS2 A7.2 nêu rõ không cần đổi kỳ. | Không tiếp tục báo guard chọn giá v1: v2 đã bỏ chọn giá thủ công. |
| R03-03: previewAccepted chưa có sự kiện | Bỏ previewAccepted; actor gửi sự kiện nhập/ghi chú/lưu/đóng/kiểm tra kết quả. | Hành vi điều khiển form rõ hơn, không thêm nút chấp nhận riêng. |
| R03-04: lỗi quyền/trạng thái bị gộp với sửa trường | Create d.137–144 tách lỗi kết thúc; update d.254–267 tách lỗi trường/token/không thể mở; conflict kết thúc form để tải lại. | Phân loại cơ bản đã có; preview còn thiếu đường phản hồi theo R04-01. |
| Điểm vào/chọn dữ liệu | Từ chi tiết hợp đồng, contractId cố định, kỳ theo cấu hình, giá Active tự lấy, note tùy chọn. | Khớp P-18.1..3; không áp lại quy trình chọn hợp đồng/bảng giá của v1. |
| Chồng lấn tháng/quý | findOverlap và lockContractScopeAndCreate; thao tác kiểm tra lại và ghi trong giao dịch. | Là phương án kỹ thuật có lý do/thay thế, chưa phải bằng chứng chạy đồng thời thành công. |
| Giá thay đổi trước lưu | A11.1/AU4.1 tính theo Active và quay hiển thị kết quả mới, không cho giữ giá cũ. | Khớp xác nhận P-18.3; khoảng nguồn đổi giữa lần đọc cuối và commit đã được ghi là giới hạn kỹ thuật, không báo lại như suy diễn bị bỏ sót. |

## 4. OQ và xác nhận nghiệp vụ v2

| OQ / nội dung | Trạng thái theo bằng chứng đã đọc | Tác động review |
|---|---|---|
| OQ-01 — tháng/quý/chồng lấn | Đã xác nhận tại P-18.3; OQ2 d.31, SYS2 d.143. | Không tiếp tục coi phạm vi chồng lấn là chưa có đáp án. Loại kỳ vẫn theo cấu hình; không tự cho người dùng đổi cấu hình hợp đồng trong form lập. |
| OQ-US05-02 — lập mới sau hủy | Đã xác nhận trong bộ US05 v2; user-review-us-05 §2.1 và OQ2 d.17. | Có căn cứ loại Cancelled khỏi phạm vi chiếm kỳ. Không suy ra unique theo tháng đơn lẻ đủ chống chồng lấn quý/tháng; DD2 đã nêu giới hạn này. |
| OQ-US01-01 — giá | Đã rõ dùng giá Active gắn hợp đồng khi tính/lưu, giá mới chưa Active không dùng; P-18.1/3. | Chỉ còn câu hỏi đồng bộ mọi Draft đang không được mở khi giá đổi. Không tự thêm tác vụ nền hoặc yêu cầu người dùng chọn giá. |
| OQ-US01-05 — Active | Đã rõ kiểm tra trạng thái Active theo P-18.1. | Còn mở hiệu lực đối với kỳ quá khứ/một phần kỳ; giữ câu hỏi này ở đúng phạm vi, không coi toàn bộ kiểm tra Active chưa rõ. |
| OQ-US01-02 — sửa Draft | Cần xác nhận ma trận trường sửa, trường server tính, điều kiện đọc lại nguồn/tính lại. | Luồng U3/U4 chưa đủ để chốt request và mọi validation chi tiết; ghi chú tùy chọn lúc tạo chưa tự xác nhận phạm vi sửa mọi trường. |
| OQ-US01-03 — quyền | Cần xác nhận quyền lập trên hợp đồng và sửa bảng của người khác. | Quyền xem chi tiết hợp đồng không tự cấp quyền lập; quyền hủy US05 không tự trở thành quyền lập/sửa. |
| OQ-US01-04 — sản lượng/dòng | Cần xác nhận rỗng/0, gộp/tách dịch vụ, đối soát một phần, nguồn thay đổi sau preview. | Các placeholder chưa phải luồng runtime cuối cùng. Không mặc định thiếu=0, không tự quyết lấy nguồn cũ/mới. |
| OQ-US03-03 — tiền | Thuế, độ chính xác và làm tròn còn Cần xác nhận; đề xuất P-04..07 chưa được duyệt. | Chặn công thức tiền cuối cùng; không chặn phép nhân PAY-03 hay hình thức giao diện. |
| OQ-04/OQ-US03-07 — Rejected | Cần xác nhận đích sau từ chối và sự kiện mở sửa. | Chỉ chặn sửa bảng bị từ chối; không tự chuyển Rejected → Draft, không chặn lập mới. |
| OQ-US01-06 — đo NFR | Cần xác nhận điểm đo, cách đếm dòng và môi trường. | Giữ ≤3 giây, <200 dòng; chưa kết luận đạt hiệu năng. |

Các OQ được đánh dấu đúng trạng thái không bị tính là lỗi thiết kế. Phần `POLICY_DEPENDENT` trong sequence đã có ghi chú là phần chưa chốt và DD2 d.44 nói không phải mã API cuối; cần thay bằng các tình huống dữ liệu cụ thể khi có câu trả lời, không bàn giao placeholder như hợp đồng runtime chính thức.

## 5. Bao phủ và giới hạn bàn giao

| Yêu cầu / AC | Kết quả kiểm tra tài liệu |
|---|---|
| US-PAY-01; AC-US01-01, 21–25, 27–30 | Có điểm vào từ chi tiết hợp đồng, chọn kỳ/ghi chú, xem trước, lưu, thông báo, đóng form và chống chồng lấn. Có vòng quay lại. |
| Vai trò/quyền; AC-US01-02/03 | Có kiểm tra độc lập phía server trong DD2; quyền cụ thể còn OQ, phản hồi preview cần bổ sung R04-01. |
| PAY-01; AC-US01-04..07/14/30 | Có Active, kỳ, loại Cancelled, overlap và ý định bảo đảm khi ghi đồng thời. Chưa có phép thử DB; không dùng source code demo hợp đồng làm căn cứ nghiệp vụ. |
| PAY-02/PAY-03; AC-US01-08..12/26 | Có đọc nguồn, Đã đối soát, q × p và reprice theo Active. Ánh xạ/sản lượng/tiền còn OQ đã công bố. |
| Lỗi/phiên bản; AC-US01-13/16/19/29 | Có lỗi nguồn, rollback, commit ba kết quả, lookup và token. Các đường VERSION_REQUIRED/K1 cần rõ hơn theo R04-02/03. |
| Sửa/trạng thái; AC-US01-17/18 | Có candidate, kiểm tra Draft/version, audit trước/sau cùng dữ liệu; phạm vi trường sửa và Rejected vẫn chờ xác nhận. |
| NFR-PAY-01; AC-US01-15/17 | Có audit ai/lúc nào/thay đổi gì và cùng transaction; chưa có test tích hợp chứng minh. |
| NFR-PAY-02; AC-US01-20 | Giữ đúng ≤3 giây với hợp đồng <200 dòng; OQ-US01-06 mở, chưa đo. |
| PAY-04..08 / US-PAY-02..05 | Chỉ đối chiếu phần liên quan/ranh giới. Không kết luận đã đáp ứng toàn bộ module. |

Sơ đồ có lifeline, thông điệp/return, self-call, alt/opt/loop/group và note; không phát hiện lỗi cú pháp. Thiếu activation bar không tự nó là lỗi. UI→Service là mức trừu tượng được DD2 nêu rõ, không bắt buộc thêm controller chỉ để giống v1. Hình hiện tại 2244 × 8642 px, lồng tối đa 10 mức; có thể tách create/update hoặc phân trang để đọc khi nộp, đây là gợi ý trình bày, không phải lỗi chặn nghiệp vụ.

Kết luận: **Cần chỉnh sửa / Chờ xác nhận nghiệp vụ** cho US-01 v2. Sửa ba đường tương tác ở §2; tiếp tục xác nhận các OQ còn mở tại §4. Chưa đủ đầu vào kết luận trên toàn bộ HLD/LLD/API/data. Không phê duyệt nghiệp vụ hoặc tự đánh giá nhận xét AI thay nhóm.

## 6. Nhật ký và kiểm chứng

- Ngày theo người dùng: 08/11/2026, Asia/Saigon. Công cụ: Codex / GPT-6, PowerShell/Git, Python 3.12.15, Java và PlantUML 1.2024.3.
- Đã đọc AGENTS.md và naming-versioning. Skill graphify đã đọc từ lượt trước; kiểm tra graphify-out/graph.json → không có; đọc trực tiếp tài liệu, không tạo graph hay subagent.
- Working tree có các thay đổi v1/OQ/nhật ký và file v2 chưa track từ trước. Không hoàn tác, ghi đè hay đưa các thay đổi đó vào kết quả do reviewer tạo.
- `java -jar C:/Users/phong/.vscode/extensions/jebbs.plantuml-2.18.1/plantuml.jar -charset UTF-8 -checkonly docs/design/payment-management/v2/diagrams/seq-us-01-v2.puml` → không báo lỗi; nguồn được kết xuất PNG tiếp theo thành công.
- `java -DPLANTUML_LIMIT_SIZE=24000 -jar C:/Users/phong/.vscode/extensions/jebbs.plantuml-2.18.1/plantuml.jar -charset UTF-8 -tpng -o <TEMP>/qtkd-us01-v2-review-20261108 docs/design/payment-management/v2/diagrams/seq-us-01-v2.puml` → tiến trình exit 0; đã xem PNG bằng view_image. Chỉ ghi ảnh QA trong TEMP, không ghi đè SVG/PUML của người dùng.
- Python kiểm tra 30 AC không trùng; SVG XML hợp lệ, kích thước 2244 × 8642 px; alt/opt/loop/group/break lồng tối đa 10 mức và đóng đủ. Đây là kiểm tra cấu trúc/render, không chứng minh nghiệp vụ hoặc DB đúng.
- `& C:/Users/phong/AppData/Roaming/uv/python/cpython-3.12.15-windows-x86_64-none/python.exe -X utf8 scripts/verify_agent_config.py` trước báo cáo → `RESULT: PASS (0 failed checks)`.
- Đã lưu SHA-256 của toàn bộ file docs/src trước khi tạo báo cáo để kiểm tra giữ nguyên đầu vào sau review. Không chạy ứng dụng, test tích hợp hoặc đo NFR.
- Sau khi tạo báo cáo: đối chiếu SHA-256 → toàn bộ file docs/src có trước review giữ nguyên; kiểm tra riêng báo cáo → 3 R-ID duy nhất, bảng 8 cột, liên kết cục bộ tồn tại. Chạy lại verify_agent_config.py → `RESULT: PASS (0 failed checks)`; `git diff --check` → exit 0, chỉ cảnh báo LF/CRLF có sẵn của prompt-log.md. Lệnh diff không kiểm tra nội dung file chưa track; báo cáo mới đã được kiểm tra riêng. Các thay đổi working tree có trước được giữ nguyên, reviewer chỉ thêm ai-review-04-v2.md.
- AI chỉ viết báo cáo này; chưa có phần nhóm sửa, chưa commit. Nhật ký giữ trong báo cáo do phạm vi reviewer chỉ ghi báo cáo; không sửa prompt-log.md.

Prompt nguyên văn của yêu cầu được thực hiện:

```text
review lại cho version 2
```
