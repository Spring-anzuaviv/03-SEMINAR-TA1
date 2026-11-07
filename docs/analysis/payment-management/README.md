# Phân tích yêu cầu – Bảng thanh toán

Đầu ra vai trò **ba** ([AGENTS.md](../../../AGENTS.md)). Tên file và version theo
[naming-versioning](../../../skills/naming-versioning/SKILL.md).

| Thư mục | Ý nghĩa |
|---|---|
| [v1/](v1) | Bản lần chạy đầu – đóng băng khi có `ai-review-01-v1.md` |
| [v2/](v2) | Bản sau review – sao chép đủ v1 rồi sửa theo nhận xét được chấp nhận |

## File trong mỗi version (ví dụ v1)

| File | Nội dung | Người phụ trách | Trạng thái |
|---|---|---|---|
| `sys-us-01-v1.md` | US-PAY-01 Lập bảng thanh toán | | Chưa làm |
| `sys-us-02-v1.md` | US-PAY-02 Trình duyệt | | Chưa làm |
| `sys-us-03-v1.md` | US-PAY-03 Duyệt / từ chối | | Chưa làm |
| `sys-us-04-v1.md` | US-PAY-04 Điều chỉnh bảng đã duyệt | | Chưa làm |
| `sys-us-05-v1.md` | US-PAY-05 Hủy bảng nháp | BA Team | Đã lập (v1) |
| `open-questions-v1.md` | Bảng OQ dùng chung (OQ-01..05 giữ chỗ + OQ-USNN-kk) | BA Team | Đang cập nhật (v1) |
| `requirements-checklist-v1.md` | 5 US, 8 PAY, 2 NFR → trạng thái/OQ | | Chưa làm |

Nhóm tự điền cột Người phụ trách/Trạng thái. Năm file sys-us có thể chia cho
năm người làm song song: mỗi người chỉ đặt OQ mới dạng `OQ-USNN-kk` của US mình,
dùng chung `OQ-01..05` cho các mâu thuẫn đã biết
([ngữ cảnh chung §4](../../../skills/_shared/payment-context.md#4-mâu-thuẫnthiếu-đã-biết--id-giữ-chỗ-không-tự-chọn-phía)).
