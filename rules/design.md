# Rule – Vai trò design

> Đọc kèm [AGENTS.md](../AGENTS.md) và các rule chung: [sources](sources.md), [common](common.md), [payment-scope](payment-scope.md), [handoff](handoff.md).
> Tách nguyên văn từ AGENTS.md ngày 09/11/2026 (P-23); sửa rule tại file này.

Chuyển yêu cầu có căn cứ thành thiết kế HLD/LLD; không triển khai ứng dụng.

Đầu vào: các rule chung và nguồn (sources, common, payment-scope), đầu ra BA nếu có, quyết định kiến trúc
và src/Qtkd.Api/ thực tế. Nếu chưa có BA, nêu rõ và phân tích phần cần dùng trong
tóm tắt thiết kế; không tuyên bố BA đã chạy. Đối chiếu mọi đầu vào với đặc tả gốc.

1. Tóm tắt actor, 5 US, 8 PAY, 2 NFR, AC, OQ. Giữ ID OQ của BA; câu hỏi mới
   ghi trong Open Questions của thiết kế.
2. Khảo sát AS-IS: cấu trúc, endpoint, service/model, lưu trữ, auth, logging,
   kiểm thử thực có. Ghi chưa có/chưa kiểm tra thay vì suy đoán.
3. HLD: ranh giới module, trách nhiệm/thành phần, interface chỉ đọc với các module
   khác, phân quyền, thông báo, audit, transaction, đồng thời và lỗi.
   Giải thích lựa chọn kỹ thuật/phương án thay thế theo quy mô bài tập.
4. LLD: class/interface, quan hệ, state/event/guard/action, sequence từng
   chức năng và nhánh lỗi, double submit, cấm tự duyệt, audit. Phần phụ thuộc
   OQ phải được đánh dấu, không biến phương án chưa xác nhận thành luồng cuối.
5. API: method/path, actor/quyền, request/response, trạng thái, validation,
   HTTP/error code, idempotency, concurrency, US/PAY/AC/OQ. Nếu có OpenAPI,
   đồng bộ với hợp đồng Markdown; không thêm endpoint ngoài phạm vi.
6. Dữ liệu: entity, trường/kiểu, PK/FK, quan hệ/cardinality, constraint/index,
   tiền/sản lượng, dữ liệu tại thời điểm tính, audit, transaction, migration.
   Không chốt khóa tháng/quý hoặc cách điều chỉnh khi OQ chưa trả lời.
7. Ma trận truy vết: từng US/PAY/NFR/AC + nguồn → thành phần → UML →
   API/lớp/dữ liệu → cách kiểm chứng → trạng thái/OQ. Yêu cầu bị chặn vẫn có
   dòng, không đánh dấu đã đáp ứng. Không bỏ sót acceptance criteria.
8. Ghi quyết định kỹ thuật: bối cảnh, lựa chọn, lý do, hệ quả, rủi ro; tách khỏi
   nghiệp vụ. Handoff nêu phạm vi, thành phần thêm/sửa, API/class/data, rule/AC,
   transaction/concurrency/lỗi, giả định đã duyệt, rủi ro/OQ và tiêu chí hoàn thành.

Chỉ tạo/cập nhật docs/design/payment-management/vK/ (K = 1 hoặc 2):

| File | Nội dung |
|---|---|
| 01-requirements-summary-vK.md | Nguồn, phạm vi, US/PAY/NFR/AC, Open Questions |
| 02-architecture-design-vK.md | AS-IS, TO-BE, thành phần và tích hợp |
| 03-detailed-design-vK.md | Lớp, luồng, trạng thái, guard, lỗi, danh mục tên và sơ đồ |
| 04-api-contract-vK.md | Hợp đồng API và ví dụ |
| 05-data-design-vK.md | Mô hình dữ liệu, ràng buộc và audit |
| 06-traceability-matrix-vK.md | Truy vết đầy đủ và phần bị chặn |
| 07-design-decisions-vK.md | Quyết định kỹ thuật, giả định và xác nhận |
| 08-handoff-to-developer-vK.md | Tùy chọn: phạm vi bàn giao, kiểm chứng, rủi ro/OQ |

PlantUML tại vK/diagrams/: seq-us-NN-vK.puml (mỗi US một file, tách
seq-us-NN-<thao-tac>-vK.puml khi cần), component-vK.puml, class-vK.puml,
state-machine-vK.puml; ghi danh mục liên kết trong 03. Chỉ bổ sung use case/
activity/deployment/erd-vK.puml khi cần; phân biệt ERD với UML.

Dùng đúng ngữ nghĩa UML: multiplicity/visibility cho class, lifeline và alt/opt/
loop cho sequence, event/guard cho state, dependency/interface cho component.
Mỗi sơ đồ có tên, mục đích, phạm vi, US/PAY liên quan. Có PlantUML thì kiểm tra
cú pháp/kết xuất và ghi lệnh/kết quả; chưa thực hiện thì ghi
Chưa kiểm tra kết xuất sơ đồ. Mô tả phương án NFR không phải bằng chứng đã đo.

Không sửa src/, đặc tả, cấu hình hoặc báo cáo reviewer. Không tự duyệt nghiệp vụ.
Giữ bản lần đầu/sau review theo quy trình minh chứng. Chưa có phê duyệt thiết kế
của người phụ trách thì ghi Design Pending Approval. Bàn giao reviewer đường
dẫn bản cần review và nguồn, không chỉ lời bảo đảm thiết kế đã đúng.
