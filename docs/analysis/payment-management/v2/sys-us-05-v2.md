# SYS-US-05 – Hủy bảng nháp (v2)

> Phiên bản: v2 · Ngày: 11/11/2026 · Người phụ trách: Phan Trung Tuấn
> Đầu vào: [TA-SPEC](../../../requirements/payment-management/spec.md) §1, §2, §3, §4.5, §5 PAY-01, PAY-05, PAY-08, §6; TA-PDF tr.1–3; sys-us-05-v1.md; [sys-us-01-v2.md](sys-us-01-v2.md), [sys-us-03-v2.md](sys-us-03-v2.md); Báo cáo đánh giá nhóm 3 – bảng II.2 cột “Cách nhóm xử lý” và bảng III (R01-xx Đúng)
> AI: Claude Code / Claude Opus 5.5 · Prompt: P-29 trong [prompt-log](../../../workflow/prompt-log.md)
> Trạng thái: Bản sau review – BA Pending Approval
> Nhãn: [ĐẶC TẢ] · [AC dẫn xuất] · [ĐỀ XUẤT KỸ THUẬT] · [GIẢ ĐỊNH – Cần xác nhận: OQ-…] = áp dụng cách xử lý **nhóm đề xuất**, chưa có xác nhận của khách hàng (R01-20). Mã SYS/AC/OQ là mã nội bộ, không phải mã trong đề.

## 1. Use case

| Thuộc tính | Chi tiết |
|---|---|
| Tên | SYS-US-05 – Hủy bảng nháp. [ĐẶC TẢ] [TA-SPEC §4.5; TA-PDF tr.2] |
| Tác nhân chính | **Chỉ NVKD được phân công phụ trách hợp đồng** của bảng; không bắt buộc là người lập. KTT, GĐKD không được hủy. [ĐẶC TẢ] §2, §4.5; [GIẢ ĐỊNH – Cần xác nhận: OQ-US05-01, OQ-US01-03] |
| Tác nhân liên quan | Không có tác nhân nhận thông báo; việc theo dõi lịch sử dựa trên audit log (bỏ “KTT, GĐKD theo dõi audit” của v1 vì chưa có căn cứ – R01-20). [ĐẶC TẢ] §6 |
| Mục tiêu | Chuyển bảng `Draft` không còn cần thiết sang `Cancelled`; bảng không dùng lại được. [ĐẶC TẢ] §3, §4.5 |
| Kích hoạt | NVKD chọn “Hủy bảng” trên bảng `Draft` và nhập lý do hủy. [ĐỀ XUẤT KỸ THUẬT] tên nút; lý do: [GIẢ ĐỊNH – Cần xác nhận: OQ-US05-03] |
| P1 | Người dùng đã xác thực, vai trò NVKD. [ĐẶC TẢ] §2 |
| P2 | Bảng tồn tại; NVKD được phân công hợp đồng của bảng. [GIẢ ĐỊNH – Cần xác nhận: OQ-US05-01] |
| P3 | Bảng đang `Draft`. Bảng `Rejected` phải được NVKD “Chỉnh sửa” về `Draft` trước (SYS-US-03 §1.5) rồi mới hủy. [ĐẶC TẢ] §3, §4.5; [GIẢ ĐỊNH – Cần xác nhận: OQ-04, OQ-US03-07]; R01-21 |
| P4 | Có lý do hủy không rỗng. [GIẢ ĐỊNH – Cần xác nhận: OQ-US05-03] |
| Hậu điều kiện thành công | **S1** Bảng ở `Cancelled`, version tăng. [ĐẶC TẢ] §3, §4.5<br>**S2** Bảng không dùng lại được: không sửa, tải lại nguồn, trình, duyệt, từ chối, reopen hay điều chỉnh. [ĐẶC TẢ] §4.5<br>**S3** Audit cancel: ai, lúc nào, `Draft` → `Cancelled`, lý do hủy. [ĐẶC TẢ] §6; [GIẢ ĐỊNH – Cần xác nhận: OQ-US05-03]<br>**S4** Lý do hủy cũng lưu trên bảng (`cancelReason`) để hiển thị khi tra cứu. [ĐỀ XUẤT KỸ THUẬT] DD-12<br>**S5** Kỳ thanh toán được giải phóng: NVKD được lập bảng mới cho cùng kỳ; bảng Cancelled chỉ giữ để tra cứu và audit, không tính vào giới hạn một bảng mỗi kỳ. [GIẢ ĐỊNH – Cần xác nhận: OQ-US05-02] |
| Hậu điều kiện thất bại | **F1** Trạng thái bảng không đổi. **F2** Không có audit cancel nào được ghi. **F3** Trả mã lỗi và lý do. [ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §6] |
| Dòng cơ bản | **1.** NVKD gửi yêu cầu hủy kèm `expectedVersion` và lý do. [ĐẶC TẢ] §4.5; [GIẢ ĐỊNH – Cần xác nhận: OQ-US05-03]; version: [ĐỀ XUẤT KỸ THUẬT] DD-08<br>**2.** Hệ thống xác thực và kiểm tra vai trò NVKD. [ĐẶC TẢ] §2<br>**3.** Hệ thống đọc bảng. [ĐỀ XUẤT KỸ THUẬT]<br>**4.** Hệ thống kiểm tra NVKD được phân công hợp đồng của bảng. [GIẢ ĐỊNH – Cần xác nhận: OQ-US05-01]<br>**5.** Hệ thống kiểm tra bảng đang `Draft`. [ĐẶC TẢ] §3, §4.5<br>**6.** Hệ thống kiểm tra lý do hủy không rỗng (bỏ khoảng trắng đầu/cuối). [GIẢ ĐỊNH – Cần xác nhận: OQ-US05-03]<br>**7.** Hệ thống mở giao dịch; cập nhật có điều kiện (`Draft`, version khớp) sang `Cancelled`, lưu `cancelReason`, tăng version; ghi audit cancel kèm lý do; commit. [ĐẶC TẢ] §3, §4.5, §6; [ĐỀ XUẤT KỸ THUẬT] DD-02, DD-03<br>**8.** Sau commit thành công, hệ thống trả bảng `Cancelled` (id, version, lý do) và thông báo hủy thành công. [ĐỀ XUẤT KỸ THUẬT] |
| Dòng thay thế | Mỗi nhánh **kết thúc use case** tại điểm phát hiện, không đi tiếp các bước sau (R01-12).<br>**A2** (bước 2) Chưa xác thực → 401 `UNAUTHENTICATED`; không phải NVKD (kể cả KTT/GĐKD) → 403 `FORBIDDEN`. [ĐẶC TẢ] §2; [GIẢ ĐỊNH – Cần xác nhận: OQ-US05-01]<br>**A3** (bước 3) Bảng không tồn tại → 404 `NOT_FOUND`; lỗi đọc → 503 `SOURCE_UNAVAILABLE`. [ĐỀ XUẤT KỸ THUẬT]<br>**A4** (bước 4) NVKD không được phân công hợp đồng → 403 `FORBIDDEN`; trạng thái giữ nguyên. [GIẢ ĐỊNH – Cần xác nhận: OQ-US05-01]<br>**A5** (bước 5) Bảng ở `PendingApproval`, `Approved`, `Rejected` hoặc đã `Cancelled` → 409 `INVALID_STATE`; với `Rejected`, thông điệp hướng dẫn bấm “Chỉnh sửa” để về `Draft` trước. [ĐẶC TẢ] §3, §4.5, PAY-05; [GIẢ ĐỊNH – Cần xác nhận: OQ-04, OQ-US03-07]<br>**A6** (bước 6) Lý do rỗng hoặc chỉ khoảng trắng → 400 `REASON_REQUIRED`, bảng giữ `Draft`. [GIẢ ĐỊNH – Cần xác nhận: OQ-US05-03]<br>**A7** (bước 7) Cập nhật có điều kiện trả 0 dòng (bảng vừa được trình, sửa hoặc hủy bởi yêu cầu khác) → rollback, 409 `CONCURRENT_MODIFICATION`; client đọc lại bằng E6. [ĐỀ XUẤT KỸ THUẬT] DD-02; R01-14<br>**A7.1** (bước 7) Lỗi mở giao dịch, lưu trạng thái, ghi audit, hoặc commit xác định chưa xảy ra → rollback, 500 `PERSISTENCE_ERROR`; bảng giữ `Draft` (không lưu Cancelled khi chưa ghi được audit). [ĐẶC TẢ] §6; [ĐỀ XUẤT KỸ THUẬT]<br>**A7.2** (bước 7) Mất kết quả commit → 503 `RESULT_UNKNOWN`; không kết luận đã hủy hay chưa; client đọc lại bằng E6 trước khi gửi lại. [ĐỀ XUẤT KỸ THUẬT]; R01-12 |
| NFR | **NFR-PAY-01: áp dụng** – audit `Draft` → `Cancelled` với ai, lúc nào, thay đổi gì, lý do. [ĐẶC TẢ] §6<br>**NFR-PAY-02: không áp dụng** – chỉ cho lập bảng; không đặt SLA cho hủy. [ĐẶC TẢ] §6 |

**Ảnh hưởng sang US-PAY-01** [GIẢ ĐỊNH – Cần xác nhận: OQ-US05-02]: kiểm tra chồng lấn kỳ ở SYS-US-01 bước 7, 11, 12 chỉ xét các bảng khác `Cancelled`; ràng buộc duy nhất ở mức dữ liệu phải loại trừ bảng `Cancelled` (vd. unique có điều kiện) – đồng bộ vào `05-data-design-v2.md`.

## 2. Điểm cần xác nhận

Mẫu 9 cột theo [rules/common.md](../../../../rules/common.md) (R01-28). “Nhóm đề xuất” chưa phải xác nhận khách hàng.

| ID | Vị trí mọi nguồn | Loại | Mô tả | Lý do cần xác nhận | Lựa chọn (đề xuất nhóm áp dụng ở v2) | Ảnh hưởng tới Phần 1 | Trạng thái | Người/ngày/câu trả lời và tham chiếu |
|---|---|---|---|---|---|---|---|---|
| OQ-US05-01 | TA-SPEC §4.5 tr.2 (“Bảng ở trạng thái Draft có thể bị hủy…”); §2 tr.1 | Mơ hồ | Ai được hủy bảng Draft? | Phân quyền chức năng hủy | Chỉ NVKD phụ trách hợp đồng được hủy bảng Draft của hợp đồng đó (cùng quy tắc OQ-US01-03, OQ-US02-01) | Tác nhân, P1, P2, bước 2, 4; A2, A4; AC-01, 04, 10 | Nhóm đề xuất | Nhóm 3 – báo cáo đánh giá, bảng II.2 (10/2026) |
| OQ-US05-02 | TA-SPEC §4.5 (“không dùng lại được”) ↔ §5 PAY-01 (“một bảng… mỗi tháng”) | Mơ hồ | Hủy xong có được lập bảng mới cho cùng kỳ? | Nếu không, kỳ đó không lập được nữa | Được lập bảng mới cho cùng kỳ; Cancelled chỉ để tra cứu/audit, không tính vào giới hạn; kiểm tra trùng chỉ xét bảng chưa hủy | S5; AC-08 | Nhóm đề xuất | Nhóm 3 – bảng II.2 |
| OQ-US05-03 | TA-SPEC §4.5 tr.2; §6 tr.3 | Thiếu | Có bắt buộc lý do hủy; lưu ở đâu? | Màn hình, API, dữ liệu | Bắt buộc nhập lý do; lý do và hành động hủy ghi vào audit log (PAY-08 tương tự cho từ chối, §6). Lưu thêm trên bảng là đề xuất kỹ thuật DD-12 | Kích hoạt, P4, bước 1, 6, 7; A6; S3, S4; AC-01, 07, 11 | Nhóm đề xuất | Nhóm 3 – bảng II.2 |
| OQ-US01-03 | TA-SPEC §2; §4.1 | Thiếu | Phạm vi NVKD trên bảng | Quy tắc chung với hủy | NVKD thao tác bảng của hợp đồng mình phụ trách, không bắt buộc là người lập | Tác nhân; AC-10 | Nhóm đề xuất | Nhóm 3 – bảng II.2 |
| OQ-04 / OQ-US03-07 | TA-SPEC §3 ↔ PAY-08 | Mâu thuẫn / Thiếu | Bảng Rejected có hủy được? | Phạm vi hủy theo §4.5 | Rejected về Draft khi NVKD bấm “Chỉnh sửa”; sau đó hủy được theo §4.5. Không hủy trực tiếp từ Rejected | P3; A5; AC-03, 12 | Nhóm đề xuất | Nhóm 3 – bảng II.2; R01-21 |

## 3. Acceptance criteria

> Mã `AC-US05-01`..`AC-US05-12` là mã tự đặt nội bộ, không phải mã trong đề. Giữ ID v1; tách phần bám đề với phần theo đề xuất nhóm (R01-20); thêm AC-10..12.

| ID | Given / When / Then | Nhãn | Nguồn | OQ |
|---|---|---|---|---|
| AC-US05-01 | Given bảng `Draft`; When hủy thành công; Then bảng `Cancelled` và có audit ai/lúc nào/`Draft` → `Cancelled` (bám đề). Given NVKD phụ trách hợp đồng và lý do không rỗng; Then audit có lý do, bảng có `cancelReason` (theo đề xuất nhóm). | [ĐẶC TẢ] + [GIẢ ĐỊNH – Cần xác nhận] | §3, §4.5, §6 | OQ-US05-01, OQ-US05-03 |
| AC-US05-02 | Given bảng `Cancelled`; When sửa (E8), tải lại nguồn, trình (E9), duyệt (E10), từ chối (E11), lập hồ sơ điều chỉnh (E12), hủy lại (E13) hoặc reopen (E14); Then bị từ chối 409 `INVALID_STATE`, giữ `Cancelled`. | [ĐẶC TẢ] | §4.5 | – (R01-17: trỏ E8–E14) |
| AC-US05-03 | Given bảng `PendingApproval`, `Approved`, `Rejected` hoặc `Cancelled`; When gửi yêu cầu hủy; Then 409 `INVALID_STATE`, trạng thái không đổi. | [ĐẶC TẢ] | §3, §4.5, PAY-05 | – |
| AC-US05-04 | Given bảng `Draft` và người gọi là KTT, GĐKD hoặc NVKD không được phân công hợp đồng; When hủy; Then 403 `FORBIDDEN`, bảng giữ `Draft` (A2, A4). | [GIẢ ĐỊNH – Cần xác nhận] | §2, §4.5 | OQ-US05-01 |
| AC-US05-05 | Given yêu cầu hủy và một yêu cầu khác (trình, sửa, hủy) cùng `expectedVersion`; When xử lý đồng thời; Then đúng một yêu cầu thành công, yêu cầu còn lại 409 `CONCURRENT_MODIFICATION`, không ghi audit cho yêu cầu thua (A7). | [AC dẫn xuất] | §3, §4.5 | – |
| AC-US05-06 | Given bảng `Draft`, người dùng hợp lệ; When ghi audit thất bại; Then rollback, không lưu `Cancelled`, 500 `PERSISTENCE_ERROR`, giữ `Draft` (A7.1). | [AC dẫn xuất] | §6 | – |
| AC-US05-07 | Given lý do hủy rỗng, thiếu hoặc chỉ khoảng trắng; When hủy; Then 400 `REASON_REQUIRED`, giữ `Draft` (A6). | [GIẢ ĐỊNH – Cần xác nhận] | §4.5, §6 | OQ-US05-03 |
| AC-US05-08 | Given bảng của hợp đồng C kỳ M đã `Cancelled` và không còn bảng chưa hủy nào chồng lấn kỳ M; When NVKD lập bảng mới cho C kỳ M; Then được lập; bảng cũ giữ `Cancelled` để tra cứu. | [GIẢ ĐỊNH – Cần xác nhận] | §4.5, PAY-01 | OQ-US05-02 |
| AC-US05-09 | Given mã bảng không tồn tại; When hủy; Then 404 `NOT_FOUND` (A3). | [AC dẫn xuất] | §4.5 | – |
| AC-US05-10 | Given bảng `Draft` do NVKD A lập, NVKD B cùng được phân công hợp đồng; When B hủy với lý do; Then thành công, audit ghi người thực hiện là B. | [GIẢ ĐỊNH – Cần xác nhận] | §2, §4.5, §6 | OQ-US05-01, OQ-US01-03 |
| AC-US05-11 | Given chưa xác thực; When hủy; Then 401 `UNAUTHENTICATED`, không đọc bảng (A2). | [AC dẫn xuất] | §2 | – (R01-12) |
| AC-US05-12 | Given bảng `Rejected`; When NVKD bấm “Chỉnh sửa” (bảng về `Draft`) rồi hủy với lý do; Then bảng `Cancelled`, có hai audit reopen và cancel. | [GIẢ ĐỊNH – Cần xác nhận] | §3, §4.5, PAY-08, §6 | OQ-04, OQ-US03-07 |

## 4. Bàn giao

- Sequence cùng version: [seq-us-05-v2.puml](../../../design/payment-management/v2/diagrams/seq-us-05-v2.puml).
- Cần đồng bộ vào `04-api-contract-v2.md` (chưa tạo): E13 `POST /api/payment-sheets/{id}/cancel` với `reason` **bắt buộc**; tác nhân NVKD phụ trách hợp đồng. Vào `05-data-design-v2.md`: ràng buộc không chồng lấn kỳ loại trừ `Cancelled`; cột `cancel_reason`.

## Thay đổi so với v1

| # | Vị trí | Thay đổi | Căn cứ |
|---|---|---|---|
| 1 | Tác nhân, P1, P2, bước 2, 4, A2, A4, AC-04, 10 | Quyền hủy: chỉ NVKD phụ trách hợp đồng; bỏ phương án KTT/GĐKD. | OQ-US05-01 |
| 2 | Kích hoạt, P4, bước 6, A6, S3, AC-07 | Lý do hủy bắt buộc, ghi audit; lưu trên bảng là đề xuất kỹ thuật. | OQ-US05-03 |
| 3 | S5, AC-08, ghi chú ảnh hưởng US-01 | Cho lập bảng mới cùng kỳ sau hủy; kiểm tra trùng chỉ xét bảng chưa hủy. | OQ-US05-02 |
| 4 | Thứ tự bước, A2–A7.2 | Xác thực/vai trò trước, đọc bảng, rồi phân công; mỗi nhánh lỗi kết thúc use case; thêm 401 và nhánh kết quả commit. | R01-12, R01-25 |
| 5 | P3, A5, AC-12 | Rejected không hủy trực tiếp; về Draft qua “Chỉnh sửa” rồi hủy. | OQ-04, OQ-US03-07; R01-21 |
| 6 | Tác nhân liên quan | Bỏ “KTT, GĐKD theo dõi audit” chưa có căn cứ. | R01-20 |
| 7 | AC-02 | Liệt kê đủ endpoint bị chặn E8–E14. | R01-17 |
| 8 | AC-01, §2 | Tách phần bám đề với phần đề xuất; bảng OQ trạng thái “Nhóm đề xuất”. | R01-20, R01-04 |
