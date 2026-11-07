# Báo cáo đánh giá độc lập: US-PAY-05 (v1)

> Phiên bản được review: v1 · Ngày review: 07/11/2026 · Reviewer: AI Reviewer (Độc lập)  
> Đối tượng review: US-PAY-05 (Hủy bảng nháp) trong `docs/analysis/payment-management/v1/` và `docs/design/payment-management/v1/`  
> Nguồn đối chiếu nghiệp vụ: TA-SPEC (§1–6), TA-PDF (tr.1–3), sources.md  
> AI: Gemini 3.8 Flash · Prompt: P-13 trong docs/workflow/prompt-log.md  
> Kết luận: **Chưa đủ đầu vào / Cần chỉnh sửa** (Thiếu các tài liệu thiết kế bắt buộc LLD/API/Data/Traceability; Use case và Sequence đã lập bám sát đặc tả nhưng còn phụ thuộc các OQ mở)

---

## 1. Nguồn đối chiếu và tài liệu đã đọc

### 1.1. Nguồn căn cứ nghiệp vụ (Cục bộ duy nhất)
* **TA-SPEC** ([spec.md](../../requirements/payment-management/spec.md)):
  * §1 Mục đích và phạm vi: Module chỉ bao gồm lập, trình duyệt, duyệt/từ chối, điều chỉnh và hủy bảng thanh toán; chỉ đọc dữ liệu từ Hợp đồng, Bảng giá, Sản lượng.
  * §2 Thuật ngữ và vai trò: NVKD, KTT, GĐKD.
  * §3 Trạng thái bảng thanh toán: 5 trạng thái (`Draft`, `PendingApproval`, `Approved`, `Rejected`, `Cancelled`). Luồng chuyển trạng thái: `Draft` có thể chuyển sang `Cancelled`.
  * §4.5 US-PAY-05: "Bảng ở trạng thái Draft có thể bị hủy khi không còn cần thiết. Sau khi hủy, bảng chuyển sang Cancelled và không dùng lại được."
  * §5 PAY-01: "Mỗi hợp đồng chỉ có một bảng thanh toán cho mỗi tháng."
  * §5 PAY-05: "Bảng thanh toán đã Approved không được sửa dưới bất kỳ hình thức nào."
  * §6 Yêu cầu phi chức năng:
    * Gạch 1: "Mọi thay đổi trạng thái và mọi điều chỉnh phải được ghi audit log (ai, lúc nào, thay đổi gì)." (Mã nội bộ: NFR-PAY-01).
    * Gạch 2: "Chức năng lập bảng phải phản hồi trong vòng 3 giây với hợp đồng có dưới 200 dòng." (Mã nội bộ: NFR-PAY-02).
* **TA-PDF** ([assignment-ta-1-2.pdf](../../requirements/payment-management/assignment-ta-1-2.pdf)): Bản gốc đối chiếu số trang (tr.1: §1–3; tr.2: §4–5; tr.3: §6 và Yêu cầu bài tập).
* **Sổ nguồn** ([sources.md](../../requirements/payment-management/sources.md)).

### 1.2. Tài liệu thiết kế và phân tích v1 đã kiểm tra
* **Phân tích yêu cầu**:
  * [`docs/analysis/payment-management/v1/sys-us-05-v1.md`](../../analysis/payment-management/v1/sys-us-05-v1.md) (Đặc tả use case hệ thống SYS-US-05).
  * [`docs/analysis/payment-management/v1/open-questions-v1.md`](../../analysis/payment-management/v1/open-questions-v1.md) (Bảng Open Questions dùng chung).
* **Thiết kế**:
  * [`docs/design/payment-management/v1/diagrams/seq-us-05-v1.puml`](../../design/payment-management/v1/diagrams/seq-us-05-v1.puml) (Sơ đồ tuần tự PlantUML cho US-PAY-05).

---

## 2. Phần chưa kiểm tra được (Thiếu đầu vào theo quy trình)

Căn cứ theo [AGENTS.md](../../../AGENTS.md) (Quy tắc chung và Vai trò reviewer) cùng [naming-versioning](../../../skills/naming-versioning/SKILL.md), bản thiết kế v1 hiện tại **chưa đầy đủ các tài liệu cấu thành bắt buộc**:

1. **Chưa có các tài liệu tài liệu thiết kế mức hệ thống và chi tiết**:
   * `01-requirements-summary-v1.md`: Chưa lập (chưa tóm tắt tổng thể yêu cầu và OQ thiết kế).
   * `02-architecture-design-v1.md` & `component-v1.puml`: Chưa lập (chưa kiểm chứng được ranh giới module và interface chỉ đọc với module Hợp đồng).
   * `03-detailed-design-v1.md`: Chưa lập file thiết kế chi tiết chính thức (chưa có class diagram `class-v1.puml`, chưa có state machine diagram `state-machine-v1.puml`).
   * `04-api-contract-v1.md`: Chưa lập (chưa có hợp đồng API chính thức để đối chiếu endpoint, request body, response schema và format lỗi).
   * `05-data-design-v1.md` & `erd-v1.puml`: Chưa lập (chưa kiểm chứng được mô hình thực thể `PaymentSheet`, trường lưu `Status`, `Version` kiểm soát concurrency, trường lưu lý do hủy, và ràng buộc chỉ mục kỳ thanh toán).
   * `06-traceability-matrix-v1.md`: Chưa lập (chưa có ma trận truy vết yêu cầu ↔ UML ↔ API ↔ Dữ liệu).
   * `07-design-decisions-v1.md`: Chưa lập (chưa có văn bản ghi nhận quyết định kỹ thuật cho giải pháp Transaction và Optimistic Concurrency).
2. **Chưa có bằng chứng kết xuất sơ đồ PlantUML**:
   * Chưa có file ảnh `seq-us-05-v1.svg` hoặc `seq-us-05-v1.png` kết xuất từ file nguồn. Môi trường kiểm tra ghi nhận chưa có công cụ `plantuml.jar` trên PATH.

*Ghi chú*: Reviewer không tạo nhận xét giả cho các tài liệu chưa tồn tại; chỉ đánh giá trên các file thực tế đã được cung cấp (`sys-us-05-v1.md`, `open-questions-v1.md`, `seq-us-05-v1.puml`).

---

## 3. Bảng kiểm tra độ bao phủ yêu cầu đối với US-PAY-05

| Yêu cầu / Quy tắc gốc | Vị trí đặc tả | Mức độ đáp ứng trong phân tích (`sys-us-05-v1.md`) | Mức độ đáp ứng trong thiết kế (`seq-us-05-v1.puml`) | Đánh giá của Reviewer |
|---|---|---|---|---|
| **Chuyển trạng thái Draft → Cancelled khi không còn cần thiết** | TA-SPEC §3, §4.5; TA-PDF tr.1, tr.2 | **Đạt**: Đã mô tả rõ trong Dòng cơ bản Bước 5, Hậu điều kiện S1, và tiêu chí `AC-US05-01`. | **Đạt**: Message 13–15 thể hiện cập nhật `Status = Cancelled`. | Bao phủ đầy đủ luồng chính. |
| **Bảng Cancelled không được dùng lại** | TA-SPEC §4.5; TA-PDF tr.2 | **Đạt**: Khẳng định bảng đóng vĩnh viễn (Hậu điều kiện S2, `AC-US05-02`). | **Đạt một phần**: Có ghi chú khóa bảng ở Message 24; tuy nhiên **chưa có State Machine diagram** chứng minh không có transition nào đi ra từ trạng thái `Cancelled`. | Cần State Machine để kiểm chứng tính khép kín. |
| **Quyền hạn thực hiện thao tác hủy** | TA-SPEC §2, §4.5; TA-PDF tr.1, tr.2 | **Đạt (Ghi nhận OQ)**: Nhận diện thể bị động trong đề, lập `OQ-US05-01`, gắn `Blocked by OQ-US05-01`. | **Đạt (Ghi nhận OQ)**: Có kiểm tra `CheckPermission` và nhánh A2 (403 Forbidden) gắn `Blocked by OQ-US05-01`. | Đúng nguyên tắc không tự chốt nghiệp vụ khi đề chưa rõ vai trò. |
| **PAY-01: Ràng buộc 1 bảng/tháng khi bảng đã hủy** | TA-SPEC §5 PAY-01, §4.5; TA-PDF tr.2 | **Đạt (Ghi nhận OQ)**: Đặt câu hỏi `OQ-US05-02` về việc có được lập lại bảng mới cho kỳ đã hủy hay không (`AC-US05-08`). | **Đạt (Ghi nhận OQ)**: Có note ghi nhận phụ thuộc `OQ-US05-02` tại Message 24. | Đúng quy tắc; cần lưu ý ảnh hưởng thiết kế CSDL (Filtered Index). |
| **PAY-05: Bảng Approved cấm sửa/hủy** | TA-SPEC §5 PAY-05, §3; TA-PDF tr.1, tr.2 | **Đạt**: Tiền điều kiện P3 chỉ cho phép `Draft`, nhánh A3 chặn các trạng thái khác (`AC-US05-03`). | **Đạt**: Message 8 và nhánh A3 chặn rõ trạng thái khác `Draft`, trả lỗi `INVALID_STATE` (400). | Đáp ứng tốt quy tắc bất biến. |
| **NFR-PAY-01: Audit log thay đổi trạng thái (ai, lúc nào, thay đổi gì)** | TA-SPEC §6; TA-PDF tr.3 | **Đạt**: NFR áp dụng bắt buộc; Dòng cơ bản bước 6; Hậu điều kiện S3; tiêu chí `AC-US05-01`, `AC-US05-06`. | **Đạt**: Message 19–20 gọi `AuditLogService` trong `group Transaction`; nhánh A6 rollback toàn bộ nếu ghi audit lỗi. | Thiết kế đảm bảo tính toàn vẹn kiểm toán rất tốt. |
| **NFR-PAY-02: Phản hồi ≤ 3 giây với < 200 dòng** | TA-SPEC §6; TA-PDF tr.3 | **Đạt**: Ghi rõ không áp dụng cho chức năng hủy bảng vì đề chỉ quy định cho chức năng lập bảng (US-PAY-01). | **Không áp dụng**: Không đưa SLA giả định vào sơ đồ. | Chính xác, không tự ý bịa thêm SLA. |

---

## 4. Bảng nhận xét chi tiết (Review Findings)

| ID | Vị trí file/mục/dòng | Loại | Mức độ | Nhận xét và tác động | Đề xuất / Cách kiểm chứng | Căn cứ trang/mục/US/PAY | OQ |
|---|---|---|---|---|---|---|---|
| **R01-01** | `docs/design/payment-management/v1/` | Thiếu sót tài liệu | **Cao** | **Thiếu toàn bộ các tài liệu thiết kế hệ thống và chi tiết theo quy trình**.<br>Thư mục thiết kế chỉ có duy nhất file `seq-us-05-v1.puml`. Chưa có các tài liệu `01-` đến `07-`. Tác động: Không thể đối chiếu chéo tính nhất quán giữa Sequence với Class Diagram, State Diagram, API Contract và Data Design. | Đội ngũ Design cần bổ sung các tài liệu `01-requirements-summary-v1.md` đến `07-design-decisions-v1.md` theo đúng quy định tại AGENTS.md và naming-versioning trước khi bàn giao review toàn diện. | [QUY TRÌNH] AGENTS.md (Vai trò design); TA-PDF tr.3 (Yêu cầu bài tập mục 1). | - |
| **R01-02** | `sys-us-05-v1.md` (Mục 1 P1, B2, A2); `seq-us-05-v1.puml` (dòng 15, 44–54) | Mơ hồ đặc tả | **Trung bình** | **Quyền hủy bảng nháp chưa có căn cứ đặc tả rõ ràng**.<br>Đặc tả §4.5 dùng thể bị động ("có thể bị hủy khi không còn cần thiết"); §2 chỉ định nghĩa NVKD là người "lập và trình duyệt bảng". Phân tích và Thiết kế đã xử lý đúng khi gắn cờ `Blocked by OQ-US05-01`. Nhánh A2 (`CheckPermission`) hiện mang tính giả định cho đến khi OQ được trả lời. | Giữ nguyên trạng thái `Cần xác nhận` cho `OQ-US05-01`. Chờ người phụ trách/PO chốt quyền (Lựa chọn A: Chỉ người tạo; Lựa chọn B: NVKD phụ trách; Lựa chọn C: NVKD hoặc Quản lý). Không tự ý đóng OQ. | [ĐẶC TẢ] [TA-SPEC §2, §4.5; TA-PDF tr.1, tr.2]. | OQ-US05-01 |
| **R01-03** | `docs/design/payment-management/v1/diagrams/` | Thiếu sót thiết kế | **Trung bình** | **Chưa có State Machine Diagram để kiểm chứng tính bất biến của trạng thái `Cancelled`**.<br>Đặc tả §4.5 yêu cầu: "Sau khi hủy, bảng chuyển sang Cancelled và không dùng lại được". Sequence chỉ thể hiện được chiều chuyển sang `Cancelled` nhưng chưa chứng minh được từ `Cancelled` không thể phát sinh bất kỳ chuyển đổi trạng thái nào khác. | Đội ngũ Design cần bổ sung sơ đồ `state-machine-v1.puml` thể hiện `Cancelled` là trạng thái kết thúc (Terminal State), không có transition ra ngoài đối với mọi event (`submit`, `approve`, `reject`, `adjust`, `update`). | [ĐẶC TẢ] [TA-SPEC §3, §4.5; TA-PDF tr.1, tr.2]. | - |
| **R01-04** | `seq-us-05-v1.puml` (dòng 88–98, Nhánh A5); `sys-us-05-v1.md` (Nhánh A5) | Đề xuất kỹ thuật | **Trung bình** | **Cơ chế chống xung đột đồng thời A5 dựa trên Concurrency Token/Version chưa có căn cứ trong Quyết định kỹ thuật và Mô hình dữ liệu**.<br>Sơ đồ sequence sử dụng lệnh `UPDATE ... SET Status = 'Cancelled', Version = Version + 1 WHERE Id = id AND Version = currentVersion`. Đây là đề xuất kỹ thuật hợp lý nhưng chưa có tài liệu `07-design-decisions-v1.md` ghi nhận quyết định (DD) và chưa có `05-data-design-v1.md` để xác nhận entity có trường `Version`. | Bổ sung quyết định kỹ thuật `DD-kk` vào `07-design-decisions-v1.md` giải thích lý do dùng Optimistic Concurrency thay vì Pessimistic Lock, và cập nhật trường `Version` vào schema `05-data-design-v1.md`. | [ĐỀ XUẤT KỸ THUẬT] Không có căn cứ trong đặc tả gốc (đề xuất kỹ thuật giải quyết bài toán đồng thời); AGENTS.md (Quy tắc ghi quyết định kỹ thuật). | - |
| **R01-05** | `seq-us-05-v1.puml` (dòng 23, 41, 53, 65, 74, 98, 116, 133); `sys-us-05-v1.md` (B1, A4) | Không nhất quán API | **Thấp** | **Chưa có hợp đồng API chuẩn hóa cấu trúc Request/Response và Error Code**.<br>Sequence sử dụng endpoint `POST /api/payment-sheets/{id}/cancel` với body `{ reason? }` và các mã lỗi `NOT_FOUND`, `FORBIDDEN`, `INVALID_STATE`, `INVALID_REASON`, `CONCURRENCY_CONFLICT`, `INTERNAL_ERROR`. Do chưa có `04-api-contract-v1.md`, các mã lỗi và schema này chưa được chuẩn hóa chính thức. | Bổ sung đặc tả endpoint này vào `04-api-contract-v1.md` (quy định rõ status code HTTP 400 vs 409, cấu trúc trả về theo `ApiError` hoặc RFC 7807 Problem Details). | [ĐỀ XUẤT KỸ THUẬT] Không có căn cứ trong đặc tả gốc (phạm vi thiết kế API); AGENTS.md (Vai trò design mục 5). | OQ-US05-03 |
| **R01-06** | `sys-us-05-v1.md` (S4, AC-US05-08); `open-questions-v1.md` (OQ-US05-02); `seq-us-05-v1.puml` (dòng 127) | Mơ hồ đặc tả | **Trung bình** | **Ảnh hưởng của việc hủy bảng tới ràng buộc kỳ thanh toán theo PAY-01 chưa được mô hình hóa trong thiết kế dữ liệu**.<br>PAY-01 quy định mỗi hợp đồng chỉ có một bảng cho mỗi tháng. Nếu sau khi hủy được phép lập lại (Phương án A của OQ-US05-02) thì CSDL bắt buộc phải dùng Filtered Unique Index (`WHERE Status != 'Cancelled'`). Do chưa có `05-data-design-v1.md`, phương án này chưa được thể hiện. | Giữ `Blocked by OQ-US05-02`. Trong `05-data-design-v1.md`, cần thiết kế phương án chỉ mục duy nhất có điều kiện (Filtered Unique Index) gắn nhãn `[GIẢ ĐỊNH – Cần xác nhận]`. | [ĐẶC TẢ] [TA-SPEC §4.5, §5 PAY-01; TA-PDF tr.2]. | OQ-US05-02 |
| **R01-07** | `docs/design/payment-management/v1/diagrams/seq-us-05-v1.puml` | Chưa kiểm chứng | **Thấp** | **Sơ đồ PlantUML chưa có bằng chứng kết xuất đồ họa**.<br>File `seq-us-05-v1.puml` có cú pháp PlantUML hợp lệ về mặt cấu trúc văn bản (đóng mở alt/group cân bằng), nhưng chưa được biên dịch và kết xuất file hình ảnh (`.svg`/`.png`) để kiểm tra trực quan. | Nhóm tải `plantuml.jar` (không commit) và chạy lệnh: `java -jar plantuml.jar -checkonly docs/design/payment-management/v1/diagrams/seq-us-05-v1.puml` và `java -jar plantuml.jar -tsvg ...` để tạo file SVG minh chứng. | [QUY TRÌNH] AGENTS.md (Làm việc đúng phạm vi và kiểm chứng); payment-context.md §7. | - |

---

## 5. Kết luận của Reviewer

* **Kết luận tổng thể**: **Chưa đủ đầu vào / Cần chỉnh sửa** (Incomplete Inputs & Revisions Needed).
* **Đánh giá chung**:
  1. **Điểm tốt**: Đặc tả use case [`sys-us-05-v1.md`](../../analysis/payment-management/v1/sys-us-05-v1.md) và sơ đồ tuần tự [`seq-us-05-v1.puml`](../../design/payment-management/v1/diagrams/seq-us-05-v1.puml) được xây dựng chặt chẽ, bao phủ đầy đủ 100% dòng cơ bản và 6 nhánh dòng thay thế (A1..A6). Thiết kế transaction bao bọc cập nhật trạng thái và ghi nhận audit log tuân thủ xuất sắc yêu cầu phi chức năng **NFR-PAY-01** (tính toàn vẹn kiểm toán). Các điểm chưa rõ ràng trong đặc tả đều được nhận diện chính xác thành Open Questions (`OQ-US05-01`, `OQ-US05-02`, `OQ-US05-03`), gắn cờ `Blocked by OQ` và giữ nguyên trạng thái `Cần xác nhận`, không tự tiện suy đoán nghiệp vụ.
  2. **Điểm cần khắc phục**: Bản thiết kế v1 hiện tại còn thiếu các tài liệu thiết kế hệ thống và chi tiết bắt buộc (`01-` đến `07-`, `state-machine-v1.puml`, `class-v1.puml`), dẫn đến việc chưa thể đối chiếu tính nhất quán đa chiều giữa sơ đồ tuần tự và kiến trúc dữ liệu/API.
* **Tuân thủ quy chế Reviewer**:
  * Reviewer **không sửa bất kỳ file thiết kế hay đặc tả nào**.
  * Reviewer **không tự ý đóng hay quyết định đáp án cho bất kỳ Open Question nào**.
  * Báo cáo này được bàn giao cho Nhóm dự án và Người phụ trách để tiến hành đánh giá nhận xét (Đúng/Sai/Thừa) tại `review-assessment-01-v1.md` theo quy trình.

