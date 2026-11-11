# SYS-US-01 – Lập bảng thanh toán (v2)

> Phiên bản: v2 · Ngày: 11/11/2026 · Người phụ trách: Phạm Thanh Phong
> Đầu vào: [TA-SPEC](../../../requirements/payment-management/spec.md) §1–6; sys-us-01-v1.md; Báo cáo đánh giá nhóm 3 (`BÁO CÁO ĐÁNH GIÁ.md`) – bảng II.2 “Các vấn đề phát hiện trong đặc tả”, cột “Cách nhóm xử lý”, và bảng III (R01-xx nhóm đánh giá Đúng)
> AI: Claude Code / Claude Opus 5.5 · Prompt: P-29 trong [prompt-log](../../../workflow/prompt-log.md)
> Trạng thái: Bản sau review – BA Pending Approval
> Nhãn: [ĐẶC TẢ] bám TA-SPEC · [AC dẫn xuất] · [ĐỀ XUẤT KỸ THUẬT] · [GIẢ ĐỊNH – Cần xác nhận: OQ-…] = áp dụng **cách xử lý nhóm đề xuất** cho OQ đó (trạng thái “Nhóm đề xuất”, chưa có xác nhận của khách hàng – theo R01-20).

Mã SYS/AC/OQ/NFR là mã nội bộ, trừ US-PAY/PAY do đề đặt. Phạm vi: lập bảng và sửa Draft của US-PAY-01. Hợp đồng, bảng giá, sản lượng chỉ được đọc [ĐẶC TẢ] [TA-SPEC §1, §4.1; TA-PDF tr.1–2].

**Thay đổi chính so với v1:** NVKD **không chọn bảng giá**; hệ thống tự lấy bảng giá Active gắn với hợp đồng (R01-03, OQ-US01-01). Các điểm Blocked của v1 được thay bằng cách xử lý nhóm đề xuất ở bảng II.2. Chi tiết ở mục “Thay đổi so với v1”.

## 1. Use case

### 1.1. Phạm vi và căn cứ

| Yêu cầu | Áp dụng trong v2 | Căn cứ |
|---|---|---|
| US-PAY-01 | NVKD chọn hợp đồng và kỳ; hệ thống tự sinh dòng, tính tổng, lưu Draft; NVKD sửa khi Draft. | [ĐẶC TẢ] TA-SPEC §4.1 |
| PAY-01 | Hợp đồng Active **tại thời điểm lập**; có bảng giá Active gắn với hợp đồng; mỗi hợp đồng một bảng cho mỗi khoảng thời gian, kiểm tra chồng lấn theo khoảng ngày với các bảng **chưa hủy**. | [ĐẶC TẢ] §5 PAY-01; [GIẢ ĐỊNH – Cần xác nhận: OQ-01, OQ-US01-01, OQ-US01-05, OQ-US05-02] |
| PAY-02 | Chỉ dùng sản lượng Đã đối soát; kỳ còn bản ghi chưa đối soát hoặc không có dữ liệu thì không cho lập. | [ĐẶC TẢ] §5 PAY-02; [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-04] |
| PAY-03 | Thành tiền dòng = sản lượng × đơn giá tại thời điểm tính (khi xem trước và khi lưu). Tổng gồm thuế GTGT, làm tròn lên theo đồng. | [ĐẶC TẢ] §5 PAY-03; [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-01, OQ-US03-03] |
| PAY-04 | Kiểm tra tổng âm, dòng bắt buộc, chống trình trùng thuộc US-PAY-02; không là điều kiện lập Draft. | [ĐẶC TẢ] §4.2, PAY-04 |
| PAY-05 | Approved không sửa; điều chỉnh qua hồ sơ riêng của US-PAY-04, ngoài luồng này. | [ĐẶC TẢ] PAY-05; [GIẢ ĐỊNH – Cần xác nhận: OQ-03] |
| PAY-06, PAY-07 | Thuộc US-PAY-03. Luồng này ghi `createdBy` = NVKD tạo bảng ở Draft để US-PAY-03 kiểm tra PAY-07. | [ĐẶC TẢ] PAY-06, PAY-07; [GIẢ ĐỊNH – Cần xác nhận: OQ-US03-01] |
| PAY-08 | Bảng Rejected về Draft khi NVKD bấm “Chỉnh sửa” (đặc tả ở SYS-US-03 §1.5), sau đó sửa theo §1.5 của file này. | [ĐẶC TẢ] §3, PAY-08; [GIẢ ĐỊNH – Cần xác nhận: OQ-04, OQ-US03-07] |
| NFR-PAY-01 | Audit create, update (và reopen ở SYS-US-03): ai, lúc nào, thay đổi gì. | [ĐẶC TẢ] §6 gạch 1 |
| NFR-PAY-02 | ≤ 3 giây với hợp đồng < 200 dòng; đo từ lúc server nhận yêu cầu lập (Lưu nháp) đến khi trả kết quả đã lưu; đếm dòng sau gộp. Chưa đo. | [ĐẶC TẢ] §6 gạch 2; [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-06] |

### 1.2. Thông tin chung

| Mục | Đặc tả |
|---|---|
| Tên | SYS-US-01 – Lập bảng thanh toán. [ĐẶC TẢ] [TA-SPEC §4.1] |
| Tác nhân chính | NVKD **được phân công phụ trách hợp đồng**. [ĐẶC TẢ] §2, §4.1; [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-03] |
| Tác nhân liên quan | Module Hợp đồng, Bảng giá, Sản lượng (chỉ đọc qua interface). [ĐẶC TẢ] §1 |
| Mục tiêu | Có bảng Draft được sinh tự động từ nguồn chỉ đọc. [ĐẶC TẢ] §4.1 |
| Kích hoạt | NVKD bấm “Lập bảng thanh toán”. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1] |
| P1 – Người dùng | Đã xác thực, giữ vai trò NVKD (mỗi người dùng một vai trò). [ĐẶC TẢ] §2; [GIẢ ĐỊNH – Cần xác nhận: OQ-US03-01] |
| P2 – Hợp đồng | NVKD được phân công hợp đồng; hợp đồng Active tại thời điểm lập. Hợp đồng đã hết hiệu lực không lập bù. [ĐẶC TẢ] PAY-01; [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-03, OQ-US01-05] |
| P3 – Kỳ | Kỳ đúng cấu hình của hợp đồng (tháng hoặc quý); khoảng ngày của kỳ không chồng lấn bảng chưa hủy nào của hợp đồng. [ĐẶC TẢ] §2, PAY-01; [GIẢ ĐỊNH – Cần xác nhận: OQ-01, OQ-US05-02] |
| P4 – Nguồn | Hợp đồng có đúng một bảng giá Active gắn với hợp đồng; kỳ có bản ghi sản lượng và tất cả đã đối soát. [ĐẶC TẢ] PAY-01, PAY-02; [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-01, OQ-US01-04] |
| Hậu điều kiện thành công | Bảng ở Draft gồm: hợp đồng, kỳ (ngày bắt đầu/kết thúc), `createdBy`, bảng giá đã dùng, các dòng (dịch vụ, sản lượng gộp, đơn giá lúc lưu, thành tiền), danh sách bản ghi sản lượng nguồn của từng dòng, tạm tính, thuế suất, tiền thuế, tổng, ghi chú, version; audit create cùng giao dịch. [ĐẶC TẢ] §4.1, §6; [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-01, OQ-US01-04, OQ-US03-03]; lưu version: [ĐỀ XUẤT KỸ THUẬT] |
| Hậu điều kiện lỗi | Không có bảng/dòng/audit lưu một phần; form giữ lựa chọn và báo đúng lý do. Kết quả commit chưa rõ không bị báo là chưa tạo. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §6] |
| NFR-PAY-01 | Áp dụng cho create và update; mở form/xem trước không đổi bảng nên không ghi audit thay đổi bảng. [ĐẶC TẢ] §6 gạch 1 |
| NFR-PAY-02 | Áp dụng cho thao tác lưu nháp (bước 11–13). Cách đo: server nhận yêu cầu E5 → trả kết quả đã lưu; số dòng = dòng thanh toán sau gộp; kiểm thử trên môi trường của nhóm với hợp đồng 199 dòng; đạt khi ≤ 3 giây. Chưa đo, không kết luận đạt. Không áp SLA cho sửa Draft hay xem trước. [ĐẶC TẢ] §6 gạch 2; [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-06] |

**Dữ liệu trên biểu mẫu lập mới**

| Thông tin | NVKD | Hệ thống | Căn cứ |
|---|---|---|---|
| Hợp đồng | Chọn từ danh sách hợp đồng mình phụ trách. | Lọc theo phân công; kiểm tra Active; trả cấu hình kỳ và cảnh báo kỳ chưa lập trước ngày hết hạn. | PAY-01; OQ-US01-03, OQ-US01-05 |
| Kỳ thanh toán | Chọn kỳ theo cấu hình (tháng hoặc quý). | Kiểm tra cấu hình kỳ, chồng lấn khoảng ngày với bảng chưa hủy. | §2, PAY-01; OQ-01, OQ-US05-02 |
| Bảng giá | **Không chọn**, chỉ xem. | Tự lấy bảng giá Active gắn với hợp đồng tại thời điểm tính. | PAY-01, PAY-03; OQ-US01-01; R01-03 |
| Dòng, tạm tính, thuế, tổng | Chỉ xem. | Gộp sản lượng đã đối soát theo dịch vụ, tính tiền, thuế, tổng. | §2, PAY-02, PAY-03; OQ-US01-04, OQ-US03-03 |
| Ghi chú | Nhập (không bắt buộc). | Lưu cùng bảng. | [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-02] |

**Quy tắc tính tiền** [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-04, OQ-US03-03]; công thức dòng: [ĐẶC TẢ] PAY-03

1. Mỗi dịch vụ trong kỳ là một dòng: `sảnLượng = Σ` sản lượng các bản ghi Đã đối soát của dịch vụ đó; lưu danh sách mã bản ghi nguồn để truy vết.
2. `thànhTiền = ceil(sảnLượng × đơnGiá)` (làm tròn lên theo đồng); đơn giá lấy từ bảng giá Active tại thời điểm tính.
3. `tạmTính = Σ thànhTiền`; `tiềnThuế = ceil(tạmTính × thuếSuất)`; thuế suất là tham số cấu hình, mặc định 10%.
4. `tổng = tạmTính + tiềnThuế` (đã là số nguyên đồng, bước làm tròn lên ở tổng không đổi giá trị).
5. Tổng này là tổng dùng so ngưỡng 500.000.000 đ ở US-PAY-02/03 (R01-02).

### 1.3. Dòng cơ bản – lập bảng

| Bước | Tác nhân | Hành động và phản hồi |
|---|---|---|
| 1 | NVKD | Bấm “Lập bảng thanh toán”. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.1] |
| 2 | Hệ thống | Kiểm tra phiên và vai trò NVKD; đọc danh sách hợp đồng NVKD được phân công. Chưa ghi bảng. [ĐẶC TẢ] §2; [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-03] |
| 3 | Hệ thống | Hiển thị biểu mẫu với danh sách hợp đồng. [ĐỀ XUẤT KỸ THUẬT] |
| 4 | NVKD | Chọn hợp đồng. [ĐẶC TẢ] §4.1 |
| 5 | Hệ thống | Đọc hợp đồng; kiểm tra tồn tại, NVKD được phân công, Active tại thời điểm lập. Trả cấu hình kỳ, danh sách kỳ còn trống và **cảnh báo các kỳ chưa lập bảng trước ngày hợp đồng hết hạn**. [ĐẶC TẢ] PAY-01; [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-03, OQ-US01-05, OQ-01] |
| 6 | NVKD | Chọn kỳ theo cấu hình của hợp đồng (tháng hoặc quý). [ĐẶC TẢ] §2, §4.1 |
| 7 | Hệ thống | Kiểm tra kỳ đúng cấu hình; tra chồng lấn khoảng ngày với các bảng **khác Cancelled** của hợp đồng; tự xác định bảng giá Active gắn với hợp đồng. Không có bảng giá Active thì dừng (A7). [ĐẶC TẢ] §2, PAY-01; [GIẢ ĐỊNH – Cần xác nhận: OQ-01, OQ-US05-02, OQ-US01-01] |
| 8 | Hệ thống | Đọc sản lượng của kỳ; kiểm tra có dữ liệu và mọi bản ghi Đã đối soát; gộp theo dịch vụ; tính thành tiền, tạm tính, thuế, tổng theo §1.2; lập `calculationContext` (bảng giá + version/đơn giá, danh sách bản ghi nguồn, thuế suất). Kết quả là **xem trước, chưa lưu**. [ĐẶC TẢ] PAY-02, PAY-03; [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-04, OQ-US03-03]; context: [ĐỀ XUẤT KỸ THUẬT] |
| 9 | Hệ thống | Hiển thị dòng (dịch vụ, sản lượng, đơn giá, thành tiền), bảng giá đã dùng (chỉ đọc), tạm tính, thuế suất, tiền thuế, tổng. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §2, §4.1] |
| 10 | NVKD | Kiểm tra, nhập ghi chú nếu cần, bấm “Lưu nháp”; gửi hợp đồng, kỳ, ghi chú và `calculationContext`. Không gửi số tiền làm số liệu quyết định. [ĐỀ XUẤT KỸ THUẬT] |
| 11 | Hệ thống | Kiểm tra lại phía server: phiên, vai trò, phân công, hợp đồng Active, chồng lấn kỳ, bảng giá Active, đối soát; **tính lại** theo giá tại thời điểm lưu và so với `calculationContext`. Khác nhau (giá hoặc bản ghi nguồn đã đổi) thì không lưu, trả kết quả tính mới và báo NVKD (A11.2). [ĐẶC TẢ] PAY-01..03; [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-01] |
| 12 | Hệ thống | Trong một giao dịch: lưu bảng Draft (`createdBy` = NVKD), dòng, liên kết dòng – bản ghi nguồn, tổng và audit create (ai, lúc nào, trước = chưa có bảng, sau = dữ liệu đã lưu); bảo đảm không chồng lấn kỳ một cách nguyên tử. [ĐẶC TẢ] §3, §4.1, PAY-01, §6; [GIẢ ĐỊNH – Cần xác nhận: OQ-01, OQ-US05-02, OQ-US03-01]; giao dịch: [ĐỀ XUẤT KỸ THUẬT] |
| 13 | Hệ thống | Sau commit thành công, hiển thị bảng Draft với id, version, dòng và tổng. Chưa trình duyệt. [ĐẶC TẢ] §4.1 |

### 1.4. Dòng thay thế

| Nhánh | Rẽ từ | Xử lý |
|---|---|---|
| A2 | 2 và mọi yêu cầu sau | Chưa xác thực → 401 `UNAUTHENTICATED`; không phải NVKD → 403 `FORBIDDEN`. Không tải dữ liệu, không ghi bảng. [ĐẶC TẢ] §2; [ĐỀ XUẤT KỸ THUẬT] mã lỗi |
| A3 | 2–3 | Lỗi đọc danh sách → 503 `SOURCE_UNAVAILABLE`, cho thử lại. Danh sách rỗng → báo “Chưa có hợp đồng được phân công”, không tạo bảng rỗng. [ĐỀ XUẤT KỸ THUẬT] |
| A5 | 5 | Hợp đồng không tồn tại → 404 `NOT_FOUND`; NVKD không được phân công → 403 `FORBIDDEN`; không Active tại thời điểm lập (kể cả đã hết hiệu lực) → 409 `CONTRACT_NOT_ACTIVE`, không lập bù. Quay bước 4. [AC dẫn xuất] PAY-01; [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-03, OQ-US01-05] |
| A7 | 7 | Kỳ sai cấu hình → 400 `INVALID_PERIOD`; khoảng ngày chồng lấn bảng chưa hủy (vd. đã có tháng 1 thì không lập quý I; đã có quý II thì không lập tháng 4–6) → 409 `PAYMENT_EXISTS`, quay bước 6. Không có bảng giá Active, hoặc có nhiều hơn một → 409 `PRICE_NOT_SUITABLE`, không cho lập. Bảng Cancelled không chặn. [AC dẫn xuất] PAY-01; [GIẢ ĐỊNH – Cần xác nhận: OQ-01, OQ-US05-02, OQ-US01-01] |
| A8 | 8 | Kỳ không có bản ghi sản lượng → 409 `QUANTITY_EMPTY`; còn bản ghi chưa đối soát → 409 `QUANTITY_NOT_RECONCILED`; báo lý do, không coi thiếu là 0, không cho lập. Dịch vụ có sản lượng nhưng bảng giá Active không có đơn giá → 409 `PRICE_NOT_SUITABLE`. [AC dẫn xuất] PAY-02, PAY-03; [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-04, OQ-US01-01] |
| A10 | 2, 5, 7, 8, 11 | Lỗi đọc module nguồn → 503 `SOURCE_UNAVAILABLE`; giữ lựa chọn, cho thử lại; không coi lỗi đọc là “không có dữ liệu”. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §1] |
| A10.1 | 4–9 | NVKD đổi hợp đồng: xóa kỳ và kết quả xem trước, quay bước 5. Đổi kỳ: xóa kết quả xem trước, quay bước 7. Phản hồi của lựa chọn cũ đến muộn bị bỏ qua. [ĐỀ XUẤT KỸ THUẬT] |
| A10.2 | 1–10 | NVKD đóng biểu mẫu trước khi lưu: không tạo bảng, không audit; không phải thao tác hủy (Cancelled) của US-PAY-05. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.5] |
| A11.1 | 11 | Điều kiện không còn đạt (hợp đồng hết Active, kỳ vừa bị chiếm, bảng giá không còn Active, sản lượng không còn đối soát): trả mã lỗi như A5/A7/A8, không ghi bảng. [AC dẫn xuất] PAY-01..03 |
| A11.2 | 11 | Giá hoặc bản ghi nguồn đổi giữa lúc xem trước và lúc lưu → 409 `SOURCE_CHANGED` kèm kết quả tính mới; không lưu; NVKD xem lại (quay bước 9) và bấm “Lưu nháp” lần nữa. [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-01] |
| A12 | 12 | Yêu cầu khác vừa lưu bảng chồng lấn kỳ (vi phạm ràng buộc khi ghi) → rollback, 409 `PAYMENT_EXISTS`; không tạo bảng thứ hai. [ĐỀ XUẤT KỸ THUẬT] PAY-01 |
| A12.1 | 12 | Lỗi mở giao dịch, ghi bảng/dòng/audit hoặc commit xác định chưa xảy ra → rollback, 500 `PERSISTENCE_ERROR`, không lưu một phần. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §6] |
| A12.2 | 12 | Mất kết quả commit → 503 `RESULT_UNKNOWN`; không tự gửi lại; NVKD kiểm tra bằng E7 (tra bảng theo hợp đồng/kỳ) trước khi lưu lại. [ĐỀ XUẤT KỸ THUẬT] |

### 1.5. Sửa bảng Draft đã lưu

[GIẢ ĐỊNH – Cần xác nhận: OQ-US01-02, OQ-US01-01, OQ-US01-03] Sản lượng, đơn giá, thành tiền và thông tin hợp đồng **khóa, chỉ đọc từ nguồn**. NVKD chỉ (a) sửa ghi chú, (b) dùng “Tải lại dữ liệu nguồn” để hệ thống tính lại toàn bộ dòng và tổng. Bảng Draft giữ đơn giá lúc lưu; số liệu chỉ tính lại khi NVKD tải lại nguồn rồi lưu. Hai đề xuất OQ-US01-01 (“chỉ tính lại khi NVKD sửa và lưu lại”) và OQ-US01-02 (“tải lại dữ liệu nguồn”) được hiểu chung như vậy; cách hiểu này cần nhóm xác nhận.

| Bước | Hành động và phản hồi |
|---|---|
| U1 | NVKD mở bảng và bấm “Chỉnh sửa”. Nếu bảng đang Rejected, hệ thống chuyển Rejected → Draft theo SYS-US-03 §1.5 (có audit) rồi tiếp tục U2. [ĐẶC TẢ] §4.1, PAY-08; [GIẢ ĐỊNH – Cần xác nhận: OQ-04, OQ-US03-07] |
| U2 | Hệ thống kiểm tra phiên, vai trò NVKD, NVKD được phân công hợp đồng của bảng (**không bắt buộc là người lập**), bảng đang Draft; hiển thị biểu mẫu: số liệu chỉ đọc, ô ghi chú, nút “Tải lại dữ liệu nguồn”, version. [ĐẶC TẢ] §4.1; [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-03, OQ-US01-02] |
| U3 | NVKD sửa ghi chú và/hoặc bấm “Tải lại dữ liệu nguồn”. Với tải lại, hệ thống đọc lại hợp đồng, bảng giá Active, sản lượng; kiểm tra PAY-01..03 như bước 5, 7, 8 (bỏ qua chính bảng này khi tra chồng lấn); tính lại toàn bộ dòng/tổng và hiển thị kết quả xem trước, chưa lưu. [ĐẶC TẢ] PAY-01..03; [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-02] |
| U4 | NVKD bấm “Lưu thay đổi”, gửi `expectedVersion`, ghi chú, cờ `reloadSource` và `calculationContext` (nếu đã tải lại). Server đọc bảng, kiểm tra quyền/trạng thái/version. Nếu `reloadSource`: kiểm tra lại PAY-01..03, tính lại và so với context (khác → AU4.2). Nếu không: giữ nguyên dòng, đơn giá, tổng đã lưu. [ĐỀ XUẤT KỸ THUẬT]; [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-01, OQ-US01-02] |
| U5 | Trong một giao dịch: cập nhật có điều kiện (trạng thái Draft, version khớp), tăng version, ghi audit update với trước/sau (ghi chú; và dòng/tổng nếu tải lại). [ĐẶC TẢ] §6; [ĐỀ XUẤT KỸ THUẬT] DD-02 |
| U6 | Trả và hiển thị dữ liệu đã lưu, trạng thái Draft, version mới. [ĐẶC TẢ] §4.1 |

| Nhánh | Rẽ từ | Xử lý |
|---|---|---|
| AU1 | U1, U4 | Bảng không tồn tại → 404 `NOT_FOUND`; lỗi đọc → 503; không mở form từ dữ liệu thiếu. [ĐỀ XUẤT KỸ THUẬT] |
| AU2 | U2, U4 | Chưa xác thực/không phải NVKD/không được phân công → 401/403; bảng PendingApproval, Approved, Cancelled → 409 `INVALID_STATE`. Approved điều chỉnh qua US-PAY-04. [AC dẫn xuất] §3, PAY-05; [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-03] |
| AU3 | U3 | Tải lại nguồn không đạt PAY-01..03 → trả mã lỗi như A5/A7/A8; bảng đã lưu giữ nguyên. NVKD có thể hủy bảng theo US-PAY-05 nếu không còn cần. [AC dẫn xuất] PAY-01..03 |
| AU4 | U4 | Gửi trường khóa (sản lượng, đơn giá, thành tiền, hợp đồng, kỳ) → 400 `FIELD_NOT_EDITABLE`; thiếu version → 400 `VERSION_REQUIRED`. Giữ form. [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-02]; [ĐỀ XUẤT KỸ THUẬT] mã lỗi |
| AU4.2 | U4 | Nguồn đổi sau lần tải lại → 409 `SOURCE_CHANGED` kèm kết quả mới; không lưu, NVKD xem lại rồi lưu lại. [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-01] |
| AU5 | U5 | 0 dòng được cập nhật (trạng thái/version đã đổi) → rollback, 409 `CONCURRENT_MODIFICATION`; client đọc lại bằng E6. [ĐỀ XUẤT KỸ THUẬT] DD-02 |
| AU5.1 | U5 | Lỗi lưu/audit/commit xác định chưa commit → rollback, 500 `PERSISTENCE_ERROR`; mất kết quả commit → 503 `RESULT_UNKNOWN`. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §6] |

**Quy tắc mã lỗi khi cập nhật đồng thời (R01-14)** [ĐỀ XUẤT KỸ THUẬT]: trạng thái đọc được không cho phép thao tác → `INVALID_STATE`; cập nhật có điều kiện trả 0 dòng → `CONCURRENT_MODIFICATION`; vi phạm ràng buộc không chồng lấn kỳ → `PAYMENT_EXISTS`. Áp dụng chung cho SYS-US-02..05.

## 2. Điểm cần xác nhận

Theo mẫu 9 cột [rules/common.md](../../../../rules/common.md) (R01-28). “Nhóm đề xuất” = nhóm 3 đã chọn cách xử lý trong báo cáo đánh giá; **chưa có xác nhận của khách hàng**, nên các phần dùng đề xuất mang nhãn [GIẢ ĐỊNH – Cần xác nhận].

| ID | Vị trí mọi nguồn | Loại | Mô tả | Lý do cần xác nhận | Lựa chọn (đề xuất nhóm áp dụng ở v2) | Ảnh hưởng tới Phần 1 | Trạng thái | Người/ngày/câu trả lời và tham chiếu |
|---|---|---|---|---|---|---|---|---|
| OQ-01 | TA-SPEC §2 “tháng hoặc quý tùy cấu hình” ↔ §5 PAY-01 “mỗi tháng” | Mâu thuẫn | Giới hạn một bảng tính theo tháng hay theo kỳ cấu hình; tháng/quý có chồng lấn? | Quyết định cách kiểm tra trùng kỳ | Kỳ theo cấu hình hợp đồng; mỗi hợp đồng một bảng cho mỗi khoảng thời gian; kiểm tra chồng lấn theo khoảng ngày | P3, bước 5, 7, 11, 12; A7, A12; AC-06, AC-14 | Nhóm đề xuất | Nhóm 3 – báo cáo đánh giá, bảng II.2 (10/2026) |
| OQ-US01-01 | §4.1 “từ sản lượng và bảng giá”; PAY-01 “bảng giá phù hợp”; PAY-03 “tại thời điểm tính”; R01-03 | Mơ hồ | Mốc chọn đơn giá, liên kết hợp đồng, giá đổi giữa xem trước/lưu và trong Draft | Tránh sai số tiền | Tự lấy bảng giá Active gắn với hợp đồng khi xem trước và khi lưu; NVKD không chọn; giá đổi thì tính lại và báo; Draft giữ đơn giá lúc lưu; không có bảng giá Active thì không lập | P4, bước 7, 8, 11; A7, A8, A11.2; §1.5; AC-08, 09, 26 | Nhóm đề xuất | Nhóm 3 – bảng II.2; R01-03 (Đúng) |
| OQ-US01-02 | §4.1 “được phép chỉnh sửa… Draft”; PAY-01..03 | Thiếu | Trường được sửa, trường server tính, điều kiện đọc lại nguồn | Tách quyền sửa bảng khỏi dữ liệu nguồn | Khóa sản lượng, đơn giá, thành tiền, thông tin hợp đồng; NVKD chỉ sửa ghi chú và “Tải lại dữ liệu nguồn” | §1.5 U2–U4, AU4; AC-17, 29, 30 | Nhóm đề xuất | Nhóm 3 – bảng II.2 |
| OQ-US01-03 | §2 “NVKD… lập”; §4.1 “NVKD… chỉnh sửa”; PAY-07 | Thiếu | Phạm vi hợp đồng được lập; sửa Draft của người khác | Quyền xem ≠ quyền lập/sửa | NVKD chỉ lập cho hợp đồng mình phụ trách; sửa mọi Draft thuộc hợp đồng đó, không bắt buộc là người lập | Tác nhân, P2, bước 2, 5, 11; U2; A5, AU2; AC-03 | Nhóm đề xuất | Nhóm 3 – bảng II.2 |
| OQ-US01-04 | §2 “một dịch vụ trong bảng”; §4.1; PAY-02, PAY-03 | Thiếu | Sản lượng rỗng, nhiều bản ghi cùng dịch vụ, đối soát một phần | Tránh bỏ sót/tính nhầm | Chỉ dùng bản ghi đã đối soát; gộp theo dịch vụ, lưu danh sách bản ghi nguồn; còn bản ghi chưa đối soát hoặc không có dữ liệu thì không lập; không coi thiếu là 0 | P4, bước 8; A8; AC-10, 28 | Nhóm đề xuất | Nhóm 3 – bảng II.2 |
| OQ-US01-05 | PAY-01 “đang hiệu lực (Active)”; §2 kỳ thanh toán | Mơ hồ | Mốc kiểm tra Active; kỳ quá khứ/hiệu lực một phần | Tránh loại nhầm kỳ hợp lệ | Active tại thời điểm lập; hết hiệu lực không lập bù; cảnh báo kỳ chưa lập trước ngày hết hạn | P2, bước 5, 11; A5; AC-05, 27 | Nhóm đề xuất | Nhóm 3 – bảng II.2 |
| OQ-US01-06 | §6 gạch 2 “3 giây… dưới 200 dòng” | Thiếu | Điểm đo, cách đếm dòng, môi trường | Cần phép đo thống nhất | Server nhận yêu cầu lập → trả kết quả đã lưu; đếm dòng sau gộp; môi trường nhóm, hợp đồng 199 dòng; đạt khi ≤ 3 giây | NFR-PAY-02; AC-20 | Nhóm đề xuất | Nhóm 3 – bảng II.2; R01-27 (Đúng) |
| OQ-US01-07 | §4.1–4.3; PAY-01..04; R01-08 | Thiếu | Có kiểm tra lại dữ liệu nguồn sau khi lưu Draft? | Nguồn có thể đổi giữa lập và trình/duyệt | Kiểm tra lại PAY-01..03 khi trình (SYS-US-02) và khi duyệt (SYS-US-03); chặn nếu nguồn không còn đạt. Ở US-01: tái kiểm tra khi lưu (bước 11) và khi tải lại (U3) | Bước 11; U3; AC-26 | Nhóm đề xuất | Nhóm 3 – bảng III, R01-08 (Đúng) |
| OQ-US05-02 | §4.5 “không dùng lại được” ↔ PAY-01 “một bảng… mỗi tháng” | Mơ hồ | Bảng Cancelled có chiếm kỳ không? | Nếu chiếm, kỳ đó không lập được nữa | Được lập bảng mới cho cùng kỳ; Cancelled chỉ để tra cứu/audit, không tính vào giới hạn; kiểm tra trùng chỉ xét bảng chưa hủy | P3, bước 7, 12; A7; AC-07 | Nhóm đề xuất | Nhóm 3 – bảng II.2 |
| OQ-US03-01 | PAY-07; §2; §4.3 | Mơ hồ | Ai là người lập; một người nhiều vai trò | US-01 phải lưu đúng người lập | Người lập là người tạo bảng ở Draft; mỗi người dùng một vai trò | P1, bước 12 (`createdBy`) | Nhóm đề xuất | Nhóm 3 – bảng II.2 |
| OQ-US03-03 | §4.1, §4.3, PAY-03, PAY-06; R01-02 | Thiếu | Tổng: thời điểm, VAT, làm tròn | Tổng quyết định người duyệt | Tổng đã lưu lúc lập, gồm thuế GTGT; thuế suất % cấu hình, mặc định 10%; làm tròn lên theo đồng ở dòng, thuế và tổng; chỉ sửa ở Draft | Quy tắc tính tiền §1.2; bước 8, 11; AC-11, 12 | Nhóm đề xuất | Nhóm 3 – bảng II.2; R01-02 (Đúng) |
| OQ-03 | §4.4 ↔ PAY-05 | Mâu thuẫn | Điều chỉnh bảng Approved (thuộc US-PAY-04) | Ranh giới với sửa Draft | Bảng Approved giữ nguyên; điều chỉnh là hồ sơ riêng (SYS-US-04) | §1.1 PAY-05; AU2 | Nhóm đề xuất | Nhóm 3 – bảng II.2 |
| OQ-04 | §3 “Rejected” ↔ PAY-08 “quay về Draft” | Mâu thuẫn | Đích sau từ chối | Ảnh hưởng mở sửa | Từ chối → Rejected; về Draft khi NVKD mở chỉnh sửa | U1; AC-18 | Nhóm đề xuất | Nhóm 3 – bảng II.2 |
| OQ-US03-07 | §3; PAY-08 | Thiếu | Ai/khi nào Rejected → Draft | Ảnh hưởng mở sửa | Khi NVKD bấm “Chỉnh sửa”; chuyển trạng thái được audit | U1; AC-18 | Nhóm đề xuất | Nhóm 3 – bảng II.2 |

## 3. Acceptance criteria

Mã `AC-US01-kk` do nhóm đặt, không phải mã của đề. Giữ ID v1; AC dựa trên đề xuất nhóm ghi OQ ở cột cuối và chưa coi là đã được khách hàng xác nhận.

| ID | Given / When / Then | Nhãn | Nguồn | OQ |
|---|---|---|---|---|
| AC-US01-01 | Given dữ liệu hợp lệ; When NVKD đi bước 1–13; Then bảng, dòng, tổng lưu ở Draft, hiển thị id/version sau commit, chưa trình duyệt. | [AC dẫn xuất] | §4.1 | – |
| AC-US01-02 | Given chưa xác thực hoặc không phải NVKD; When gọi bất kỳ bước nào; Then 401/403, không ghi (A2). | [ĐỀ XUẤT KỸ THUẬT] | §2, §4.1 | – |
| AC-US01-03 | Given NVKD không được phân công hợp đồng X; When tải danh sách, chọn X hoặc sửa Draft của X; Then X không có trong danh sách và thao tác bị 403 (A5, AU2). Given NVKD B được phân công X; When sửa Draft do NVKD A lập; Then được phép. | [GIẢ ĐỊNH – Cần xác nhận] | §2, §4.1 | OQ-US01-03 |
| AC-US01-04 | Given thiếu/sai hợp đồng hoặc kỳ; When chọn hoặc lưu; Then báo lỗi tại trường, không ghi Draft (A5, A7). | [AC dẫn xuất] | §4.1 | – |
| AC-US01-05 | Given hợp đồng không Active tại thời điểm lập (kể cả đã hết hạn sau kỳ cần lập); When chọn (5) hoặc lưu (11); Then 409 `CONTRACT_NOT_ACTIVE`, không lập bù. | [GIẢ ĐỊNH – Cần xác nhận] | PAY-01 | OQ-US01-05 |
| AC-US01-06 | Given hợp đồng kỳ quý đã có bảng tháng 1 chưa hủy; When lập quý I; Then 409 `PAYMENT_EXISTS`. Given đã có bảng quý II; When lập tháng 5; Then 409. Given kỳ sai cấu hình; Then 400 `INVALID_PERIOD`. | [GIẢ ĐỊNH – Cần xác nhận] | §2, PAY-01 | OQ-01 |
| AC-US01-07 | Given bảng cùng kỳ đã Cancelled và không có bảng chưa hủy chồng lấn; When lập; Then được lập bảng mới, bảng cũ giữ Cancelled. | [GIẢ ĐỊNH – Cần xác nhận] | §4.5, PAY-01 | OQ-US05-02 |
| AC-US01-08 | Given hợp đồng không có (hoặc có nhiều hơn một) bảng giá Active; When chọn kỳ hoặc lưu; Then 409 `PRICE_NOT_SUITABLE`, không lập. | [GIẢ ĐỊNH – Cần xác nhận] | PAY-01 | OQ-US01-01 |
| AC-US01-09 | Given form lập mới; When xem trước và lưu; Then hệ thống tự dùng bảng giá Active gắn hợp đồng, NVKD không có thao tác chọn bảng giá; bảng giá đã dùng hiển thị chỉ đọc. | [GIẢ ĐỊNH – Cần xác nhận] | §4.1, PAY-01, PAY-03; R01-03 | OQ-US01-01 |
| AC-US01-10 | Given kỳ không có bản ghi sản lượng, hoặc còn bản ghi chưa đối soát; When tính (8) hoặc lưu (11); Then 409 `QUANTITY_EMPTY` / `QUANTITY_NOT_RECONCILED`, không lập, không thay bằng 0. | [GIẢ ĐỊNH – Cần xác nhận] | PAY-02 | OQ-US01-04 |
| AC-US01-11 | Given dịch vụ có sản lượng gộp q và đơn giá p; When tính; Then `thànhTiền = ceil(q × p)` theo đồng. | [AC dẫn xuất] | PAY-03 | OQ-US03-03 (làm tròn) |
| AC-US01-12 | Given các dòng đã tính và thuế suất cấu hình t (mặc định 10%); When tính tổng; Then `tạmTính = Σ thànhTiền`, `tiềnThuế = ceil(tạmTính × t)`, `tổng = tạmTính + tiềnThuế`; tổng này lưu trên bảng và dùng so ngưỡng ở US-02/03. | [GIẢ ĐỊNH – Cần xác nhận] | §4.1, PAY-03; R01-02 | OQ-US03-03 |
| AC-US01-13 | Given lỗi đọc module nguồn; When tải form/chọn/tính/lưu; Then 503 `SOURCE_UNAVAILABLE`, giữ lựa chọn, không ghi (A3, A10, AU1). | [ĐỀ XUẤT KỸ THUẬT] | §1 | – |
| AC-US01-14 | Given hai yêu cầu lưu cùng chồng lấn một khoảng ngày; When ghi (12); Then nhiều nhất một bảng được tạo, yêu cầu thua 409 `PAYMENT_EXISTS` (A12). | [AC dẫn xuất] / [ĐỀ XUẤT KỸ THUẬT] | PAY-01 | OQ-01, OQ-US05-02 |
| AC-US01-15 | Given lưu hợp lệ; When commit; Then bảng, dòng, liên kết bản ghi nguồn và audit create cùng tồn tại, audit có ai/lúc nào/thay đổi gì. | [AC dẫn xuất] | §6 gạch 1 | – |
| AC-US01-16 | Given lỗi giao dịch; When lưu (12/U5); Then lỗi xác định chưa commit không lưu một phần (A12.1/AU5.1); mất kết quả commit trả `RESULT_UNKNOWN` (A12.2). | [ĐỀ XUẤT KỸ THUẬT] | §6 gạch 1 | – |
| AC-US01-17 | Given bảng Draft, NVKD được phân công; When sửa ghi chú và lưu (U1–U6, không tải lại); Then chỉ ghi chú đổi, dòng/đơn giá/tổng giữ nguyên, version tăng, audit update có trước/sau. | [GIẢ ĐỊNH – Cần xác nhận] | §4.1, §6 | OQ-US01-02, OQ-US01-01 |
| AC-US01-18 | Given bảng PendingApproval, Approved hoặc Cancelled; When bấm “Chỉnh sửa”; Then 409 `INVALID_STATE`. Given bảng Rejected; When NVKD được phân công bấm “Chỉnh sửa”; Then bảng chuyển Draft (audit theo SYS-US-03) rồi mở form sửa. | [GIẢ ĐỊNH – Cần xác nhận] | §3, §4.1, PAY-08 | OQ-04, OQ-US03-07 |
| AC-US01-19 | Given representation có version; When tạo/đọc/sửa; Then response có version; thiếu version → 400 `VERSION_REQUIRED`; version cũ → 409 `CONCURRENT_MODIFICATION` (AU4, AU5). | [ĐỀ XUẤT KỸ THUẬT] | §4.1 | – |
| AC-US01-20 | Given hợp đồng có 199 dòng thanh toán sau gộp, môi trường kiểm thử của nhóm; When server nhận yêu cầu lưu nháp (E5); Then trả kết quả đã lưu trong ≤ 3 giây. Hợp đồng đúng 200 dòng không thuộc điều kiện này. | [GIẢ ĐỊNH – Cần xác nhận] | §6 gạch 2 | OQ-US01-06; chưa đo |
| AC-US01-21 | Given chưa chọn dữ liệu; When bấm “Lập bảng thanh toán” (1–3); Then mở form với danh sách hợp đồng được phân công, chưa ghi Draft; danh sách rỗng thì báo (A3). | [ĐỀ XUẤT KỸ THUẬT] | §4.1 | OQ-US01-03 |
| AC-US01-22 | Given form mở; When chọn hợp đồng (4–5) rồi kỳ (6–7); Then hệ thống tải dữ liệu phụ thuộc theo thứ tự và tự xác định bảng giá; không có bước chọn bảng giá. | [ĐỀ XUẤT KỸ THUẬT] | §4.1; R01-03 | OQ-US01-01 |
| AC-US01-23 | Given đã chọn đủ; When xem trước (8–9); Then hiển thị dòng, tạm tính, thuế, tổng; chỉ “Lưu nháp” mới ghi (10–13). | [ĐỀ XUẤT KỸ THUẬT] | §4.1 | – |
| AC-US01-24 | Given đã có kết quả xem trước; When đổi hợp đồng/kỳ (A10.1); Then xóa kết quả phụ thuộc và tính lại; bỏ phản hồi cũ đến muộn. | [ĐỀ XUẤT KỸ THUẬT] | §4.1, PAY-03 | – |
| AC-US01-25 | Given chưa lưu; When đóng form (A10.2); Then không có bảng hay audit được tạo. | [ĐỀ XUẤT KỸ THUẬT] | §3, §4.5 | – |
| AC-US01-26 | Given xem trước hợp lệ nhưng đơn giá hoặc bản ghi nguồn đổi trước khi lưu; When bấm “Lưu nháp” (11); Then 409 `SOURCE_CHANGED` kèm kết quả tính mới, không lưu; NVKD xem lại và lưu lại thì bảng dùng giá tại thời điểm lưu. | [GIẢ ĐỊNH – Cần xác nhận] | PAY-01..03 | OQ-US01-01, OQ-US01-07 |
| AC-US01-27 | Given hợp đồng có ngày hết hạn và còn kỳ trước ngày đó chưa có bảng chưa hủy; When NVKD chọn hợp đồng (5); Then hệ thống hiển thị cảnh báo liệt kê các kỳ chưa lập. | [GIẢ ĐỊNH – Cần xác nhận] | PAY-01 | OQ-US01-05 |
| AC-US01-28 | Given dịch vụ S có nhiều bản ghi đã đối soát trong kỳ; When sinh dòng; Then có đúng một dòng cho S với sản lượng bằng tổng các bản ghi, và lưu đủ danh sách bản ghi nguồn của dòng. | [GIẢ ĐỊNH – Cần xác nhận] | §2, PAY-02, PAY-03 | OQ-US01-04 |
| AC-US01-29 | Given bảng Draft; When gửi thay đổi sản lượng, đơn giá, thành tiền, hợp đồng hoặc kỳ; Then 400 `FIELD_NOT_EDITABLE`, bảng không đổi. | [GIẢ ĐỊNH – Cần xác nhận] | §4.1 | OQ-US01-02 |
| AC-US01-30 | Given bảng Draft và nguồn đã thay đổi; When NVKD bấm “Tải lại dữ liệu nguồn” rồi “Lưu thay đổi” (U3–U6); Then toàn bộ dòng và tổng được tính lại theo nguồn và giá hiện tại, audit update ghi trước/sau. Nếu nguồn không còn đạt PAY-01..03 thì báo lỗi và giữ dữ liệu cũ (AU3). | [GIẢ ĐỊNH – Cần xác nhận] | §4.1, PAY-01..03, §6 | OQ-US01-02, OQ-US01-07 |

## 4. Bàn giao

- Sequence cùng version: [seq-us-01-v2.puml](../../../design/payment-management/v2/diagrams/seq-us-01-v2.puml).
- Tên mới dùng tạm, cần đồng bộ vào `03-detailed-design-v2.md` và `04-api-contract-v2.md` (chưa tạo): mã lỗi `QUANTITY_EMPTY`, `SOURCE_CHANGED`, `FIELD_NOT_EDITABLE`; E3 đổi thành kiểm tra kỳ và trả bảng giá tự xác định; E4/E5 bỏ `priceListId` khỏi request; E8 nhận `{expectedVersion, note, reloadSource, calculationContext?}`.
- Dữ liệu cần đồng bộ vào `05-data-design-v2.md` (R01-15): giữ `price_list_id` trên bảng; thêm bảng liên kết dòng – bản ghi sản lượng nguồn; thêm cột kỳ bắt đầu/kết thúc, `subtotal`, `tax_rate`, `tax_amount`, `total_amount`, `note`.

## Thay đổi so với v1

| # | Vị trí | Thay đổi | Căn cứ (R-ID đã chấp nhận / OQ đã có đề xuất nhóm) |
|---|---|---|---|
| 1 | Đầu file, §1.2, §1.3 bước 7–9 | Bỏ bước NVKD chọn bảng giá và nhãn “QUYẾT ĐỊNH ĐÃ XÁC NHẬN – tương tác P-17”; hệ thống tự lấy bảng giá Active gắn hợp đồng. Dòng cơ bản rút từ 16 xuống 13 bước. | R01-03; OQ-US01-01 |
| 2 | §1.2 quy tắc tính tiền; bước 8; AC-11, 12 | Tổng gồm thuế GTGT (thuế suất cấu hình, mặc định 10%), làm tròn lên ở dòng, thuế, tổng. | R01-02; OQ-US03-03 |
| 3 | P3, bước 7, A7, AC-06, 07, 14 | Kiểm tra chồng lấn khoảng ngày tháng/quý với bảng chưa hủy; Cancelled không chặn lập lại. | OQ-01; OQ-US05-02 |
| 4 | P4, bước 8, A8, AC-10, 28 | Gộp sản lượng theo dịch vụ, lưu bản ghi nguồn; không có dữ liệu/chưa đối soát thì chặn. | OQ-US01-04; R01-15 (ghi cho 05) |
| 5 | P2, bước 5, A5, AC-05, 27 | Active tại thời điểm lập, không lập bù; cảnh báo kỳ chưa lập trước hạn. | OQ-US01-05 |
| 6 | Tác nhân, bước 2, 5, U2, AC-03 | Quyền theo phân công hợp đồng; sửa Draft của người khác cùng hợp đồng. | OQ-US01-03 |
| 7 | §1.5, AU4, AC-17, 29, 30 | Khóa số liệu nguồn; chỉ sửa ghi chú và “Tải lại dữ liệu nguồn”. | OQ-US01-02, OQ-US01-01 |
| 8 | Bước 11, A11.2, AU4.2, AC-26 | Giá/nguồn đổi giữa xem trước và lưu: tính lại và báo NVKD (`SOURCE_CHANGED`). | OQ-US01-01; OQ-US01-07 (R01-08) |
| 9 | U1, AC-18 | Bảng Rejected về Draft khi NVKD bấm “Chỉnh sửa” (audit ở SYS-US-03). | OQ-04, OQ-US03-07; R01-05 |
| 10 | NFR-PAY-02, AC-20 | Chốt cách đo đề xuất: E5 server nhận → trả; dòng sau gộp; 199 dòng. Vẫn chưa đo. | OQ-US01-06; R01-27 |
| 11 | §1.5 cuối | Thêm quy tắc ánh xạ mã lỗi khi cập nhật đồng thời. | R01-14 |
| 12 | §2 | Bảng OQ theo mẫu 9 cột; trạng thái “Nhóm đề xuất”; thêm OQ-US01-07. | R01-04, R01-28, R01-08 |
| 13 | §3 | AC giữ ID 01–26, cập nhật nội dung; thêm AC-27..30. | R01-17, R01-20 |
