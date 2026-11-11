# SYS-US-03 – Duyệt hoặc từ chối bảng thanh toán (v2)

## 1. Use case

### 1.1. Duyệt hoặc từ chối bảng thanh toán

| Mục | Đặc tả |
|---|---|
| Tên UC | Duyệt hoặc từ chối bảng thanh toán |
| Use case ID | SYS-US-03 |
| Mô tả | Người duyệt có thẩm quyền xem bảng đang PendingApproval và duyệt (bảng chuyển sang Approved) hoặc từ chối kèm lý do (bảng chuyển sang Rejected). Thẩm quyền theo vai trò dựa trên tổng tiền đã lưu tại thời điểm lập (đã gồm thuế GTGT): từ 500.000.000 đ trở lên do GĐKD duyệt, dưới mức đó do KTT duyệt; không vai trò nào duyệt thay. Người lập bảng không được duyệt hay từ chối bảng do chính mình lập. Khi duyệt, hệ thống kiểm tra lại dữ liệu nguồn. Lý do từ chối bắt buộc, tối đa 500 từ, được lưu cùng bảng và NVKD xem được. Sau khi duyệt hoặc từ chối, NVKD đã tạo bảng nhận thông báo trong hệ thống (thông báo từ chối kèm lý do). Bảng bị từ chối ở trạng thái Rejected và chỉ về Draft khi NVKD bấm “Chỉnh sửa” (use case SYS-US-03b, mục 1.2). Mọi chuyển trạng thái đều ghi audit log. Việc chuyển bảng Approved sang kế toán nằm ngoài phạm vi module. |
| Actor | KTT hoặc GĐKD (người duyệt theo thẩm quyền). |
| Độ ưu tiên | Cao |
| Trigger | Người duyệt chọn “Duyệt” hoặc “Từ chối” trên bảng PendingApproval. |
| Tiền điều kiện | 1. Bảng tồn tại và đang ở PendingApproval.<br>2. Người thao tác đã đăng nhập, giữ vai trò KTT hoặc GĐKD đúng với tổng tiền của bảng (mỗi người dùng chỉ một vai trò).<br>3. Người thao tác không phải người lập bảng (người tạo bảng ở Draft).<br>4. Khi duyệt: dữ liệu nguồn vẫn đạt điều kiện (hợp đồng Active, bảng giá đã dùng còn Active, bản ghi sản lượng nguồn vẫn đã đối soát và không thay đổi).<br>5. Khi từ chối: có lý do không rỗng, không quá 500 từ. |
| Hậu điều kiện | Duyệt thành công: bảng ở Approved và không được sửa; có audit log (ai, lúc nào, PendingApproval → Approved); NVKD đã tạo bảng nhận thông báo.<br>Từ chối thành công: bảng ở Rejected, lý do được lưu cùng bảng; có audit log kèm lý do; NVKD đã tạo bảng nhận thông báo kèm lý do; hệ thống không tự chuyển bảng về Draft.<br>Thất bại: trạng thái và dữ liệu giữ nguyên, không ghi audit; lỗi gửi thông báo không hoàn tác kết quả đã lưu. |
| Dòng cơ bản | 1. Người duyệt chọn “Duyệt” trên bảng PendingApproval.<br>2. Hệ thống kiểm tra đăng nhập và vai trò KTT hoặc GĐKD.<br>3. Hệ thống đọc bảng thanh toán.<br>4. Hệ thống kiểm tra bảng đang ở PendingApproval.<br>5. Hệ thống xác định vai trò duyệt từ tổng tiền đã lưu (từ 500.000.000 đ trở lên là GĐKD, dưới mức đó là KTT) và kiểm tra khớp với vai trò người duyệt.<br>6. Hệ thống kiểm tra người duyệt không phải người lập bảng.<br>7. Hệ thống đọc lại và kiểm tra dữ liệu nguồn (hợp đồng, bảng giá, sản lượng).<br>8. Hệ thống chuyển bảng sang Approved và ghi audit log trong cùng một giao dịch.<br>9. Hệ thống gửi thông báo trong hệ thống cho NVKD đã tạo bảng: “Bảng đã được duyệt”.<br>10. Hệ thống báo người duyệt duyệt thành công. Use case kết thúc. |
| Luồng thay thế | R. Từ chối bảng (rẽ từ bước 1):<br>R1. Người duyệt chọn “Từ chối” và nhập lý do.<br>R2–R6. Hệ thống kiểm tra như bước 2–6 (người lập cũng không được từ chối bảng của mình).<br>R7. Hệ thống kiểm tra lý do không rỗng (chỉ khoảng trắng coi là rỗng) và không quá 500 từ; không kiểm tra lại dữ liệu nguồn.<br>R8. Hệ thống chuyển bảng sang Rejected, lưu lý do cùng bảng và ghi audit log kèm lý do trong cùng một giao dịch.<br>R9. Hệ thống gửi thông báo trong hệ thống kèm lý do cho NVKD đã tạo bảng.<br>R10. Hệ thống báo từ chối thành công.<br>9a. Gửi thông báo kết quả thất bại: kết quả duyệt/từ chối vẫn giữ nguyên, hệ thống báo thông báo chưa gửi được. |
| Luồng ngoại lệ | 2a. Chưa đăng nhập: yêu cầu đăng nhập. Không có vai trò KTT hoặc GĐKD: từ chối.<br>3a. Không tìm thấy bảng hoặc lỗi đọc dữ liệu: báo lỗi.<br>4a. Bảng không ở PendingApproval (kể cả đã được người khác xử lý trước): từ chối, không thay đổi dữ liệu.<br>5a. Sai vai trò theo tổng tiền (KTT với bảng từ 500.000.000 đ trở lên; GĐKD với bảng dưới 500.000.000 đ): từ chối.<br>6a. Người thao tác là người lập bảng: từ chối, áp dụng cho cả duyệt và từ chối.<br>7a. Khi duyệt, dữ liệu nguồn không còn đạt hoặc lỗi đọc nguồn: chặn duyệt, bảng giữ PendingApproval; người duyệt có thể từ chối để NVKD tải lại dữ liệu nguồn.<br>R7a. Lý do từ chối rỗng: yêu cầu nhập lý do, bảng giữ PendingApproval.<br>R7b. Lý do từ chối quá 500 từ: từ chối, bảng giữ PendingApproval.<br>8a. Lỗi khi lưu trạng thái hoặc audit log: hủy giao dịch, bảng giữ PendingApproval, báo lỗi, không gửi thông báo.<br>8b. Hai yêu cầu duyệt/từ chối đồng thời trên cùng bảng: chỉ một yêu cầu thành công, yêu cầu còn lại bị từ chối với thông báo xung đột.<br>8c. Không xác định được kết quả lưu: báo chưa xác định, người duyệt xem lại trạng thái bảng. |

### 1.2. Chỉnh sửa bảng thanh toán bị từ chối

| Mục | Đặc tả |
|---|---|
| Tên UC | Chỉnh sửa bảng thanh toán bị từ chối |
| Use case ID | SYS-US-03b |
| Mô tả | NVKD được phân công phụ trách hợp đồng mở bảng Rejected, xem lý do từ chối và bấm “Chỉnh sửa” để đưa bảng về Draft. Lý do từ chối được giữ lại để tham chiếu. Hệ thống không tự chuyển bảng Rejected về Draft. Việc chuyển trạng thái ghi audit log. Sau khi bảng về Draft, NVKD sửa theo SYS-US-01 và trình lại theo SYS-US-02. |
| Actor | NVKD được phân công phụ trách hợp đồng. |
| Độ ưu tiên | Cao |
| Trigger | NVKD chọn “Chỉnh sửa” trên bảng Rejected. |
| Tiền điều kiện | 1. Bảng tồn tại và đang ở Rejected (đã bị từ chối theo SYS-US-03).<br>2. Người thao tác đã đăng nhập, giữ vai trò NVKD và được phân công phụ trách hợp đồng của bảng. |
| Hậu điều kiện | Thành công: bảng chuyển từ Rejected về Draft, lý do từ chối được giữ để tham chiếu; có audit log.<br>Thất bại: trạng thái và dữ liệu giữ nguyên, không ghi audit. |
| Dòng cơ bản | 1. NVKD mở bảng Rejected, xem lý do từ chối và bấm “Chỉnh sửa”.<br>2. Hệ thống kiểm tra vai trò NVKD, NVKD được phân công hợp đồng và bảng đang ở Rejected.<br>3. Hệ thống chuyển bảng từ Rejected về Draft (giữ lý do từ chối để tham chiếu) và ghi audit log trong cùng một giao dịch.<br>4. Hệ thống mở biểu mẫu sửa bảng Draft (SYS-US-01); sau khi sửa, NVKD trình lại bảng thanh toán. Use case kết thúc. |
| Luồng thay thế | Không có. |
| Luồng ngoại lệ | 2a. Chưa đăng nhập, không phải NVKD, không được phân công hợp đồng hoặc không tìm thấy bảng: từ chối.<br>2b. Bảng không ở Rejected: từ chối (bảng Draft được sửa trực tiếp theo SYS-US-01).<br>3a. Bảng vừa bị thay đổi, lỗi khi lưu hoặc ghi audit log: hủy giao dịch, báo lỗi. |
