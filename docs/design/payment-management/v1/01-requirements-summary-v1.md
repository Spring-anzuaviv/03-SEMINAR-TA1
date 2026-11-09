# 01 – Tóm tắt yêu cầu (v1)

> Phiên bản: v1 · Ngày: 09/11/2026 · Người phụ trách: Chờ nhóm điền
> Đầu vào: [TA-SPEC](../../../requirements/payment-management/spec.md) §1–6; `sys-us-01..05-v1.md`; [open-questions-v1.md](../../../analysis/payment-management/v1/open-questions-v1.md); `seq-us-01..05-v1.puml`
> AI: ChatGPT 5.5 · Prompt: P-21 trong [prompt-log](../../../workflow/prompt-log.md)
> Trạng thái: Bản lần chạy đầu – Design Pending Approval

Tổng hợp từ 5 đặc tả use case và 5 sequence v1, đối chiếu lại TA-SPEC. Không thêm
nghiệp vụ. `SYS-US`, `AC-USNN-kk`, `OQ-USNN-kk`, `NFR-PAY-0N` là mã nội bộ; chỉ
`US-PAY-0N`, `PAY-0N` là mã của đề.

## 1. Nguồn và phạm vi

| Nguồn                                                                                                                                             | Đã đọc                      | Ghi chú                                                                          |
| ------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- | -------------------------------------------------------------------------------- |
| TA-SPEC §1–6                                                                                                                                      | Có                          | Căn cứ nghiệp vụ                                                                 |
| TA-PDF                                                                                                                                            | Không đọc trực tiếp lần này | Dẫn trang theo [sources.md](../../../requirements/payment-management/sources.md) |
| [sys-us-01-v1](../../../analysis/payment-management/v1/sys-us-01-v1.md) … [sys-us-05-v1](../../../analysis/payment-management/v1/sys-us-05-v1.md) | Có, cả 5                    | Bản trên máy ngày 09/11/2026                                                     |
| [seq-us-01-v1](diagrams/seq-us-01-v1.puml) … [seq-us-05-v1](diagrams/seq-us-05-v1.puml)                                                           | Có, cả 5                    |                                                                                  |
| [open-questions-v1.md](../../../analysis/payment-management/v1/open-questions-v1.md)                                                              | Có                          | Bản đang sửa trên máy, chưa commit                                               |
| `src/Qtkd.Api/`                                                                                                                                   | Có                          | AS-IS, xem 02                                                                    |

**Phạm vi** [ĐẶC TẢ] [TA-SPEC §1; TA-PDF tr.1]: lập (và sửa Draft), trình duyệt,
duyệt/từ chối, điều chỉnh, hủy bảng thanh toán. Hợp đồng, bảng giá, sản lượng là module
khác – chỉ đọc.

## 2. Tác nhân và trạng thái

| Tác nhân                               | Vai trò                                                  | US                                 | Căn cứ                    |
| -------------------------------------- | -------------------------------------------------------- | ---------------------------------- | ------------------------- |
| NVKD                                   | Lập, sửa Draft, trình duyệt                              | 01, 02 (05: Blocked by OQ-US05-01) | [ĐẶC TẢ] §2, §4.1–4.2     |
| KTT                                    | Duyệt/từ chối bảng dưới ngưỡng; điều chỉnh bảng Approved | 03, 04                             | [ĐẶC TẢ] §4.3–4.4, PAY-06 |
| GĐKD                                   | Duyệt/từ chối bảng trên ngưỡng                           | 03                                 | [ĐẶC TẢ] §4.3, PAY-06     |
| Module Hợp đồng / Bảng giá / Sản lượng | Cung cấp dữ liệu chỉ đọc                                 | 01                                 | [ĐẶC TẢ] §1               |

Trạng thái [ĐẶC TẢ] [TA-SPEC §3]: `Draft`, `PendingApproval`, `Approved`, `Rejected`,
`Cancelled`. Không thêm trạng thái.

## 3. User story

| US        | Tên                 | Tác nhân             | Luồng chính (tóm tắt)                                                                                                       | Nhánh lỗi chính                                                                                                                | PAY                  | Đặc tả / Sequence                                                                                  |
| --------- | ------------------- | -------------------- | --------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | -------------------- | -------------------------------------------------------------------------------------------------- |
| US-PAY-01 | Lập bảng            | NVKD                 | Mở form → chọn HĐ → kỳ → bảng giá → xem trước → Lưu nháp (Draft); sửa Draft có version                                      | Sai quyền, HĐ không Active, kỳ trùng, không có giá, chưa đối soát, lỗi nguồn, xung đột, lỗi lưu/audit, không rõ kết quả commit | 01, 02, 03           | [sys](../../../analysis/payment-management/v1/sys-us-01-v1.md) · [seq](diagrams/seq-us-01-v1.puml) |
| US-PAY-02 | Trình duyệt         | NVKD                 | Kiểm tra quyền → Draft → PAY-04 → xác định người duyệt → chuyển PendingApproval + audit → thông báo                         | Không tìm thấy, trình lại, sai trạng thái, tổng âm, thiếu dòng bắt buộc, xung đột, lỗi lưu/audit, gửi thông báo lỗi            | 04, 06               | [sys](../../../analysis/payment-management/v1/sys-us-02-v1.md) · [seq](diagrams/seq-us-02-v1.puml) |
| US-PAY-03 | Duyệt / từ chối     | KTT, GĐKD            | Kiểm tra PendingApproval → vai trò theo tổng → không phải người lập → Approved, hoặc Rejected kèm lý do → audit → thông báo | Sai vai trò, tự duyệt, thiếu lý do, lý do quá dài, xung đột, lỗi lưu/audit                                                     | 05, 06, 07, 08       | [sys](../../../analysis/payment-management/v1/sys-us-03-v1.md) · [seq](diagrams/seq-us-03-v1.puml) |
| US-PAY-04 | Điều chỉnh Approved | KTT                  | Kiểm tra KTT, Approved, biên bản → phương án A (hồ sơ riêng) hoặc B (sửa bảng gốc) → audit                                  | Sai quyền/trạng thái, thiếu biên bản, không đạt tiêu chí, lỗi giao dịch                                                        | 05 (mâu thuẫn)       | [sys](../../../analysis/payment-management/v1/sys-us-04-v1.md) · [seq](diagrams/seq-us-04-v1.puml) |
| US-PAY-05 | Hủy bảng nháp       | Chưa rõ (OQ-US05-01) | Tìm bảng → quyền → Draft → lý do (?) → Cancelled + audit                                                                    | Không tìm thấy, sai quyền, sai trạng thái, thiếu lý do, xung đột, lỗi audit                                                    | 01 (lập lại sau hủy) | [sys](../../../analysis/payment-management/v1/sys-us-05-v1.md) · [seq](diagrams/seq-us-05-v1.puml) |

## 4. Quy tắc nghiệp vụ

| PAY    | Nội dung (TA-SPEC §5, tr.2)                           | US                        | Thiết kế ở                                      | OQ                                        |
| ------ | ----------------------------------------------------- | ------------------------- | ----------------------------------------------- | ----------------------------------------- |
| PAY-01 | HĐ Active + bảng giá phù hợp; một bảng/HĐ/tháng       | 01, 05                    | Guard T1; `FindConflict`                        | OQ-01, OQ-US01-01, OQ-US01-05, OQ-US05-02 |
| PAY-02 | Sản lượng kỳ Đã đối soát                              | 01                        | Guard T1; `IQuantityReader`                     | OQ-US01-04                                |
| PAY-03 | Thành tiền = sản lượng × đơn giá tại thời điểm tính   | 01                        | `PaymentLine` snapshot (DD-04)                  | OQ-US01-01, OQ-US03-03                    |
| PAY-04 | Chặn tổng âm / thiếu dòng bắt buộc; chống trình trùng | 02                        | Guard T3; DD-02                                 | OQ-05                                     |
| PAY-05 | Approved không được sửa                               | 03, 04                    | State `Approved`; T8                            | OQ-03                                     |
| PAY-06 | Trên 500 triệu → GĐKD; còn lại → KTT                  | 02, 03                    | Guard T5; `PaymentSheet.RequiredApproverRole()` | OQ-02, OQ-US03-02, OQ-US03-03             |
| PAY-07 | Người lập không tự duyệt                              | 03                        | Guard T5/T6; `CreatedBy`                        | OQ-US03-01                                |
| PAY-08 | Từ chối phải có lý do; quay về Draft                  | 03 (01, 02 khi trình lại) | Guard T6; T6a/T6b/T7                            | OQ-04, OQ-US03-04, OQ-US03-07             |

## 5. Yêu cầu phi chức năng

| ID nội bộ  | Nội dung (TA-SPEC §6, tr.3)                                               | Áp dụng | Phương án thiết kế                               | Trạng thái             |
| ---------- | ------------------------------------------------------------------------- | ------- | ------------------------------------------------ | ---------------------- |
| NFR-PAY-01 | Audit mọi thay đổi trạng thái và mọi điều chỉnh: ai, lúc nào, thay đổi gì | 01–05   | `AuditEntry`, `IAuditLog` cùng giao dịch (DD-03) | Đề xuất, chưa kiểm thử |
| NFR-PAY-02 | Lập bảng ≤ 3 giây với HĐ có **dưới** 200 dòng                             | Chỉ 01  | Chưa thiết kế đo; điểm đo Blocked by OQ-US01-06  | Chưa đo                |

## 6. Acceptance criteria

| US        | AC trong sys-us v1 | Ghi chú                                                           |
| --------- | ------------------ | ----------------------------------------------------------------- |
| US-PAY-01 | AC-US01-01..26     | Nhiều AC Blocked by OQ (xem sys-us-01 §3)                         |
| US-PAY-02 | AC-US02-01..13     |                                                                   |
| US-PAY-03 | AC-US03-01..15     | Bổ sung ở P-22 (AI soạn theo yêu cầu người dùng, nhóm chưa duyệt) |
| US-PAY-04 | AC-US04-01..10     | Bổ sung ở P-22 cùng bảng tham chiếu OQ; toàn bộ Blocked by OQ-03  |
| US-PAY-05 | AC-US05-01..09     |                                                                   |

Tổng 73 AC; truy vết ở [06-traceability-matrix-v1.md](06-traceability-matrix-v1.md).
Lần P-21 ghi nhận sys-us-03/04 thiếu AC; P-22 đã bổ sung theo yêu cầu người dùng.

## 7. Open Questions

Giữ nguyên ID của BA. Tất cả đang **Cần xác nhận**. Một số OQ của US-PAY-03 (và OQ-02,
OQ-04) có **đề xuất của Đan Anh ngày 07/11/2026**, chưa có xác nhận khách hàng – thiết
kế v1 vẽ cả hai phía, không coi đề xuất là quyết định.

| ID         | Loại      | Vấn đề (tóm tắt)                              | Vị trí đặc tả                     | Ảnh hưởng thiết kế                                                       |
| ---------- | --------- | --------------------------------------------- | --------------------------------- | ------------------------------------------------------------------------ |
| OQ-01      | Mâu thuẫn | Kỳ tháng/quý ↔ duy nhất theo tháng            | §2 ↔ PAY-01                       | `BillingPeriod`, `FindConflict`, khóa duy nhất                           |
| OQ-02      | Mâu thuẫn | Đúng 500.000.000 đ ai duyệt                   | §4.3 "từ…trở lên" ↔ PAY-06 "trên" | Guard T5, `PaymentSheet.RequiredApproverRole()`, người nhận thông báo T3 |
| OQ-03      | Mâu thuẫn | Điều chỉnh bảng Approved                      | §4.4 ↔ PAY-05                     | T8, `PaymentAdjustment`, `UpdateApproved`                                |
| OQ-04      | Mâu thuẫn | Sau từ chối: Rejected hay Draft               | §3 ↔ PAY-08                       | T6a/T6b                                                                  |
| OQ-05      | Thiếu     | Dòng dịch vụ bắt buộc là gì                   | PAY-04                            | Guard T3, `REQUIRED_SERVICE_MISSING`                                     |
| OQ-US01-01 | Mơ hồ     | Tiêu chí bảng giá phù hợp, giá đổi trong kỳ   | §4.1, PAY-01, PAY-03              | Guard T1, `IPriceReader`, DD-04                                          |
| OQ-US01-02 | Thiếu     | Draft được sửa trường nào                     | §4.1                              | T2, `Update`                                                             |
| OQ-US01-03 | Thiếu     | Phạm vi hợp đồng NVKD được lập/sửa            | §2, §4.1                          | Kiểm tra quyền T1/T2                                                     |
| OQ-US01-04 | Thiếu     | Dữ liệu rỗng/0, gộp/tách dòng                 | §2, §4.1, PAY-02                  | Multiplicity `PaymentLine` 0..\*                                         |
| OQ-US01-05 | Mơ hồ     | Mốc đánh giá Active                           | PAY-01                            | Guard T1                                                                 |
| OQ-US01-06 | Thiếu     | Cách đo ≤ 3 giây, đếm dòng                    | §6                                | NFR-PAY-02                                                               |
| OQ-US02-01 | Mơ hồ     | NVKD được trình bảng nào                      | §2, §4.2                          | Kiểm tra quyền T3                                                        |
| OQ-US02-02 | Thiếu     | Kênh thông báo, xử lý gửi lỗi                 | §4.2                              | `INotifier`, DD-05                                                       |
| OQ-US03-01 | Mơ hồ     | Ai là "người lập"; PAY-07 áp cho từ chối?     | PAY-07                            | Guard T5/T6, `CreatedBy`                                                 |
| OQ-US03-02 | Mơ hồ     | Duyệt theo vai trò hay cá nhân, thay thế chéo | §2, §4.3, PAY-06                  | `PaymentSheet.RequiredApproverRole()`                                    |
| OQ-US03-03 | Thiếu     | Tổng so ngưỡng: thời điểm, VAT, làm tròn      | §4.1, §4.3, PAY-03, PAY-06        | `TotalAmount`, `decimal`                                                 |
| OQ-US03-04 | Thiếu     | Ràng buộc lý do từ chối, ai xem               | PAY-08                            | `RejectionReason`, `REASON_TOO_LONG`                                     |
| OQ-US03-05 | Thiếu     | Có thông báo kết quả duyệt không              | §4.3                              | `NotifyResult`                                                           |
| OQ-US03-06 | Mơ hồ     | Chuyển kế toán sau Approved                   | §1                                | Ngoài module (component)                                                 |
| OQ-US03-07 | Thiếu     | Ai/khi nào Rejected → Draft                   | §3, PAY-08                        | T7                                                                       |
| OQ-US04-01 | Thiếu     | Tiêu chí biên bản, nội dung được điều chỉnh   | §4.4                              | T8, `PaymentAdjustment`                                                  |
| OQ-US04-02 | Thiếu     | Duyệt lại, dùng số điều chỉnh khi nào         | §1, §4.4                          | T8                                                                       |
| OQ-US05-01 | Mơ hồ     | Ai được hủy Draft                             | §4.5                              | Guard T4                                                                 |
| OQ-US05-02 | Mơ hồ     | Lập lại sau hủy cùng kỳ                       | §4.5 ↔ PAY-01                     | `FindConflict`, khóa duy nhất                                            |
| OQ-US05-03 | Thiếu     | Lý do hủy bắt buộc không                      | §4.5, §6                          | `CancelReason`, T4                                                       |

### Open Questions mới do design phát hiện

| ID      | Vị trí mọi nguồn                                                                                     | Loại  | Mô tả                                                                                                                                                                                        | Lý do cần xác nhận                                                         | Lựa chọn                                                                     | Ảnh hưởng                                                      | Trạng thái   | Người/ngày/trả lời                          |
| ------- | ---------------------------------------------------------------------------------------------------- | ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | -------------------------------------------------------------- | ------------ | ------------------------------------------- |
| OQ-D-01 | TA-SPEC §3 (chỉ "Draft có thể chuyển sang Cancelled"); §4.5; PAY-01 "một bảng cho mỗi tháng"; PAY-08 | Thiếu | Bảng đang `Rejected` mà không còn cần thiết thì xử lý thế nào? §3 không có `Rejected → Cancelled`. Nếu bảng đi qua Rejected (một phía của OQ-04), nó có tiếp tục chiếm kỳ theo PAY-01 không? | Có thể làm kỳ bị chiếm vĩnh viễn; ảnh hưởng state machine và khóa duy nhất | A: phải về Draft rồi hủy; B: cho hủy từ Rejected; C: Rejected không chiếm kỳ | State `Rejected` (không có lối ra đã xác nhận), `FindConflict` | Cần xác nhận | – (phụ thuộc OQ-04, OQ-US03-07, OQ-US05-02) |

## Kiểm chứng

| Kiểm tra                     | Lệnh                                    | Kết quả                   |
| ---------------------------- | --------------------------------------- | ------------------------- |
| Tên file, liên kết, checksum | `python scripts/verify_agent_config.py` | Xem P-21 trong prompt-log |
| Cú pháp/kết xuất PlantUML    | `java -jar plantuml.jar -checkonly …`   | Xem P-21 trong prompt-log |

Thiết kế chưa được kiểm thử bằng code; đây là bản thiết kế, không phải bằng chứng đã đáp ứng.
