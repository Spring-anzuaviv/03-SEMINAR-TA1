# SYS-US-03 – Duyệt hoặc từ chối bảng thanh toán (v1)

> Phiên bản: v1 · Ngày: 07/11/2026 · Người phụ trách: Đan Anh
> Đầu vào: [TA-SPEC](../../../requirements/payment-management/spec.md) §2, §3, §4.3, §5 PAY-05..08, §6; TA-PDF tr.1–3; [open-questions-v1.md](open-questions-v1.md); đề xuất của Đan Anh ngày 07/11/2026 (ghi ở open-questions-v1.md)
> AI: Claude Code / Claude Sonnet 5.5 · Prompt: P-03, P-04, P-05, P-06, P-07 trong [prompt-log](../../../workflow/prompt-log.md)
> Trạng thái: Bản lần chạy đầu – Design Pending Approval
> Bổ sung 09/11/2026: Phần 2 (tham chiếu OQ) và Phần 3 (AC) do Claude Code / Claude Opus 5.5 soạn theo P-22; Phần 1 giữ nguyên.
>
> Chỉ đánh dấu các đề xuất: **[GIẢ ĐỊNH – Cần xác nhận]** (do Đan Anh đề xuất, chưa được khách hàng xác nhận; xem open-questions-v1.md) và **[ĐỀ XUẤT KỸ THUẬT]**. Nội dung không có nhãn bám đề (TA-SPEC) hoặc suy ra trực tiếp từ đề.
> Mã `OQ-USNN-kk` là mã tự đặt. Đặc tả TA không bị sửa: chỗ đề còn mâu thuẫn chữ nghĩa (vd. PAY-06 "trên") vẫn giữ nguyên trong TA; tài liệu này ghi các đề xuất đang chờ khách hàng xác nhận.

## 1. Use case

| Mục | Đặc tả |
|---|---|
| **Tên** | SYS-US-03 – Duyệt hoặc từ chối bảng thanh toán [TA-SPEC §4.3; TA-PDF tr.2] |
| **Tác nhân chính** | Người duyệt theo **vai trò**: Giám đốc kinh doanh hoặc Kế toán trưởng tùy tổng tiền; Giám đốc kinh doanh và Kế toán trưởng **không duyệt thay nhau** [GIẢ ĐỊNH – Cần xác nhận] [OQ-US03-02].<br>Mỗi người dùng **một vai trò** [GIẢ ĐỊNH – Cần xác nhận] [OQ-US03-01]. |
| **Tác nhân liên quan** | Nhân viên kinh doanh – người tạo Draft; xem được lý do từ chối và là người chỉnh sửa bảng bị từ chối [GIẢ ĐỊNH – Cần xác nhận] [OQ-US03-04, OQ-US03-07]; là người nhận thông báo kết quả [GIẢ ĐỊNH – Cần xác nhận] [OQ-US03-05].<br>Module Hợp đồng/Bảng giá/Sản lượng: không tham gia [TA-SPEC §1].<br>Module kế toán: ngoài phạm vi [GIẢ ĐỊNH – Cần xác nhận] [OQ-US03-06]. |
| **Mục tiêu** | Người có thẩm quyền duyệt (→ `Approved`) hoặc từ chối kèm lý do bảng đang chờ duyệt [TA-SPEC §1, §4.3, PAY-08]. |
| **Kích hoạt** | Người duyệt chọn "Duyệt" hoặc "Từ chối" trên bảng `PendingApproval` (tên nút: [ĐỀ XUẤT KỸ THUẬT]). |
| **Tiền điều kiện** | **P1** Bảng tồn tại, ở `PendingApproval` [TA-SPEC §3, §4.2].<br>**P2** Người thao tác đã xác thực; vai trò đúng với tổng tiền: ≥ 500.000.000 đ → chỉ Giám đốc kinh doanh; < 500.000.000 đ → chỉ Kế toán trưởng [GIẢ ĐỊNH – Cần xác nhận] [OQ-02; TA-SPEC §4.3].<br>Tổng tiền là tổng **đã lưu tại thời điểm lập**, gồm VAT, làm tròn **từng dòng và tổng, làm tròn lên** theo đồng [GIẢ ĐỊNH – Cần xác nhận] [OQ-US03-03; cách hiểu ghi ở open-questions-v1.md]; thuế là VAT, dạng **một giá trị x (số tiền) hoặc một tỷ lệ % trên tổng** [GIẢ ĐỊNH – Cần xác nhận] [OQ-US03-03]; **giá trị cụ thể chờ khách hàng** (Cần xác nhận, **không chặn thiết kế**: không chốt giá trị).<br>Bảng chỉ sửa được ở `Draft` nên tổng không đổi trong lúc chờ duyệt [GIẢ ĐỊNH – Cần xác nhận] [OQ-US03-03; TA-SPEC §4.1].<br>**P3** Người thao tác không phải người tạo Draft, áp dụng cả duyệt và từ chối [GIẢ ĐỊNH – Cần xác nhận] [OQ-US03-01; PAY-07].<br>**P4** (từ chối) Lý do không rỗng, tối đa 500 từ [PAY-08]; [GIẢ ĐỊNH – Cần xác nhận] [OQ-US03-04]. |
| **Hậu điều kiện – duyệt** | Bảng ở `Approved`, khóa sửa theo PAY-05 [TA-SPEC §3, PAY-05] (điều chỉnh: US-PAY-04, OQ-03, không chặn US này).<br>Một bản ghi audit: ai, lúc nào, `PendingApproval` → `Approved` [TA-SPEC §6].<br>Có thông báo trong hệ thống [GIẢ ĐỊNH – Cần xác nhận] [OQ-US03-05] (người nhận: Nhân viên kinh doanh người tạo Draft).<br>Không chuyển kế toán trong module [GIẢ ĐỊNH – Cần xác nhận] [OQ-US03-06]. |
| **Hậu điều kiện – từ chối** | Bảng ở `Rejected`, lý do được lưu, Nhân viên kinh doanh xem được lý do [GIẢ ĐỊNH – Cần xác nhận] [OQ-04, OQ-US03-04; TA-SPEC §3, PAY-08].<br>Audit `PendingApproval` → `Rejected` kèm lý do [TA-SPEC §6].<br>Có thông báo trong hệ thống, **kèm lý do** [GIẢ ĐỊNH – Cần xác nhận] [OQ-US03-05] (người nhận: Nhân viên kinh doanh người tạo Draft).<br>Bước `Rejected` → `Draft` do **Nhân viên kinh doanh chỉnh sửa bảng bị từ chối**, không do hệ thống tự động trong thao tác từ chối [GIẢ ĐỊNH – Cần xác nhận] [OQ-US03-07]; thao tác này nằm ngoài US-PAY-03 (liên quan US-PAY-01/02) và có audit riêng theo §6. |
| **Hậu điều kiện – thất bại** | Trạng thái và dữ liệu giữ nguyên, không audit mồ côi; trả mã lỗi và lý do [TA-SPEC §6]. |
| **Dòng cơ bản – Duyệt** | **1.** Người duyệt gửi yêu cầu duyệt [TA-SPEC §4.3].<br>**2.** Hệ thống xác thực, lấy vai trò [ĐỀ XUẤT KỸ THUẬT] (AS-IS chưa có xác thực).<br>**3.** Đọc bảng; tồn tại.<br>**4.** Kiểm tra `PendingApproval` [TA-SPEC §3].<br>**5.** Xác định vai trò bắt buộc từ tổng tiền đã lưu (≥ 500.000.000 đ → Giám đốc kinh doanh, ngược lại Kế toán trưởng) và kiểm tra khớp vai trò người gọi [GIẢ ĐỊNH – Cần xác nhận] [OQ-02, OQ-US03-02, OQ-US03-03; PAY-06].<br>**6.** Kiểm tra người gọi khác người tạo Draft [GIẢ ĐỊNH – Cần xác nhận] [OQ-US03-01; PAY-07].<br>**7.** Trong một giao dịch: chuyển `Approved` bằng cập nhật có điều kiện theo trạng thái hiện tại, ghi audit [TA-SPEC §6; cơ chế có điều kiện: ĐỀ XUẤT KỸ THUẬT].<br>**8.** Sau commit, gửi thông báo trong hệ thống [GIẢ ĐỊNH – Cần xác nhận] [OQ-US03-05] (người nhận: Nhân viên kinh doanh người tạo Draft); lỗi thông báo không hoàn tác việc duyệt [ĐỀ XUẤT KỸ THUẬT].<br>**9.** Trả kết quả thành công, trạng thái `Approved`. |
| **Dòng cơ bản – Từ chối (R)** | Rẽ từ bước 1: người duyệt chọn từ chối, nhập lý do [TA-SPEC §4.3, PAY-08].<br>**R2–R6.** Như bước 2–6 (PAY-07 áp dụng cho cả từ chối).<br>**R7.** Kiểm tra lý do: không rỗng [PAY-08], không quá 500 từ [GIẢ ĐỊNH – Cần xác nhận] [OQ-US03-04]; chuỗi khoảng trắng coi là rỗng, cách đếm từ (tách theo khoảng trắng) [ĐỀ XUẤT KỸ THUẬT].<br>**R8.** Trong một giao dịch: chuyển `PendingApproval` → `Rejected`, lưu lý do, ghi audit kèm lý do [GIẢ ĐỊNH – Cần xác nhận] [OQ-04; TA-SPEC §6].<br>**R9.** Sau commit, gửi thông báo trong hệ thống kèm lý do từ chối (người nhận: Nhân viên kinh doanh người tạo Draft).<br>**R10.** Trả kết quả thành công, trạng thái `Rejected`, kèm lý do. |
| **Dòng thay thế** | **2a.** Chưa xác thực/không có vai trò duyệt → từ chối [TA-SPEC §2].<br>**3a.** Không tồn tại → không tìm thấy.<br>**4a.** Sai trạng thái (gồm đã bị người khác xử lý trước) → từ chối, không đổi dữ liệu, không audit [TA-SPEC §3].<br>**5a.** Sai vai trò theo tổng tiền (Kế toán trưởng với bảng ≥ 500 triệu; Giám đốc kinh doanh với bảng < 500 triệu) → từ chối [GIẢ ĐỊNH – Cần xác nhận] [OQ-02, OQ-US03-02].<br>**6a.** Người gọi là người tạo Draft → từ chối, cả duyệt lẫn từ chối [GIẢ ĐỊNH – Cần xác nhận] [OQ-US03-01; PAY-07].<br>**R7a.** Lý do rỗng → từ chối, giữ `PendingApproval` [PAY-08].<br>**R7b.** Lý do quá 500 từ → từ chối, giữ `PendingApproval` [GIẢ ĐỊNH – Cần xác nhận] [OQ-US03-04].<br>**7a.** Lỗi ghi dữ liệu hoặc audit → hoàn tác, giữ `PendingApproval`, báo lỗi [TA-SPEC §6].<br>**7b.** Hai yêu cầu đồng thời → một thành công, một bị từ chối như 4a [ĐỀ XUẤT KỸ THUẬT: cơ chế xử lý đồng thời; đề chỉ yêu cầu chống trùng cho trình duyệt, PAY-04]. |
| **Yêu cầu phi chức năng** | **NFR-PAY-01 áp dụng**: duyệt và từ chối đều đổi trạng thái → audit ai, lúc nào, thay đổi gì [TA-SPEC §6; TA-PDF tr.3].<br>**NFR-PAY-02 không áp dụng** (chỉ nói về lập bảng). |

## 2. Điểm cần xác nhận

Chi tiết từng OQ (vị trí nguồn, lựa chọn, đề xuất của Đan Anh, trạng thái) nằm trong
[open-questions-v1.md](open-questions-v1.md); bảng dưới chỉ nêu chỗ dùng trong Phần 1.
Tất cả **Cần xác nhận** – đề xuất của nhóm chưa có xác nhận khách hàng.

| ID | Loại | Vấn đề | Dùng ở Phần 1 |
|---|---|---|---|
| OQ-02 | Mâu thuẫn | Đúng 500.000.000 đ ai duyệt (§4.3 ↔ PAY-06) | P2, bước 5, 5a |
| OQ-04 | Mâu thuẫn | Đích sau từ chối: Rejected hay Draft (§3 ↔ PAY-08) | Hậu điều kiện từ chối, R8 |
| OQ-US03-01 | Mơ hồ | Ai là "người lập"; PAY-07 có áp cho từ chối | P3, bước 6, 6a |
| OQ-US03-02 | Mơ hồ | Duyệt theo vai trò hay cá nhân; thay thế chéo | Tác nhân chính, bước 5, 5a |
| OQ-US03-03 | Thiếu | Tổng so ngưỡng: thời điểm, VAT, làm tròn | P2, bước 5 |
| OQ-US03-04 | Thiếu | Ràng buộc/độ dài lý do; NVKD xem được không | P4, R7, R7b |
| OQ-US03-05 | Thiếu | Có thông báo kết quả không; người nhận; kênh | Bước 8, R9 |
| OQ-US03-06 | Mơ hồ | Chuyển kế toán sau Approved | Hậu điều kiện duyệt |
| OQ-US03-07 | Thiếu | Ai/khi nào Rejected → Draft | Hậu điều kiện từ chối |
| OQ-03 | Mâu thuẫn | Điều chỉnh Approved (thuộc US-PAY-04) | Hậu điều kiện duyệt |

## 3. Acceptance criteria

Mã `AC-US03-kk` là mã tự đặt (P-22, AI soạn từ Phần 1 và TA-SPEC; nhóm chưa duyệt).
AC có cột OQ khác "–" chưa được coi là đã đáp ứng.

| ID | Given / When / Then | Nhãn | Nguồn | OQ |
|---|---|---|---|---|
| AC-US03-01 | Given bảng `PendingApproval`, người gọi có vai trò đúng theo tổng và không phải người lập; When duyệt (bước 1–9); Then bảng `Approved`, có một bản ghi audit ai/lúc nào/`PendingApproval` → `Approved`. | [ĐẶC TẢ] | §3, §4.3, §6; TA-PDF tr.1–3 | Vai trò: Blocked by OQ-02, OQ-US03-02 |
| AC-US03-02 | Given như AC-01 và lý do hợp lệ; When từ chối (R1–R10); Then lý do được lưu, audit kèm lý do, bảng chuyển sang trạng thái đích sau từ chối. | [AC dẫn xuất] | §3, §4.3, PAY-08, §6 | Đích: Blocked by OQ-04 |
| AC-US03-03 | Given chưa xác thực hoặc không có vai trò KTT/GĐKD; When duyệt/từ chối; Then từ chối thao tác, không đổi dữ liệu (2a). | [AC dẫn xuất] | §2, §4.3 | – |
| AC-US03-04 | Given mã bảng không tồn tại; When duyệt/từ chối; Then báo không tìm thấy, không ghi audit (3a). | [AC dẫn xuất] | §4.3 | – |
| AC-US03-05 | Given bảng không ở `PendingApproval`; When duyệt/từ chối; Then từ chối, giữ nguyên trạng thái, không ghi audit (4a). | [AC dẫn xuất] | §3, §4.3 | – |
| AC-US03-06 | Given tổng dưới 500 triệu và người gọi là GĐKD, hoặc tổng trên 500 triệu và người gọi là KTT; When duyệt/từ chối; Then từ chối do sai người duyệt (5a). | [AC dẫn xuất] | §4.3, PAY-06 | OQ-US03-02 (thay thế chéo), OQ-US03-03 |
| AC-US03-07 | Given tổng đúng 500.000.000 đ; When xác định người duyệt (bước 5); Then áp dụng đúng phía được xác nhận, hệ thống không tự chọn KTT hay GĐKD. | [AC dẫn xuất] | §4.3 ↔ PAY-06 | Blocked by OQ-02 |
| AC-US03-08 | Given người gọi là người lập bảng; When duyệt; Then từ chối (6a, PAY-07). | [ĐẶC TẢ] | PAY-07 | Định nghĩa người lập: OQ-US03-01 |
| AC-US03-09 | Given người gọi là người lập bảng; When từ chối; Then xử lý theo phạm vi PAY-07 được xác nhận cho thao tác từ chối (6a). | [AC dẫn xuất] | PAY-07 | Blocked by OQ-US03-01 |
| AC-US03-10 | Given lý do rỗng hoặc chỉ có khoảng trắng; When từ chối; Then chặn, giữ `PendingApproval` (R7a). | [ĐẶC TẢ] | §4.3, PAY-08 | – |
| AC-US03-11 | Given lý do vượt giới hạn độ dài được xác nhận; When từ chối; Then chặn, giữ `PendingApproval` (R7b). | [GIẢ ĐỊNH – Cần xác nhận] | PAY-08 | Blocked by OQ-US03-04 |
| AC-US03-12 | Given lỗi ghi trạng thái hoặc audit; When duyệt/từ chối; Then rollback, giữ `PendingApproval`, không có audit mồ côi, báo lỗi (7a). | [AC dẫn xuất] | §6 | – |
| AC-US03-13 | Given hai yêu cầu duyệt/từ chối đồng thời trên cùng bảng; When xử lý; Then nhiều nhất một yêu cầu đổi trạng thái, yêu cầu còn lại bị từ chối như 4a (7b). | [ĐỀ XUẤT KỸ THUẬT] | §3, §6 | – |
| AC-US03-14 | Given duyệt/từ chối đã commit; When gửi thông báo kết quả; Then gửi theo quyết định được xác nhận; lỗi gửi không hoàn tác thay đổi đã lưu (bước 8, R9). | [GIẢ ĐỊNH – Cần xác nhận] | §4.3 | Blocked by OQ-US03-05 |
| AC-US03-15 | Given bảng đã `Approved`; When bất kỳ thao tác sửa nào ngoài US-PAY-04; Then bị từ chối (PAY-05). | [ĐẶC TẢ] | PAY-05 | Điều chỉnh: OQ-03 |