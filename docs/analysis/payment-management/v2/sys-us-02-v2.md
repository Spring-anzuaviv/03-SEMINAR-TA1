# SYS-US-02 – Trình duyệt (v2)

> Phiên bản: v2 · Ngày: 11/11/2026 · Người phụ trách: Phan Trung Hiếu
> Đầu vào: [TA-SPEC](../../../requirements/payment-management/spec.md) §1–6; sys-us-02-v1.md; [sys-us-01-v2.md](sys-us-01-v2.md), [sys-us-03-v2.md](sys-us-03-v2.md); Báo cáo đánh giá nhóm 3 – bảng II.2 cột “Cách nhóm xử lý” và bảng III (R01-xx Đúng)
> AI: Claude Code / Claude Opus 5.5 · Prompt: P-29 trong [prompt-log](../../../workflow/prompt-log.md)
> Trạng thái: Bản sau review – BA Pending Approval
> Nhãn: [ĐẶC TẢ] · [AC dẫn xuất] · [ĐỀ XUẤT KỸ THUẬT] · [GIẢ ĐỊNH – Cần xác nhận: OQ-…] = áp dụng cách xử lý **nhóm đề xuất**, chưa có xác nhận của khách hàng (R01-20). SYS/AC/OQ/NFR là mã nội bộ.

Phạm vi: thao tác trình duyệt (submit) và gửi lại thông báo trình duyệt của US-PAY-02. Không thiết kế API, lớp hay dữ liệu chi tiết.

## 1. Use case

### 1.1. Căn cứ

- [ĐẶC TẢ] US-PAY-02: NVKD chọn “Trình duyệt”; kiểm tra PAY-04; nếu đạt chuyển `PendingApproval` và gửi thông báo cho người duyệt. [TA-SPEC §4.2; TA-PDF tr.2]
- [ĐẶC TẢ] PAY-04: chặn tổng âm hoặc thiếu dòng dịch vụ bắt buộc; chống trình trùng. [TA-SPEC §5]
- [ĐẶC TẢ] §4.3 “từ 500 triệu trở lên” do GĐKD duyệt ↔ PAY-06 “trên 500 triệu”. v2 áp dụng §4.3 (OQ-02). [TA-SPEC §4.3, §5 PAY-06]
- [ĐẶC TẢ] PAY-07 cấm tự duyệt chỉ kiểm tra ở thao tác duyệt (US-PAY-03), không chặn người lập trình duyệt. [TA-SPEC §5]
- [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-07] Khi trình, kiểm tra lại PAY-01..03 trên dữ liệu nguồn (R01-08).

### 1.2. Đặc tả tương tác

| Mục | Đặc tả |
|---|---|
| Tên | SYS-US-02 – Trình duyệt. [ĐẶC TẢ] §4.2 |
| Tác nhân chính | NVKD **được phân công phụ trách hợp đồng của bảng**, không bắt buộc là người lập bảng. [ĐẶC TẢ] §2, §4.2; [GIẢ ĐỊNH – Cần xác nhận: OQ-US02-01] |
| Tác nhân liên quan | Mọi người dùng giữ vai trò duyệt theo thẩm quyền: tổng ≥ 500.000.000 đ → GĐKD; < 500.000.000 đ → KTT; nhận thông báo trong hệ thống. Module Hợp đồng/Bảng giá/Sản lượng (chỉ đọc). [ĐẶC TẢ] §4.3; [GIẢ ĐỊNH – Cần xác nhận: OQ-02, OQ-US03-02, OQ-US02-02] |
| Mục tiêu | Đưa bảng hợp lệ vào chờ duyệt và thông báo người duyệt. [ĐẶC TẢ] §4.2 |
| Kích hoạt | NVKD chọn “Trình duyệt” trên bảng. [ĐẶC TẢ] §4.2 |
| P1 | Người gửi đã xác thực, vai trò NVKD, được phân công hợp đồng của bảng. [ĐẶC TẢ] §2; [GIẢ ĐỊNH – Cần xác nhận: OQ-US02-01] |
| P2 | Bảng tồn tại, đang `Draft`. Bảng `Rejected` phải được NVKD mở “Chỉnh sửa” về `Draft` trước (SYS-US-03 §1.5). [ĐẶC TẢ] §3; [GIẢ ĐỊNH – Cần xác nhận: OQ-04, OQ-US03-07] |
| P3 | Nguồn còn đạt PAY-01..03: hợp đồng còn Active, bảng giá đã dùng còn Active, các bản ghi sản lượng nguồn còn Đã đối soát và không đổi. [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-07] |
| P4 | Tổng (đã lưu, gồm thuế GTGT) không âm; mọi dịch vụ khai báo trong hợp đồng đều có dòng trong bảng. [ĐẶC TẢ] PAY-04; [GIẢ ĐỊNH – Cần xác nhận: OQ-05, OQ-US03-03] |
| Hậu điều kiện thành công | Bảng `Draft` → `PendingApproval`, `submissionNo` (số lần trình) tăng 1; audit submit (ai, lúc nào, Draft → PendingApproval) lưu **trước** khi gửi thông báo, cùng giao dịch với chuyển trạng thái. Thông báo trong hệ thống gửi tới mọi người giữ vai trò duyệt theo thẩm quyền, gồm mã bảng, hợp đồng, kỳ thanh toán, tổng tiền. [ĐẶC TẢ] §3, §4.2, §6; [GIẢ ĐỊNH – Cần xác nhận: OQ-US02-02, OQ-02, OQ-US03-02]; `submissionNo`: [ĐỀ XUẤT KỸ THUẬT] |
| Hậu điều kiện khi gửi thông báo lỗi | Bảng **giữ** `PendingApproval`; NVKD nhận kết quả “Đã trình duyệt, thông báo chưa gửi thành công” và có thể gửi lại (§1.5). [GIẢ ĐỊNH – Cần xác nhận: OQ-US02-02] |
| Hậu điều kiện thất bại | Yêu cầu bị chặn không đổi trạng thái, không ghi audit chuyển trạng thái, không gửi thông báo. [AC dẫn xuất] PAY-04, §6 |
| NFR | NFR-PAY-01 áp dụng (audit submit). NFR-PAY-02 không áp dụng (chỉ cho lập bảng); không đặt SLA mới. [ĐẶC TẢ] §6 |

### 1.3. Dòng cơ bản

| Bước | Tương tác và kết quả | Căn cứ |
|---|---|---|
| 1 | NVKD gửi yêu cầu trình duyệt cho bảng, kèm `expectedVersion`. | [ĐẶC TẢ] §4.2; version: [ĐỀ XUẤT KỸ THUẬT] DD-08 |
| 2 | Hệ thống xác thực người gửi và kiểm tra vai trò NVKD (**trước** khi đọc bảng). | [ĐẶC TẢ] §2; R01-25 |
| 3 | Hệ thống đọc bảng (trạng thái, version, hợp đồng, tổng, dòng, `submissionNo`). | [ĐỀ XUẤT KỸ THUẬT] |
| 4 | Hệ thống kiểm tra NVKD được phân công hợp đồng của bảng. | [GIẢ ĐỊNH – Cần xác nhận: OQ-US02-01]; R01-25 |
| 5 | Hệ thống kiểm tra bảng đang `Draft`. | [ĐẶC TẢ] §3, §4.2 |
| 6 | Hệ thống đọc lại nguồn và kiểm tra PAY-01..03: hợp đồng Active, bảng giá đã dùng còn Active, bản ghi sản lượng nguồn còn Đã đối soát và không đổi. | [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-07] |
| 7 | Hệ thống kiểm tra PAY-04: tổng đã lưu không âm (tổng bằng 0 không bị chặn chỉ vì bằng 0); đọc danh sách dịch vụ khai báo trong hợp đồng và kiểm tra mỗi dịch vụ có dòng trong bảng. | [ĐẶC TẢ] PAY-04; [GIẢ ĐỊNH – Cần xác nhận: OQ-05] |
| 8 | Hệ thống xác định vai trò duyệt từ tổng đã lưu (gồm thuế GTGT): **tổng ≥ 500.000.000 đ → GĐKD; tổng < 500.000.000 đ → KTT**; người nhận là mọi người dùng giữ vai trò đó. Cùng quy tắc với kiểm tra quyền duyệt ở SYS-US-03. | [ĐẶC TẢ] §4.3; [GIẢ ĐỊNH – Cần xác nhận: OQ-02, OQ-US03-02, OQ-US03-03]; R01-01 |
| 9 | Trong một giao dịch: cập nhật có điều kiện (`Draft`, version khớp) sang `PendingApproval`, tăng version và `submissionNo`; ghi audit submit; commit. | [ĐẶC TẢ] §3, PAY-04, §6; [ĐỀ XUẤT KỸ THUẬT] DD-02 |
| 10 | Sau commit, tạo và gửi thông báo trong hệ thống cho từng người nhận, mỗi thông báo định danh bằng (bảng, `submissionNo`, người nhận) để không tạo trùng; nội dung: mã bảng, hợp đồng, kỳ thanh toán, tổng tiền. | [ĐẶC TẢ] §4.2; [GIẢ ĐỊNH – Cần xác nhận: OQ-US02-02]; khóa chống trùng: [ĐỀ XUẤT KỸ THUẬT] |
| 11 | Trả kết quả: trạng thái `PendingApproval`, version mới, vai trò duyệt, `notificationStatus` = `SENT` (gửi đủ) hoặc `FAILED` (A10). | [ĐỀ XUẤT KỸ THUẬT]; [GIẢ ĐỊNH – Cần xác nhận: OQ-US02-02] |

### 1.4. Dòng thay thế

| Nhánh | Xử lý | Căn cứ |
|---|---|---|
| A2 | Chưa xác thực → 401 `UNAUTHENTICATED`; không phải NVKD → 403 `FORBIDDEN`. Không đọc bảng, không đổi trạng thái. | [ĐẶC TẢ] §2; [ĐỀ XUẤT KỸ THUẬT] mã lỗi |
| A3 | Không tìm thấy bảng → 404 `NOT_FOUND`. Lỗi đọc → 503 `SOURCE_UNAVAILABLE`. | [ĐỀ XUẤT KỸ THUẬT] |
| A4 | NVKD không được phân công hợp đồng của bảng → 403 `FORBIDDEN`. | [GIẢ ĐỊNH – Cần xác nhận: OQ-US02-01] |
| A5 | `PendingApproval` (đã trình thành công, gửi lại) → 409 `DUPLICATE_SUBMIT`, không tạo chuyển trạng thái/audit mới; client đọc lại trạng thái bằng E6. | [ĐẶC TẢ] PAY-04; R01-09 |
| A5.1 | `Approved` hoặc `Cancelled` → 409 `INVALID_STATE`. | [ĐẶC TẢ] §3, §4.5, PAY-05 |
| A5.2 | `Rejected` → 409 `INVALID_STATE` với thông báo “Bảng bị từ chối – bấm Chỉnh sửa để đưa về Draft, sửa rồi trình lại”. Hệ thống không tự chuyển Rejected → Draft khi trình. | [ĐẶC TẢ] §3, PAY-08; [GIẢ ĐỊNH – Cần xác nhận: OQ-04, OQ-US03-07]; R01-13 |
| A6 | Nguồn không còn đạt PAY-01..03 (hợp đồng hết Active, bảng giá không còn Active, sản lượng không còn đối soát hoặc đã đổi) → 409 `SOURCE_NOT_VALID` kèm lý do; giữ `Draft`; NVKD dùng “Tải lại dữ liệu nguồn” (SYS-US-01 §1.5) hoặc hủy bảng (US-PAY-05). Lỗi đọc nguồn → 503 `SOURCE_UNAVAILABLE`, không coi là đạt. | [GIẢ ĐỊNH – Cần xác nhận: OQ-US01-07] |
| A7 | Tổng âm → 400 `NEGATIVE_TOTAL`, giữ `Draft`. | [ĐẶC TẢ] PAY-04 |
| A7.1 | Có dịch vụ của hợp đồng không có dòng → 400 `REQUIRED_SERVICE_MISSING` kèm tên các dịch vụ còn thiếu; giữ `Draft`. | [ĐẶC TẢ] PAY-04; [GIẢ ĐỊNH – Cần xác nhận: OQ-05] |
| A8 | Không có người dùng nào giữ vai trò duyệt cần thiết → vẫn có thể chuyển trạng thái nhưng thông báo không gửi được, xử lý như A10. Hệ thống không đổi sang vai trò khác. | [GIẢ ĐỊNH – Cần xác nhận: OQ-US03-02, OQ-US02-02]; R01-13 |
| A9 | Cập nhật có điều kiện trả 0 dòng (yêu cầu đồng thời đã trình trước, hoặc bảng vừa bị sửa/hủy) → rollback, 409 `CONCURRENT_MODIFICATION`; không ghi đè, không audit; client đọc lại bằng E6. Hai yêu cầu cùng `expectedVersion`: đúng một thành công. | [ĐẶC TẢ] PAY-04; [ĐỀ XUẤT KỸ THUẬT] DD-02; R01-14 |
| A9.1 | Lỗi mở giao dịch, lưu trạng thái, ghi audit hoặc commit xác định chưa xảy ra → rollback, 500 `PERSISTENCE_ERROR`; không gửi thông báo. Mất kết quả commit → 503 `RESULT_UNKNOWN`, client đọc lại bằng E6 trước khi trình lại. | [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §6]; R01-11 |
| A10 | Gửi thông báo thất bại (một phần hoặc toàn bộ) → giữ `PendingApproval`, không hoàn tác; trả 200 với `notificationStatus = FAILED` và thông điệp “Đã trình duyệt, thông báo chưa gửi thành công”; ghi nhận người nhận chưa gửi được để gửi lại (§1.5). | [GIẢ ĐỊNH – Cần xác nhận: OQ-US02-02] |

### 1.5. Gửi lại thông báo trình duyệt

[GIẢ ĐỊNH – Cần xác nhận: OQ-US02-02] Thao tác phụ của US-PAY-02, chỉ dùng khi lần gửi trước thất bại.

| Bước | Tương tác và kết quả |
|---|---|
| N1 | NVKD được phân công chọn “Gửi lại thông báo” trên bảng `PendingApproval` có thông báo chưa gửi thành công. |
| N2 | Hệ thống xác thực, kiểm tra vai trò NVKD, đọc bảng, kiểm tra phân công và trạng thái `PendingApproval`. |
| N3 | Hệ thống lấy các thông báo của `submissionNo` hiện tại chưa gửi thành công; gửi lại đúng các thông báo đó (cùng khóa bảng – lần trình – người nhận), không tạo thông báo mới cho người đã nhận. |
| N4 | Trả `notificationStatus` mới. **Không** chuyển trạng thái, **không** tạo audit trình duyệt. |

| Nhánh | Xử lý |
|---|---|
| AN2 | 401/403/404 như A2–A4; bảng không ở `PendingApproval` → 409 `INVALID_STATE`. |
| AN3 | Không còn thông báo chưa gửi → 200, `notificationStatus = SENT`, không gửi gì thêm (gửi lại nhiều lần không tạo trùng). |
| AN4 | Vẫn gửi lỗi → 200, `notificationStatus = FAILED`; cho gửi lại sau. |

## 2. Điểm cần xác nhận

Mẫu 9 cột theo [rules/common.md](../../../../rules/common.md). “Nhóm đề xuất” chưa phải xác nhận khách hàng.

| ID | Vị trí mọi nguồn | Loại | Mô tả | Lý do cần xác nhận | Lựa chọn (đề xuất nhóm áp dụng ở v2) | Ảnh hưởng tới Phần 1 | Trạng thái | Người/ngày/câu trả lời và tham chiếu |
|---|---|---|---|---|---|---|---|---|
| OQ-US02-01 | TA-SPEC §2, §4.2 “NVKD”; TA-PDF tr.1–2 | Mơ hồ | NVKD được trình bảng nào? | Kiểm tra quyền trên từng bảng | NVKD phụ trách hợp đồng được trình các bảng Draft của hợp đồng đó, không bắt buộc là người lập; kiểm tra vai trò rồi phân công; PAY-07 chỉ ở chức năng duyệt | Tác nhân, P1, bước 2, 4; A2, A4; AC-06, 14 | Nhóm đề xuất | Nhóm 3 – báo cáo đánh giá, bảng II.2 (10/2026); R01-25 |
| OQ-US02-02 | TA-SPEC §4.2 “gửi thông báo cho người duyệt” | Thiếu | Kênh, nội dung, gửi lỗi thì sao, gửi lại thế nào | Tránh báo thành công sai hoặc gửi trùng | Thông báo trong hệ thống; nội dung mã bảng, hợp đồng, kỳ, tổng; lưu PendingApproval + audit trước khi gửi; gửi lỗi giữ PendingApproval, trả “Đã trình duyệt, thông báo chưa gửi thành công”; cho gửi lại, không chuyển trạng thái/không audit trình; chống trùng theo bảng – lần trình – người nhận | Hậu điều kiện, bước 10–11; A8, A10; §1.5; AC-12, 15, 16 | Nhóm đề xuất | Nhóm 3 – bảng II.2 |
| OQ-02 | TA-SPEC §4.3 “từ 500 triệu… trở lên” ↔ PAY-06 “trên 500 triệu” | Mâu thuẫn | Đúng 500.000.000 đ ai duyệt? | Chọn người nhận thông báo | Áp dụng §4.3: ≥ 500.000.000 đ → GĐKD; < → KTT; dùng chung cho trình, chọn người duyệt, kiểm tra quyền duyệt | Bước 8; AC-10 | Nhóm đề xuất | Nhóm 3 – bảng II.2; R01-01 (Đúng) |
| OQ-05 | TA-SPEC PAY-04 “thiếu dòng dịch vụ bắt buộc” | Thiếu | Dòng bắt buộc là gì? | Cần để xây kiểm tra PAY-04 | Dòng bắt buộc = các dịch vụ khai báo trong hợp đồng; thiếu thì chặn và báo tên dịch vụ | P4, bước 7; A7.1; AC-04 | Nhóm đề xuất | Nhóm 3 – bảng II.2 |
| OQ-US01-07 | TA-SPEC §4.1–4.3, PAY-01..04; R01-08 | Thiếu | Kiểm tra lại nguồn khi trình? | Nguồn có thể đổi sau khi lưu Draft | Kiểm tra lại PAY-01..03 khi trình và khi duyệt, chặn nếu không còn đạt | P3, bước 6; A6; AC-17 | Nhóm đề xuất | Nhóm 3 – bảng III, R01-08 (Đúng) |
| OQ-US03-02 | TA-SPEC §2, §4.3, PAY-06 | Mơ hồ | Duyệt theo vai trò hay cá nhân; thay thế chéo | Xác định người nhận | Theo vai trò: mọi người giữ vai trò đúng thẩm quyền; không vai trò khác thay | Tác nhân liên quan, bước 8; A8 | Nhóm đề xuất | Nhóm 3 – bảng II.2 |
| OQ-US03-03 | TA-SPEC §4.1, §4.3, PAY-03, PAY-06; R01-02 | Thiếu | Tổng so ngưỡng: thời điểm, VAT, làm tròn | Có thể đổi người nhận tại biên | Tổng đã lưu lúc lập, gồm thuế GTGT (mặc định 10%), làm tròn lên theo đồng; chỉ sửa ở Draft nên tổng không đổi khi PendingApproval | P4, bước 7, 8 | Nhóm đề xuất | Nhóm 3 – bảng II.2; R01-02 |
| OQ-04 | TA-SPEC §3 ↔ PAY-08 | Mâu thuẫn | Đích sau từ chối | Tiền điều kiện trình lại | Từ chối → Rejected; về Draft khi NVKD mở chỉnh sửa | P2; A5.2; AC-09 | Nhóm đề xuất | Nhóm 3 – bảng II.2; R01-13 |
| OQ-US03-07 | TA-SPEC §3, PAY-08 | Thiếu | Ai/khi nào Rejected → Draft | Luồng trình lại | NVKD bấm “Chỉnh sửa”; có audit; hệ thống không tự chuyển | P2; A5.2; AC-09 | Nhóm đề xuất | Nhóm 3 – bảng II.2 |

## 3. Acceptance criteria

Mã `AC-US02-kk` tự đặt. Giữ ID v1, cập nhật theo đề xuất nhóm; thêm AC-14..18.

| ID | Given / When / Then | Nhãn | Nguồn | OQ |
|---|---|---|---|---|
| AC-US02-01 | Given NVKD được phân công, bảng Draft đạt PAY-01..04; When trình (bước 1–11); Then bảng PendingApproval, `submissionNo` tăng, audit submit có ai/lúc nào/Draft → PendingApproval, thông báo trong hệ thống gửi người duyệt theo thẩm quyền. | [AC dẫn xuất] | §2–4.3, PAY-04, PAY-06, §6 | OQ-US02-01, OQ-US02-02, OQ-02, OQ-05 |
| AC-US02-02 | Given tổng âm; When trình; Then 400 `NEGATIVE_TOTAL`, giữ Draft (A7). | [ĐẶC TẢ] | PAY-04 | – |
| AC-US02-03 | Given tổng bằng 0 và các điều kiện khác đạt; When kiểm tra tổng; Then không chặn vì tổng bằng 0. | [AC dẫn xuất] | PAY-04 | – |
| AC-US02-04 | Given hợp đồng khai báo dịch vụ S1, S2 và bảng chỉ có dòng S1; When trình; Then 400 `REQUIRED_SERVICE_MISSING` nêu “S2”, giữ Draft (A7.1). | [GIẢ ĐỊNH – Cần xác nhận] | PAY-04 | OQ-05 |
| AC-US02-05 | Given hai yêu cầu trình cùng `expectedVersion` hoặc bấm lặp; When xử lý; Then đúng một lần chuyển Draft → PendingApproval và một audit submit; yêu cầu sau nhận 409 `CONCURRENT_MODIFICATION` hoặc `DUPLICATE_SUBMIT` (A5, A9). | [AC dẫn xuất] | PAY-04, §6 | – |
| AC-US02-06 | Given người gửi chưa xác thực hoặc không phải NVKD; When trình; Then 401/403, không đọc bảng, không đổi trạng thái (A2). | [AC dẫn xuất] | §2, §4.2 | – |
| AC-US02-07 | Given bảng không tồn tại; When trình; Then 404 (A3). | [ĐỀ XUẤT KỸ THUẬT] | §4.2 | – |
| AC-US02-08 | Given bảng PendingApproval; When trình; Then 409 `DUPLICATE_SUBMIT`. Given Approved hoặc Cancelled; Then 409 `INVALID_STATE` (A5, A5.1). | [AC dẫn xuất] | §3, §4.5, PAY-04..05 | – |
| AC-US02-09 | Given bảng Rejected; When trình; Then 409 `INVALID_STATE` hướng dẫn bấm “Chỉnh sửa”; Given NVKD đã đưa bảng về Draft và sửa; When trình lại; Then đi luồng chính (A5.2). | [GIẢ ĐỊNH – Cần xác nhận] | §3, PAY-08 | OQ-04, OQ-US03-07 |
| AC-US02-10 | Given tổng 499.999.999 đ / 500.000.000 đ / 500.000.001 đ; When xác định người nhận (bước 8); Then KTT / GĐKD / GĐKD. | [GIẢ ĐỊNH – Cần xác nhận] | §4.3, PAY-06; R01-01 | OQ-02, OQ-US03-03 |
| AC-US02-11 | Given lỗi lưu trạng thái hoặc audit; When bước 9; Then rollback, 500 `PERSISTENCE_ERROR`, không gửi thông báo (A9.1). | [ĐỀ XUẤT KỸ THUẬT] | §4.2, §6 | – |
| AC-US02-12 | Given đã commit PendingApproval nhưng gửi thông báo lỗi; When trả kết quả; Then 200, trạng thái PendingApproval, `notificationStatus = FAILED`, thông điệp “Đã trình duyệt, thông báo chưa gửi thành công” (A10). | [GIẢ ĐỊNH – Cần xác nhận] | §4.2 | OQ-US02-02 |
| AC-US02-13 | Given trạng thái bị thao tác khác đổi trước lúc lưu; When trình; Then 409 `CONCURRENT_MODIFICATION`, không ghi đè (A9). | [ĐỀ XUẤT KỸ THUẬT] | §3, PAY-04 | – |
| AC-US02-14 | Given NVKD B được phân công hợp đồng của bảng do NVKD A lập; When B trình; Then được phép. Given NVKD C không được phân công; When C trình; Then 403 (A4). | [GIẢ ĐỊNH – Cần xác nhận] | §2, §4.2 | OQ-US02-01 |
| AC-US02-15 | Given bảng PendingApproval có thông báo lần trình hiện tại chưa gửi được; When NVKD gửi lại (§1.5); Then chỉ gửi lại thông báo chưa gửi được, trạng thái giữ nguyên, không có audit trình duyệt mới. | [GIẢ ĐỊNH – Cần xác nhận] | §4.2, §6 | OQ-US02-02 |
| AC-US02-16 | Given thông báo của lần trình k đã gửi thành công cho người nhận R; When gửi lại hoặc gửi lại nhiều lần; Then R không nhận thêm thông báo cho lần trình k. Given bảng bị từ chối rồi trình lại (lần k+1); Then R nhận thông báo mới cho lần k+1. | [GIẢ ĐỊNH – Cần xác nhận] / [ĐỀ XUẤT KỸ THUẬT] | §4.2, PAY-04 | OQ-US02-02 |
| AC-US02-17 | Given hợp đồng hết Active, bảng giá không còn Active, hoặc bản ghi sản lượng nguồn không còn đối soát/đã đổi sau khi lưu Draft; When trình; Then 409 `SOURCE_NOT_VALID` kèm lý do, giữ Draft (A6). | [GIẢ ĐỊNH – Cần xác nhận] | PAY-01..03 | OQ-US01-07 |
| AC-US02-18 | Given thông báo đã gửi thành công; When người duyệt xem; Then thông báo có mã bảng, hợp đồng, kỳ thanh toán, tổng tiền. | [GIẢ ĐỊNH – Cần xác nhận] | §4.2 | OQ-US02-02 |

## 4. Bàn giao

- Sequence cùng version: [seq-us-02-v2.puml](../../../design/payment-management/v2/diagrams/seq-us-02-v2.puml).
- Tên dùng tạm cần đồng bộ vào `03-detailed-design-v2.md`, `04-api-contract-v2.md`, `05-data-design-v2.md` (chưa tạo): mã lỗi `SOURCE_NOT_VALID`; trường `submissionNo`, `notificationStatus`; endpoint gửi lại thông báo `POST /api/payment-sheets/{id}/submit/notifications/resend` (E15, tạm); bảng thông báo với khóa duy nhất (bảng, lần trình, người nhận); `IContractReader.GetContractServices`.

## Thay đổi so với v1

| # | Vị trí | Thay đổi | Căn cứ |
|---|---|---|---|
| 1 | Tác nhân, P1, bước 2–4, A4, AC-14 | Quyền theo phân công hợp đồng; tách kiểm tra vai trò (trước đọc bảng) và phân công (sau đọc bảng). | OQ-US02-01; R01-25 |
| 2 | Bước 8, AC-10 | Bỏ Blocked ở đúng 500 triệu: ≥ 500.000.000 đ → GĐKD; tổng gồm thuế GTGT. Kiểm thử ba giá trị biên. | OQ-02, OQ-US03-03; R01-01, R01-02 |
| 3 | Bước 7, A7.1, AC-04 | Dòng bắt buộc = dịch vụ khai báo trong hợp đồng. | OQ-05 |
| 4 | Bước 6, A6, AC-17 | Thêm kiểm tra lại PAY-01..03 khi trình. | OQ-US01-07; R01-08 |
| 5 | Bước 9–11, A10, §1.5, AC-12, 15, 16, 18 | Thông báo trong hệ thống; audit trước khi gửi; gửi lỗi giữ PendingApproval; gửi lại không đổi trạng thái/không audit trình; chống trùng theo bảng – lần trình – người nhận. | OQ-US02-02 |
| 6 | A5.2, AC-09 | Rejected: trả `INVALID_STATE` có hướng dẫn “Chỉnh sửa”; không tự chuyển. | OQ-04, OQ-US03-07; R01-13 |
| 7 | A8 | Bổ sung phản hồi khi không có người giữ vai trò duyệt (thay A5 Blocked ở v1). | OQ-US03-02; R01-13 |
| 8 | A5, A9, A9.1 | Quy tắc mã lỗi đồng thời thống nhất; dẫn E6 để đọc lại; dẫn DD-02 thay DD-01; thêm `RESULT_UNKNOWN`. | R01-14, R01-09, R01-13, R01-11 |
| 9 | §2 | Bảng OQ trạng thái “Nhóm đề xuất”; thêm OQ-US01-07. | R01-04, R01-28 |
