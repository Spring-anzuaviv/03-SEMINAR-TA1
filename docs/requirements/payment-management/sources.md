# Sổ nguồn – Bảng thanh toán TA 1–2

| Mã      | File                                           | Loại                     | Dùng để                          | Ghi chú                                           |
| ------- | ---------------------------------------------- | ------------------------ | -------------------------------- | ------------------------------------------------- |
| TA-PDF  | [assignment-ta-1-2.pdf](assignment-ta-1-2.pdf) | Đề bài gốc               | Căn cứ nghiệp vụ; dẫn trang      | §1–3 tr.1; §4–5 tr.2; §6 và Yêu cầu bài tập tr.3  |
| TA-SPEC | [spec.md](spec.md)                             | Bản chép §1–6 của TA-PDF | Căn cứ nghiệp vụ; dẫn mục/US/PAY | Trích bằng `pypdf` 07/11/2026; PDF thắng nếu lệch |
| AS-IS   | [src/Qtkd.Api/](../../../src/Qtkd.Api)         | Code demo hợp đồng       | Khảo sát hiện trạng              | Không xác lập nghiệp vụ TO-BE                     |

- Chỉ TA-PDF và TA-SPEC là căn cứ nghiệp vụ. Không dùng tài liệu trực tuyến hay
  tài liệu đồ án tổng thể (nếu có ai đính kèm) để trả lời Open Questions.
- Mã `NFR-PAY-01` (audit) và `NFR-PAY-02` (lập bảng ≤ 3 giây, hợp đồng dưới 200
  dòng) là mã nội bộ nhóm đặt cho hai gạch đầu dòng §6; đề không có mã NFR.
- Phần "Yêu cầu bài tập" (tr.3) quy định sản phẩm nộp, không phải nghiệp vụ.

## Nhật ký thay đổi nguồn

| Ngày       | Thay đổi                                                         | Người                          | Lý do                                                         |
| ---------- | ---------------------------------------------------------------- | ------------------------------ | ------------------------------------------------------------- |
| 07/11/2026 | Chuyển PDF vào thư mục này; tạo `spec.md` bằng trích văn bản PDF | AI (ChatGPT) theo yêu cầu nhóm | Công cụ AI không đọc được PDF thì vẫn có bản chữ để dẫn nguồn |

Nhóm cần đối chiếu `spec.md` với PDF một lần và ghi tên người/ngày đã đối chiếu
vào bảng trên.
