# QTKD Seminar – hướng dẫn AI dùng chung

Đây là điểm vào cấu hình AI của workspace. Quy tắc chi tiết và ba vai trò ba,
design, reviewer nằm trong thư mục [rules/](rules/README.md), mỗi quy tắc chỉ ở một
file. Trước khi làm, đọc file này, các rule chung và file của vai trò được gọi.
Mọi công cụ dùng cùng nội dung này.

Khi người dùng nói “đóng vai agent <tên>” hoặc “dùng agent <tên>”, thực hiện
vai trò tương ứng trong chat hiện tại. Chỉ tạo subagent khi người dùng yêu cầu
ủy nhiệm rõ ràng; không tự mở chat hoặc chạy song song. Reviewer nên được gọi
trong chat mới để đọc đặc tả và thiết kế độc lập.

Khi người dùng nói “dùng skill <tên>”, đọc skills/<tên>/SKILL.md và
skills/_shared/payment-context.md rồi làm theo các bước trong đó, trong vai trò
mà skill ghi. Skill chỉ chi tiết hóa cách làm; quy tắc trong file này và rules/
luôn ưu tiên. Danh mục: [skills/README.md](skills/README.md).

Tên file, hai version v1 (bản lần chạy đầu) / v2 (bản sau review), mã ID và thứ
tự làm theo skill [naming-versioning](skills/naming-versioning/SKILL.md); mọi vai
trò áp dụng khi tạo file. Sys spec (sys-us-NN-vK.md) viết trước; sequence, kiến
trúc, chi tiết, API, dữ liệu và truy vết chỉ suy ra từ đầu ra cùng version.
Không sửa file trong v1/ sau khi đã có báo cáo ai-review-01-v1.md.

## Rule phải đọc

| Thứ tự | File | Áp dụng |
|---|---|---|
| 1 | [rules/sources.md](rules/sources.md) – Nguồn yêu cầu | Mọi vai trò |
| 2 | [rules/common.md](rules/common.md) – Quy tắc chung | Mọi vai trò |
| 3 | [rules/payment-scope.md](rules/payment-scope.md) – Phạm vi Bảng thanh toán | Mọi vai trò |
| 4 | [rules/handoff.md](rules/handoff.md) – Bàn giao và nhật ký | Mọi vai trò |
| 5 | Một trong ba file vai trò bên dưới | Vai trò được gọi |

| Vai trò | Rule | Công việc | Nơi được ghi đầu ra |
|---|---|---|---|
| ba | [rules/ba.md](rules/ba.md) | Phân tích yêu cầu, acceptance criteria và Open Questions | docs/analysis/payment-management/vK/ |
| design | [rules/design.md](rules/design.md) | Khảo sát AS-IS, thiết kế HLD/LLD, UML, API, dữ liệu và truy vết | docs/design/payment-management/vK/ |
| reviewer | [rules/reviewer.md](rules/reviewer.md) | Review độc lập, ghi nhận vấn đề và căn cứ | Báo cáo mới trong docs/review/payment-management/ |

Nếu không đọc được một file rule, nêu rõ file chưa đọc và dừng phần việc phụ thuộc;
không tự đoán nội dung rule.

Nếu chỉ được yêu cầu trả lời trong chat hoặc kiểm tra không ghi file, trả trong
chat. Nhiệm vụ thiết lập workspace được sửa file cấu hình chung, rules/, README và
công cụ kiểm tra; không đồng nghĩa được giao thực hiện toàn bộ BA/thiết kế/review.
