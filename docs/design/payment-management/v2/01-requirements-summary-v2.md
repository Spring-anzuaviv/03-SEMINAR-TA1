# 01 – Tóm tắt yêu cầu module Bảng thanh toán (v2)

> Phiên bản: v2 · Ngày: 11/11/2026 · Người phụ trách: chờ nhóm chỉ định
> Đầu vào: TA-SPEC §1–6, năm System Spec v2, danh mục sequence v2, thiết kế dữ liệu v2 và xác nhận của đại diện nhóm trong chat ngày 11/11/2026.
> AI: Codex / GPT-6 · [P-39](../../../workflow/prompt-log.md#p-39--đồng-bộ-01-và-02-với-thiết-kế-v2)
> Trạng thái: Bản đề xuất sau review – Design Pending Approval

## 1. Nguồn và phạm vi

**[ĐẶC TẢ]** Module lập và sửa bảng nháp, trình duyệt, duyệt/từ chối, điều chỉnh và hủy bảng thanh toán. Hợp đồng, bảng giá và sản lượng là dữ liệu chỉ đọc. Việc chuyển bảng sang kế toán và xuất hóa đơn thuộc ngoài phạm vi theo SYS-US-03 v2 §1.1. [TA-SPEC §1, §4, TA-PDF tr.1–2](../../../requirements/payment-management/spec.md)

Các cột **v2** tóm tắt hành vi trong System Spec hiện hành. Cách biểu diễn dữ liệu và các câu hỏi phát sinh lấy theo thiết kế dữ liệu v2. §6 ghi các điểm đã được đại diện nhóm xác nhận trong chat và các chi tiết còn mở. `SYS-US`, `OQ`, `AC` và `NFR-PAY` là mã nội bộ. [Danh mục sequence](03-detailed-design-v2.md) · [Thiết kế dữ liệu](05-data-design-v2.md) · [Sổ nguồn TA-PDF](../../../requirements/payment-management/sources.md)

Chưa đủ đầu vào BA tổng hợp gồm `open-questions-v2.md` và `requirements-checklist-v2.md`. Bản đề xuất đối chiếu trực tiếp năm System Spec hiện hành với TA-SPEC, giữ mã OQ đã có và dẫn theo mục/bước của v2.

## 2. Tác nhân và trạng thái

| Tác nhân theo TA-SPEC §2 (tr.1) | Quyền trong v2 | Nguồn v2 |
|---|---|---|
| Nhân viên kinh doanh (NVKD) | Với hợp đồng được phân công, NVKD lập, sửa Draft, trình, gửi lại thông báo trình duyệt, mở lại Rejected và hủy Draft. Thông báo kết quả duyệt/từ chối gửi cho NVKD đã tạo bảng. | SYS-US-01 Actor, SYS-US-02/02b Actor, SYS-US-03 §1.1 bước 9 và §1.2, SYS-US-05 P1–P4, P-39. |
| Kế toán trưởng (KTT) | Duyệt hoặc từ chối bảng có tổng đã lưu gồm GTGT dưới 500.000.000 đồng. Lập hồ sơ điều chỉnh cho bảng Approved. | SYS-US-03 §1.1 bước 5–6, SYS-US-04 §1.1. |
| Giám đốc kinh doanh (GĐKD) | Duyệt hoặc từ chối bảng có tổng đã lưu gồm GTGT từ 500.000.000 đồng. Duyệt hoặc từ chối mọi hồ sơ điều chỉnh. | SYS-US-03 §1.1 bước 5–6, SYS-US-04 §1.2. |

**Bảng thanh toán** có năm trạng thái theo TA-SPEC §3 (tr.1). Lập bảng vào `Draft`, trình sang `PendingApproval`, rồi duyệt sang `Approved` hoặc từ chối sang `Rejected`. NVKD phụ trách bấm **Chỉnh sửa** để đưa `Rejected` về `Draft`. Hủy từ `Draft` sang `Cancelled`. [SYS-US-02 §1.1, SYS-US-03 §1.1–1.2, SYS-US-05 P3 và S1]

**Hồ sơ điều chỉnh** có vòng đời Chờ duyệt → Đã duyệt hoặc Bị từ chối. Bảng gốc vẫn `Approved`. Số liệu hiệu lực áp dụng các thay đổi từ hồ sơ đã duyệt. [SYS-US-04 §1.1–1.2, Hậu điều kiện]

## 3. Yêu cầu chức năng

| US của đề (TA-PDF tr.2) | Hành vi trong v2 | Ngoại lệ chính trong v2 | System Spec |
|---|---|---|---|
| **US-PAY-01** – Lập và sửa Draft (§4.1) | Mở từ chi tiết hợp đồng, chọn kỳ tháng/quý theo cấu hình, tự lấy đúng một bảng giá Active. Gộp sản lượng đã đối soát theo dịch vụ, tính tiền và kiểm tra lại nguồn khi lưu. Draft cho sửa ghi chú hoặc **Tải lại dữ liệu nguồn**. | Sai quyền, hợp đồng hết hiệu lực, kỳ chồng lấn, thiếu giá/sản lượng, sản lượng chưa đối soát, tổng âm, xung đột kỳ hoặc lỗi lưu/audit. | [SYS-US-01, bước 1–16, A7–A15, EC.1 và E15](../../../analysis/payment-management/v2/sys-us-01-v2.md) |
| **US-PAY-02** – Trình duyệt (§4.2) | Kiểm tra quyền, `Draft`, nguồn còn hợp lệ, tổng không âm và đủ dòng cho dịch vụ hợp đồng. Chuyển `PendingApproval`, tăng phiên bản và số lần trình, ghi audit rồi gửi thông báo trong hệ thống. **02b:** gửi lại trên lần trình hiện tại theo vai trò duyệt đã xác định cho lần trình đó. | Chặn trình trùng hoặc xung đột phiên bản. Khi chưa có người nhận hoặc gửi lỗi, bảng vẫn chờ duyệt. Khi gửi lại, tìm người nhận nếu chưa có danh sách. Nếu đã có danh sách, chỉ gửi cho người chưa nhận. | [SYS-US-02 §1.1, A8/A10, E5–E9.1 và SYS-US-02b §1.2](../../../analysis/payment-management/v2/sys-us-02-v2.md) |
| **US-PAY-03** – Duyệt hoặc từ chối (§4.3) | Người đúng thẩm quyền và khác người lập xử lý bảng `PendingApproval`. Duyệt kiểm tra lại nguồn. Từ chối cần lý do có nội dung, tối đa 500 từ. Gửi kết quả cho người tạo bảng. **03b:** NVKD phụ trách mở lại `Rejected` thành `Draft`, giữ lý do để tham chiếu. | Sai vai trò, tự duyệt/từ chối, nguồn đổi khi duyệt, lý do không hợp lệ hoặc yêu cầu khác đã xử lý. Lỗi gửi thông báo giữ nguyên kết quả đã lưu. | [SYS-US-03 §1.1, A01/A02, E03–E11 và SYS-US-03b §1.2](../../../analysis/payment-management/v2/sys-us-03-v2.md) |
| **US-PAY-04** – Điều chỉnh bảng đã duyệt (§4.4) | KTT lập hồ sơ riêng gồm biên bản có số, ngày, tệp và xác nhận hai bên. Cho sửa sản lượng/đơn giá, thêm hoặc bớt dòng, kèm lý do từng thay đổi. Mỗi bảng có tối đa một hồ sơ chờ duyệt. **04b:** GĐKD khác người lập hồ sơ xử lý. | Chặn hồ sơ trùng, thiếu biên bản hoặc thay đổi sai phạm vi. GĐKD từ chối cần lý do. Khi từ chối, số liệu hiệu lực giữ nguyên và KTT có thể lập hồ sơ mới. | [SYS-US-04 §1.1, bước 3–7, 4a–7b và SYS-US-04b §1.2](../../../analysis/payment-management/v2/sys-us-04-v2.md) |
| **US-PAY-05** – Hủy bảng nháp (§4.5) | NVKD phụ trách hủy `Draft` kèm lý do. Lưu `Cancelled` và audit. Có thể lập bảng mới cùng kỳ. | Sai quyền, sai trạng thái, thiếu lý do, xung đột hoặc lỗi lưu/audit. Nếu bảng đang `Rejected`, NVKD mở lại `Draft` trước khi hủy. | [SYS-US-05 P1–P4, S1–S5, AF1/AF2 và A2–A7.2](../../../analysis/payment-management/v2/sys-us-05-v2.md), xác nhận P-39. |

## 4. Quy tắc nghiệp vụ và yêu cầu phi chức năng

| Mã | [ĐẶC TẢ] TA-SPEC §5 (tr.2) | Cách áp dụng trong v2 |
|---|---|---|
| PAY-01 | Hợp đồng Active, có bảng giá phù hợp. Mỗi hợp đồng có tối đa một bảng mỗi tháng. | Kỳ theo cấu hình tháng/quý. Khoảng ngày tính cả ngày đầu và ngày cuối theo 05 §3.1, và không chồng lấn với bảng chưa hủy của cùng hợp đồng. Khi lập, hợp đồng phải Active và có đúng một bảng giá Active. Việc kỳ có luôn gồm trọn tháng dương lịch còn ở `OQ-D-02`. [SYS-US-01 P2–P4, bước 6–9, 14–15; SYS-US-05 S5; OQ-01] |
| PAY-02 | Sản lượng của kỳ phải đã đối soát. | Kỳ phải có dữ liệu và toàn bộ bản ghi phải đã đối soát. Khi trình và duyệt, kiểm tra lại tình trạng đối soát và thay đổi của các bản ghi nguồn đã dùng. [SYS-US-01 bước 8; SYS-US-02 bước 6; SYS-US-03 bước 7] |
| PAY-03 | Thành tiền dòng bằng sản lượng nhân đơn giá tại thời điểm tính. | Lưu đơn giá và nguồn sản lượng đã dùng, tạm tính, thuế suất, tiền thuế và tổng. Hồ sơ điều chỉnh dùng thuế suất của bảng gốc và quy tắc tính chung. [SYS-US-01 bước 9–10, 14–15; SYS-US-04 §1.1 bước 6; OQ-US03-03] |
| PAY-04 | Chặn trình khi tổng âm, thiếu dòng dịch vụ bắt buộc hoặc trình trùng. | Dịch vụ bắt buộc là mọi dịch vụ khai báo trong hợp đồng. Tổng bằng 0 hợp lệ nếu đạt các điều kiện còn lại. Hai yêu cầu trình cùng phiên bản chỉ tối đa một yêu cầu được lưu. [SYS-US-02 §1.1 bước 7–9, E7.1/E9; OQ-05] |
| PAY-05 | Bảng Approved không được sửa. | Giữ nguyên bảng và số liệu gốc. KTT điều chỉnh bằng hồ sơ riêng, có hiệu lực sau khi GĐKD duyệt. [SYS-US-04 §1.1–1.2; OQ-03] |
| PAY-06 | Trên 500.000.000 đồng do GĐKD duyệt, các bảng còn lại do KTT duyệt. | V2 theo TA-SPEC §4.3 tại điểm biên. Từ 500.000.000 đồng trở lên do GĐKD xử lý, dưới mức đó do KTT, tính trên tổng đã lưu gồm GTGT. [SYS-US-02 bước 8; SYS-US-03 bước 5; OQ-02] |
| PAY-07 | Người lập không tự duyệt bảng. | Với bảng, so người thao tác với người tạo Draft cho cả duyệt và từ chối. Với hồ sơ, so với người lập hồ sơ. [SYS-US-03 §1.1 bước 6 và A01; SYS-US-04 §1.2 bước 4] |
| PAY-08 | Từ chối phải có lý do và bảng quay về Draft để sửa, trình lại. | Bảng ở `Rejected` sau khi từ chối. NVKD phụ trách chủ động bấm **Chỉnh sửa** để về `Draft` và vẫn xem được lý do. [SYS-US-03 §1.1 A01, §1.2 bước 1–7; OQ-04] |

| Mã nội bộ | [ĐẶC TẢ] TA-SPEC §6 (tr.3) | Tiêu chí trong v2 |
|---|---|---|
| NFR-PAY-01 | Audit mọi thay đổi trạng thái và mọi điều chỉnh, gồm ai, lúc nào và thay đổi gì. | Audit cả tạo và sửa Draft theo SYS-US-01. Thay đổi nghiệp vụ và audit được lưu cùng giao dịch ở các bước ghi tương ứng. Kiểm tra nội dung trước/sau, lý do khi có và khả năng hoàn tác khi ghi audit thất bại. [SYS-US-01 Hậu điều kiện/bước 15; 02 bước 9; 03 bước 8/03b bước 6; 04 bước 7/04b bước 5; 05 bước 7] |
| NFR-PAY-02 | Lập bảng phản hồi trong vòng 3 giây với hợp đồng có **dưới 200 dòng**. | Đo từ lúc server nhận yêu cầu lưu nháp đến lúc trả kết quả đã lưu. Đếm số dòng sau khi gộp. Chưa có kết quả đo. [SYS-US-01 Mô tả; OQ-US01-06] |

## 5. Tiêu chí nghiệm thu đề xuất

Các dòng dưới đây là **[AC dẫn xuất]** từ mục/bước hiện hành của System Spec v2. Năm System Spec hiện hành chưa có danh mục AC đánh mã riêng. Trạng thái các tiêu chí là chờ nghiệm thu.

| Phạm vi | Kết quả quan sát được | Căn cứ |
|---|---|---|
| US-PAY-01 | NVKD phụ trách lưu được `Draft` có dữ liệu nguồn và tổng đã tính. Kỳ chồng lấn với bảng chưa hủy hoặc sản lượng chưa đối soát bị chặn. Hai yêu cầu tạo chồng lấn không thể cùng thành công. | SYS-US-01 bước 6–15, A7/A8/A15, PAY-01..03. |
| US-PAY-01, sửa Draft | Lưu ghi chú giữ nguyên số liệu. **Tải lại dữ liệu nguồn** cập nhật dòng và tổng từ nguồn khi lưu thành công. Audit ghi thay đổi trước/sau. Chi tiết tính tiền phụ thuộc OQ-US03-03. | SYS-US-01 Mô tả, Hậu điều kiện sửa, PAY-03. |
| US-PAY-02 | Với nguồn hợp lệ, đủ dòng và tổng bằng 0, yêu cầu vẫn được trình. Tổng âm hoặc thiếu dòng giữ `Draft`. Hai yêu cầu cùng phiên bản tạo tối đa một lần trình và một audit trình duyệt. | SYS-US-02 §1.1 bước 6–10, E7/E7.1/E9, PAY-04. |
| SYS-US-02b | Với lần trình chưa có người nhận, gửi lại tìm người theo vai trò đã lưu. Với lần trình đã có danh sách, chỉ gửi cho người chưa nhận. Mỗi người nhận tối đa một thông báo trình duyệt trong cùng lần trình. Gửi lại giữ nguyên trạng thái, số lần trình và audit trình duyệt. | SYS-US-02 §1.1 bước 10, A8/A10, §1.2 bước 2–4, A3/A3.1. [Sequence gửi lại](diagrams/seq-us-02-2-v2.puml). |
| US-PAY-03 | Tổng đã lưu 499.999.999 đồng thuộc KTT. Tổng 500.000.000 và 500.000.001 đồng thuộc GĐKD. Người tạo bảng bị chặn tự duyệt/từ chối. Khi nguồn đổi, duyệt bị chặn và bảng vẫn `PendingApproval`. | SYS-US-03 §1.1 bước 4–8, E04–E06, PAY-06/07. |
| US-PAY-03, SYS-US-03b | Từ chối với lý do hợp lệ lưu `Rejected`. Lý do trống hoặc vượt 500 từ bị chặn. Khi NVKD phụ trách mở lại, bảng về `Draft`, giữ lý do và có audit. | SYS-US-03 §1.1 A01, E07/E08, §1.2 bước 1–7, PAY-08. |
| US-PAY-04, SYS-US-04b | Biên bản thiếu thông tin hoặc đã có hồ sơ chờ duyệt thì không tạo hồ sơ. Sau khi tạo hồ sơ, số liệu hiệu lực giữ nguyên cho đến khi GĐKD duyệt. Từ chối ghi lý do và giữ số liệu hiệu lực. Hai yêu cầu xử lý cùng hồ sơ chỉ có một kết quả được lưu. | SYS-US-04 §1.1 bước 4–7, 4a/7a, §1.2 bước 3–6, R/5a, PAY-05. |
| US-PAY-05 | NVKD phụ trách hủy được `Draft` với lý do hợp lệ. Bảng cũ ở `Cancelled`, chỉ giữ để tra cứu và audit. NVKD có thể tạo bảng mới cùng kỳ nếu đạt điều kiện lập. | SYS-US-05 bước 1–8, A5/A6 và AF2, P-39. |

## 6. Open Questions và xác nhận

### Phương án nhóm dùng trong v2

Các phương án được tóm tắt theo System Spec. Trạng thái OQ theo danh mục trong 03 và 05. Các xác nhận của đại diện nhóm trong chat được ghi riêng ở P-39.

| ID | Vấn đề trong đề | Phương án trong v2 và căn cứ |
|---|---|---|
| OQ-01, OQ-D-01 | §2 cho kỳ tháng/quý, PAY-01 nói mỗi tháng. §3 và §4.5 chỉ nêu hủy Draft. | Kiểm tra khoảng ngày giữa mọi bảng chưa hủy, kể cả `Rejected`. Để hủy `Rejected`, mở lại `Draft` trước. [SYS-US-01 P3, bước 7; SYS-US-03b §1.2; SYS-US-05 P3/AF1] |
| OQ-02 | §4.3 và PAY-06 khác nhau tại đúng 500.000.000 đồng. | GĐKD xử lý đúng ngưỡng theo §4.3. [SYS-US-02 bước 8, SYS-US-03 bước 5] |
| OQ-03, OQ-US04-01/02 | §4.4 cho điều chỉnh, PAY-05 cấm sửa bảng Approved. | Dùng hồ sơ riêng với biên bản và lý do. KTT lập, GĐKD xử lý. Số liệu thay đổi có hiệu lực sau khi hồ sơ được duyệt. [SYS-US-04 §1.1–1.2] |
| OQ-04, OQ-US03-07 | §3 nêu `Rejected`, PAY-08 nêu quay lại `Draft`. | Giữ `Rejected` đến khi NVKD phụ trách bấm **Chỉnh sửa**. [SYS-US-03 §1.1 A01, §1.2] |
| OQ-05 | PAY-04 chưa định nghĩa dòng dịch vụ bắt buộc. | Mọi dịch vụ khai báo trong hợp đồng phải có dòng lúc trình. [SYS-US-02 bước 7, E7.1] |
| OQ-US01-02/03/05, OQ-US02-01 | §2, §4.1–4.2 và PAY-01 chưa nêu đủ phạm vi quyền, trường được sửa và mốc kiểm tra Active. | Dựa trên phân công hợp đồng để lập, sửa và trình. Sửa Draft giới hạn ở ghi chú và tải lại nguồn. Kiểm tra Active tại lúc lập, hợp đồng hết hiệu lực không được lập bù. [SYS-US-01 Actor, Mô tả, P2; SYS-US-02 §1.1 Actor] |
| OQ-US02-02, OQ-US03-05/06 | §4.2–4.3 chưa chỉ rõ kênh, xử lý gửi lỗi hay phạm vi bàn giao kế toán. | Gửi thông báo trong hệ thống và giữ kết quả đã lưu khi gửi lỗi. Gửi lại thông báo trình duyệt theo SYS-US-02b. Kết quả duyệt/từ chối gửi cho người tạo bảng. Việc chuyển sang kế toán thuộc ngoài phạm vi. [SYS-US-02 §1.1 A8/A10, §1.2; SYS-US-03 §1.1 Mô tả/A02] |
| OQ-US03-01/02/04 | §4.3 và PAY-06..08 chưa chi tiết phạm vi cấm tự xử lý, thay thế vai trò và giới hạn lý do. | Xử lý theo vai trò có thẩm quyền, người tạo Draft không tự duyệt/từ chối. Lý do từ chối tối đa 500 từ, được lưu để NVKD xem. [SYS-US-03 §1.1 Tiền điều kiện, bước 5–6, A01] |
| OQ-US05-01/02/03 | §4.5 chưa chỉ rõ quyền, lý do hủy và lập lại cùng kỳ. | **[QUYẾT ĐỊNH ĐÃ XÁC NHẬN]** Đại diện nhóm, 11/11/2026, xác nhận trong chat quyền hủy của NVKD phụ trách, lý do bắt buộc và lập bảng mới cùng kỳ. P-39 lưu câu trả lời. SYS-US-05 và 05 §14.1 vẫn ghi trạng thái OQ trước xác nhận. [SYS-US-05 P1–P4, S1–S5, AF2] |

### Chi tiết còn cần xác nhận

| ID và loại | Nguồn và câu hỏi | Phương án và ảnh hưởng | Trạng thái |
|---|---|---|---|
| OQ-D-02 · Thiếu | TA-SPEC §2, SYS-US-01 tiền điều kiện 3. Kỳ gồm trọn tháng dương lịch hay có thể bắt đầu giữa tháng? | Kỳ trọn tháng cho phép dùng `payment_period_claims`. Nếu kỳ có thể bắt đầu giữa tháng, cần kiểm tra giao nhau theo ngày. [05 §8, §14.2](05-data-design-v2.md#142-oq-mới-của-phần-dữ-liệu-oq-d-mã-tự-đặt--cần-chép-vào-01-requirements-summary-v2md) | Cần xác nhận. Giữ chỗ theo tháng **Blocked by OQ-D-02**. |
| OQ-D-03 · Thiếu | SYS-US-02 bước 6, SYS-US-03 bước 7. Nguồn sản lượng có dấu phiên bản hoặc thời điểm cập nhật theo bản ghi không? | Nếu có, so với `source_version` đã lưu. Nếu chỉ so sản lượng và trạng thái đối soát, có thể bỏ sót thay đổi khác. [05 §3.3, §7, §14.2](05-data-design-v2.md#7-dữ-liệu-tại-thời-điểm-tính-pay-03) | Cần xác nhận dữ liệu do module nguồn cung cấp. |
| OQ-US03-03 · Thiếu | TA-SPEC §4.1, §4.3, PAY-03/PAY-06. SYS-US-01 bước 10/14 và SYS-US-04 §1.1 bước 6. Thuế suất lần đầu lấy từ đâu, làm tròn tại bước nào và xử lý thế nào nếu trong kỳ có nhiều mức thuế? | **[QUYẾT ĐỊNH ĐÃ XÁC NHẬN]** Đại diện nhóm, 11/11/2026, xác nhận US-01 dùng quy tắc tính của US-04 (P-39). **[ĐỀ XUẤT KỸ THUẬT]** Lấy mức theo hợp đồng/kỳ và làm tròn thành tiền từng dòng cùng tiền GTGT như [kiến trúc §4](02-architecture-design-v2.md#4-đề-xuất-tính-gtgt-và-làm-tròn). Cách làm tròn ảnh hưởng tổng tiền và vai trò tại biên duyệt. | Cần xác nhận chi tiết. Công thức triển khai và dữ liệu nghiệm thu tiền **Blocked by OQ-US03-03**. |
| OQ-US01-01 · Mơ hồ | PAY-01/PAY-03, SYS-US-01 bước 9/14, SYS-US-02 bước 6, SYS-US-03 bước 7. Nếu đơn giá thay đổi trong chính bảng giá đã dùng mà bảng giá vẫn Active, có chặn trình/duyệt không? | V2 dùng giá tại lúc lưu và kiểm tra bảng giá vẫn Active. Một bảng giá đã được xác nhận và chuyển trạng thái active thì không thay đổi, có thay đổi bảng giá sẽ lập bảng giá mới và chờ đến ngày hiệu lực. Giá tiền trong bảng thanh toán ánh xạ tự bảng đơn giá được liên kết, khi bảng thanh toán chưa được duyệt, hệ thống phải tự ánh xạ về bảng đơn giá đang hiệu lực. Lựa chọn ảnh hưởng kiểm tra lại nguồn và tổng trình duyệt. | Đã xác nhận.  |
| OQ-US01-04 · Thiếu | PAY-02/PAY-04, SYS-US-01 bước 8, SYS-US-02 bước 7/E7.1. Cách xử lý một dịch vụ trong hợp đồng không có bản ghi sản lượng của kỳ? | V2 chặn trình khi thiếu dòng và yêu cầu có dữ liệu sản lượng đã đối soát khi lập. Khi dịch vụ có sản lượng hoặc đơn giá bằng 0, vẫn liệt kê vào bảng thanh toán với số tiền là 0, đảm bảo đầy đủ dịch vụ sử dụng. Điều này ảnh hưởng dữ liệu đầu vào và điều kiện đủ dòng. | Đã xác nhận. |
| OQ-US01-06 · Thiếu | TA-SPEC §6, SYS-US-01 Mô tả. Đo NFR-PAY-02 ở môi trường và với bộ dữ liệu đại diện nào? | Điểm đo và cách đếm đã có trong v2. Các chỉ số đo lường yêu cầu trong môi trường vận hành, điểm so tính từ khi người dụng nhấn nút "Lập bảng thanh toán". | Đã xác nhận.  |

## Thay đổi so với v1

| Vị trí | Thay đổi | Căn cứ |
|---|---|---|
| Lập, sửa và giữ kỳ | Vào từ chi tiết hợp đồng, hệ thống lấy giá Active, kiểm tra kỳ tháng/quý theo khoảng ngày, sửa ghi chú hoặc tải lại nguồn. | SYS-US-01 v2; OQ-01, OQ-US01-01/02. |
| Trình, duyệt và từ chối | Kiểm tra lại nguồn, thống nhất ngưỡng theo tổng đã lưu gồm GTGT, thêm gửi lại thông báo và thao tác mở lại `Rejected`. | SYS-US-02/02b, SYS-US-03/03b v2; OQ-02, OQ-04, OQ-05. |
| Điều chỉnh và hủy | Hồ sơ điều chỉnh có vòng đời riêng và chỉ có hiệu lực sau khi được duyệt. Hủy nháp có quyền theo phân công, lý do bắt buộc và cho phép lập bảng mới cùng kỳ. | SYS-US-04/04b, SYS-US-05 v2; OQ-03, OQ-US05-01/02/03, P-39. |
| Nghiệm thu | Dẫn theo mục/bước hiện hành. NFR lập bảng tính từ yêu cầu lưu đến khi trả kết quả, với số dòng sau gộp. | SYS-US-01 Mô tả, TA-SPEC §6. |
