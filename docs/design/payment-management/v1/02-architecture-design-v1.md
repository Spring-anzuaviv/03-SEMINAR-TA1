# 02 – Thiết kế kiến trúc (v1)

> Phiên bản: v1 · Ngày: 09/11/2026 · Người phụ trách: Chờ nhóm điền
> Đầu vào: `seq-us-01..05-v1.puml`; `sys-us-01..05-v1.md`; [03-detailed-design-v1.md](03-detailed-design-v1.md) (danh mục tên); `src/Qtkd.Api/` (đọc lại 09/11/2026)
> AI: Claude Code / Claude Opus 5.5 · Prompt: P-21 trong [prompt-log](../../../workflow/prompt-log.md)
> Trạng thái: Bản lần chạy đầu – Design Pending Approval

Sơ đồ: [component-v1.puml](diagrams/component-v1.puml). Tên thành phần theo
[03 §1](03-detailed-design-v1.md#1-danh-mục-tên-dùng-chung).

## 1. AS-IS (đọc file thực)

| Hạng mục | Hiện trạng | File |
|---|---|---|
| Nền tảng | ASP.NET Core minimal API, `net8.0`, Nullable bật | `Qtkd.Api.csproj` |
| Endpoint | `GET /`, `GET /api/contracts`, `GET /api/contracts/{id:int}`, `POST /api/contracts`, `POST /api/contracts/{id:int}/submit` | `Program.cs` |
| Service / lưu trữ | `ContractService` singleton, `ConcurrentDictionary` trong bộ nhớ, `lock` khi submit | `Services/ContractService.cs` |
| Model | `Contract` (Id `int`, CustomerName, EffectiveDate, Status…); `ContractStatus { Draft, PendingApproval, RevisionRequested, Approved, Active }` – trạng thái **hợp đồng** | `Models/Contract.cs` |
| Lỗi | `ApiError(Code, Message)`; 400/404/409 | `Program.cs`, `Models/Contract.cs` |
| JSON | Enum dạng chuỗi (`JsonStringEnumConverter`) | `Program.cs` |
| Chưa có | Module bảng thanh toán, bảng giá, sản lượng; xác thực/phân quyền; audit log; CSDL/migration; thông báo; dự án kiểm thử. `ContractService` có TODO Withdraw/authorization/audit | – |

Kết luận AS-IS: chỉ có demo hợp đồng lưu trong bộ nhớ. Mọi thành phần của module Bảng
thanh toán dưới đây là **TO-BE**, chưa triển khai. Không suy ra TO-BE phải dùng
in-memory/`lock` như AS-IS.

## 2. TO-BE – ranh giới và thành phần

[ĐỀ XUẤT KỸ THUẬT] Module Bảng thanh toán là một module bên trong `Qtkd.Api` (DD-06),
gồm 4 lớp:

| Lớp | Thành phần | Trách nhiệm | Lấy từ sequence |
|---|---|---|---|
| Giao diện (client) | Form lập/sửa bảng, màn hình duyệt, màn hình điều chỉnh, thao tác hủy | Gọi API; không quyết định nghiệp vụ | seq-us-01 `PaymentForm`, seq-us-04 `Màn hình điều chỉnh` |
| API | `PaymentController` | Xác thực, lấy `CurrentUser`, ánh xạ mã lỗi → HTTP | seq-us-01, 02, 05 `PaymentController`; seq-us-03 `API` |
| Ứng dụng | `PaymentService`, `PaymentApprovalService`, `PaymentAdjustmentService` | Kiểm tra quyền, trạng thái, PAY; điều phối giao dịch | cả 5 seq |
| Hạ tầng | `IPaymentRepository`, `IAdjustmentRepository`, `IAuditLog`, `IUnitOfWork`, `INotifier` | Lưu bảng/dòng/audit, giao dịch, gửi thông báo | cả 5 seq |

Phụ thuộc ra ngoài module (chỉ đọc):

| Interface | Module nguồn | Dùng ở | Ghi chú |
|---|---|---|---|
| `IContractReader` | Hợp đồng | US-PAY-01 | AS-IS có `ContractService` nhưng chưa có interface đọc, chưa có cấu hình kỳ; cần adapter [ĐỀ XUẤT KỸ THUẬT] |
| `IPriceReader` | Bảng giá | US-PAY-01 | AS-IS chưa có module |
| `IQuantityReader` | Sản lượng | US-PAY-01 | AS-IS chưa có module |

Không có phương thức ghi nào tới ba module này [ĐẶC TẢ] [TA-SPEC §1]. Kế toán/xuất hóa
đơn nằm ngoài module (OQ-US03-06).

## 3. Các mối quan tâm xuyên suốt

| Mối quan tâm | Thiết kế | Yêu cầu | Trạng thái / OQ |
|---|---|---|---|
| Xác thực, phân quyền | Mỗi request kiểm tra phiên và `UserRole` phía server (NVKD/KTT/GĐKD); không dựa vào việc nút hiển thị | §2 | Cơ chế xác thực chưa chọn (AS-IS chưa có). Phạm vi quyền: OQ-US01-03, OQ-US02-01, OQ-US05-01 |
| Phân công người duyệt | `PaymentApprovalService.ResolveRequiredApprover(total)` | PAY-06 | Đúng ngưỡng: OQ-02; cá nhân/vai trò: OQ-US03-02; cơ sở tổng: OQ-US03-03 |
| Cấm tự duyệt | So `CurrentUser.UserId` với `PaymentSheet.CreatedBy` cho approve và reject | PAY-07 | Định nghĩa người lập: OQ-US03-01 |
| Audit | `IAuditLog.Append` trong cùng giao dịch, append-only | NFR-PAY-01 | DD-03 |
| Giao dịch | `IUnitOfWork` bao thay đổi bảng/dòng + audit; lỗi → rollback | NFR-PAY-01 | DD-03; CSDL chưa chọn |
| Đồng thời, trình trùng | Ghi có điều kiện trạng thái + version | PAY-04 | DD-02 |
| Duy nhất theo kỳ | Kiểm tra `FindConflict` trước và ràng buộc duy nhất khi ghi | PAY-01 | Phạm vi Blocked by OQ-01, OQ-US05-02, OQ-D-01 |
| Thông báo | `INotifier` sau commit | §4.2 | Kênh/lỗi gửi: OQ-US02-02, OQ-US03-05 (DD-05) |
| Dữ liệu tại thời điểm tính | Snapshot dòng | PAY-03 | DD-04; giá đổi: OQ-US01-01 |
| Lỗi đọc nguồn | Trả `SOURCE_UNAVAILABLE`, không coi là "không có dữ liệu" | §1 | seq-us-01 A10 |
| Hiệu năng lập bảng | Một lượt đọc HĐ/giá/sản lượng, tính trong bộ nhớ, ghi một giao dịch | NFR-PAY-02 | Chưa đo; điểm đo OQ-US01-06 |

## 4. Luồng tích hợp theo thao tác

| Thao tác | Client → API → Service | Đọc ngoài | Ghi | Sau commit |
|---|---|---|---|---|
| create (US-01) | Form → `PaymentController` → `PaymentService.Create` | Contract, Price, Quantity | `PaymentSheet` + `PaymentLine` + audit | – |
| update (US-01) | Form → … → `PaymentService.Update` | Có thể đọc lại nguồn (OQ-US01-02) | Cập nhật có điều kiện + audit | – |
| submit (US-02) | → `PaymentService.Submit` | – | `Transition(Draft→PendingApproval)` + audit | `NotifySubmission` |
| approve/reject (US-03) | → `PaymentApprovalService` | – | `Transition` + audit | `NotifyResult` (OQ-US03-05) |
| adjust (US-04) | → `PaymentAdjustmentService.Adjust` | – | A: `PaymentAdjustment` + audit; B: `UpdateApproved` + audit (OQ-03) | – |
| cancel (US-05) | → `PaymentService.Cancel` | – | `Transition(Draft→Cancelled)` + audit | – |

## 5. Quyết định kỹ thuật liên quan

DD-01 (tên), DD-02 (đồng thời), DD-03 (audit + giao dịch), DD-04 (snapshot),
DD-05 (thông báo), DD-06 (ranh giới) – chi tiết ở
[07-design-decisions-v1.md](07-design-decisions-v1.md). Phương án thay thế chính:
tách module thành service riêng (không cần ở quy mô bài tập), dùng message queue cho
audit/thông báo (thêm hạ tầng, khó bảo đảm audit cùng giao dịch).

## 6. Rủi ro

- AS-IS không có module bảng giá/sản lượng: interface đọc chỉ là hợp đồng giả định
  cho tới khi các module đó tồn tại.
- Chưa chọn CSDL: DD-02/DD-03 cần CSDL có giao dịch và cập nhật có điều kiện.
- Nhiều quy tắc phân quyền còn Blocked; `PaymentController` chỉ kiểm tra được vai trò
  theo §2 cho tới khi OQ được trả lời.
