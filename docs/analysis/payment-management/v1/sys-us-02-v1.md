# SYS-US-02 – Trình duyệt (v1)

> Phiên bản: v1 · Ngày: 08/11/2026 · Người phụ trách: Chưa được chỉ định
> Đầu vào: [TA-SPEC](../../../requirements/payment-management/spec.md) §1–6; [OQ dùng chung](open-questions-v1.md); sys-us-03/04/05 cùng version.
> AI: Codex / GPT-6 · Prompt: P-15 (soạn ban đầu), P-16 (đối chiếu và bàn giao) trong [prompt-log](../../../workflow/prompt-log.md).
> Trạng thái: Bản lần chạy đầu – BA Pending Review
> Nhãn: [ĐẶC TẢ], [AC dẫn xuất], [ĐỀ XUẤT KỸ THUẬT], [GIẢ ĐỊNH – Cần xác nhận]. SYS/AC/OQ và NFR là mã nội bộ, không phải mã mới của đề.

Nguồn đã đọc: toàn bộ TA-SPEC và các đầu vào Markdown trên. PDF đính kèm và TA-PDF cục bộ có SHA-256 giống nhau; chưa đọc trực tiếp nội dung PDF do môi trường thiếu `pypdf`. Dẫn trang theo sổ nguồn: §2–3 tr.1, §4–5 tr.2, §6 tr.3. Chỉ thực hiện phân tích US-PAY-02; không thiết kế API, lớp hay dữ liệu. Các đề xuất trong US-PAY-03/OQ dùng chung chưa phải quyết định nghiệp vụ được xác nhận.

## 1. Use case

### 1.1. Căn cứ

- [ĐẶC TẢ] US-PAY-02: NVKD chọn “Trình duyệt”; kiểm tra PAY-04, nếu đạt chuyển `PendingApproval` và thông báo người duyệt. [TA-SPEC §4.2; TA-PDF tr.2]
- [ĐẶC TẢ] PAY-04: chặn tổng tiền âm hoặc thiếu dòng dịch vụ bắt buộc; chống trình duyệt trùng. [TA-SPEC §5 PAY-04; TA-PDF tr.2]
- [ĐẶC TẢ] Luồng chính `Draft` → `PendingApproval` → `Approved`; NVKD lập và trình duyệt. [TA-SPEC §2–3; TA-PDF tr.1]
- [ĐẶC TẢ] §4.3 giao GĐKD duyệt từ 500 triệu trở lên; PAY-06 giao GĐKD duyệt trên 500 triệu, còn lại KTT. Không chọn một phía tại đúng ngưỡng. [TA-SPEC §4.3, §5 PAY-06; TA-PDF tr.2]
- [ĐẶC TẢ] PAY-07 cấm người lập tự duyệt; đây là kiểm soát của US-PAY-03, không phải căn cứ cấm người lập trình duyệt. PAY-08 cho trình lại sau từ chối nhưng đích trạng thái còn mâu thuẫn với §3. [TA-SPEC §3, §5 PAY-07..08; TA-PDF tr.1–2]

### 1.2. Đặc tả tương tác

| Mục | Đặc tả |
|---|---|
| Tên | SYS-US-02 – Trình duyệt. [ĐẶC TẢ] [TA-SPEC §4.2; TA-PDF tr.2] |
| Tác nhân chính | NVKD. Phạm vi bảng một NVKD được trình chưa rõ: Blocked by OQ-US02-01. [ĐẶC TẢ] [TA-SPEC §2, §4.2; TA-PDF tr.1–2] |
| Tác nhân liên quan | KTT hoặc GĐKD nhận thông báo theo thẩm quyền; đúng 500 triệu: Blocked by OQ-02; cách chọn cá nhân: Blocked by OQ-US03-02. [AC dẫn xuất] [TA-SPEC §4.2–4.3, PAY-06; TA-PDF tr.2] |
| Mục tiêu | Đưa bảng hợp lệ vào chờ duyệt và thông báo người duyệt. [ĐẶC TẢ] [TA-SPEC §4.2; TA-PDF tr.2] |
| Kích hoạt | NVKD chọn “Trình duyệt” cho bảng. [ĐẶC TẢ] [TA-SPEC §4.2; TA-PDF tr.2] |
| Tiền điều kiện | P1: Người gửi là NVKD; phạm vi quyền theo OQ-US02-01. P2: Bảng tồn tại và ở `Draft` theo luồng chính. P3: Tổng không âm, đủ dòng bắt buộc, chưa có lần trình trùng; định nghĩa đủ dòng: Blocked by OQ-05. Đây là các điều kiện hệ thống phải kiểm tra, không mặc nhiên tin đầu vào. [AC dẫn xuất] [TA-SPEC §2–3, §4.2, PAY-04; TA-PDF tr.1–2] |
| Hậu điều kiện thành công | Bảng chuyển `Draft` → `PendingApproval`; ghi audit ai, lúc nào, thay đổi gì; gửi thông báo người duyệt. Hoàn thiện người nhận/kênh và lỗi gửi: Blocked by OQ-02, OQ-US03-02, OQ-US02-02. [ĐẶC TẢ] [TA-SPEC §3, §4.2–4.3, PAY-06, §6; TA-PDF tr.1–3] |
| Hậu điều kiện thất bại | Yêu cầu bị chặn không tạo chuyển trạng thái mới. Với lỗi lưu/audit, đề xuất không lưu dở dang; với xung đột giữ kết quả hợp lệ của yêu cầu đã thắng. Lỗi thông báo chưa chốt kết quả toàn thao tác: Blocked by OQ-US02-02. [AC dẫn xuất / ĐỀ XUẤT KỸ THUẬT] [TA-SPEC §4.2, PAY-04, §6; TA-PDF tr.2–3] |
| Yêu cầu phi chức năng | NFR-PAY-01 áp dụng: audit mọi thay đổi trạng thái, đủ ai/lúc nào/thay đổi gì. NFR-PAY-02 không áp dụng cho trình duyệt: đề chỉ yêu cầu lập bảng ≤3 giây với hợp đồng có <200 dòng. Không đặt SLA mới. [ĐẶC TẢ] [TA-SPEC §6; TA-PDF tr.3] |

### 1.3. Dòng cơ bản

Luồng có điều kiện dưới đây chỉ hoàn chỉnh khi các OQ liên quan được xác nhận; không phải quy trình đã duyệt.

| Bước | Tương tác và kết quả | Căn cứ |
|---|---|---|
| 1 | NVKD gửi yêu cầu trình duyệt, xác định bảng cần trình. | [ĐẶC TẢ] TA-SPEC §4.2; TA-PDF tr.2 |
| 2 | Hệ thống nhận diện người gửi, kiểm tra vai trò NVKD và quyền trên bảng. Phạm vi quyền: Blocked by OQ-US02-01. | [AC dẫn xuất] TA-SPEC §2, §4.2; TA-PDF tr.1–2 |
| 3 | Hệ thống đọc bảng và kiểm tra đang `Draft`; phát hiện yêu cầu trùng. | [AC dẫn xuất] TA-SPEC §3, §4.2, PAY-04; TA-PDF tr.1–2 |
| 4 | Hệ thống kiểm tra tổng tiền không âm và đủ dòng dịch vụ bắt buộc; tiêu chí đủ dòng: Blocked by OQ-05. Không tự coi tổng bằng 0 là lỗi. | [ĐẶC TẢ / AC dẫn xuất] TA-SPEC PAY-04; TA-PDF tr.2 |
| 5 | Xác định người nhận thông báo: dưới 500 triệu là KTT, trên 500 triệu là GĐKD. Đúng 500 triệu: Blocked by OQ-02. Cách ánh xạ vai trò sang người nhận: Blocked by OQ-US03-02; cách xác định tổng so ngưỡng: Blocked by OQ-US03-03. | [AC dẫn xuất] TA-SPEC §4.2–4.3, PAY-06; TA-PDF tr.2 |
| 6 | Lưu chuyển `Draft` → `PendingApproval`, đồng thời ghi audit người thao tác, thời điểm, trạng thái trước/sau; bảo vệ chống hai lần trình thành công cho cùng một lần chuyển. | [ĐẶC TẢ] TA-SPEC §3, §4.2, PAY-04, §6; TA-PDF tr.1–3. Cơ chế nguyên tử là đề xuất ở §1.5. |
| 7 | Gửi thông báo cho người duyệt. Kênh, nội dung và xử lý gửi lỗi: Blocked by OQ-US02-02. | [ĐẶC TẢ] TA-SPEC §4.2; TA-PDF tr.2 |
| 8 | Trả kết quả trình duyệt cho NVKD, phản ánh đúng kết quả lưu và gửi thông báo; không báo hoàn tất thông báo khi gửi lỗi. Chi tiết kết quả khi gửi lỗi: Blocked by OQ-US02-02. | [ĐỀ XUẤT KỸ THUẬT] TA-SPEC §4.2; TA-PDF tr.2 |

### 1.4. Dòng thay thế

| Nhánh | Xử lý | Căn cứ |
|---|---|---|
| A2 | Không nhận diện được người gửi hoặc không phải NVKD: từ chối; không chuyển trạng thái. Quyền trên từng bảng chờ OQ-US02-01. | [AC dẫn xuất / ĐỀ XUẤT KỸ THUẬT] TA-SPEC §2, §4.2; TA-PDF tr.1–2 |
| A3 | Không tìm thấy bảng: báo không tìm thấy, dừng. | [ĐỀ XUẤT KỸ THUẬT] TA-SPEC §4.2; TA-PDF tr.2 |
| A3.1 | `PendingApproval`, `Approved`, `Cancelled`: không trình lại; `Cancelled` không dùng lại. Với `Rejected`, chưa đặc tả thao tác chuyển khi trình: Blocked by OQ-04, OQ-US03-07; không coi việc chặn vĩnh viễn hay tự chuyển là quy tắc đã chốt. Bảng đã về `Draft` hợp lệ có thể trình lại theo PAY-08. | [AC dẫn xuất] TA-SPEC §3, §4.5, PAY-05, PAY-08; TA-PDF tr.1–2 |
| A4 | Tổng âm: chặn, giữ `Draft`, báo lý do. Tổng 0 không bị chặn chỉ vì bằng 0. | [ĐẶC TẢ / AC dẫn xuất] TA-SPEC PAY-04; TA-PDF tr.2 |
| A4.1 | Thiếu dòng bắt buộc: chặn và yêu cầu bổ sung; danh sách và tiêu chí thiếu: Blocked by OQ-05. | [ĐẶC TẢ] TA-SPEC PAY-04; TA-PDF tr.2 |
| A5 | Chưa có quyết định về đúng 500 triệu hoặc chưa xác định được người nhận: phần này Blocked by OQ-02, OQ-US03-02, OQ-US03-03; không tự gán người nhận hay chốt chính sách lỗi. | [GIẢ ĐỊNH – Cần xác nhận] TA-SPEC §4.2–4.3, PAY-06; TA-PDF tr.2 |
| A6 | Nhấn lặp/gửi lại hoặc hai yêu cầu đồng thời: không tạo hai lần chuyển trạng thái; đề xuất yêu cầu thua nhận kết quả trùng/xung đột, không ghi thêm audit chuyển trạng thái không xảy ra. Nếu bảng đã bị hủy hoặc thay đổi trước khi lưu, không ghi đè kết quả đó. | [AC dẫn xuất / ĐỀ XUẤT KỸ THUẬT] TA-SPEC §3, PAY-04, §6; TA-PDF tr.1–3 |
| A6.1 | Lỗi lưu trạng thái hoặc ghi audit: đề xuất hoàn tác phần ghi của yêu cầu, báo thất bại; không gửi thông báo thành công. | [ĐỀ XUẤT KỸ THUẬT] TA-SPEC §4.2, §6; TA-PDF tr.2–3 |
| A7 | Gửi thông báo thất bại: không tuyên bố đã gửi; trạng thái cuối, thử lại và kết quả trả về: Blocked by OQ-US02-02. | [GIẢ ĐỊNH – Cần xác nhận] TA-SPEC §4.2; TA-PDF tr.2 |

### 1.5. Đề xuất kỹ thuật để design xem xét

[ĐỀ XUẤT KỸ THUẬT] Với PAY-04 và NFR-PAY-01, cân nhắc cập nhật có điều kiện trạng thái hiện tại và lưu trạng thái/audit trong một giao dịch. Mục đích: tránh trình trùng và chuyển trạng thái thiếu audit. Thay thế: khóa khi xử lý hoặc kiểm soát phiên bản; design chọn theo nền tảng thực tế. Lý do: kiểm tra trước rồi ghi riêng có thể bị hai yêu cầu cùng vượt qua. Tác động: một yêu cầu thắng, yêu cầu còn lại không tạo chuyển trạng thái mới; không đặt thêm điều kiện nghiệp vụ. Không bắt buộc Idempotency-Key hoặc chốt schema ở tài liệu BA. [TA-SPEC PAY-04, §6; TA-PDF tr.2–3]

## 2. Điểm cần xác nhận

Các đề xuất có sẵn của nhóm vẫn cần xác nhận; không sử dụng chữ “không còn” trong bảng chung như bằng chứng đóng OQ.

| ID | Vị trí mọi nguồn | Loại | Mô tả | Lý do cần xác nhận | Lựa chọn | Ảnh hưởng | Trạng thái | Người/ngày/câu trả lời và tham chiếu |
|---|---|---|---|---|---|---|---|---|
| OQ-02 | TA-SPEC §4.3 “từ 500 triệu” ↔ PAY-06 “trên 500 triệu”; TA-PDF tr.2 | Mâu thuẫn | Ai duyệt đúng 500.000.000 đồng? | Không xác định chắc người nhận | KTT / GĐKD | Bước 5, A5 | Cần xác nhận | Đan Anh đề xuất GĐKD, chưa có xác nhận khách hàng; bảng OQ v1 |
| OQ-05 | TA-SPEC PAY-04 “thiếu dòng dịch vụ bắt buộc”; TA-PDF tr.2 | Thiếu | Danh sách dòng bắt buộc và tiêu chí xác định thiếu? | Không đủ căn cứ validation | Cần người phụ trách cung cấp danh sách/quy tắc | P3, bước 4, A4.1 | Cần xác nhận | Chưa có |
| OQ-US02-01 | TA-SPEC §2, §4.2 “NVKD”; TA-PDF tr.1–2 | Mơ hồ | NVKD được trình bảng nào? | Vai trò chưa xác định quyền trên từng bảng | Chỉ bảng mình lập / phạm vi được phân công / mọi bảng; cần xác nhận | P1, bước 2, A2 | Cần xác nhận | Chưa có |
| OQ-US02-02 | TA-SPEC §4.2 “gửi thông báo cho người duyệt”; TA-PDF tr.2 | Thiếu | Kênh/nội dung thông báo, gửi lỗi thì trạng thái và kết quả trình ra sao? | Tránh tự chốt thành công khi chưa gửi hoặc phát sinh gửi trùng | Giữ trạng thái chờ và gửi lại / hoàn tác trình; cần xác nhận kênh và cách xử lý | Bước 7–8, A7, hậu điều kiện | Cần xác nhận | Chưa có; OQ-US03-05 nói thông báo kết quả duyệt, không thay câu hỏi này |
| OQ-US03-02 | TA-SPEC §2, §4.3, PAY-06; TA-PDF tr.1–2 | Mơ hồ | Chọn cá nhân hay nhóm theo vai trò, có thay thế chéo? | Cần người nhận thực tế | Theo vai trò / cá nhân được phân công | Bước 5, A5 | Cần xác nhận | Tái sử dụng OQ v1; đề xuất nhóm chưa được khách hàng xác nhận |
| OQ-US03-03 | TA-SPEC §4.1, §4.3, PAY-03, PAY-06; TA-PDF tr.2 | Thiếu | Cơ sở tổng tiền so ngưỡng, thời điểm, làm tròn/thuế chưa rõ | Có thể đổi người nhận tại biên | Cần xác nhận cơ sở tổng; không tự thêm VAT | Bước 5, A5 | Cần xác nhận | Tái sử dụng OQ v1; đề xuất nhóm chưa được khách hàng xác nhận |
| OQ-04 | TA-SPEC §3 “Rejected” ↔ PAY-08 “quay về Draft”; TA-PDF tr.1–2 | Mâu thuẫn | Đích sau từ chối? | Quyết định tiền điều kiện trình lại | Draft / Rejected rồi Draft | A3.1 | Cần xác nhận | Tái sử dụng OQ v1; chưa xác nhận khách hàng |
| OQ-US03-07 | TA-SPEC §3, PAY-08; TA-PDF tr.1–2 | Thiếu | Nếu qua Rejected thì ai/khi nào đưa về Draft? | Chưa đủ căn cứ luồng trình lại | Tự động / thao tác NVKD, cần xác nhận | A3.1 | Cần xác nhận | Tái sử dụng OQ v1; chưa xác nhận khách hàng |

## 3. Acceptance criteria

Mã AC-US02-kk tự đặt. Các tiêu chí kỹ thuật là đề xuất cần design đánh giá; các tiêu chí phụ thuộc OQ chưa thể coi là hoàn tất.

| ID | Given / When / Then | Nhãn | Nguồn | OQ |
|---|---|---|---|---|
| AC-US02-01 | Given NVKD có quyền, bảng Draft hợp lệ và xác định được người nhận; When trình duyệt (bước 1–8); Then chuyển PendingApproval, audit đủ ai/lúc nào/thay đổi gì và thông báo người duyệt. | [AC dẫn xuất] | TA-SPEC §2–4.3, PAY-04, PAY-06, §6; TA-PDF tr.1–3 | Blocked by OQ-05, OQ-02, OQ-US02-01, OQ-US02-02, OQ-US03-02, OQ-US03-03 |
| AC-US02-02 | Given tổng âm; When trình; Then chặn, giữ Draft (A4). | [ĐẶC TẢ] | TA-SPEC PAY-04; TA-PDF tr.2 | — |
| AC-US02-03 | Given tổng bằng 0 và các điều kiện khác đạt; When kiểm tra tổng; Then không chặn chỉ vì tổng bằng 0 (bước 4/A4). | [AC dẫn xuất] | TA-SPEC PAY-04; TA-PDF tr.2 | — |
| AC-US02-04 | Given thiếu dòng bắt buộc theo quy tắc đã xác nhận; When trình; Then chặn và giữ Draft (A4.1). | [AC dẫn xuất] | TA-SPEC PAY-04; TA-PDF tr.2 | Blocked by OQ-05 |
| AC-US02-05 | Given yêu cầu lặp/đồng thời cho cùng lần trình; When xử lý; Then không có hai lần chuyển Draft → PendingApproval; không ghi audit chuyển trạng thái giả (A6). | [AC dẫn xuất] | TA-SPEC PAY-04, §6; TA-PDF tr.2–3 | — |
| AC-US02-06 | Given người gửi không phải NVKD hoặc không có quyền đã xác nhận; When trình; Then từ chối, không đổi trạng thái (A2). | [AC dẫn xuất] | TA-SPEC §2, §4.2; TA-PDF tr.1–2 | Blocked by OQ-US02-01 đối với quyền trên bảng |
| AC-US02-07 | Given bảng không tồn tại; When trình; Then báo không tìm thấy, không lưu chuyển trạng thái (A3). | [ĐỀ XUẤT KỸ THUẬT] | TA-SPEC §4.2; TA-PDF tr.2 | — |
| AC-US02-08 | Given bảng PendingApproval, Approved hoặc Cancelled; When trình; Then không tạo lần trình mới (A3.1). | [AC dẫn xuất] | TA-SPEC §3, §4.5, PAY-04..05; TA-PDF tr.1–2 | — |
| AC-US02-09 | Given bảng đã từ chối; When NVKD trình lại; Then chỉ áp dụng luồng đã xác nhận về trở về Draft, không tự bỏ qua Rejected (A3.1). | [AC dẫn xuất] | TA-SPEC §3, PAY-08; TA-PDF tr.1–2 | Blocked by OQ-04, OQ-US03-07 |
| AC-US02-10 | Given tổng dưới/trên/đúng 500 triệu; When xác định người nhận; Then dưới gửi KTT, trên gửi GĐKD; đúng ngưỡng theo xác nhận, không tự chọn (bước 5/A5). | [AC dẫn xuất] | TA-SPEC §4.2–4.3, PAY-06; TA-PDF tr.2 | Blocked by OQ-02, OQ-US03-02, OQ-US03-03 |
| AC-US02-11 | Given lỗi lưu trạng thái hoặc audit; When thực hiện bước 6; Then theo đề xuất nguyên tử, không lưu chuyển trạng thái dở dang, không gửi thông báo thành công (A6.1). | [ĐỀ XUẤT KỸ THUẬT] | TA-SPEC §4.2, §6; TA-PDF tr.2–3 | — |
| AC-US02-12 | Given đã xử lý trạng thái nhưng gửi thông báo lỗi; When trả kết quả; Then không tuyên bố đã gửi, xử lý trạng thái/thử lại theo xác nhận (A7, bước 8). | [AC dẫn xuất] | TA-SPEC §4.2; TA-PDF tr.2 | Blocked by OQ-US02-02 |
| AC-US02-13 | Given trạng thái bị thao tác khác đổi trước lúc lưu; When trình; Then không ghi đè trạng thái mới, không tạo chuyển trái luồng (A6). | [ĐỀ XUẤT KỸ THUẬT] | TA-SPEC §3, PAY-04, §6; TA-PDF tr.1–3 | — |

## Minh chứng và bàn giao

- Prompt thực tế (08/11/2026): “hãy viết phần sys-us-02 theo bài tập này cho tôi vào thư mục v1 của project”. File đính kèm: `C:/Users/PC/Downloads/BAITAP_TA_1-2.pdf`.
- Công cụ: Codex / GPT-6, PowerShell `Get-Content`, `Get-FileHash`, công cụ ghi patch; skill sys-spec và naming-versioning. Không chạy ứng dụng, không đo hiệu năng, không phê duyệt nghiệp vụ.
- SHA-256 hai PDF: `BC8B34CC847343151A496C2A515A7178BF90A834D5BEE909BDDCF56179BD218E`. Đọc PDF bằng Python thất bại: `ModuleNotFoundError: pypdf`; đã dùng TA-SPEC, không tuyên bố đã đọc PDF.
- AI soạn toàn bộ file này; chưa có phần nhóm sửa. Minh chứng lần soạn đầu được bổ sung vào nhật ký chung ở P-15; lần đối chiếu và thiết kế ghi ở P-16 theo yêu cầu người dùng.
- Bàn giao design: dùng file này cùng OQ v1; các OQ mở và AC bị chặn giữ nguyên đến khi có người/ngày/tham chiếu xác nhận. Không truyền đề xuất nhóm như quy tắc đã duyệt.
- Kiểm chứng: `python scripts/verify_agent_config.py` lỗi mã hóa console; chạy lại `python -X utf8 scripts/verify_agent_config.py` → PASS (0 failed checks). Kiểm tra này xác minh cấu hình/tên file, không thay thế review nội dung.
- Đối chiếu 08/11/2026 (P-16): không có `ai-review-01-v1.md`; báo cáo `ai-review-us-05-v1.md` chỉ review US-PAY-05, không có US-PAY-02 trong phạm vi review. Tiếp tục v1 cho US-PAY-02, không sửa các bản đã review của US-PAY-05. OQ-05, OQ-US02-01, OQ-US02-02 được đồng bộ vào bảng chung; các ID phụ thuộc US-PAY-03 giữ nguyên, chưa có xác nhận nghiệp vụ. PAY-01..03 là điều kiện lập/tính bảng ở US-PAY-01, không tự bổ sung thành điều kiện tái kiểm tra khi trình. PAY-07 thuộc thao tác duyệt.
