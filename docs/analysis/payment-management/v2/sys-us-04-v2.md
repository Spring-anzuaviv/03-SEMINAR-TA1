# SYS-US-04 – Điều chỉnh bảng thanh toán đã duyệt (v2)

> Phiên bản: v2 · Ngày: 11/11/2026 · Người phụ trách: Phạm Phát Lộc
> Đầu vào: [TA-SPEC](../../../requirements/payment-management/spec.md) §1, §3, §4.3, §4.4, §5 PAY-03, PAY-05..07, §6; TA-PDF tr.1–3; sys-us-04-v1.md; [sys-us-01-v2.md](sys-us-01-v2.md) (quy tắc tính tiền); Báo cáo đánh giá nhóm 3 – bảng II.2 cột “Cách nhóm xử lý” và bảng III (R01-xx Đúng)
> AI: Claude Code / Claude Opus 5.5 · Prompt: P-29 trong [prompt-log](../../../workflow/prompt-log.md)
> Trạng thái: Bản sau review – BA Pending Approval
> Nhãn: [ĐẶC TẢ] · [AC dẫn xuất] · [ĐỀ XUẤT KỸ THUẬT] · [GIẢ ĐỊNH – Cần xác nhận: OQ-…] = áp dụng cách xử lý **nhóm đề xuất**, chưa có xác nhận của khách hàng (R01-20). Mã SYS/AC/OQ là mã nội bộ.

**Thay đổi chính so với v1:** v1 trình bày hai phương án A (hồ sơ riêng) và B (sửa bảng gốc theo ngoại lệ PAY-05). Theo đề xuất nhóm cho OQ-03, v2 **chỉ giữ phương án A**: bảng `Approved` không bị sửa; điều chỉnh là **hồ sơ điều chỉnh** riêng, liên kết bảng gốc, phải được **GĐKD duyệt** trước khi áp dụng (OQ-US04-02). Mã use case đổi từ SYS-PAY-04 thành SYS-US-04 (R01-23).

## 1. Use case

### 1.1. Căn cứ

- [ĐẶC TẢ] US-PAY-04: KTT có thể điều chỉnh bảng đã Approved nếu có biên bản xác nhận đính kèm; mọi điều chỉnh phải được ghi log. [TA-SPEC §4.4; TA-PDF tr.2]
- [ĐẶC TẢ] PAY-05: bảng Approved không được sửa dưới bất kỳ hình thức nào. PAY-07: người lập không duyệt bảng do mình lập. §6: audit mọi điều chỉnh. [TA-SPEC §5, §6]
- [GIẢ ĐỊNH – Cần xác nhận: OQ-03] Bảng Approved giữ nguyên; điều chỉnh lưu thành hồ sơ riêng kèm biên bản và nội dung thay đổi; **số liệu hiệu lực = bảng gốc + các hồ sơ điều chỉnh đã duyệt**. Cách này đáp ứng đồng thời §4.4 và PAY-05.
- [GIẢ ĐỊNH – Cần xác nhận: OQ-US04-02] KTT lập hồ sơ nên theo PAY-07 không tự duyệt; mọi hồ sơ do GĐKD duyệt, kể cả khi tổng sau điều chỉnh dưới 500 triệu hoặc đi qua ngưỡng. Kế toán chỉ dùng số liệu mới sau khi hồ sơ được duyệt.

### 1.2. Thông tin chung

| Mục | Đặc tả |
|---|---|
| Tên | SYS-US-04 – Điều chỉnh bảng thanh toán đã duyệt. [ĐẶC TẢ] §4.4; R01-23 |
| Tác nhân chính | Thao tác A (lập hồ sơ): KTT. Thao tác B (duyệt hồ sơ): GĐKD. [ĐẶC TẢ] §4.4; [GIẢ ĐỊNH – Cần xác nhận: OQ-US04-02] |
| Tác nhân liên quan | Module kế toán (ngoài phạm vi) đọc số liệu hiệu lực sau khi hồ sơ được duyệt. [GIẢ ĐỊNH – Cần xác nhận: OQ-US03-06, OQ-US04-02] |
| Mục tiêu | Ghi nhận sửa sai sau duyệt có biên bản, được GĐKD duyệt, có lịch sử đầy đủ, không sửa bảng Approved. [ĐẶC TẢ] §4.4, PAY-05, §6 |
| Kích hoạt | A: KTT phát hiện sai sót trên bảng Approved, gửi nội dung điều chỉnh và biên bản. B: GĐKD mở hồ sơ đang chờ duyệt và chọn “Duyệt hồ sơ”. [ĐẶC TẢ] §4.4; [ĐỀ XUẤT KỸ THUẬT] tên nút |
| P1 (A) | Người thao tác đã xác thực, vai trò KTT. Bảng tồn tại, ở `Approved`. [ĐẶC TẢ] §4.4 |
| P2 (A) | Có biên bản **hợp lệ**: số biên bản, ngày lập, file đính kèm và xác nhận của hai bên. [ĐẶC TẢ] §4.4 (có biên bản); [GIẢ ĐỊNH – Cần xác nhận: OQ-US04-01] (tiêu chí hợp lệ) |
| P3 (A) | Nội dung điều chỉnh chỉ gồm: sửa sản lượng và/hoặc đơn giá của dòng, thêm dòng, bớt dòng; ít nhất một thay đổi; **mỗi thay đổi có lý do**. [GIẢ ĐỊNH – Cần xác nhận: OQ-US04-01] |
| P4 (A) | Bảng chưa có hồ sơ điều chỉnh nào đang chờ duyệt. [GIẢ ĐỊNH – Cần xác nhận: OQ-US04-03] |
| P1 (B) | Người thao tác đã xác thực, vai trò GĐKD, không phải người lập hồ sơ (PAY-07). Hồ sơ tồn tại, đang chờ duyệt; bảng gốc vẫn `Approved`. [ĐẶC TẢ] PAY-07; [GIẢ ĐỊNH – Cần xác nhận: OQ-US04-02, OQ-US04-03] |
| Hậu điều kiện – A thành công | Hồ sơ điều chỉnh được lưu ở trạng thái xử lý “Chờ duyệt”, liên kết bảng gốc, gồm biên bản, danh sách thay đổi (giá trị trước/sau, lý do), số liệu đề xuất sau điều chỉnh, người lập; audit adjust (ai, lúc nào, thay đổi gì). **Bảng gốc giữ nguyên số liệu và trạng thái `Approved`**; số liệu hiệu lực chưa đổi. [ĐẶC TẢ] §4.4, PAY-05, §6; [GIẢ ĐỊNH – Cần xác nhận: OQ-03, OQ-US04-03] |
| Hậu điều kiện – B thành công | Hồ sơ chuyển “Đã duyệt”, ghi người duyệt và thời điểm; audit; số liệu hiệu lực = bảng gốc + các hồ sơ đã duyệt. Bảng gốc vẫn không đổi. [GIẢ ĐỊNH – Cần xác nhận: OQ-03, OQ-US04-02] |
| Hậu điều kiện – thất bại | Không có hồ sơ/audit lưu một phần; bảng gốc không đổi; trả mã lỗi và lý do. [ĐẶC TẢ] §6; [ĐỀ XUẤT KỸ THUẬT] |
| NFR | NFR-PAY-01 áp dụng: audit cả lập và duyệt hồ sơ, có giá trị trước/sau từng thay đổi. NFR-PAY-02 không áp dụng. [ĐẶC TẢ] §6 |

**Trạng thái xử lý của hồ sơ điều chỉnh** [GIẢ ĐỊNH – Cần xác nhận: OQ-US04-03]: “Chờ duyệt” → “Đã duyệt” (GĐKD duyệt) hoặc → “Bị từ chối” (GĐKD từ chối kèm lý do). Đây là trạng thái của **hồ sơ**, không phải trạng thái bảng thanh toán; năm trạng thái của bảng ở TA-SPEC §3 giữ nguyên. Tên enum tạm: `AdjustmentStatus { Pending, Approved, Declined }`.

**Tính số liệu sau điều chỉnh** [GIẢ ĐỊNH – Cần xác nhận: OQ-US04-01, OQ-US03-03] – dùng cùng quy tắc SYS-US-01 §1.2: mỗi dòng sau điều chỉnh `thànhTiền = ceil(sảnLượng × đơnGiá)`; `tạmTính = Σ thànhTiền`; `tiềnThuế = ceil(tạmTính × thuếSuất của bảng gốc)`; `tổng = tạmTính + tiềnThuế`. Cơ sở để áp thay đổi là số liệu hiệu lực tại lúc lập hồ sơ.

### 1.3. Dòng cơ bản – A. KTT lập hồ sơ điều chỉnh

| Bước | Tương tác và kết quả | Căn cứ |
|---|---|---|
| 1 | KTT chọn bảng Approved, nhập thông tin biên bản (số, ngày lập, xác nhận hai bên), đính kèm file biên bản, nhập danh sách thay đổi và lý do từng thay đổi, gửi yêu cầu. | [ĐẶC TẢ] §4.4; [GIẢ ĐỊNH – Cần xác nhận: OQ-US04-01] |
| 2 | Hệ thống xác thực và kiểm tra vai trò KTT. | [ĐẶC TẢ] §4.4 |
| 3 | Đọc bảng gốc và số liệu hiệu lực (bảng gốc + hồ sơ đã duyệt); kiểm tra bảng tồn tại và `Approved`. | [ĐẶC TẢ] §3, §4.4; [GIẢ ĐỊNH – Cần xác nhận: OQ-03] |
| 4 | Kiểm tra biên bản đủ số biên bản, ngày lập, file đính kèm và xác nhận của hai bên. | [GIẢ ĐỊNH – Cần xác nhận: OQ-US04-01] |
| 5 | Kiểm tra từng thay đổi: loại hợp lệ (sửa dòng / thêm dòng / bớt dòng); sửa và bớt phải trỏ tới dòng đang hiệu lực; thêm dòng không trùng dịch vụ đã có; sản lượng, đơn giá không âm; có lý do. | [GIẢ ĐỊNH – Cần xác nhận: OQ-US04-01]; trùng dịch vụ, không âm: [ĐỀ XUẤT KỸ THUẬT] |
| 6 | Tính số liệu đề xuất sau điều chỉnh (dòng, tạm tính, thuế, tổng) theo §1.2. | [ĐẶC TẢ] PAY-03; [GIẢ ĐỊNH – Cần xác nhận: OQ-US03-03] |
| 7 | Mở giao dịch: lưu hồ sơ (Chờ duyệt), các thay đổi (trước/sau, lý do), tham chiếu biên bản; ràng buộc mỗi bảng tối đa một hồ sơ Chờ duyệt; ghi audit adjust; commit. Không ghi vào bảng gốc. | [ĐẶC TẢ] PAY-05, §6; [GIẢ ĐỊNH – Cần xác nhận: OQ-03, OQ-US04-03]; [ĐỀ XUẤT KỸ THUẬT] giao dịch |
| 8 | Trả kết quả: mã hồ sơ, trạng thái Chờ duyệt, số liệu đề xuất; hiển thị “Hồ sơ chờ GĐKD duyệt – số liệu hiệu lực chưa thay đổi”. | [GIẢ ĐỊNH – Cần xác nhận: OQ-US04-02] |

### 1.4. Dòng cơ bản – B. GĐKD duyệt hồ sơ điều chỉnh

| Bước | Tương tác và kết quả | Căn cứ |
|---|---|---|
| B1 | GĐKD mở hồ sơ Chờ duyệt, xem bảng gốc, biên bản, thay đổi và số liệu đề xuất; chọn “Duyệt hồ sơ” (gửi `expectedVersion` của hồ sơ). | [GIẢ ĐỊNH – Cần xác nhận: OQ-US04-02] |
| B2 | Hệ thống xác thực, kiểm tra vai trò GĐKD. | [GIẢ ĐỊNH – Cần xác nhận: OQ-US04-02] |
| B3 | Đọc hồ sơ và bảng gốc; kiểm tra hồ sơ tồn tại, Chờ duyệt, bảng gốc `Approved`. | [GIẢ ĐỊNH – Cần xác nhận: OQ-US04-03] |
| B4 | Kiểm tra người duyệt khác người lập hồ sơ. | [ĐẶC TẢ] PAY-07 (áp dụng tương tự cho hồ sơ); [GIẢ ĐỊNH – Cần xác nhận: OQ-US04-02] |
| B5 | Mở giao dịch: cập nhật có điều kiện hồ sơ Chờ duyệt → Đã duyệt (version khớp), ghi người duyệt, thời điểm; ghi audit (ai, lúc nào, hồ sơ Chờ duyệt → Đã duyệt, số liệu hiệu lực trước/sau); commit. Bảng gốc không đổi. | [ĐẶC TẢ] PAY-05, §6; [ĐỀ XUẤT KỸ THUẬT] DD-02 |
| B6 | Trả kết quả: hồ sơ Đã duyệt; số liệu hiệu lực mới (bảng gốc + hồ sơ đã duyệt). | [GIẢ ĐỊNH – Cần xác nhận: OQ-03] |

### 1.5. Dòng thay thế

| Nhánh | Xử lý | Căn cứ |
|---|---|---|
| 2a | Chưa xác thực → 401 `UNAUTHENTICATED`; không phải KTT → 403 `FORBIDDEN`. | [ĐẶC TẢ] §4.4 |
| 3a | Bảng không tồn tại → 404 `NOT_FOUND`; không `Approved` → 409 `INVALID_STATE`. | [ĐẶC TẢ] §3, §4.4 |
| 4a | Thiếu biên bản hoặc biên bản thiếu số, ngày lập, file hoặc xác nhận hai bên → 400 `MINUTES_INVALID` nêu trường thiếu. | [ĐẶC TẢ] §4.4; [GIẢ ĐỊNH – Cần xác nhận: OQ-US04-01] |
| 5a | Không có thay đổi, loại thay đổi không thuộc phạm vi (vd. đổi hợp đồng, kỳ, thuế suất), thay đổi thiếu lý do, trỏ dòng không tồn tại, sản lượng/đơn giá âm → 400 `ADJUSTMENT_INVALID` nêu thay đổi lỗi. | [GIẢ ĐỊNH – Cần xác nhận: OQ-US04-01]; [ĐỀ XUẤT KỸ THUẬT] |
| 7a | Bảng đã có hồ sơ Chờ duyệt (kể cả hai yêu cầu lập đồng thời) → rollback yêu cầu thua, 409 `ADJUSTMENT_PENDING_EXISTS`. | [GIẢ ĐỊNH – Cần xác nhận: OQ-US04-03]; R01-10 |
| 7b | Lỗi lưu hồ sơ/thay đổi/audit hoặc commit xác định chưa xảy ra → rollback, 500 `PERSISTENCE_ERROR`; mất kết quả commit → 503 `RESULT_UNKNOWN`. | [ĐẶC TẢ] §6; [ĐỀ XUẤT KỸ THUẬT] |
| B2a | Chưa xác thực → 401; không phải GĐKD → 403 `FORBIDDEN`. | [GIẢ ĐỊNH – Cần xác nhận: OQ-US04-02] |
| B3a | Hồ sơ không tồn tại → 404; không ở Chờ duyệt → 409 `INVALID_STATE`. | [AC dẫn xuất] |
| B4a | Người duyệt là người lập hồ sơ → 403 `SELF_APPROVAL_FORBIDDEN`. | [ĐẶC TẢ] PAY-07 |
| B5a | 0 dòng cập nhật (hồ sơ vừa được xử lý) → 409 `CONCURRENT_MODIFICATION`; lỗi lưu/audit → rollback, 500; mất kết quả commit → 503. | [ĐỀ XUẤT KỸ THUẬT] DD-02; R01-14 |
| B7 | GĐKD chọn “Từ chối hồ sơ”, nhập lý do → kiểm tra như B2–B4 và lý do không rỗng; giao dịch Chờ duyệt → Bị từ chối, lưu lý do, audit; số liệu hiệu lực không đổi; KTT có thể lập hồ sơ mới. Lý do rỗng → 400 `REASON_REQUIRED`. | [GIẢ ĐỊNH – Cần xác nhận: OQ-US04-03] |
| X1 | Mọi yêu cầu sửa trực tiếp bảng Approved (E8 update, submit, cancel…) → 409 `INVALID_STATE`; điều chỉnh chỉ qua hồ sơ. | [ĐẶC TẢ] PAY-05 |

## 2. Điểm cần xác nhận

Mẫu 9 cột theo [rules/common.md](../../../../rules/common.md) (R01-28). “Nhóm đề xuất” chưa phải xác nhận khách hàng.

| ID | Vị trí mọi nguồn | Loại | Mô tả | Lý do cần xác nhận | Lựa chọn (áp dụng ở v2) | Ảnh hưởng tới Phần 1 | Trạng thái | Người/ngày/câu trả lời và tham chiếu |
|---|---|---|---|---|---|---|---|---|
| OQ-03 | TA-SPEC §4.4 “KTT có thể điều chỉnh bảng đã Approved” ↔ §5 PAY-05 “không được sửa dưới bất kỳ hình thức nào”; TA-PDF tr.2 | Mâu thuẫn quy tắc | Điều chỉnh là hồ sơ riêng hay sửa trực tiếp bảng gốc? | Quyết định nơi ghi thay đổi, có cần ngoại lệ PAY-05 | Bảng Approved giữ nguyên; hồ sơ điều chỉnh riêng liên kết bảng gốc, kèm biên bản, nội dung thay đổi; số liệu hiệu lực = bảng gốc + hồ sơ đã duyệt (phương án B của v1 bị loại) | Toàn bộ §1; AC-01, 02, 03, 11 | Nhóm đề xuất | Nhóm 3 – báo cáo đánh giá, bảng II.2 (10/2026) |
| OQ-US04-01 | TA-SPEC §4.4 “biên bản xác nhận đính kèm” | Thiếu | Biên bản thế nào là hợp lệ; được điều chỉnh nội dung gì | Kiểm tra đầu vào | Hợp lệ khi có số biên bản, ngày lập, file đính kèm và xác nhận của hai bên; được điều chỉnh sản lượng, đơn giá từng dòng, thêm/bớt dòng; mỗi thay đổi có lý do và ghi log | P2, P3, bước 4–5; 4a, 5a; AC-06, 07, 12 | Nhóm đề xuất | Nhóm 3 – bảng II.2 |
| OQ-US04-02 | TA-SPEC §4.3, §4.4, PAY-06, PAY-07 | Thiếu luồng | Có duyệt lại sau điều chỉnh, ai duyệt (GĐKD từng duyệt; tổng qua ngưỡng 500 triệu; KTT điều chỉnh bảng mình từng duyệt) | Thẩm quyền và thời điểm áp dụng số mới | Hồ sơ phải được duyệt trước khi áp dụng; mọi hồ sơ do GĐKD duyệt, kể cả tổng dưới 500 triệu hoặc đi qua ngưỡng; kế toán chỉ dùng số mới sau khi hồ sơ được duyệt | Tác nhân, §1.4; AC-10, 13, 14 | Nhóm đề xuất | Nhóm 3 – bảng II.2; R01-16 (Đúng) |
| OQ-US04-03 | TA-SPEC §3 (5 trạng thái bảng), §4.4; suy ra từ OQ-03 và OQ-US04-02 | Thiếu | Hồ sơ điều chỉnh có trạng thái xử lý nào? GĐKD có được từ chối hồ sơ không? Một bảng có được nhiều hồ sơ chờ duyệt cùng lúc không? Có thông báo cho GĐKD/KTT không? | Đề xuất nhóm yêu cầu duyệt hồ sơ nhưng chưa nêu các điểm này; ảnh hưởng dữ liệu, đồng thời (AC-09) và luồng | Giả định tạm: hồ sơ Chờ duyệt → Đã duyệt / Bị từ chối (kèm lý do); mỗi bảng tối đa một hồ sơ Chờ duyệt; chưa thiết kế thông báo | P4, P1(B), §1.2 trạng thái hồ sơ; 7a, B7; AC-09, 15 | Cần xác nhận | Câu hỏi mới ở v2 (P-29); chưa có câu trả lời |
| OQ-US03-06 | TA-SPEC §1 | Mơ hồ | Chuyển kế toán sau duyệt | Phạm vi module | Ngoài phạm vi; module chỉ bảo đảm số liệu hiệu lực đọc được | Tác nhân liên quan; AC-10 | Nhóm đề xuất | Nhóm 3 – bảng II.2 |
| OQ-US03-03 | TA-SPEC §4.1, §4.3, PAY-03 | Thiếu | VAT, làm tròn | Tính số liệu sau điều chỉnh | Thuế suất % (của bảng gốc), làm tròn lên theo đồng ở dòng, thuế, tổng | §1.2 tính số liệu; bước 6 | Nhóm đề xuất | Nhóm 3 – bảng II.2 |

## 3. Acceptance criteria

Mã `AC-US04-kk` tự đặt. Giữ ID v1; AC-03 đã hủy; thêm AC-11..15. Trạng thái AC được thống nhất với ma trận truy vết (R01-17).

| ID | Given / When / Then | Nhãn | Nguồn | OQ |
|---|---|---|---|---|
| AC-US04-01 | Given KTT, bảng Approved, biên bản hợp lệ, thay đổi hợp lệ; When lập hồ sơ (bước 1–8); Then hồ sơ Chờ duyệt được lưu, liên kết bảng gốc và biên bản, có audit ai/lúc nào/thay đổi gì. | [GIẢ ĐỊNH – Cần xác nhận] | §4.4, §6 | OQ-03, OQ-US04-01 |
| AC-US04-02 | Given hồ sơ được lập (hoặc được duyệt); When đọc bảng gốc; Then bảng vẫn `Approved` và giữ nguyên số liệu đã duyệt. | [GIẢ ĐỊNH – Cần xác nhận] | §4.4, PAY-05 | OQ-03 |
| AC-US04-03 | Đã hủy – phương án B (sửa bảng gốc theo ngoại lệ PAY-05) bị loại theo đề xuất nhóm cho OQ-03; không tái sử dụng ID. | – | – | OQ-03 |
| AC-US04-04 | Given người gọi không phải KTT; When lập hồ sơ; Then 403, không ghi dữ liệu (2a). | [ĐẶC TẢ] | §4.4 | – |
| AC-US04-05 | Given bảng không tồn tại hoặc không ở `Approved`; When lập hồ sơ; Then 404 / 409 `INVALID_STATE` (3a). | [AC dẫn xuất] | §3, §4.4 | – |
| AC-US04-06 | Given không có biên bản đính kèm; When lập hồ sơ; Then 400 `MINUTES_INVALID` (4a). | [ĐẶC TẢ] | §4.4 | – |
| AC-US04-07 | Given biên bản thiếu số, ngày lập, file hoặc xác nhận hai bên; hoặc thay đổi thiếu lý do / ngoài phạm vi; When lập hồ sơ; Then 400 `MINUTES_INVALID` / `ADJUSTMENT_INVALID` nêu trường lỗi (4a, 5a). | [GIẢ ĐỊNH – Cần xác nhận] | §4.4 | OQ-US04-01 |
| AC-US04-08 | Given lỗi khi ghi hồ sơ, thay đổi hoặc audit; When lập hoặc duyệt hồ sơ; Then rollback toàn bộ, bảng và hồ sơ không đổi, 500 (7b, B5a). | [AC dẫn xuất] | §6 | – |
| AC-US04-09 | Given hai yêu cầu lập hồ sơ đồng thời cho cùng bảng (hoặc bảng đã có hồ sơ Chờ duyệt); When xử lý; Then chỉ một hồ sơ Chờ duyệt được lưu, yêu cầu thua 409 `ADJUSTMENT_PENDING_EXISTS`. Given hai yêu cầu duyệt đồng thời cùng hồ sơ; Then đúng một thành công, còn lại 409 `CONCURRENT_MODIFICATION`. | [ĐỀ XUẤT KỸ THUẬT] / [GIẢ ĐỊNH – Cần xác nhận] | §4.4, §6; R01-10 | OQ-US04-03 |
| AC-US04-10 | Given hồ sơ Chờ duyệt; When module kế toán đọc số liệu hiệu lực; Then nhận số liệu bảng gốc (chưa áp hồ sơ). Given hồ sơ đã được GĐKD duyệt; Then nhận bảng gốc + hồ sơ đã duyệt. | [GIẢ ĐỊNH – Cần xác nhận] | §1, §4.4 | OQ-US04-02, OQ-US03-06 |
| AC-US04-11 | Given dòng có sản lượng 100, đơn giá 1.000 đ; When hồ sơ sửa sản lượng thành 120 và được duyệt; Then số liệu hiệu lực của dòng là 120 × 1.000 = 120.000 đ, tạm tính, thuế (thuế suất bảng gốc) và tổng hiệu lực tính lại, làm tròn lên. | [GIẢ ĐỊNH – Cần xác nhận] | PAY-03, §4.4 | OQ-03, OQ-US03-03 |
| AC-US04-12 | Given hồ sơ có thay đổi sửa dòng, thêm dòng và bớt dòng, mỗi thay đổi có lý do; When lưu; Then mỗi thay đổi lưu giá trị trước/sau và lý do, audit có đủ các thay đổi. | [GIẢ ĐỊNH – Cần xác nhận] | §4.4, §6 | OQ-US04-01 |
| AC-US04-13 | Given hồ sơ Chờ duyệt; When KTT hoặc người không phải GĐKD duyệt; Then 403. When GĐKD duyệt, kể cả khi tổng hiệu lực mới < 500.000.000 đ; Then hồ sơ Đã duyệt, audit ghi người duyệt, thời điểm, số liệu hiệu lực trước/sau (B1–B6). | [GIẢ ĐỊNH – Cần xác nhận] | §4.3, §4.4, PAY-07 | OQ-US04-02 |
| AC-US04-14 | Given người lập hồ sơ cũng là người gọi duyệt; When duyệt; Then 403 `SELF_APPROVAL_FORBIDDEN` (B4a). | [ĐẶC TẢ] | PAY-07 | OQ-US04-02 |
| AC-US04-15 | Given hồ sơ Chờ duyệt; When GĐKD từ chối với lý do; Then hồ sơ Bị từ chối, lý do lưu, audit; số liệu hiệu lực không đổi; KTT lập được hồ sơ mới. Lý do rỗng → 400 (B7). | [GIẢ ĐỊNH – Cần xác nhận] | §4.4, §6 | OQ-US04-03 |

## 4. Bàn giao

- Sequence cùng version: [seq-us-04-v2.puml](../../../design/payment-management/v2/diagrams/seq-us-04-v2.puml) – thao tác A (lập hồ sơ) và B (GĐKD duyệt/từ chối hồ sơ).
- Tên dùng tạm cần đồng bộ vào `03`, `04`, `05`, `class-v2.puml` (chưa tạo): `PaymentAdjustment` (hồ sơ), `AdjustmentChange` (thay đổi), `AdjustmentStatus { Pending, Approved, Declined }`; `IAdjustmentRepository.Create/GetById/FindPending/Transition`; `PaymentAdjustmentService.Adjust(id, minutes, changes, currentUser)` (đồng bộ chữ ký với request E12 – R01-10), `ApproveAdjustment`, `DeclineAdjustment`; endpoint E12 `POST /api/payment-sheets/{id}/adjustments`, E16 `POST /api/payment-sheets/{id}/adjustments/{adjustmentId}/approve`, E17 `…/decline` (tạm); mã lỗi `MINUTES_INVALID`, `ADJUSTMENT_INVALID`, `ADJUSTMENT_PENDING_EXISTS`. Bỏ `IPaymentRepository.UpdateApproved` (phương án B).

## Thay đổi so với v1

| # | Vị trí | Thay đổi | Căn cứ |
|---|---|---|---|
| 1 | Tên, sequence | Đổi SYS-PAY-04 thành SYS-US-04. | R01-23 |
| 2 | Toàn bộ §1; AC-03 | Bỏ phương án B; chỉ giữ hồ sơ điều chỉnh riêng; bảng Approved không đổi; AC-03 đánh dấu Đã hủy. | OQ-03 |
| 3 | P2, P3, bước 4–5, 4a, 5a, AC-07, 12 | Tiêu chí biên bản hợp lệ và phạm vi điều chỉnh (sản lượng, đơn giá, thêm/bớt dòng, lý do từng thay đổi). | OQ-US04-01 |
| 4 | §1.4, AC-10, 13, 14 | Thêm thao tác GĐKD duyệt hồ sơ trước khi áp dụng; kế toán dùng số mới sau duyệt. | OQ-US04-02; R01-16 |
| 5 | §1.2 trạng thái hồ sơ, P4, 7a, B7, AC-09, 15; OQ-US04-03 mới | Giả định trạng thái hồ sơ, một hồ sơ chờ duyệt/bảng, từ chối hồ sơ; AC-09 áp dụng cho hồ sơ điều chỉnh. | R01-10; câu hỏi mới OQ-US04-03 |
| 6 | §1.2 tính số liệu, AC-11 | Số liệu sau điều chỉnh dùng cùng quy tắc tiền với US-01 (VAT, làm tròn lên). | OQ-US03-03; R01-02 |
| 7 | §3 | AC-04..06 thống nhất trạng thái với ma trận (không còn ghi Blocked khác nhau). | R01-17 |
