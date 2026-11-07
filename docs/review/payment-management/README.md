# Review – Bảng thanh toán

Báo cáo AI reviewer và đánh giá của nhóm. Không chia thư mục; version của bản được
review nằm trong tên file ([naming-versioning §3](../../../skills/naming-versioning/SKILL.md#3-bảng-tên-file)).

| File | Nội dung | Ai ghi |
|---|---|---|
| `ai-review-us-05-v1.md` | Báo cáo reviewer độc lập cho US-PAY-05 (v1); nhận xét `R01-01` đến `R01-07` | AI, vai trò reviewer |
| `user-review-us-05.md` | Báo cáo đánh giá của nhóm cho US-PAY-05 (vấn đề phát hiện + đánh giá nhận xét AI) | Nhóm |
| `ai-review-01-v1.md` | Báo cáo reviewer lần 01 trên toàn bộ bản v1 (khi hoàn thành đủ 5 US); nhận xét `R01-kk` | AI, vai trò reviewer, chat mới |
| `review-assessment-01-v1.md` | Đánh giá từng `R01-kk`: Đúng/Sai/Thừa, lý do, căn cứ, chấp nhận/từ chối/chờ, file/commit sửa ở v2, người/ngày | Nhóm |
| `evaluation-report.md` | **Báo cáo đánh giá nộp – mục 2 của đề** | Nhóm |

Review lần sau tăng số: `ai-review-02-v2.md` + `review-assessment-02-v2.md`.

## Cấu trúc `evaluation-report.md`

Đề yêu cầu: "bảng vấn đề phát hiện (vị trí trong đặc tả, loại vấn đề, cách nhóm xử
lý) và đánh giá nhận xét của AI Reviewer (đúng, sai, thừa)" [TA-PDF tr.3, mục 2].

1. **Bảng vấn đề phát hiện trong đặc tả** – lấy từ `open-questions-vK.md`:

   | OQ | Vị trí trong đặc tả | Loại (Mâu thuẫn/Mơ hồ/Thiếu) | Mô tả | Cách nhóm xử lý | Trạng thái |
   |---|---|---|---|---|---|

   "Cách nhóm xử lý" nêu: giữ Cần xác nhận / phương án thiết kế có nhãn giả định /
   đã hỏi ai, ngày nào, câu trả lời – không tự chốt nghiệp vụ.

2. **Đánh giá nhận xét của AI Reviewer** – tổng hợp từ `review-assessment-NN-vK.md`:

   | R-ID | Tóm tắt nhận xét | Đánh giá Đúng/Sai/Thừa | Lý do + căn cứ | Xử lý (sửa ở v2 / từ chối / chờ) |
   |---|---|---|---|---|

   Kèm số lượng Đúng/Sai/Thừa và liên kết thay đổi v1 → v2.
