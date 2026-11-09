# AI Review 01 – Bản v1 module Bảng thanh toán

> Phiên bản được review: **v1** (bản lần chạy đầu) · Ngày: 09/11/2026
> Vai trò: reviewer ([rules/reviewer.md](../../../rules/reviewer.md)) · AI: Claude Opus 5.5 (Claude Code, desktop) · Prompt: P-25 trong [prompt-log](../../workflow/prompt-log.md)
> Trạng thái: Báo cáo review AI – **chưa được nhóm đánh giá**. Nhóm ghi Đúng/Sai/Thừa trong `review-assessment-01-v1.md`; reviewer không tự đánh giá nhận xét của mình.
> Theo [naming-versioning](../../../skills/naming-versioning/SKILL.md), từ khi có file này, v1 bị đóng băng; mọi sửa đổi đưa vào v2.

Reviewer chỉ đọc file thực và đặc tả, không dùng lời giải thích của người thiết kế. Mọi nhận xét
dẫn vị trí file/mục/dòng (dòng theo bản đọc ngày 09/11/2026, HEAD `a1b9d68`) và căn cứ
TA-SPEC/TA-PDF. Nhận xét không có căn cứ trong đặc tả ghi rõ **Không có căn cứ trong đặc tả – đề xuất kỹ thuật**.
Reviewer không chọn phía nào của mâu thuẫn và không đóng OQ.

## 1. Nguồn và bản đã đọc

| Nguồn | Bản / cách đọc | Ghi chú |
|---|---|---|
| [AGENTS.md](../../../AGENTS.md), [rules/sources.md](../../../rules/sources.md), [common.md](../../../rules/common.md), [payment-scope.md](../../../rules/payment-scope.md), [handoff.md](../../../rules/handoff.md), [reviewer.md](../../../rules/reviewer.md) | Đọc toàn bộ | Quy tắc áp dụng cho báo cáo |
| [naming-versioning](../../../skills/naming-versioning/SKILL.md), [payment-context](../../../skills/_shared/payment-context.md) | Đọc phần liên quan | Quy ước tên, ID, đóng băng v1 |
| TA-SPEC [spec.md](../../requirements/payment-management/spec.md) §1–6 | Đọc toàn bộ | Căn cứ nghiệp vụ |
| TA-PDF [assignment-ta-1-2.pdf](../../requirements/payment-management/assignment-ta-1-2.pdf) tr.1–3 | `pdftotext -layout` | Phông mất dấu tiếng Việt nhưng đối chiếu được cấu trúc §1–6 và câu chữ; không thấy lệch với TA-SPEC. §4.3 "từ 500 triệu đồng trở lên", PAY-06 "trên 500 triệu đồng" có trong cả hai |
| `docs/analysis/payment-management/v1/`: [sys-us-01-v1](../../analysis/payment-management/v1/sys-us-01-v1.md) … [sys-us-05-v1](../../analysis/payment-management/v1/sys-us-05-v1.md), [open-questions-v1](../../analysis/payment-management/v1/open-questions-v1.md) | Đọc toàn bộ | 73 AC (26/13/15/10/9), 25 OQ |
| `docs/design/payment-management/v1/`: [01](../../design/payment-management/v1/01-requirements-summary-v1.md), [02](../../design/payment-management/v1/02-architecture-design-v1.md), [03](../../design/payment-management/v1/03-detailed-design-v1.md), [04](../../design/payment-management/v1/04-api-contract-v1.md), [05](../../design/payment-management/v1/05-data-design-v1.md), [07](../../design/payment-management/v1/07-design-decisions-v1.md) | Đọc toàn bộ | OQ-D-01 ở 01 §7 |
| [06-traceability-matrix-v1](../../design/payment-management/v1/06-traceability-matrix-v1.md) (88 KB) | Đọc §1, §2, §4–§8 toàn bộ; §3 (73 dòng AC) đọc theo cột ID/API/kiểm chứng/trạng thái/OQ và đối chiếu mẫu 18 dòng | Không đối chiếu từng chữ cột "Nội dung rút gọn" của 73 dòng |
| `v1/diagrams/`: `seq-us-01..05-v1.puml`, `class-v1.puml`, `state-machine-v1.puml`, `component-v1.puml`, `erd-v1.puml` (+ SVG, PNG seq-us-02) | Đọc toàn bộ nguồn `.puml`; SVG đối chiếu bằng bản render lại | Xem §2 |
| `src/Qtkd.Api/` (`Program.cs`, `Models/Contract.cs`, `Services/ContractService.cs`, `.csproj`) | Kiểm tra các khẳng định AS-IS ở 02 §1 | Khớp: 5 endpoint hợp đồng, `ContractStatus` 5 giá trị, `net8.0`, Nullable, TODO Withdraw |
| [prompt-log](../../workflow/prompt-log.md) P-13, P-15..P-24 | Đọc phần ghi kiểm chứng | Dùng làm bằng chứng render/test của design |
| Git history `docs/review/` | `git log --all -- docs/review` | Xem §2 về các báo cáo cũ đã bị xóa |

Không dùng tài liệu đồ án tổng thể, Excel hay nguồn trực tuyến. Không đọc thư mục `v2/`
ngoài việc ghi nhận nó tồn tại (review chỉ dành cho v1).

## 2. Bằng chứng render/test và phần chưa kiểm được

| Kiểm tra | Lệnh | Kết quả |
|---|---|---|
| Cú pháp 9 file PlantUML v1 | `java -jar plantuml.jar -charset UTF-8 -checkonly *.puml` (PlantUML 1.2024.3, jar của extension VS Code `jebbs.plantuml-2.18.1`, Java 21) | exit 0 |
| Kết xuất lại SVG | `-tsvg -o <scratchpad>` | exit 0, 9 SVG; không SVG nào chứa thông báo lỗi |
| SVG trong repo có khớp nguồn hiện tại không | So md5 phần text của SVG trong repo với bản vừa render | 9/9 giống nhau → SVG đã commit phản ánh đúng `.puml` hiện tại |
| Cấu hình workspace | `python -X utf8 scripts/verify_agent_config.py` | **FAIL (5 checks)**: thiếu `docs/review/payment-management` và `README.md` của nó; prompt-log link tới `v2/03-detailed-design-v2.md` không tồn tại; 2 tên file trong `analysis/v2/` sai quy ước. Không có lỗi tên trong `v1/` |
| Kiểm thử ứng dụng / đo hiệu năng | – | Không có code module Bảng thanh toán, không có dự án test. Mọi trạng thái "Đã thiết kế" trong 06 là **chưa kiểm thử**; NFR-PAY-02 **chưa đo** |
| Phê duyệt người phụ trách | – | Không tìm thấy bằng chứng phê duyệt; mọi file ghi `Design Pending Approval` / `BA Pending Review` |

Phần chưa kiểm được / giới hạn:

- Không xem bằng mắt bố cục từng SVG/PNG (chỉ kiểm tra render thành công và nội dung text).
- 06 §3: không đối chiếu từng chữ cột "Nội dung rút gọn" của 73 dòng AC với sys-us.
- Không kiểm tra lời giải thích hay câu trả lời OQ nằm ngoài file (chat, Excel, v2).
- Lịch sử Git có các báo cáo `ai-review-03-v1.md`, `ai-review-04-v2.md`, `ai-review-us-05-v1.md` và
  `review/payment-management/README.md` bị xóa ở commit `b7da5fa` (09/11/2026). Thư mục
  `docs/review/` không còn khi bắt đầu review này; tên `ai-review-01-v1.md` được dùng theo nhiệm vụ
  và chưa từng tồn tại trong lịch sử, nên không ghi đè báo cáo nào. Nhóm cần quyết định cách đánh số
  so với các báo cáo đã xóa.

## 3. Bảng bao phủ

Đánh giá dưới đây là **mức có trong tài liệu**, không phải kết quả kiểm thử.

### 3.1. User story, quy tắc, NFR

| ID | sys-us | seq | class/state | API | Dữ liệu | 06 | Nhận xét liên quan |
|---|---|---|---|---|---|---|---|
| US-PAY-01 | Có (26 AC) | seq-us-01 | T1, T2 | E1–E8 | sheets, lines, audit | Có | R01-03, R01-15, R01-17, R01-27 |
| US-PAY-02 | Có (13 AC) | seq-us-02 | T3 | E9 | sheets, audit | Có | R01-08, R01-09, R01-13, R01-14, R01-25 |
| US-PAY-03 | Có (15 AC, AI bổ sung, nhóm chưa duyệt) | seq-us-03 | T5, T6a/T6b, T7 | E10, E11 | sheets, audit | Có | R01-01, R01-02, R01-05, R01-06, R01-07, R01-11 |
| US-PAY-04 | Có (10 AC, AI bổ sung, nhóm chưa duyệt) | seq-us-04 (A/B) | T8 | E12 | adjustments / sheets, audit | Có | R01-10, R01-16, R01-23 |
| US-PAY-05 | Có (9 AC) | seq-us-05 | T4, T9 | E13 | sheets, audit | Có | R01-12 |
| PAY-01 | Có; tháng/quý, lập lại sau hủy, Rejected chiếm kỳ: OQ-01, OQ-US05-02, OQ-D-01 | seq-us-01 | T1 | E2, E3, E5 | `ux_sheet_period` chưa chốt (05 §8) | Có | R01-15 |
| PAY-02 | Có | seq-us-01 | T1 | E4, E5 | `quantity_source_ref` | Có | R01-08 |
| PAY-03 | Có | seq-us-01 | `PaymentLine` | E4, E5 | snapshot (DD-04) | Có | R01-02, R01-15 |
| PAY-04 | Có; dòng bắt buộc: OQ-05 | seq-us-02 | T3 | E9 | `version` | Có | R01-09, R01-14, R01-22 |
| PAY-05 | Có; mâu thuẫn §4.4: OQ-03 | seq-us-03 note, seq-us-04 | `Approved`, T8 | E8/E9/E13 → 409 | – | Có | R01-10 |
| PAY-06 | Có; đúng 500 triệu: OQ-02 | seq-us-02, seq-us-03 | T5, `RequiredApproverRole()` | E9, E10, E11 | `total_amount` | Có | **R01-01**, R01-02, R01-07 |
| PAY-07 | Có; phạm vi từ chối: OQ-US03-01 | seq-us-03 | T5, T6 | E10, E11 | `created_by` | Có | R01-06 |
| PAY-08 | Có; đích sau từ chối: OQ-04, OQ-US03-07 | seq-us-03 | T6a/T6b/T7 | E11 | `rejection_reason` | Có | R01-05 |
| NFR-PAY-01 (audit) | Có ở 5 sys-us | 5 seq có `IAuditLog.Append` trong giao dịch | action "ghi audit" T1–T8 | E5, E8–E13 | `audit_entries` append-only | Có | Xem §3.3 |
| NFR-PAY-02 (≤3 giây, <200 dòng) | Có; giữ đúng "dưới 200", không thêm percentile/tải | Chỉ ghi chú | – | E5 (dự kiến đo) | – | Có, "chưa đo" | R01-27 |

### 3.2. Acceptance criteria

| US | Số AC sys-us | Có dòng trong 06 | Ghi chú |
|---|---|---|---|
| US-PAY-01 | 26 | 26 | Cột API/kiểm chứng phần lớn chung chung (R01-17) |
| US-PAY-02 | 13 | 13 | – |
| US-PAY-03 | 15 | 15 | AC do AI soạn ở P-22, nhóm chưa duyệt; nhãn/ngưỡng lệch (R01-07, R01-20) |
| US-PAY-04 | 10 | 10 | AC do AI soạn ở P-22, nhóm chưa duyệt; trạng thái Blocked lệch giữa sys-us-04 và 06 (R01-17) |
| US-PAY-05 | 9 | 9 | – |
| **Tổng** | **73** | **73** | 06 §7: 27 "Đã thiết kế – chưa kiểm thử", 7 một phần, 39 Blocked |

### 3.3. Kiểm tra trọng tâm

| Chủ đề | Kết quả kiểm | Nhận xét |
|---|---|---|
| Audit mọi chuyển trạng thái | T1–T6, T8 có audit cùng giao dịch trong seq + 05 §10; T7 (Rejected → Draft) chưa có event/actor nên chưa có audit – đánh dấu Blocked by OQ-04, OQ-US03-07 đúng trạng thái | – |
| Audit mọi điều chỉnh | E12 cả A và B ghi `adjust` có `attachment_ref`; A không đổi `version` | R01-10 |
| Chống trình trùng (PAY-04) | Cập nhật có điều kiện trạng thái + version (DD-02, DD-08); không dùng Idempotency-Key, có nêu thay thế | R01-09, R01-14 |
| Cấm tự duyệt (PAY-07) | `userId != createdBy` cho approve; reject không thống nhất | R01-06 |
| Ngưỡng 500 triệu | Không thống nhất giữa seq-us-02 và seq-us-03 | **R01-01** |
| Ranh giới module, interface chỉ đọc | `IContractReader`, `IPriceReader`, `IQuantityReader` chỉ có method đọc; không endpoint/bảng CRUD cho 3 module; không FK chéo module | R01-26 (tích hợp kế toán) |
| Không thêm trạng thái | Enum, CHECK CSDL, state machine đúng 5 trạng thái §3 | – |
| Khẳng định AS-IS | 02 §1 khớp `src/Qtkd.Api/` | – |
| Render/test | Xem §2 | R01-18, R01-19 |

## 4. Nhận xét

Loại: Mâu thuẫn nội bộ · Tự chốt nghiệp vụ · Suy diễn ngoài đặc tả · Thiếu OQ · Không nhất quán ·
Thiếu truy vết · Nhánh lỗi · Bằng chứng · Nhãn nguồn · Đề xuất kỹ thuật. Mức độ: Cao / TB / Thấp.
Thứ tự: ba nhận xét mức Cao đứng đầu; phần còn lại xếp theo luồng US rồi theo chủ đề
(truy vết, bằng chứng, OQ bỏ sót), không theo mức độ. Tổng: 28 nhận xét – 3 Cao, 7 TB, 18 Thấp.

| ID | Vị trí file/mục/dòng | Loại | Mức độ | Nhận xét và tác động | Đề xuất / cách kiểm chứng | Căn cứ trang/mục/US/PAY | OQ |
|---|---|---|---|---|---|---|---|
| R01-01 | `seq-us-03-v1.puml` dòng 65 (`total >= 500.000.000 -> Giám đốc kinh doanh; ngược lại Kế toán trưởng`); `sys-us-03-v1.md` §1 Tiền điều kiện P2 (dòng 21), bước 5 (dòng 25), 5a (dòng 27) ↔ `seq-us-02-v1.puml` dòng 85–91 (`total = 500.000.000 — Blocked by OQ-02`); `03` §5 T5; `04` E10; `state-machine-v1.puml` note PendingApproval; `06` PAY-06 | Mâu thuẫn nội bộ; Tự chốt nghiệp vụ | Cao | Hai sequence gọi **cùng** `PaymentSheet.RequiredApproverRole()` nhưng mô tả hai hành vi khác nhau tại đúng 500.000.000 đ: seq-us-03 đi theo phía §4.3 ("từ… trở lên"), seq-us-02/03 §5/04/06 ghi "Blocked, không chọn". Phía được chọn là đề xuất của Đan Anh chưa có xác nhận khách hàng (OQ-02). Nếu hiện thực theo seq-us-03, bảng đúng 500 triệu chỉ GĐKD duyệt được, trong khi PAY-06 ("trên 500 triệu") giao cho KTT; người nhận thông báo lúc trình (US-PAY-02) và người được phép duyệt (US-PAY-03) có thể lệch nhau. | Đưa seq-us-03 bước 5/5a và sys-us-03 P2/5/5a về cùng trạng thái với seq-us-02 (ba nhánh <, >, = với nhánh = Blocked by OQ-02) cho tới khi có xác nhận. Kiểm chứng: tìm `>=` / `≥ 500` trong v2 và đối chiếu với `RequiredApproverRole()` ở class/03/04; test biên 499.999.999 / 500.000.000 / 500.000.001 sau khi OQ-02 được trả lời. | TA-SPEC §4.3 ↔ §5 PAY-06; TA-PDF tr.2; rules/payment-scope.md (bảng tình huống) | OQ-02, OQ-US03-02 |
| R01-02 | `seq-us-03-v1.puml` note dòng 66–71 ("total … gồm VAT, làm tròn từng dòng và tổng, lên đồng"; "giá trị chờ khách hàng, không chặn sơ đồ"); `sys-us-03-v1.md` P2 (dòng 21) ↔ `sys-us-01-v1.md` AC-US01-12 ("không tự thêm VAT/làm tròn"); `seq-us-01-v1.puml` note dòng 227 ("không tự thêm VAT"); `05` §4.1 `total_amount = Σ line_amount` (dòng 45), §7; `04` §1 hàng "Tiền" | Mâu thuẫn nội bộ; Tự chốt nghiệp vụ | Cao | US-PAY-03 coi tổng so ngưỡng là tổng đã gồm VAT và làm tròn lên, còn US-PAY-01, dữ liệu và API coi tổng là Σ thành tiền, không có cột/trường thuế. Đặc tả không nêu thuế hay làm tròn. Cùng một bảng có thể vượt hoặc không vượt ngưỡng 500 triệu tùy cách hiểu → sai người duyệt. Câu "không chặn thiết kế" trong seq-us-03 trái với 05 §7 "Blocked by OQ-US03-03". | Thống nhất một cách ghi "Blocked by OQ-US03-03" cho cơ sở tổng tiền ở sys-us-03, seq-us-03, 05, 04; không trình bày VAT/làm tròn như điều kiện guard khi chưa có xác nhận khách hàng. Kiểm chứng: grep "VAT", "làm tròn" trong v2 và đối chiếu với cột `total_amount`. | TA-SPEC §4.1, §4.3, §5 PAY-03, PAY-06 (không có thuế/làm tròn); TA-PDF tr.2 | OQ-US03-03 |
| R01-03 | `sys-us-01-v1.md` đoạn mở đầu dòng 11, §1.2 hàng "Kích hoạt" (dòng 35), hàng "Bảng giá" (dòng 49), §1.3 bước 8–9 (dòng 65–66); lan sang `04` E3/E4/E5 (`priceListId`), `05` §4.1 `price_list_id` NOT NULL, `seq-us-01` bước 9 | Suy diễn ngoài đặc tả; Nhãn nguồn | Cao | §4.1 chỉ nêu "NVKD chọn hợp đồng và kỳ thanh toán. Hệ thống tự sinh các dòng … từ sản lượng và bảng giá". Bản v1 thêm bước **NVKD chọn bảng giá** và gắn nhãn `[QUYẾT ĐỊNH ĐÃ XÁC NHẬN]` theo P-17 ("người dùng trong chat"), không nêu tên/vai trò người xác nhận và không phải người phụ trách nghiệp vụ. Bước này làm thay đổi trách nhiệm chọn giá (người hay hệ thống) và chồng lên câu hỏi "bảng giá phù hợp" của OQ-US01-01. | Tách "trình tự màn hình theo hướng dẫn người dùng" khỏi "ai chọn bảng giá"; nếu giữ bước chọn bảng giá, ghi OQ riêng hoặc nối vào OQ-US01-01 và đổi nhãn về `[GIẢ ĐỊNH – Cần xác nhận]` cho tới khi có người/ngày/tham chiếu xác nhận nghiệp vụ. Kiểm chứng: đối chiếu nhãn với rules/common.md (QUYẾT ĐỊNH ĐÃ XÁC NHẬN cần người, ngày, tham chiếu). | TA-SPEC §4.1, §5 PAY-01 "có bảng giá phù hợp"; TA-PDF tr.2; rules/common.md | OQ-US01-01 |
| R01-04 | `open-questions-v1.md` dòng 19, 31, 32, 34, 35, 36 (OQ-02, OQ-US03-01, 02, 04, 05, 06: Trạng thái "Đề xuất của Đan Anh – chờ khách hàng xác nhận", cột Còn mở "Không còn"); `01` §7 dòng 84 ("Tất cả đang Cần xác nhận"); `sys-us-02-v1.md` §2 dòng 70; `sys-us-03-v1.md` (dùng các đề xuất làm luồng) | Không nhất quán; Tự chốt nghiệp vụ | TB | Cùng một OQ có ba cách hiểu trạng thái: "đề xuất chờ xác nhận" (OQ table), "Không còn" (cột ảnh hưởng), "Cần xác nhận" (01, sys-us-02). Chữ "Không còn" dễ bị đọc là đã đóng, và sys-us-03/seq-us-03 thực tế đã dùng các đề xuất này làm luồng chính (≥ 500 triệu, Rejected, 500 từ, người nhận thông báo). Rủi ro role sau coi đề xuất là quy tắc đã duyệt. | Dùng một giá trị Trạng thái theo mẫu rules/common.md ("Cần xác nhận") và tách đề xuất sang cột Lựa chọn; bỏ "Không còn" khi chưa có xác nhận khách hàng. Kiểm chứng: đếm OQ có Trạng thái khác "Cần xác nhận"/"Đã xác nhận" trong v2. | rules/common.md (giữ Cần xác nhận đến khi người phụ trách trả lời); TA-SPEC §4.3, PAY-06, PAY-07, PAY-08 | OQ-02, OQ-US03-01..06 |
| R01-05 | `sys-us-03-v1.md` Hậu điều kiện – từ chối (dòng 23), R8 (dòng 26); `seq-us-03-v1.puml` dòng 123, 131, 142 (`Transition(… PendingApproval, Rejected …)`, `result(status=Rejected)`) ↔ `03` §5 T6a/T6b; `state-machine-v1.puml` dòng 27–29; `04` E11 (dòng 160); `05` §9 | Không nhất quán; Tự chốt nghiệp vụ | TB | seq-us-03 và sys-us-03 chỉ vẽ phía §3 (→ Rejected) và mô tả Rejected → Draft "do NVKD chỉnh sửa" (đề xuất OQ-US03-07), trong khi state/03/04/05 trình bày hai phương án T6a/T6b. Không có sequence nào cho phương án PAY-08 (→ Draft ngay). Người hiện thực đọc seq sẽ code một phía duy nhất. | Trong seq-us-03, biểu diễn đích sau từ chối như `alt` hai phương án (hoặc một nhánh ghi "Blocked by OQ-04") giống state machine. Kiểm chứng: so `to_status` của audit `reject` trong seq-us-03 với 05 §10. | TA-SPEC §3 ↔ §5 PAY-08; TA-PDF tr.1–2 | OQ-04, OQ-US03-07, OQ-D-01 |
| R01-06 | `state-machine-v1.puml` dòng 27, 29 (guard reject `!= CreatedBy` không ghi OQ); `03` §5 T6a; `seq-us-03-v1.puml` dòng 77 ↔ `04` E11 (dòng 157 "PAY-07 với từ chối: Blocked by OQ-US03-01"); `06` PAY-07 ("từ chối: Blocked"); `sys-us-03` AC-US03-09 (Blocked) | Không nhất quán | TB | PAY-07 chỉ nói "không được **duyệt**". Việc áp dụng cho **từ chối** là đề xuất chưa xác nhận. State machine và 03 đặt guard này cho reject như điều kiện chắc chắn; API và ma trận lại ghi Blocked. | Ghi `Blocked by OQ-US03-01` cho guard PAY-07 của reject ở state machine và 03 §5 (giữ nguyên cho approve). Kiểm chứng: so guard T6a/T6b với AC-US03-09. | TA-SPEC §5 PAY-07; §4.3; TA-PDF tr.2 | OQ-US03-01 |
| R01-07 | `sys-us-03-v1.md` AC-US03-06 (dòng 61: "tổng **trên** 500 triệu và người gọi là KTT") ↔ P2/5a cùng file ("≥ 500.000.000 đ") | Không nhất quán | Thấp | Trong cùng file, AC dùng "trên", luồng dùng "≥". Tại đúng 500 triệu, AC-US03-06 và 5a cho kết quả khác nhau. | Viết lại AC-US03-06 chỉ cho "dưới" và "trên" ngưỡng, để biên cho AC-US03-07 (Blocked by OQ-02). Kiểm chứng: đọc chéo AC-US03-06/07 với bước 5a. | TA-SPEC §4.3, PAY-06; TA-PDF tr.2 | OQ-02 |
| R01-08 | `sys-us-02-v1.md` "Minh chứng và bàn giao" dòng 111 ("PAY-01..03 … không tự bổ sung thành điều kiện tái kiểm tra khi trình"); `04` E9, E10 (không kiểm tra lại nguồn) | Thiếu OQ | TB | Đặc tả không nói gì về việc hợp đồng hết Active, bảng giá thay đổi hoặc sản lượng bị mở lại đối soát **sau khi** Draft đã lưu và trước khi trình/duyệt. v1 đã chọn "không kiểm tra lại" mà không có OQ. Quyết định này có thể dẫn tới duyệt bảng của hợp đồng không còn hiệu lực, hoặc ngược lại chặn trình sai nếu chọn kiểm tra lại. | Ghi OQ mới: có kiểm tra lại PAY-01..03 khi trình/duyệt không, nếu có thì xử lý khi điều kiện không còn đúng ra sao. Kiểm chứng: có OQ tương ứng trong open-questions-v2 và luồng E9/E10 ghi Blocked. | TA-SPEC §4.1, §4.2, §5 PAY-01..04; TA-PDF tr.2 (đặc tả im lặng) | – (chưa có) |
| R01-09 | `sys-us-02-v1.md` A6 (dòng 60), §1.5; `07` DD-02 (hệ quả: "không phân biệt nhấn lặp với người khác vừa đổi"); `04` E9 hàng "Chống trùng" | Thiếu OQ; Đề xuất kỹ thuật | TB | PAY-04 "chống thao tác trình duyệt trùng" được hiểu là gửi lặp/đồng thời cho **cùng một bảng**. Chưa hỏi nghĩa khác (trình hai bảng cho cùng hợp đồng/kỳ, hay trình lại bảng có nội dung trùng). Ngoài ra, lần gửi lại do mất phản hồi mạng sẽ nhận 409 dù lần đầu đã thành công; DD-02 đã nêu rủi ro nhưng không có hướng xử lý cho client. | Ghi OQ về phạm vi "trùng"; bổ sung trong 04 cách client xác định kết quả khi nhận `DUPLICATE_SUBMIT` (vd. đọc lại E6). Kiểm chứng: test gửi E9 hai lần tuần tự, lần hai nhận mã và hướng dẫn đúng. | TA-SPEC §5 PAY-04; TA-PDF tr.2. Phần xử lý client: Không có căn cứ trong đặc tả – đề xuất kỹ thuật | – (chưa có) |
| R01-10 | `class-v1.puml` dòng 172 (`PaymentAdjustmentService.Adjust(id, content, minutesRef, expectedVersion, user)`), dòng 182 (`UpdateApproved(sheet, minutesRef, expectedVersion)`); `seq-us-04-v1.puml` dòng 34, 36 ↔ `04` E12 request có `changes`; `04` E12 phương án A "`version` không đổi"; `sys-us-04` AC-US04-09 | Không nhất quán; Nhánh lỗi | TB | (1) Chữ ký service không nhận `changes`, nên phương án B không có dữ liệu để cập nhật trường. (2) seq-us-04 kiểm tra quyền KTT/biên bản **trước** khi đọc bảng, không có nhánh `UNAUTHENTICATED`, không phân biệt `NOT_FOUND`/`INVALID_STATE` theo thứ tự ở 04 §1. (3) Với A, `expectedVersion` không có tác dụng, nên hai điều chỉnh đồng thời đều thành công, trái với AC-US04-09 ("yêu cầu thua nhận lỗi xung đột"). Toàn bộ US-PAY-04 vẫn Blocked by OQ-03, nhưng hai phương án cần nhất quán để nhóm/khách hàng so sánh. | Đồng bộ chữ ký `Adjust`/`UpdateApproved` với E12 (có `changes`); làm rõ AC-US04-09 áp cho A hay chỉ B. Kiểm chứng: đối chiếu tham số seq-us-04 ↔ class ↔ 04 E12. | TA-SPEC §4.4, §5 PAY-05, §6; TA-PDF tr.2–3. Chữ ký/kiểm soát đồng thời: đề xuất kỹ thuật | OQ-03, OQ-US04-01 |
| R01-11 | `seq-us-03-v1.puml` dòng 54 (`UOW.Begin()` trước `GetById`), các nhánh 3a/4a/5a/6a/R7a/R7b (dòng 58–80, 115–120) trả lỗi không `Rollback`; dòng 101, 139 `Commit()` không xử lý kết quả | Nhánh lỗi | Thấp | Giao dịch mở trước khi kiểm tra rồi kết thúc nhánh lỗi mà không đóng; không có nhánh commit thất bại/không rõ kết quả như seq-us-01 (A15.1/A15.2) và seq-us-02 (A6.1). Lệch mức chi tiết giữa các seq khiến 03 §1.3 `RESULT_UNKNOWN` không áp dụng thống nhất. | Mở giao dịch ngay trước `Transition`, hoặc thêm `Rollback` ở các nhánh lỗi; thêm nhánh kết quả commit. Kiểm chứng: đếm Begin/Commit/Rollback theo từng nhánh trong seq. | TA-SPEC §6 (audit cùng thay đổi); phần giao dịch: đề xuất kỹ thuật (DD-03) | – |
| R01-12 | `seq-us-05-v1.puml` dòng 41, 53, 64, 73 (`alt [A1]…end`, `alt [A2]…end`, … không có `else`) | Nhánh lỗi | Thấp | Theo ngữ nghĩa UML, sau `alt` chỉ có một nhánh, luồng tiếp tục xuống bước sau, tức là sơ đồ cho thấy vẫn kiểm tra quyền/trạng thái và ghi `Cancelled` sau khi đã trả 404/403/409/400. Không có nhánh `UNAUTHENTICATED` và kết quả `Commit()`. | Dùng `break` (như seq-us-02) hoặc lồng `else`. Kiểm chứng: xem SVG, mỗi nhánh lỗi phải kết thúc. | TA-SPEC §3, §4.5; TA-PDF tr.1–2 | OQ-US05-01, OQ-US05-03 |
| R01-13 | `seq-us-02-v1.puml` dòng 62–68 (A3.1 Rejected), 96–101 (A5) chỉ có note, không có message trả về; dòng 105, 110 ghi "DD-01" cho cập nhật có điều kiện | Nhánh lỗi; Thiếu truy vết | Thấp | Hai nhánh `break` không trả kết quả cho NVKD, nên chưa biết API phản hồi gì khi chưa có xác nhận (hiện chỉ ghi Blocked là đúng trạng thái, nhưng thiếu phản hồi tạm thời). DD-01 là quyết định về **tên**; cơ chế đồng thời là DD-02. | Ghi phản hồi tạm (vd. `INVALID_STATE` cho Rejected kèm "Blocked by OQ-04") hoặc ghi rõ "chưa định nghĩa phản hồi"; sửa tham chiếu DD-01 → DD-02. Kiểm chứng: đối chiếu với 07. | TA-SPEC §3, PAY-08; 07 DD-01/DD-02 | OQ-04, OQ-US03-07, OQ-02 |
| R01-14 | `04` E9 hàng "Chống trùng" (dòng 139: request thua → `CONCURRENT_MODIFICATION`) ↔ `05` §9 (dòng 161–164: 0 dòng → `CONCURRENT_MODIFICATION`/`DUPLICATE_SUBMIT`/`INVALID_STATE` "tùy trạng thái đọc lại") ↔ `seq-us-02` A6 | Không nhất quán | Thấp | Khi hai request cùng `expectedVersion`, request thua sẽ đọc lại thấy `PendingApproval`; theo 05 §9 phải trả `DUPLICATE_SUBMIT`, theo 04/seq-us-02 trả `CONCURRENT_MODIFICATION`. Test PAY-04 ở 06 không chỉ rõ mã mong đợi. | Chốt một quy tắc ánh xạ trong 03 §1.3 và dùng chung cho 04/05/seq. Kiểm chứng: test song song E9 → kiểm tra mã lỗi của request thua. | TA-SPEC §5 PAY-04; phần mã lỗi: đề xuất kỹ thuật (DD-10) | – |
| R01-15 | `05` §4.1 `price_list_id` một giá trị NOT NULL (dòng 43); §4.2 `quantity_source_ref`, `price_source_ref` một giá trị NOT NULL (dòng 69–70); `class-v1.puml` `PaymentLine.QuantitySourceRef : string` | Tự chốt nghiệp vụ (cấu trúc dữ liệu) | Thấp | OQ-US01-01 còn mở phương án "tách theo giai đoạn giá" (nhiều bảng giá/đơn giá trong kỳ) và OQ-US01-04 còn mở việc gộp nhiều bản ghi sản lượng vào một dòng. Cột đơn trị NOT NULL đã ngầm chọn "một bảng giá/bảng" và "một bản ghi nguồn/dòng" nhưng không ghi Blocked như các cột khác. | Ghi `Blocked by OQ-US01-01/OQ-US01-04` cho các cột này hoặc nêu phương án thay thế (bảng liên kết nguồn). Kiểm chứng: cột OQ của 05 §4.1–4.2. | TA-SPEC §2 "Dòng thanh toán", §4.1, §5 PAY-01, PAY-03; TA-PDF tr.1–2 | OQ-US01-01, OQ-US01-04 |
| R01-16 | `sys-us-04-v1.md` System Spec (dòng 13–21); `seq-us-04-v1.puml` (cả file); `04` E12 | Thiếu OQ | Thấp | Chưa có câu hỏi riêng về quan hệ giữa điều chỉnh và ngưỡng duyệt: KTT điều chỉnh bảng ≥ 500 triệu do GĐKD đã duyệt, hoặc điều chỉnh làm tổng vượt/xuống dưới ngưỡng; KTT điều chỉnh bảng do chính mình đã duyệt. OQ-US04-02 chỉ hỏi chung "có duyệt lại không, ai duyệt". | Bổ sung chi tiết vào OQ-US04-02 hoặc OQ mới (không tự chọn cách xử lý). Kiểm chứng: OQ v2 nêu rõ ba tình huống. | TA-SPEC §4.3, §4.4, §5 PAY-06, PAY-07; TA-PDF tr.2 | OQ-US04-02, OQ-03 |
| R01-17 | `06` §3: cột API/kiểm chứng của các dòng AC-US01-01..26 hầu hết là "E1–E5, E7, E8" / "Test API E1–E5: dựng Given, gọi When, kiểm tra Then"; AC-US01-01 "Đã thiết kế" trong khi sys-us-01 ghi "Phần kỳ/giá/tổng theo OQ"; AC-US04-04, 05, 06 "Blocked by OQ-03" trong 06 nhưng "–" trong sys-us-04 §AC; AC-US05-02 chỉ trỏ E13 dù yêu cầu chặn cả sửa/trình/duyệt/từ chối | Thiếu truy vết; Không nhất quán | TB | Ma trận đủ dòng (73/73) nhưng nhiều dòng không truy tới endpoint/nhánh cụ thể, nên không dùng để kiểm thử từng AC được; trạng thái chặn lệch giữa sys-us và 06 làm sai số liệu bao phủ ở 06 §7. | Ghi endpoint + nhánh (vd. E5 A15) và mã lỗi mong đợi cho từng AC; đồng bộ trạng thái Blocked với cột OQ của sys-us; AC-US05-02 trỏ E8–E11, E13. Kiểm chứng: lấy ngẫu nhiên 10 AC, mỗi AC phải tìm được đúng nhánh trong seq và endpoint. | rules/reviewer.md mục 4–5; rules/payment-scope.md (bao phủ US/PAY/NFR/AC) | – |
| R01-18 | `06` §1 dòng 22 và `01` §1 dòng 20 ("chưa commit"); `01` mục Kiểm chứng và `03` §6 (trỏ sang prompt-log thay vì ghi kết quả); `seq-us-03-v1.puml` dòng 10 ("Chưa kiểm tra kết xuất sơ đồ") ↔ `03` §3 ("SVG (P-24)"); `sys-us-01-v1.md` dòng 7, 167 nhắc "ai-review-02-v1.md" | Bằng chứng | Thấp | (1) Các file đã được commit (`a1b9d68`, `b7da5fa`) nhưng tài liệu vẫn ghi "chưa commit", không có mã commit. (2) 01/03 không ghi trực tiếp lệnh và kết quả. (3) seq-us-03 ghi chưa kết xuất trong khi SVG có và khớp nguồn (§2). (4) `ai-review-02-v1.md` không tồn tại trong lịch sử Git; các báo cáo review cũ (`ai-review-03-v1`, `ai-review-us-05-v1`…) đã bị xóa ở `b7da5fa`, nên câu "báo cáo review cũ vẫn phản ánh bản trước" không kiểm chứng được. | Ghi mã commit/tag `design-v1`, lệnh và kết quả kiểm tra ngay trong 01 hoặc 06 §8; cập nhật header seq-us-03; sửa tham chiếu tới báo cáo không tồn tại. Kiểm chứng: `git log`, `git tag`, đối chiếu §2 của báo cáo này. | rules/common.md (không nói đã chạy/render khi chưa có bằng chứng); rules/handoff.md | – |
| R01-19 | `docs/workflow/prompt-log.md` dòng 288 và 340 (hai mục **P-15**), 306 và 448 (hai mục **P-16**); không có mục P-23 dù `rules/*.md` ghi "Tách … (P-23)"; `scripts/verify_agent_config.py` FAIL 5 checks | Bằng chứng; Thiếu truy vết | Thấp | sys-us-01 dẫn "P-15, P-16, P-17", sys-us-02 dẫn "P-15, P-16" – không xác định được mục nào. Thiếu P-23 làm đứt minh chứng cho việc tách rules. Script kiểm tra workspace hiện không PASS. | Thêm mục đính chính đổi ID (không sửa mục cũ, theo quy ước prompt-log); bổ sung P-23 hoặc ghi lý do thiếu; xử lý 5 FAIL. Kiểm chứng: `python -X utf8 scripts/verify_agent_config.py` → PASS. | rules/handoff.md; docs/workflow/prompt-log.md (mục Mẫu) | – |
| R01-20 | `sys-us-03-v1.md` AC-US03-01 nhãn `[ĐẶC TẢ]` nhưng Blocked by OQ-02, OQ-US03-02 (dòng 56); P4 dẫn "[PAY-08]" cho "tối đa 500 từ" (dòng 21); `sys-us-05-v1.md` AC-US05-01 `[ĐẶC TẢ]` nhưng Blocked by OQ-US05-01/03 (dòng 47); "Tác nhân liên quan: KTT, GĐKD (theo dõi audit log)" gắn `[THAM KHẢO]` không có nguồn (dòng 17) | Nhãn nguồn | Thấp | AC phụ thuộc OQ hoặc có điều kiện bổ sung phải là AC dẫn xuất chờ xác nhận; PAY-08 chỉ yêu cầu "phải nhập lý do", không có giới hạn 500 từ; vai trò KTT/GĐKD "theo dõi audit" không có trong §2/§6. Nhãn sai làm tăng số yêu cầu "có căn cứ đặc tả" trong 06. | Đổi nhãn sang `[AC dẫn xuất]`/`[GIẢ ĐỊNH – Cần xác nhận]`; tách căn cứ PAY-08 và OQ-US03-04; bỏ hoặc gắn OQ cho trách nhiệm "theo dõi audit". | rules/common.md (phân loại kết luận); TA-SPEC §2, §5 PAY-08, §6 | OQ-02, OQ-US03-02, OQ-US03-04, OQ-US05-01, OQ-US05-03 |
| R01-21 | `03` §5 (không có chuyển rời `PendingApproval` ngoài approve/reject); `state-machine-v1.puml`; `sys-us-05` A3 | Thiếu OQ | Thấp | Đặc tả không có cách để NVKD rút lại hoặc hủy bảng đang `PendingApproval` (vd. phát hiện sai ngay sau khi trình), và không nói bảng `Approved` có bị hủy được không. Thiết kế đúng khi không tự thêm chuyển trạng thái, nhưng chưa có OQ ghi nhận khoảng trống này (OQ-D-01 chỉ hỏi `Rejected`). | Ghi OQ "lối ra của PendingApproval/Approved ngoài luồng chính"; không thêm trạng thái/chuyển. | TA-SPEC §3, §4.2, §4.5; TA-PDF tr.1–2 | OQ-D-01 (liên quan) |
| R01-22 | `sys-us-02-v1.md` bước 4, A4, AC-US02-03 (tổng 0 không bị chặn); `05` §4.1 "Không CHECK ≥ 0" | Thiếu OQ | Thấp | PAY-04 chặn "tổng tiền âm" nhưng PAY-03 tính q × p từ nguồn chỉ đọc; đặc tả không nói tổng âm phát sinh từ đâu (dòng giảm trừ, sản lượng/đơn giá âm, hay sửa tay ở Draft). Điều này quyết định có cần kiểm tra dấu ở từng dòng và phạm vi sửa Draft (OQ-US01-02). | Ghi OQ về nguồn giá trị âm hoặc nối vào OQ-US01-02/OQ-US01-04. | TA-SPEC §5 PAY-03, PAY-04; TA-PDF tr.2 | OQ-US01-02, OQ-US01-04 |
| R01-23 | `sys-us-04-v1.md` dòng 13 ("SYS-PAY-04"); `seq-us-04-v1.puml` dòng 3 (title "SYS-PAY-04"); header seq-us-04 thiếu dòng "Nguồn"/"Kết xuất" như các seq khác | Không nhất quán | Thấp | Các US khác dùng `SYS-US-0N`; mã `SYS-PAY-04` dễ nhầm với mã `PAY-0N` của đề. | Đổi về `SYS-US-04` trong v2. | skills/naming-versioning; rules/common.md (mã tự đặt không phải mã của đề) | – |
| R01-24 | `05` §4.3, §10; `07` DD-11 | Thiếu OQ | Thấp | §6 chỉ yêu cầu "ai, lúc nào, thay đổi gì". Thiết kế chọn mức chi tiết (ảnh chụp JSON) và gắn đúng nhãn đề xuất kỹ thuật, nhưng chưa có câu hỏi về ai được xem audit, thời gian lưu, và việc gửi thông báo thất bại/thử lại có phải là "thay đổi" cần audit không. | Ghi OQ về quyền xem và lưu giữ audit; giữ DD-11 là đề xuất. | TA-SPEC §6 gạch 1; TA-PDF tr.3 | OQ-US02-02 (liên quan thông báo) |
| R01-25 | `04` §1 hàng "Thứ tự kiểm tra" (dòng 24: tồn tại → quyền trên bảng) ↔ `seq-us-02-v1.puml` dòng 34 (kiểm tra "quyền trên bảng" trước `GetById` ở dòng 46) | Không nhất quán | Thấp | Không thể kiểm tra quyền trên một bảng trước khi đọc bảng; thứ tự trong seq-us-02 trái với quy ước chung của 04 (03 §2 đã ghi nhận nhưng chưa xử lý). | Tách "vai trò NVKD" (trước) và "quyền trên bảng" (sau GetById) trong seq-us-02. | TA-SPEC §2, §4.2; phần thứ tự: đề xuất kỹ thuật | OQ-US02-01 |
| R01-26 | `component-v1.puml` dòng 97 (`Acc ..> IHttp : đọc bảng Approved`) | Suy diễn ngoài đặc tả (ranh giới module) | Thấp | Sơ đồ thêm phụ thuộc "Kế toán đọc bảng Approved qua HTTP" – một tích hợp không có trong đặc tả; cách chuyển kế toán đang chờ OQ-US03-06 (đề xuất "ngoài phạm vi"). Có thể bị hiểu là cam kết API cho module kế toán. | Ghi "Blocked by OQ-US03-06" trên liên kết hoặc bỏ liên kết, giữ thành phần kế toán ở ngoài ranh giới. | TA-SPEC §1 ("chuyển kế toán xuất hóa đơn" – không nêu cơ chế); TA-PDF tr.1 | OQ-US03-06 |
| R01-27 | `02` §3 hàng "Hiệu năng lập bảng" ("một lượt đọc HĐ/giá/sản lượng") ↔ `seq-us-01` (E1–E4 nhiều lượt đọc, E5 đọc lại toàn bộ nguồn + `FindConflict`); `06` NFR-PAY-02 (đo E5 với 199 dòng) | Bằng chứng; Đề xuất kỹ thuật | Thấp | Phương án hiệu năng mô tả "một lượt đọc" nhưng luồng có nhiều lượt; chưa có giả định thời gian cho reader của module khác (AS-IS chưa có). Trạng thái "chưa đo" được ghi trung thực. | Ghi rõ phép đo dự kiến áp cho E5 hay E4+E5 (chờ OQ-US01-06) và ngân sách thời gian cho từng lượt đọc như đề xuất; không kết luận đạt ≤3 giây khi chưa đo. | TA-SPEC §6 gạch 2; TA-PDF tr.3 | OQ-US01-06 |
| R01-28 | `open-questions-v1.md` tiêu đề bảng (dòng 16); OQ-03 cột "Đề xuất / Lựa chọn" = "–" (dòng 20) trong khi phương án A/B nằm ở cột "Còn mở"; OQ-US04-01, 02 không có lựa chọn | Không nhất quán (mẫu OQ) | Thấp | Bảng OQ chung không theo mẫu của rules/common.md (thiếu cột "Lý do cần xác nhận"; cột "Trạng thái" lẫn đề xuất). Người chấm phải tìm lựa chọn ở cột khác. | Chuyển về đúng mẫu 9 cột trong v2; đặt lựa chọn A/B của OQ-03 vào cột Lựa chọn. | rules/common.md (Mẫu Open Questions) | OQ-03, OQ-US04-01, OQ-US04-02 |

## 5. Vấn đề đặc tả mà OQ hiện có còn bỏ sót

Đối chiếu 25 OQ trong `open-questions-v1.md` và OQ-D-01 trong `01` §7. Các vấn đề đã có OQ:
đúng 500 triệu (OQ-02), điều chỉnh Approved (OQ-03), Rejected/Draft (OQ-04, OQ-US03-07, OQ-D-01),
tháng/quý (OQ-01), dòng bắt buộc (OQ-05). Dưới đây là các vấn đề **chưa có OQ** hoặc mới được hỏi một phần.
Reviewer chỉ nêu câu hỏi, không chọn đáp án.

| # | Vị trí TA-SPEC / TA-PDF | Loại | Vấn đề | Vì sao cần xác nhận | OQ gần nhất | Nhận xét |
|---|---|---|---|---|---|---|
| S-01 | §4.1, §4.2, §5 PAY-01..03; tr.2 | Thiếu | Có kiểm tra lại hợp đồng Active, bảng giá phù hợp, sản lượng Đã đối soát khi **trình** hoặc **duyệt** không, nếu nguồn đã đổi sau khi lưu Draft? | v1 đã tự chọn "không kiểm tra lại" | Không có (OQ-US01-01/04/05 chỉ hỏi giữa xem trước và lưu) | R01-08 |
| S-02 | §5 PAY-04; tr.2 | Mơ hồ | "Thao tác trình duyệt trùng" là gửi lặp cùng một bảng, hay trình hai bảng cho cùng hợp đồng/kỳ, hay nội dung trùng? | Quyết định cơ chế chống trùng và mã lỗi | Không có | R01-09 |
| S-03 | §1, §4.1 ("NVKD chọn hợp đồng và kỳ"; "hệ thống tự sinh … từ … bảng giá"); tr.1–2 | Mơ hồ | Ai chọn bảng giá: hệ thống tự xác định hay NVKD chọn? | v1 thêm bước NVKD chọn bảng giá theo hướng dẫn trong chat | OQ-US01-01 (một phần: tiêu chí "phù hợp") | R01-03 |
| S-04 | §5 PAY-03, PAY-04; tr.2 | Thiếu | Tổng tiền âm phát sinh từ đâu (dòng giảm trừ, giá trị nguồn âm, sửa tay)? Tổng bằng 0 có được trình không (v1 hiểu theo câu chữ là được)? | Quyết định kiểm tra dòng và phạm vi sửa Draft | OQ-US01-02 (một phần) | R01-22 |
| S-05 | §3, §4.2, §4.5; tr.1–2 | Thiếu | Bảng `PendingApproval` có được rút lại/hủy không; bảng `Approved` có bị hủy (vd. hợp đồng chấm dứt) không? | Không có lối ra ngoài approve/reject | OQ-D-01 (chỉ `Rejected`) | R01-21 |
| S-06 | §4.3, §4.4, PAY-06, PAY-07; tr.2 | Thiếu | Điều chỉnh bảng ≥ 500 triệu (do GĐKD duyệt) bởi KTT; điều chỉnh làm tổng đi qua ngưỡng; KTT điều chỉnh bảng do chính mình duyệt | Ảnh hưởng thẩm quyền và kiểm soát tách nhiệm | OQ-US04-02 (một phần) | R01-16 |
| S-07 | §6 gạch 1; tr.3 | Thiếu | Ai được xem audit, lưu bao lâu, mức chi tiết "thay đổi gì"; gửi thông báo thất bại có cần audit không | Ảnh hưởng quyền đọc và schema audit | OQ-US02-02 (một phần, thông báo) | R01-24 |
| S-08 | §2 "Dòng thanh toán: một dịch vụ"; §4.1; PAY-03; tr.1–2 | Mơ hồ | Một bảng có thể dùng nhiều bảng giá (giá đổi trong kỳ) và một dòng có thể gộp nhiều bản ghi sản lượng không – ảnh hưởng cấu trúc dữ liệu đã chốt | Cột đơn trị NOT NULL ở 05 | OQ-US01-01, OQ-US01-04 (có hỏi nghiệp vụ, chưa nêu tác động dữ liệu) | R01-15 |

## 6. Kết luận

**Cần chỉnh sửa.**

- Có hai nhận xét mức Cao về mâu thuẫn nội bộ và tự chốt nghiệp vụ ở luồng duyệt (R01-01 ngưỡng
  đúng 500 triệu, R01-02 cơ sở tổng tiền VAT/làm tròn) và một nhận xét mức Cao về bước nghiệp vụ
  không có trong đặc tả được gắn nhãn đã xác nhận (R01-03).
- Bao phủ về mặt danh mục đủ: 5/5 US, 8/8 PAY, 2/2 NFR, 73/73 AC có dòng truy vết; 9/9 sơ đồ render được.
  Đây chưa phải bằng chứng đáp ứng: không có kiểm thử, NFR-PAY-02 chưa đo, chưa có phê duyệt người phụ trách.
- Sau khi chỉnh sửa trong v2, phần lớn thiết kế vẫn ở trạng thái **Chờ xác nhận nghiệp vụ** do các OQ
  OQ-01, OQ-02, OQ-03, OQ-04, OQ-05, OQ-US03-03, OQ-US03-07, OQ-US05-02, OQ-D-01 và các vấn đề ở §5.
- Reviewer không có quyền duyệt nghiệp vụ, không đóng OQ và không đánh giá các nhận xét trên là Đúng/Sai/Thừa.

## 7. Bàn giao

- Người nhận: người phụ trách module và nhóm đánh giá (6 thành viên) – ghi kết quả vào
  `docs/review/payment-management/review-assessment-01-v1.md` (Đúng/Sai/Thừa, lý do, chấp nhận/từ chối/chờ,
  thay đổi file/commit, người/ngày) theo [rules/handoff.md](../../../rules/handoff.md).
- v1 đóng băng kể từ báo cáo này; design chỉ sửa trong `v2/` theo các nhận xét được chấp nhận.
- File này là đầu ra duy nhất của lần review (cùng mục P-25 trong prompt-log). Không file thiết kế,
  phân tích, đặc tả, rules, skill hay script nào bị sửa.
