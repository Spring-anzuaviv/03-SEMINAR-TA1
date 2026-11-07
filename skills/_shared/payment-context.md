# Ngữ cảnh dùng chung cho các skill – Bảng thanh toán TA 1–2

Tài liệu tham chiếu cho mọi skill trong [skills/](../README.md). Không thay
[AGENTS.md](../../AGENTS.md); khi có khác biệt, AGENTS.md và TA-SPEC thắng.
Tên file, version và mã ID theo skill [naming-versioning](../naming-versioning/SKILL.md).
Mọi dữ kiện dưới đây phải được kiểm tra lại trên file thực trước khi dùng.

## 1. Nguồn và cách dẫn

| Mã | File | Dùng để |
|---|---|---|
| TA-SPEC | [spec.md](../../docs/requirements/payment-management/spec.md) | Căn cứ nghiệp vụ (bản chép §1–6 của TA-PDF) |
| TA-PDF | [assignment-ta-1-2.pdf](../../docs/requirements/payment-management/assignment-ta-1-2.pdf) | Dẫn trang: §1–3 tr.1; §4–5 tr.2; §6 tr.3 |
| AS-IS | [src/Qtkd.Api/](../../src/Qtkd.Api) | Bằng chứng hiện trạng, không xác lập TO-BE |

Sổ nguồn: [sources.md](../../docs/requirements/payment-management/sources.md).
Mẫu dẫn: `[ĐẶC TẢ] [TA-SPEC §4.3, US-PAY-03; TA-PDF tr.2]`.
Nhãn bắt buộc: `[ĐẶC TẢ]`, `[AC dẫn xuất]`, `[THAM KHẢO]`, `[ĐỀ XUẤT KỸ THUẬT]`,
`[GIẢ ĐỊNH – Cần xác nhận]`, `[QUYẾT ĐỊNH ĐÃ XÁC NHẬN]` (chỉ khi có người/ngày/tham chiếu).

## 2. Danh mục ID phải bao phủ

| ID | Nội dung rút gọn | Vị trí |
|---|---|---|
| US-PAY-01 | Lập bảng (NVKD), sinh dòng, tổng tiền, lưu Draft; sửa khi Draft | §4.1, tr.2 |
| US-PAY-02 | Trình duyệt (NVKD), kiểm tra PAY-04, → PendingApproval, thông báo người duyệt | §4.2, tr.2 |
| US-PAY-03 | Duyệt (→ Approved) / từ chối kèm lý do | §4.3, tr.2 |
| US-PAY-04 | KTT điều chỉnh bảng Approved khi có biên bản; ghi log | §4.4, tr.2 |
| US-PAY-05 | Hủy bảng Draft → Cancelled, không dùng lại | §4.5, tr.2 |
| PAY-01 | HĐ Active + bảng giá phù hợp; một bảng/HĐ/tháng | §5, tr.2 |
| PAY-02 | Sản lượng kỳ phải "Đã đối soát" | §5, tr.2 |
| PAY-03 | Thành tiền = sản lượng × đơn giá tại thời điểm tính | §5, tr.2 |
| PAY-04 | Chặn tổng âm/thiếu dòng bắt buộc; chống trình trùng | §5, tr.2 |
| PAY-05 | Approved không được sửa dưới bất kỳ hình thức nào | §5, tr.2 |
| PAY-06 | Trên 500 triệu → GĐKD; còn lại → KTT | §5, tr.2 |
| PAY-07 | Người lập không duyệt bảng mình lập | §5, tr.2 |
| PAY-08 | Từ chối phải có lý do; quay về Draft để sửa và trình lại | §5, tr.2 |
| NFR-PAY-01 | Audit mọi thay đổi trạng thái/điều chỉnh: ai, lúc nào, thay đổi gì | §6 gạch 1, tr.3 (mã nội bộ) |
| NFR-PAY-02 | Lập bảng ≤ 3 giây với HĐ có **dưới** 200 dòng | §6 gạch 2, tr.3 (mã nội bộ) |

Vai trò §2: NVKD, KTT, GĐKD. Trạng thái §3 (đúng chính tả, không thêm):
`Draft`, `PendingApproval`, `Approved`, `Rejected`, `Cancelled`.

Ánh xạ use case hệ thống: `US-PAY-NN` ↔ `docs/analysis/payment-management/vK/sys-us-NN-vK.md`
↔ `docs/design/payment-management/vK/diagrams/seq-us-NN[-<thao-tac>]-vK.puml`.

| US | Thao tác (động từ dùng chung) | PAY/§ thường liên quan |
|---|---|---|
| 01 | `create`, `update` | PAY-01, 02, 03; §2 kỳ thanh toán; NFR-PAY-02 |
| 02 | `submit` | PAY-04, 06 (chọn người nhận thông báo); §3 |
| 03 | `approve`, `reject` | PAY-05, 06, 07, 08; §3; NFR-PAY-01 |
| 04 | `adjust` | PAY-05 (mâu thuẫn); §4.4 biên bản; NFR-PAY-01 |
| 05 | `cancel` | §3, §4.5 |

## 3. Quy ước mã tự đặt

Xem [naming-versioning §4](../naming-versioning/SKILL.md#4-mã-id). Mã tự đặt không
phải mã trong đề; ghi rõ điều đó lần đầu xuất hiện trong mỗi file.

## 4. Mâu thuẫn/thiếu đã biết – ID giữ chỗ, không tự chọn phía

Năm vấn đề dưới đây đã được AGENTS.md nêu; ID giữ chỗ để các thành viên viết
sys-us song song dùng chung một mã. BA ghi đủ cột theo mẫu OQ vào
`open-questions-vK.md`. Giữ chỗ ID **không** phải câu trả lời nghiệp vụ.

| ID | Vấn đề | Vị trí | US bị ảnh hưởng |
|---|---|---|---|
| OQ-01 | Kỳ tháng/quý ↔ duy nhất theo tháng | §2 ↔ PAY-01 | 01 |
| OQ-02 | Đúng 500.000.000 đ ai duyệt | §4.3 "từ … trở lên" ↔ PAY-06 "trên" | 02, 03 |
| OQ-03 | Điều chỉnh bảng Approved | §4.4 US-PAY-04 ↔ PAY-05 | 04 |
| OQ-04 | Sau từ chối: Rejected hay Draft | §3 ↔ PAY-08 | 03 (và 01 nếu sửa lại) |
| OQ-05 | "Dòng dịch vụ bắt buộc" là gì | PAY-04 | 02 |

Các điểm khác (quyền hủy, phạm vi sửa Draft, định nghĩa "người lập", làm tròn,
VAT, lập lại sau hủy, kênh thông báo, thoát khỏi Rejected…) là việc **nhóm tự phát
hiện** trong sys-us và đặt mã `OQ-USNN-kk`; danh sách này không thay việc đọc đặc tả.

Phần phụ thuộc ghi `Blocked by OQ-…`. Có thể vẽ/thiết kế các phương án nhưng
gắn `[GIẢ ĐỊNH – Cần xác nhận]` và không gọi là luồng cuối.

## 5. Ảnh chụp AS-IS (đọc file thực ngày 07/11/2026 – phải đọc lại)

- `src/Qtkd.Api/Qtkd.Api.csproj`: ASP.NET Core minimal API, `net8.0`, Nullable bật.
- `Program.cs`: endpoint `GET /`, `GET /api/contracts`, `GET /api/contracts/{id:int}`,
  `POST /api/contracts`, `POST /api/contracts/{id:int}/submit`; enum serialize dạng
  chuỗi (`JsonStringEnumConverter`); lỗi trả `ApiError(Code, Message)`, 404/400/409.
- `Services/ContractService.cs`: lưu trong bộ nhớ (`ConcurrentDictionary`), singleton,
  `lock (_gate)` khi Submit; mã lỗi `NOT_FOUND`, `INVALID_STATE`, `INVALID_CONTRACT`,
  `INVALID_DATE`; TODO Withdraw/authorization/audit.
- `Models/Contract.cs`: `ContractStatus { Draft, PendingApproval, RevisionRequested,
  Approved, Active }` – trạng thái của **hợp đồng**, không phải bảng thanh toán.
- Chưa có: module/entity bảng thanh toán, bảng giá, sản lượng, xác thực/phân quyền,
  audit log, logging cấu hình riêng, CSDL/migration, dự án kiểm thử.

Không suy ra rằng TO-BE phải dùng in-memory/lock; đó chỉ là hiện trạng demo.

## 6. Tên dùng chung giữa tài liệu, UML, API, dữ liệu

- Nguồn duy nhất của tên: mục **"Danh mục tên dùng chung"** trong
  `docs/design/payment-management/vK/03-detailed-design-vK.md` (class, enum, thao tác,
  sự kiện, endpoint, bảng/cột). Skill đầu tiên cần tên mà mục này chưa có (thường là
  sequence ở bước 4) ghi bảng **"Tên dùng tạm – cần đồng bộ vào 03"** trong đầu ra.
- Tên trạng thái giữ nguyên 5 giá trị §3 ở mọi nơi (enum, state, cột, JSON).
- Một thao tác dùng cùng một động từ ở state event, sequence message, method,
  endpoint và audit action (`create/update/submit/approve/reject/adjust/cancel`).
- Khác biệt tên giữa các file cùng version là lỗi phải sửa trước khi bàn giao.

## 7. Kiểm chứng PlantUML

Máy tạo workspace có Java 21 và Graphviz; chưa có `plantuml` trên PATH (07/11/2026).
Tải `plantuml.jar` (nhóm tự tải, không commit) rồi chạy, ghi lệnh và kết quả:

```sh
java -jar plantuml.jar -checkonly docs/design/payment-management/v1/diagrams/*.puml
java -jar plantuml.jar -tsvg docs/design/payment-management/v1/diagrams/*.puml
```

Không chạy được thì ghi đúng câu `Chưa kiểm tra kết xuất sơ đồ` cạnh danh mục sơ đồ.
