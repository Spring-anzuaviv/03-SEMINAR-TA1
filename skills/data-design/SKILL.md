---
name: data-design
description: Viết 05-data-design-vK.md (entity, trường/kiểu, PK/FK, cardinality, constraint/index, tiền và sản lượng, dữ liệu tại thời điểm tính, audit, transaction, migration) và erd-vK.puml tùy chọn cho Bảng thanh toán, suy ra từ class/API cùng version, không chốt phần phụ thuộc OQ.
---

# Skill: data-design – Thiết kế dữ liệu

Vai trò: **design** trong [AGENTS.md](../../AGENTS.md) (bước 6). Đọc AGENTS.md và
[ngữ cảnh dùng chung](../_shared/payment-context.md) và
[naming-versioning](../naming-versioning/SKILL.md).

## Đầu vào (bước 8 của thứ tự phụ thuộc)

- TA-SPEC; cùng version vK: `sys-us-*-vK.md`, `open-questions-vK.md`.
- **Bắt buộc** cùng version: `class-vK.puml` và danh mục tên trong
  `03-detailed-design-vK.md`; `04-api-contract-vK.md` (field JSON ↔ cột phải khớp).
  Thiếu thì trả lời "Chưa đủ đầu vào: <file>".
- AS-IS: đọc lại `src/Qtkd.Api/`. Tại 07/11/2026 chỉ có lưu trong bộ nhớ, không
  CSDL/migration – ghi đúng như vậy nếu vẫn thế.

## Đầu ra

- `docs/design/payment-management/vK/05-data-design-vK.md`.
- Tùy chọn `vK/diagrams/erd-vK.puml` – ghi rõ là **ERD (mô hình dữ liệu)**, không phải
  UML class diagram.

## Cấu trúc 05-data-design-vK.md

1. **Nguồn và phạm vi** – nguồn đã đọc/chưa có; chỉ dữ liệu của module Bảng thanh
   toán; dữ liệu hợp đồng/bảng giá/sản lượng chỉ tham chiếu qua interface đọc.
2. **AS-IS lưu trữ** – theo file thực (không suy đoán).
3. **Danh sách entity** – mục đích, US/PAY, ánh xạ class trong `class-vK.puml`.
4. **Chi tiết từng entity** – bảng:

   | Cột | Kiểu | Null | Khóa/Constraint | Mô tả | Nguồn/Nhãn | OQ |
   |---|---|---|---|---|---|---|

5. **Quan hệ & cardinality** – vd. bảng 1 — 1..* dòng; bảng 1 — 0..* audit.
6. **Constraint & index** – mỗi cái nêu mục đích + yêu cầu (PAY-04 chống trùng,
   truy vấn danh sách chờ duyệt, lọc theo hợp đồng/kỳ…).
7. **Tiền và sản lượng** – kiểu số thập phân chính xác (không float/double) là
   `[ĐỀ XUẤT KỸ THUẬT]` có lý do; số chữ số thập phân, đơn vị tiền, làm tròn,
   VAT → `Blocked by OQ` nếu chưa có trả lời. Tổng tiền: tính lại hay lưu (nêu
   lựa chọn + DD-kk), luôn khớp tổng thành tiền các dòng.
8. **Dữ liệu tại thời điểm tính (PAY-03)** – lưu snapshot sản lượng, đơn giá,
   tham chiếu phiên bản bảng giá/bản ghi sản lượng đã dùng, thời điểm tính,
   để bảng không đổi khi module nguồn thay đổi. Ghi là phương án đáp ứng PAY-03.
9. **Khóa duy nhất theo kỳ (PAY-01)** – trình bày các phương án (theo tháng / theo
   kỳ tháng-quý của hợp đồng) và tác động; `Blocked by OQ-01` kỳ tháng/quý;
   bảng `Cancelled` có chiếm khóa không → OQ (lập lại sau hủy). Dẫn `OQ-01`. Không chốt.
10. **Trạng thái & quy trình** – cột trạng thái chỉ nhận 5 giá trị §3; người lập,
    người trình, người duyệt, thời điểm, lý do từ chối; định nghĩa "người lập"
    theo OQ trong `sys-us-03-vK.md` (nếu BA đã nêu). Cột chống cập nhật đồng thời (version/rowversion) là đề xuất.
11. **Audit (NFR-PAY-01)** – entity audit: ai, lúc nào, thao tác, trạng thái
    trước/sau, nội dung thay đổi (giá trị cũ/mới), lý do, tham chiếu biên bản;
    chỉ thêm (append-only), không sửa/xóa. Ghi cùng transaction với thay đổi.
12. **Điều chỉnh Approved (US-PAY-04 ↔ PAY-05)** – `Blocked by OQ-03`; có thể
    mô tả phương án dữ liệu (sửa tại chỗ + audit / bản điều chỉnh riêng) có nhãn
    giả định; biên bản đính kèm (metadata file) chỉ khi phục vụ §4.4.
13. **Transaction & đồng thời** – thao tác nào trong một transaction, isolation/
    khóa lạc quan đề xuất; ánh xạ sequence tương ứng.
14. **Migration** – AS-IS chưa có CSDL: nêu cách tạo schema ban đầu (đề xuất),
    dữ liệu khởi tạo nếu có; không viết code migration.
15. **Open Questions & giả định của dữ liệu** – dẫn ID có sẵn; mới thì `OQ-D-kk`
    ghi vào `01-requirements-summary-vK.md`.

## Không được

- Thiết kế bảng CRUD cho hợp đồng/bảng giá/sản lượng (chỉ khóa tham chiếu/ snapshot).
- Thêm cột thuế, chiết khấu, hạn duyệt, kênh thông báo, trạng thái mới không có nguồn.
- Chốt unique theo tháng hoặc quý; chốt ngưỡng 500 triệu dưới dạng constraint.

## Kiểm chứng

- Mỗi entity ↔ class trong `class-vK.puml`; mỗi field API ↔ cột (hoặc ghi lý do khác).
- Mỗi US/PAY/NFR có dữ liệu liên quan xuất hiện ít nhất một lần trong 05.
- `grep -n "Blocked by OQ" 05-data-design-vK.md` khớp danh sách OQ ở mục 15.
- ERD (nếu có) kiểm tra kết xuất hoặc ghi `Chưa kiểm tra kết xuất sơ đồ`.
- Ghi `Design Pending Approval` và prompt-log. Không sửa `src/`.
