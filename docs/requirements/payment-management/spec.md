# TA-SPEC – Đặc tả nghiệp vụ Bảng thanh toán (TA 1–2)

> Bản chép §1–6 từ [assignment-ta-1-2.pdf](assignment-ta-1-2.pdf) (TA-PDF).
> Cách tạo: trích văn bản bằng `pypdf` ngày 07/11/2026, chỉ nối lại dòng bị ngắt
> và dựng lại bảng; giữ nguyên câu chữ, kể cả chỗ mâu thuẫn/mơ hồ.
> Không sửa nội dung file này. Nếu thấy lệch với PDF thì PDF thắng; ghi lại
> trong [sources.md](sources.md) trước khi sửa lỗi chép.
> Trang: §1–3 tr.1; §4–5 tr.2; §6 tr.3.

## 1. Mục đích và phạm vi

Công ty cung cấp dịch vụ cho khách hàng theo hợp đồng. Định kỳ, nhân viên kinh
doanh lập bảng thanh toán dựa trên sản lượng thực tế nhân đơn giá trong bảng giá.
Bảng thanh toán phải được duyệt trước khi chuyển kế toán xuất hóa đơn.

Module này chỉ bao gồm: lập, trình duyệt, duyệt/từ chối, điều chỉnh và hủy bảng
thanh toán. Quản lý hợp đồng, bảng giá và sản lượng là module khác; module này chỉ
đọc dữ liệu từ chúng.

## 2. Thuật ngữ và vai trò

| Thuật ngữ / vai trò | Ý nghĩa |
|---|---|
| NVKD | Nhân viên kinh doanh, lập và trình duyệt bảng |
| KTT | Kế toán trưởng |
| GĐKD | Giám đốc kinh doanh |
| Kỳ thanh toán | Khoảng thời gian tính tiền, là tháng hoặc quý tùy cấu hình của từng hợp đồng |
| Sản lượng đã đối soát | Sản lượng đã được hai bên xác nhận |
| Dòng thanh toán | Một dịch vụ trong bảng: sản lượng, đơn giá, thành tiền |

## 3. Trạng thái bảng thanh toán

Bảng thanh toán có các trạng thái: Draft, PendingApproval, Approved, Rejected,
Cancelled.

Luồng chính: Draft → PendingApproval → Approved. Khi bị từ chối, bảng chuyển sang
Rejected. Draft có thể chuyển sang Cancelled.

## 4. Yêu cầu chức năng

### 4.1 US-PAY-01: Lập bảng thanh toán (NVKD)

NVKD chọn hợp đồng và kỳ thanh toán. Hệ thống tự sinh các dòng thanh toán từ sản
lượng và bảng giá, tính tổng tiền, lưu ở trạng thái Draft. NVKD được phép chỉnh sửa
bảng khi còn ở Draft.

### 4.2 US-PAY-02: Trình duyệt (NVKD)

NVKD chọn "Trình duyệt". Hệ thống kiểm tra hợp lệ theo PAY-04; nếu đạt, chuyển sang
PendingApproval và gửi thông báo cho người duyệt.

### 4.3 US-PAY-03: Duyệt hoặc từ chối

Bảng có tổng tiền từ 500 triệu đồng trở lên do GĐKD duyệt; bảng dưới mức đó do KTT
duyệt. Người duyệt có thể duyệt (→ Approved) hoặc từ chối kèm lý do (xem PAY-08).

### 4.4 US-PAY-04: Điều chỉnh bảng đã duyệt (KTT)

Khi phát hiện sai sót sau khi duyệt, KTT có thể điều chỉnh bảng đã Approved nếu có
biên bản xác nhận đính kèm. Mọi điều chỉnh phải được ghi log.

### 4.5 US-PAY-05: Hủy bảng nháp

Bảng ở trạng thái Draft có thể bị hủy khi không còn cần thiết. Sau khi hủy, bảng
chuyển sang Cancelled và không dùng lại được.

## 5. Quy tắc nghiệp vụ

| Mã | Nội dung |
|---|---|
| PAY-01 | Chỉ lập bảng thanh toán cho hợp đồng đang hiệu lực (Active) và có bảng giá phù hợp. Mỗi hợp đồng chỉ có một bảng thanh toán cho mỗi tháng. |
| PAY-02 | Sản lượng của kỳ phải ở trạng thái "Đã đối soát" trước khi lập bảng. |
| PAY-03 | Thành tiền mỗi dòng = sản lượng × đơn giá tại thời điểm tính. |
| PAY-04 | Khi trình duyệt, hệ thống chặn nếu tổng tiền âm hoặc thiếu dòng dịch vụ bắt buộc. Hệ thống chống thao tác trình duyệt trùng. |
| PAY-05 | Bảng thanh toán đã Approved không được sửa dưới bất kỳ hình thức nào. |
| PAY-06 | Bảng có tổng tiền trên 500 triệu đồng phải do GĐKD duyệt; các bảng còn lại do KTT duyệt. |
| PAY-07 | Người lập bảng không được duyệt bảng do chính mình lập. |
| PAY-08 | Khi từ chối phải nhập lý do; sau khi bị từ chối, bảng quay về trạng thái Draft để NVKD chỉnh sửa và trình lại. |

## 6. Yêu cầu phi chức năng

- Mọi thay đổi trạng thái và mọi điều chỉnh phải được ghi audit log (ai, lúc nào,
  thay đổi gì).
- Chức năng lập bảng phải phản hồi trong vòng 3 giây với hợp đồng có dưới 200 dòng.
