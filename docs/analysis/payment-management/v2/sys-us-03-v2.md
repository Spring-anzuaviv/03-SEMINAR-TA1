# SYS-US-03 – Duyệt hoặc từ chối bảng thanh toán (v2)

> Phiên bản: v2 · Ngày: 11/11/2026 · Người phụ trách: Nguyễn Ngọc Mai Xuân, Lê Hồ Đan Anh
> Đầu vào: [TA-SPEC](../../../requirements/payment-management/spec.md) §2, §3, §4.3, §5 PAY-01..08, §6; TA-PDF tr.1–3; sys-us-03-v1.md; [sys-us-01-v2.md](sys-us-01-v2.md), [sys-us-02-v2.md](sys-us-02-v2.md); Báo cáo đánh giá nhóm 3 – bảng II.2 cột “Cách nhóm xử lý” và bảng III (R01-xx Đúng)
> AI: Claude Code / Claude Opus 5.5 · Prompt: P-29 trong [prompt-log](../../../workflow/prompt-log.md)
> Trạng thái: Bản sau review – BA Pending Approval
> Nhãn: [ĐẶC TẢ] · [AC dẫn xuất] · [ĐỀ XUẤT KỸ THUẬT] · [GIẢ ĐỊNH – Cần xác nhận: OQ-…] = áp dụng cách xử lý **nhóm đề xuất**, chưa có xác nhận của khách hàng (R01-20). Mã `OQ-USNN-kk`, `AC-USNN-kk` là mã tự đặt. Đặc tả TA không bị sửa (PAY-06 vẫn ghi “trên”).

Phạm vi: duyệt (approve), từ chối (reject) bảng `PendingApproval`, và bước NVKD đưa bảng `Rejected` về `Draft` khi bấm “Chỉnh sửa” (reopen) theo R01-05.

## 1. Use case

### 1.1. Thông tin chung

| Mục | Đặc tả |
|---|---|
| Tên | SYS-US-03 – Duyệt hoặc từ chối bảng thanh toán [ĐẶC TẢ] [TA-SPEC §4.3; TA-PDF tr.2] |
| Tác nhân chính | Người duyệt **theo vai trò**: mọi người giữ vai trò GĐKD (tổng ≥ 500.000.000 đ) hoặc KTT (tổng < 500.000.000 đ); không cho vai trò khác duyệt thay; mỗi người dùng chỉ giữ một vai trò. [ĐẶC TẢ] §2, §4.3; [GIẢ ĐỊNH – Cần xác nhận: OQ-02, OQ-US03-02, OQ-US03-01] |
| Tác nhân liên quan | NVKD: người tạo bảng nhận thông báo kết quả; NVKD phụ trách hợp đồng xem lý do từ chối và thực hiện reopen (§1.5). Module Hợp đồng/Bảng giá/Sản lượng: chỉ đọc khi kiểm tra lại nguồn lúc duyệt. Module kế toán: ngoài phạm vi. [ĐẶC TẢ] §1; [GIẢ ĐỊNH – Cần xác nhận: OQ-US03-04, OQ-US03-05, OQ-US03-06, OQ-US01-07, OQ-US01-03] |
| Mục tiêu | Người có thẩm quyền duyệt (→ `Approved`) hoặc từ chối kèm lý do (→ `Rejected`). [ĐẶC TẢ] §3, §4.3, PAY-08 |
| Kích hoạt | Người duyệt chọn “Duyệt” hoặc “Từ chối” trên bảng `PendingApproval`. Tên nút: [ĐỀ XUẤT KỸ THUẬT] |
| P1 | Bảng tồn tại, ở `PendingApproval`. [ĐẶC TẢ] §3, §4.2 |
| P2 | Người thao tác đã xác thực, vai trò KTT hoặc GĐKD, **đúng** vai trò yêu cầu theo tổng: ≥ 500.000.000 đ → GĐKD; < 500.000.000 đ → KTT. Cùng quy tắc với SYS-US-02 bước 8. [ĐẶC TẢ] §4.3; [GIẢ ĐỊNH – Cần xác nhận: OQ-02, OQ-US03-02]; R01-01 |
| P3 | Tổng dùng so ngưỡng là **tổng đã lưu tại thời điểm lập**, gồm thuế GTGT; thuế suất % là tham số cấu hình, mặc định 10%; làm tròn lên theo đồng ở từng dòng, tiền thuế và tổng (SYS-US-01 §1.2). Bảng chỉ sửa được ở `Draft` nên tổng không đổi khi chờ duyệt. [GIẢ ĐỊNH – Cần xác nhận: OQ-US03-03]; R01-02 |
| P4 | Người thao tác không phải người lập (người tạo bảng ở `Draft`, `createdBy`); áp dụng cho **cả duyệt và từ chối**. [ĐẶC TẢ] PAY-07; [GIẢ ĐỊNH – Cần xác nhận: OQ-US03-01]; R01-06 |
| P5 (duyệt) | Nguồn còn đạt PAY-01..03: hợp đồng Active, bảng giá đã dùng còn Active, bản ghi sản lượng nguồn còn Đã đối soát và không đổi. [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-07]; R01-08 |
| P6 (từ chối) | Lý do không rỗng (sau khi bỏ khoảng trắng), tối đa 500 từ. [ĐẶC TẢ] PAY-08 (bắt buộc); [GIẢ ĐỊNH – Cần xác nhận: OQ-US03-04] (giới hạn 500 từ) |
| Hậu điều kiện – duyệt | Bảng `Approved`, khóa sửa theo PAY-05 (điều chỉnh qua hồ sơ riêng ở US-PAY-04). Một audit approve: ai, lúc nào, `PendingApproval` → `Approved`. Thông báo trong hệ thống cho NVKD đã tạo bảng. Module chỉ bảo đảm bảng Approved đọc được cho kế toán; không thiết kế tích hợp. [ĐẶC TẢ] §3, PAY-05, §6; [GIẢ ĐỊNH – Cần xác nhận: OQ-US03-05, OQ-US03-06, OQ-03] |
| Hậu điều kiện – từ chối | Bảng `Rejected`; lý do lưu **cùng bảng** và trong audit; NVKD xem được lý do. Audit reject: ai, lúc nào, `PendingApproval` → `Rejected`, lý do. Thông báo trong hệ thống **kèm lý do** cho NVKD đã tạo bảng. Hệ thống **không** tự chuyển sang `Draft`. [ĐẶC TẢ] §3, PAY-08, §6; [GIẢ ĐỊNH – Cần xác nhận: OQ-04, OQ-US03-04, OQ-US03-05, OQ-US03-07] |
| Hậu điều kiện – thất bại | Trạng thái và dữ liệu giữ nguyên, không audit mồ côi; trả mã lỗi và lý do. [ĐẶC TẢ] §6 |
| NFR | NFR-PAY-01 áp dụng cho approve, reject, reopen. NFR-PAY-02 không áp dụng (chỉ lập bảng). [ĐẶC TẢ] §6 |

### 1.2. Dòng cơ bản – Duyệt

Thứ tự kiểm tra [ĐỀ XUẤT KỸ THUẬT]: xác thực → vai trò duyệt → tồn tại → trạng thái → vai trò theo tổng → PAY-07 → (duyệt: nguồn; từ chối: lý do) → giao dịch. Giao dịch chỉ mở sát bước ghi (R01-11).

| Bước | Tương tác và kết quả | Căn cứ |
|---|---|---|
| 1 | Người duyệt gửi yêu cầu duyệt kèm `expectedVersion`. | [ĐẶC TẢ] §4.3; version: [ĐỀ XUẤT KỸ THUẬT] DD-08 |
| 2 | Hệ thống xác thực, lấy `userId` và vai trò; vai trò phải là KTT hoặc GĐKD. | [ĐẶC TẢ] §2 |
| 3 | Đọc bảng (trạng thái, tổng đã lưu, `createdBy`, version, hợp đồng, bảng giá, bản ghi nguồn). | [ĐỀ XUẤT KỸ THUẬT] |
| 4 | Kiểm tra `PendingApproval`. | [ĐẶC TẢ] §3 |
| 5 | Xác định vai trò yêu cầu từ tổng đã lưu (≥ 500.000.000 đ → GĐKD, ngược lại KTT) và so với vai trò người gọi. | [ĐẶC TẢ] §4.3; [GIẢ ĐỊNH – Cần xác nhận: OQ-02, OQ-US03-02, OQ-US03-03] |
| 6 | Kiểm tra người gọi khác `createdBy`. | [ĐẶC TẢ] PAY-07; [GIẢ ĐỊNH – Cần xác nhận: OQ-US03-01] |
| 7 | Đọc lại nguồn, kiểm tra PAY-01..03 như SYS-US-02 bước 6. | [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-07] |
| 8 | Mở giao dịch; cập nhật có điều kiện (`PendingApproval`, version khớp) sang `Approved`, tăng version; ghi audit approve; commit. | [ĐẶC TẢ] §3, §6; [ĐỀ XUẤT KỸ THUẬT] DD-02 |
| 9 | Sau commit thành công: gửi thông báo trong hệ thống cho NVKD đã tạo bảng (“Bảng … đã được duyệt”). Lỗi gửi không hoàn tác việc duyệt. | [GIẢ ĐỊNH – Cần xác nhận: OQ-US03-05]; không hoàn tác: [ĐỀ XUẤT KỸ THUẬT] DD-05 |
| 10 | Trả kết quả: `Approved`, version mới, `notificationStatus`. | [ĐỀ XUẤT KỸ THUẬT] |

### 1.3. Dòng cơ bản – Từ chối (R)

| Bước | Tương tác và kết quả | Căn cứ |
|---|---|---|
| R1 | Người duyệt chọn “Từ chối”, nhập lý do, gửi kèm `expectedVersion`. | [ĐẶC TẢ] §4.3, PAY-08 |
| R2–R6 | Như bước 2–6 (PAY-07 áp dụng cho cả từ chối). | [GIẢ ĐỊNH – Cần xác nhận: OQ-US03-01] |
| R7 | Kiểm tra lý do: không rỗng (chuỗi chỉ khoảng trắng coi là rỗng); không quá 500 từ (đếm theo khoảng trắng). Không kiểm tra lại nguồn khi từ chối. | [ĐẶC TẢ] PAY-08; [GIẢ ĐỊNH – Cần xác nhận: OQ-US03-04]; cách đếm: [ĐỀ XUẤT KỸ THUẬT] |
| R8 | Mở giao dịch; cập nhật có điều kiện sang `Rejected`, lưu `rejectReason` trên bảng, tăng version; ghi audit reject kèm lý do; commit. | [ĐẶC TẢ] §3, §6; [GIẢ ĐỊNH – Cần xác nhận: OQ-04, OQ-US03-04] |
| R9 | Sau commit: gửi thông báo trong hệ thống **kèm lý do** cho NVKD đã tạo bảng. Lỗi gửi không hoàn tác. | [GIẢ ĐỊNH – Cần xác nhận: OQ-US03-05] |
| R10 | Trả kết quả: `Rejected`, lý do, version mới, `notificationStatus`. | [ĐỀ XUẤT KỸ THUẬT] |

### 1.4. Dòng thay thế (duyệt và từ chối)

| Nhánh | Xử lý | Căn cứ |
|---|---|---|
| 2a | Chưa xác thực → 401 `UNAUTHENTICATED`; không có vai trò KTT/GĐKD → 403 `FORBIDDEN`. | [ĐẶC TẢ] §2 |
| 3a | Không tồn tại → 404 `NOT_FOUND`; lỗi đọc → 503 `SOURCE_UNAVAILABLE`. | [ĐỀ XUẤT KỸ THUẬT] |
| 4a | Không ở `PendingApproval` (kể cả đã bị người khác xử lý trước) → 409 `INVALID_STATE`, không đổi dữ liệu, không audit. | [ĐẶC TẢ] §3 |
| 5a | Sai vai trò theo tổng (KTT với bảng ≥ 500.000.000 đ; GĐKD với bảng < 500.000.000 đ) → 403 `APPROVER_NOT_AUTHORIZED`. | [ĐẶC TẢ] §4.3; [GIẢ ĐỊNH – Cần xác nhận: OQ-02, OQ-US03-02] |
| 6a | Người gọi là `createdBy` → 403 `SELF_APPROVAL_FORBIDDEN`, cả duyệt lẫn từ chối. (Với quy tắc một người một vai trò, nhánh này là kiểm tra phòng vệ.) | [ĐẶC TẢ] PAY-07; [GIẢ ĐỊNH – Cần xác nhận: OQ-US03-01] |
| 7a | (duyệt) Nguồn không còn đạt PAY-01..03 → 409 `SOURCE_NOT_VALID` kèm lý do; giữ `PendingApproval`. Người duyệt có thể từ chối với lý do để NVKD tải lại nguồn. Lỗi đọc nguồn → 503, không coi là đạt. | [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-07] |
| R7a | Lý do rỗng → 400 `REASON_REQUIRED`, giữ `PendingApproval`. | [ĐẶC TẢ] PAY-08 |
| R7b | Lý do quá 500 từ → 400 `REASON_TOO_LONG`, giữ `PendingApproval`. | [GIẢ ĐỊNH – Cần xác nhận: OQ-US03-04] |
| 8a | Lỗi mở giao dịch, ghi trạng thái/audit, hoặc commit xác định chưa xảy ra → rollback, giữ `PendingApproval`, 500 `PERSISTENCE_ERROR`; không gửi thông báo. | [ĐẶC TẢ] §6; R01-11 |
| 8b | Cập nhật có điều kiện trả 0 dòng (yêu cầu đồng thời đã xử lý trước) → rollback, 409 `CONCURRENT_MODIFICATION`. Đúng một yêu cầu đổi trạng thái. | [ĐỀ XUẤT KỸ THUẬT] DD-02; R01-14 |
| 8c | Mất kết quả commit → 503 `RESULT_UNKNOWN`; không gửi thông báo; client đọc lại bằng E6. | [ĐỀ XUẤT KỸ THUẬT]; R01-11 |
| 9a | Gửi thông báo lỗi → giữ kết quả đã commit, trả `notificationStatus = FAILED`. | [ĐỀ XUẤT KỸ THUẬT]; [GIẢ ĐỊNH – Cần xác nhận: OQ-US03-05] |

### 1.5. NVKD mở chỉnh sửa bảng Rejected (Rejected → Draft)

[GIẢ ĐỊNH – Cần xác nhận: OQ-04, OQ-US03-07, OQ-US01-03] Từ chối đưa bảng sang `Rejected` (đúng §3). Bảng chỉ về `Draft` khi NVKD mở để chỉnh sửa, đáp ứng “quay về Draft để NVKD chỉnh sửa và trình lại” của PAY-08. Bảng `Rejected` không trình lại hay hủy trực tiếp; phải qua bước này.

| Bước | Tương tác và kết quả | Căn cứ |
|---|---|---|
| D1 | NVKD mở bảng `Rejected`, xem lý do từ chối, bấm “Chỉnh sửa” (gửi `expectedVersion`). | [ĐẶC TẢ] PAY-08; [GIẢ ĐỊNH – Cần xác nhận: OQ-US03-04, OQ-US03-07] |
| D2 | Hệ thống xác thực, kiểm tra vai trò NVKD; đọc bảng; kiểm tra NVKD được phân công hợp đồng; kiểm tra `Rejected`. | [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-03] |
| D3 | Mở giao dịch; cập nhật có điều kiện `Rejected` → `Draft`, tăng version, giữ `rejectReason` để tham chiếu; ghi audit reopen (ai, lúc nào, `Rejected` → `Draft`); commit. | [ĐẶC TẢ] §6; [GIẢ ĐỊNH – Cần xác nhận: OQ-US03-07]; tên `reopen`: [ĐỀ XUẤT KỸ THUẬT] |
| D4 | Trả bảng `Draft` và version mới; giao diện mở biểu mẫu sửa theo SYS-US-01 §1.5 (U2). | [ĐẶC TẢ] §4.1 |

| Nhánh | Xử lý |
|---|---|
| D2a | 401/403 như 2a (vai trò phải là NVKD); không được phân công → 403 `FORBIDDEN`; không tồn tại → 404. |
| D2b | Bảng không ở `Rejected` → 409 `INVALID_STATE` (đã `Draft` thì mở sửa trực tiếp theo SYS-US-01 U2). |
| D3a | 0 dòng cập nhật → 409 `CONCURRENT_MODIFICATION`; lỗi lưu/audit → rollback, 500 `PERSISTENCE_ERROR`; mất kết quả commit → 503 `RESULT_UNKNOWN`. |

## 2. Điểm cần xác nhận

Mẫu 9 cột theo [rules/common.md](../../../../rules/common.md) (R01-28). “Nhóm đề xuất” chưa phải xác nhận khách hàng.

| ID | Vị trí mọi nguồn | Loại | Mô tả | Lý do cần xác nhận | Lựa chọn (đề xuất nhóm áp dụng ở v2) | Ảnh hưởng tới Phần 1 | Trạng thái | Người/ngày/câu trả lời và tham chiếu |
|---|---|---|---|---|---|---|---|---|
| OQ-02 | TA-SPEC §4.3 “từ 500 triệu… trở lên” ↔ PAY-06 “trên 500 triệu”; TA-PDF tr.2 | Mâu thuẫn | Đúng 500.000.000 đ ai duyệt? | Chọn người duyệt và người nhận thông báo | Áp dụng §4.3: ≥ 500.000.000 đ → GĐKD; < → KTT; dùng chung cho trình và duyệt | P2, bước 5, 5a; AC-06, 07 | Nhóm đề xuất | Nhóm 3 – báo cáo đánh giá, bảng II.2 (10/2026); R01-01, R01-07 |
| OQ-04 | TA-SPEC §3 “Rejected” ↔ PAY-08 “quay về Draft” | Mâu thuẫn | Đích sau từ chối | State machine, điều kiện sửa và trình lại | Từ chối → Rejected; về Draft khi NVKD mở chỉnh sửa | Hậu điều kiện từ chối, R8; §1.5; AC-02, 16 | Nhóm đề xuất | Nhóm 3 – bảng II.2; R01-05 |
| OQ-US03-01 | PAY-07; §2; §4.3 | Mơ hồ | Ai là người lập; PAY-07 cho từ chối; nhiều vai trò | Xác định guard PAY-07 | Người lập là người tạo bảng ở Draft; PAY-07 áp dụng cho duyệt và từ chối; mỗi người dùng một vai trò | Tác nhân, P4, bước 6, 6a; AC-08, 09 | Nhóm đề xuất | Nhóm 3 – bảng II.2; R01-06 |
| OQ-US03-02 | §4.3; PAY-06; §2 | Mơ hồ | Theo vai trò hay cá nhân; thay thế chéo | Xác định ai được duyệt | Theo vai trò; mọi người giữ vai trò đúng thẩm quyền được duyệt (trừ người lập); không vai trò khác duyệt thay | Tác nhân, P2, bước 5, 5a; AC-06 | Nhóm đề xuất | Nhóm 3 – bảng II.2 |
| OQ-US03-03 | §4.3; PAY-06; PAY-03; §4.1 | Thiếu | Tổng: thời điểm, VAT, làm tròn; sửa khi PendingApproval | Có thể đổi người duyệt | Tổng đã lưu lúc lập, gồm thuế GTGT; thuế suất % cấu hình, mặc định 10%; làm tròn lên ở dòng, thuế, tổng; chỉ sửa ở Draft | P3, bước 5; AC-07 | Nhóm đề xuất | Nhóm 3 – bảng II.2; R01-02 |
| OQ-US03-04 | §4.3; PAY-08 | Thiếu | Ràng buộc lý do, nơi lưu, NVKD xem được? | Validation và dữ liệu | Bắt buộc, tối đa 500 từ; lưu cùng bảng và audit; NVKD xem được | P6, R7, R7b, R8, D1; AC-10, 11, 17 | Nhóm đề xuất | Nhóm 3 – bảng II.2; R01-20 |
| OQ-US03-05 | §4.2; §4.3; §3 | Thiếu | Thông báo kết quả, người nhận, kênh | Thiết kế thông báo | Thông báo trong hệ thống cho NVKD đã tạo bảng khi duyệt hoặc từ chối; từ chối kèm lý do | Bước 9, R9, 9a; AC-14 | Nhóm đề xuất | Nhóm 3 – bảng II.2 |
| OQ-US03-06 | §1 | Mơ hồ | Chuyển kế toán sau Approved | Phạm vi module | Ngoài phạm vi; chỉ bảo đảm bảng Approved đọc được; không thiết kế tích hợp | Hậu điều kiện duyệt | Nhóm đề xuất | Nhóm 3 – bảng II.2; R01-26 |
| OQ-US03-07 | §3 “Rejected”; PAY-08 | Thiếu | Ai/khi nào Rejected → Draft | Luồng sửa và trình lại | Không tự chuyển khi từ chối; Rejected → Draft khi NVKD mở chỉnh sửa; có audit | Hậu điều kiện từ chối; §1.5; AC-16 | Nhóm đề xuất | Nhóm 3 – bảng II.2; R01-05 |
| OQ-US01-07 | §4.1–4.3; PAY-01..04; R01-08 | Thiếu | Kiểm tra lại nguồn khi duyệt? | Nguồn có thể đổi khi chờ duyệt | Kiểm tra lại PAY-01..03 khi trình và khi duyệt; chặn nếu không còn đạt | P5, bước 7, 7a; AC-18 | Nhóm đề xuất | Nhóm 3 – bảng III, R01-08 |
| OQ-US01-03 | §2; §4.1 | Thiếu | Phạm vi NVKD trên bảng | Quyền reopen | NVKD phụ trách hợp đồng được thao tác Draft của hợp đồng đó (áp dụng cho reopen) | §1.5 D2; AC-16 | Nhóm đề xuất | Nhóm 3 – bảng II.2 |
| OQ-03 | §4.4 ↔ PAY-05 | Mâu thuẫn | Điều chỉnh Approved (thuộc US-PAY-04) | Hậu điều kiện duyệt | Bảng Approved giữ nguyên; điều chỉnh là hồ sơ riêng | Hậu điều kiện duyệt; AC-15 | Nhóm đề xuất | Nhóm 3 – bảng II.2 |

## 3. Acceptance criteria

Mã `AC-US03-kk` tự đặt. Giữ ID v1; tách phần bám đề và phần theo đề xuất nhóm (R01-20); thêm AC-16..19.

| ID | Given / When / Then | Nhãn | Nguồn | OQ |
|---|---|---|---|---|
| AC-US03-01 | Given bảng `PendingApproval`, người gọi đúng vai trò theo tổng, không phải người lập, nguồn còn đạt; When duyệt (1–10); Then bảng `Approved`, có đúng một audit ai/lúc nào/`PendingApproval` → `Approved`. | [ĐẶC TẢ] (§3, §4.3, §6) + [GIẢ ĐỊNH – Cần xác nhận] (vai trò, nguồn) | §3, §4.3, §6 | OQ-02, OQ-US03-02, OQ-US01-07 |
| AC-US03-02 | Given như AC-01 và lý do hợp lệ; When từ chối (R1–R10); Then bảng `Rejected`, `rejectReason` lưu trên bảng, audit kèm lý do; bảng **không** ở `Draft` sau thao tác này. | [GIẢ ĐỊNH – Cần xác nhận] | §3, §4.3, PAY-08, §6 | OQ-04, OQ-US03-04 |
| AC-US03-03 | Given chưa xác thực hoặc không có vai trò KTT/GĐKD; When duyệt/từ chối; Then 401/403, không đổi dữ liệu (2a). | [AC dẫn xuất] | §2, §4.3 | – |
| AC-US03-04 | Given mã bảng không tồn tại; When duyệt/từ chối; Then 404, không audit (3a). | [AC dẫn xuất] | §4.3 | – |
| AC-US03-05 | Given bảng không ở `PendingApproval`; When duyệt/từ chối; Then 409 `INVALID_STATE`, không audit (4a). | [AC dẫn xuất] | §3, §4.3 | – |
| AC-US03-06 | Given tổng < 500.000.000 đ và người gọi là GĐKD, hoặc tổng ≥ 500.000.000 đ và người gọi là KTT; When duyệt/từ chối; Then 403 `APPROVER_NOT_AUTHORIZED` (5a). | [GIẢ ĐỊNH – Cần xác nhận] | §4.3, PAY-06 | OQ-02, OQ-US03-02 |
| AC-US03-07 | Given tổng đã lưu (gồm thuế GTGT) đúng 500.000.000 đ; When xác định vai trò (bước 5); Then vai trò yêu cầu là GĐKD; với 499.999.999 đ là KTT; với 500.000.001 đ là GĐKD. | [GIẢ ĐỊNH – Cần xác nhận] | §4.3 ↔ PAY-06; R01-01, R01-07 | OQ-02, OQ-US03-03 |
| AC-US03-08 | Given người gọi là người lập bảng; When duyệt; Then 403 `SELF_APPROVAL_FORBIDDEN` (6a). | [ĐẶC TẢ] | PAY-07 | OQ-US03-01 (định nghĩa người lập) |
| AC-US03-09 | Given người gọi là người lập bảng; When từ chối; Then 403 `SELF_APPROVAL_FORBIDDEN` (6a). | [GIẢ ĐỊNH – Cần xác nhận] | PAY-07 | OQ-US03-01 |
| AC-US03-10 | Given lý do rỗng hoặc chỉ khoảng trắng; When từ chối; Then 400 `REASON_REQUIRED`, giữ `PendingApproval` (R7a). | [ĐẶC TẢ] | PAY-08 | – |
| AC-US03-11 | Given lý do 501 từ; When từ chối; Then 400 `REASON_TOO_LONG`; Given 500 từ; Then hợp lệ (R7b). | [GIẢ ĐỊNH – Cần xác nhận] | PAY-08 | OQ-US03-04 |
| AC-US03-12 | Given lỗi ghi trạng thái hoặc audit; When duyệt/từ chối; Then rollback, giữ `PendingApproval`, không có audit mồ côi, 500, không gửi thông báo (8a). | [AC dẫn xuất] | §6 | – |
| AC-US03-13 | Given hai yêu cầu duyệt/từ chối đồng thời trên cùng bảng; When xử lý; Then đúng một yêu cầu đổi trạng thái, yêu cầu còn lại 409 `CONCURRENT_MODIFICATION` (8b). | [ĐỀ XUẤT KỸ THUẬT] | §3, §6 | – |
| AC-US03-14 | Given duyệt/từ chối đã commit; When gửi thông báo; Then NVKD đã tạo bảng nhận thông báo trong hệ thống, thông báo từ chối có lý do; lỗi gửi không hoàn tác (9, R9, 9a). | [GIẢ ĐỊNH – Cần xác nhận] | §4.3 | OQ-US03-05 |
| AC-US03-15 | Given bảng `Approved`; When bất kỳ thao tác sửa trực tiếp nào (update, submit, reject, cancel); Then bị từ chối 409; điều chỉnh chỉ qua hồ sơ US-PAY-04 và không đổi bảng (PAY-05). | [ĐẶC TẢ] | PAY-05 | OQ-03 |
| AC-US03-16 | Given bảng `Rejected`, NVKD được phân công hợp đồng; When bấm “Chỉnh sửa” (D1–D4); Then bảng `Draft`, version tăng, audit reopen ai/lúc nào/`Rejected` → `Draft`. Given NVKD không được phân công; Then 403. Given bảng không `Rejected`; Then 409. | [GIẢ ĐỊNH – Cần xác nhận] | §3, PAY-08, §6 | OQ-04, OQ-US03-07, OQ-US01-03 |
| AC-US03-17 | Given bảng bị từ chối; When NVKD xem bảng (Rejected hoặc sau khi về Draft); Then thấy lý do từ chối. | [GIẢ ĐỊNH – Cần xác nhận] | PAY-08 | OQ-US03-04 |
| AC-US03-18 | Given hợp đồng hết Active, hoặc bảng giá/bản ghi sản lượng nguồn không còn đạt; When duyệt; Then 409 `SOURCE_NOT_VALID`, giữ `PendingApproval` (7a). Từ chối không bị chặn bởi kiểm tra này. | [GIẢ ĐỊNH – Cần xác nhận] | PAY-01..03 | OQ-US01-07 |
| AC-US03-19 | Given bảng `Approved`; When module kế toán đọc; Then module cung cấp dữ liệu bảng ở chế độ chỉ đọc; module không gọi hay đẩy dữ liệu sang kế toán. | [GIẢ ĐỊNH – Cần xác nhận] | §1 | OQ-US03-06 |

## 4. Bàn giao

- Sequence cùng version: [seq-us-03-v2.puml](../../../design/payment-management/v2/diagrams/seq-us-03-v2.puml) – gồm duyệt, từ chối và reopen (Rejected → Draft).
- Tên dùng tạm cần đồng bộ vào `03-detailed-design-v2.md`, `04-api-contract-v2.md`, `state-machine-v2.puml` (chưa tạo): thao tác/audit action `reopen`; endpoint `POST /api/payment-sheets/{id}/reopen` (E14, tạm); mã lỗi `SOURCE_NOT_VALID`; state machine bỏ nhánh `PendingApproval` → `Draft` khi từ chối, thêm `Rejected` → `Draft` [reopen, NVKD phụ trách hợp đồng].

## Thay đổi so với v1

| # | Vị trí | Thay đổi | Căn cứ |
|---|---|---|---|
| 1 | Đầu file, toàn bộ nhãn | Nhãn giả định dẫn OQ cụ thể; tách AC bám đề với AC theo đề xuất nhóm. | R01-20, R01-04 |
| 2 | P2, bước 5, AC-07 | Giữ ≥ 500.000.000 đ → GĐKD, thống nhất với SYS-US-02 bước 8; AC-07 thêm ba giá trị biên. | OQ-02; R01-01, R01-07 |
| 3 | P3 | Tổng gồm thuế GTGT với thuế suất % cấu hình, mặc định 10% (thay “x hoặc %” của v1). | OQ-US03-03; R01-02 |
| 4 | P5, bước 7, 7a, AC-18 | Thêm kiểm tra lại PAY-01..03 khi duyệt. | OQ-US01-07; R01-08 |
| 5 | §1.2 thứ tự, bước 8, 8a–8c | Giao dịch mở sát bước ghi; thêm nhánh commit thất bại/chưa rõ. | R01-11 |
| 6 | §1.5, AC-16, 17 | Thêm luồng reopen Rejected → Draft khi NVKD bấm “Chỉnh sửa”, có audit; bỏ phương án về Draft ngay. | OQ-04, OQ-US03-07; R01-05 |
| 7 | P4, 6a, AC-09 | PAY-07 áp dụng cho từ chối có căn cứ OQ-US03-01. | R01-06 |
| 8 | AC-19 | Kế toán ngoài phạm vi, chỉ đọc. | OQ-US03-06; R01-26 |
| 9 | §2 | Bảng OQ đủ 9 cột, trạng thái “Nhóm đề xuất”. | R01-04, R01-28 |
