# SYS-US-04 – Điều chỉnh bảng thanh toán đã duyệt (v2)

## 1. Use case

### 1.1. Lập hồ sơ điều chỉnh bảng thanh toán đã duyệt

| Mục | Đặc tả |
|---|---|
| Tên UC | Lập hồ sơ điều chỉnh bảng thanh toán đã duyệt |
| Use case ID | SYS-US-04 |
| Mô tả | Khi phát hiện sai sót sau khi duyệt, KTT lập hồ sơ điều chỉnh cho bảng Approved kèm biên bản xác nhận. Bảng Approved giữ nguyên, không bị sửa; hồ sơ điều chỉnh được lưu riêng, liên kết với bảng gốc, gồm biên bản và nội dung thay đổi. Biên bản hợp lệ khi có số biên bản, ngày lập, file đính kèm và xác nhận của hai bên. Nội dung được điều chỉnh gồm sản lượng và đơn giá của từng dòng, thêm hoặc bớt dòng; mỗi thay đổi bắt buộc có lý do. Số liệu sau điều chỉnh tính theo cùng quy tắc lập bảng (thành tiền, thuế GTGT theo thuế suất của bảng gốc, làm tròn lên theo đồng). Mỗi bảng chỉ có tối đa một hồ sơ chờ duyệt. Hồ sơ được lập ở trạng thái Chờ duyệt và được GĐKD xử lý theo SYS-US-04b (mục 1.2); số liệu hiệu lực chưa thay đổi. Mọi điều chỉnh đều ghi audit log. |
| Actor | KTT (lập hồ sơ điều chỉnh). |
| Độ ưu tiên | Trung bình |
| Trigger | KTT chọn “Điều chỉnh” trên bảng Approved và gửi nội dung điều chỉnh cùng biên bản. |
| Tiền điều kiện | 1. KTT đã đăng nhập, giữ vai trò KTT; bảng tồn tại và đang ở Approved.<br>2. Có biên bản hợp lệ: số biên bản, ngày lập, file đính kèm, xác nhận của hai bên.<br>3. Có ít nhất một thay đổi thuộc phạm vi (sửa sản lượng/đơn giá của dòng, thêm dòng, bớt dòng), mỗi thay đổi có lý do.<br>4. Bảng chưa có hồ sơ điều chỉnh nào đang chờ duyệt. |
| Hậu điều kiện | Lập hồ sơ thành công: hồ sơ điều chỉnh ở trạng thái Chờ duyệt, liên kết bảng gốc, lưu biên bản, các thay đổi (giá trị trước/sau, lý do), số liệu đề xuất sau điều chỉnh và người lập; có audit log. Bảng gốc vẫn Approved, số liệu không đổi.<br>Thất bại: không lưu dở dang hồ sơ hay audit; bảng gốc không đổi; hệ thống báo lý do. |
| Dòng cơ bản | 1. KTT chọn bảng Approved, nhập thông tin biên bản (số, ngày lập, xác nhận hai bên), đính kèm file biên bản, nhập các thay đổi và lý do từng thay đổi, gửi yêu cầu.<br>2. Hệ thống kiểm tra đăng nhập và vai trò KTT.<br>3. Hệ thống đọc bảng gốc cùng số liệu hiệu lực hiện tại và kiểm tra bảng đang ở Approved.<br>4. Hệ thống kiểm tra biên bản đủ số biên bản, ngày lập, file đính kèm và xác nhận của hai bên.<br>5. Hệ thống kiểm tra từng thay đổi: đúng loại (sửa, thêm, bớt dòng), dòng được sửa/bớt đang tồn tại, dòng thêm không trùng dịch vụ đã có, sản lượng và đơn giá không âm, có lý do.<br>6. Hệ thống tính số liệu đề xuất sau điều chỉnh: thành tiền từng dòng, tạm tính, thuế GTGT, tổng tiền.<br>7. Hệ thống lưu hồ sơ điều chỉnh ở trạng thái Chờ duyệt cùng các thay đổi, biên bản và ghi audit log trong cùng một giao dịch; không ghi vào bảng gốc.<br>8. Hệ thống báo KTT “Hồ sơ chờ GĐKD duyệt – số liệu hiệu lực chưa thay đổi”. Use case kết thúc. |
| Luồng thay thế | Không có. |
| Luồng ngoại lệ | 2a. Chưa đăng nhập: yêu cầu đăng nhập. Không phải KTT: từ chối.<br>3a. Bảng không tồn tại hoặc không ở Approved: từ chối, báo lý do.<br>4a. Thiếu biên bản hoặc biên bản thiếu số, ngày lập, file hoặc xác nhận hai bên: từ chối, báo trường còn thiếu.<br>5a. Không có thay đổi, thay đổi ngoài phạm vi (ví dụ đổi hợp đồng, kỳ, thuế suất), thiếu lý do, trỏ tới dòng không tồn tại hoặc giá trị âm: từ chối, báo thay đổi bị lỗi.<br>7a. Bảng đã có hồ sơ chờ duyệt (kể cả hai yêu cầu lập đồng thời): chỉ một hồ sơ được lưu, yêu cầu còn lại bị từ chối.<br>7b. Lỗi khi lưu hồ sơ, thay đổi hoặc audit log: hủy toàn bộ giao dịch, báo lỗi. |
| Ràng buộc chung | Mọi yêu cầu sửa trực tiếp bảng Approved (sửa, trình, hủy…): từ chối; điều chỉnh chỉ thực hiện qua hồ sơ điều chỉnh. |

### 1.2. Duyệt hoặc từ chối hồ sơ điều chỉnh

| Mục | Đặc tả |
|---|---|
| Tên UC | Duyệt hoặc từ chối hồ sơ điều chỉnh |
| Use case ID | SYS-US-04b |
| Mô tả | GĐKD xem hồ sơ điều chỉnh đang Chờ duyệt được lập theo SYS-US-04 (mục 1.1), cùng bảng gốc, biên bản, các thay đổi và số liệu đề xuất, rồi duyệt hoặc từ chối kèm lý do. Vì KTT là người lập hồ sơ nên không tự duyệt; mọi hồ sơ điều chỉnh do GĐKD duyệt, kể cả khi tổng sau điều chỉnh dưới 500.000.000 đ hoặc đi qua ngưỡng. Hồ sơ được duyệt chuyển sang Đã duyệt; hồ sơ bị từ chối chuyển sang Bị từ chối. Số liệu hiệu lực của bảng \= bảng gốc \+ các hồ sơ đã duyệt; kế toán chỉ dùng số liệu mới sau khi hồ sơ được duyệt. Mọi điều chỉnh đều ghi audit log. Bảng gốc vẫn Approved, số liệu gốc không đổi. |
| Actor | GĐKD (duyệt hoặc từ chối hồ sơ điều chỉnh). |
| Độ ưu tiên | Trung bình |
| Trigger | GĐKD chọn “Duyệt hồ sơ” hoặc “Từ chối hồ sơ” trên hồ sơ đang chờ duyệt. |
| Tiền điều kiện | 1. Hồ sơ tồn tại và đang Chờ duyệt; bảng gốc tồn tại và vẫn ở Approved.<br>2. GĐKD đã đăng nhập, giữ vai trò GĐKD.<br>3. Người thao tác không phải người lập hồ sơ.<br>4. Khi từ chối: có lý do không rỗng. |
| Hậu điều kiện | Duyệt hồ sơ thành công: hồ sơ ở trạng thái Đã duyệt, lưu người duyệt và thời điểm; có audit log; số liệu hiệu lực \= bảng gốc \+ các hồ sơ đã duyệt. Bảng gốc vẫn không đổi.<br>Từ chối thành công: hồ sơ ở trạng thái Bị từ chối, lý do được lưu và có audit log; số liệu hiệu lực không đổi; KTT có thể lập hồ sơ điều chỉnh mới.<br>Thất bại: không lưu dở dang kết quả xử lý hay audit; hồ sơ, bảng gốc và số liệu hiệu lực không đổi; hệ thống báo lý do. |
| Dòng cơ bản | 1. GĐKD mở hồ sơ chờ duyệt, xem bảng gốc, biên bản, các thay đổi, số liệu đề xuất và chọn “Duyệt hồ sơ”.<br>2. Hệ thống kiểm tra đăng nhập và vai trò GĐKD.<br>3. Hệ thống đọc hồ sơ và bảng gốc; kiểm tra hồ sơ đang chờ duyệt và bảng gốc vẫn Approved.<br>4. Hệ thống kiểm tra GĐKD không phải người lập hồ sơ.<br>5. Hệ thống chuyển hồ sơ sang Đã duyệt, ghi người duyệt, thời điểm và audit log (số liệu hiệu lực trước và sau) trong cùng một giao dịch.<br>6. Hệ thống hiển thị hồ sơ đã duyệt và số liệu hiệu lực mới. Use case kết thúc. |
| Luồng thay thế | R. GĐKD từ chối hồ sơ (rẽ từ bước 1): GĐKD chọn “Từ chối hồ sơ” và nhập lý do; hệ thống kiểm tra như bước 2–4 và lý do không rỗng; chuyển hồ sơ sang Bị từ chối, lưu lý do, ghi audit log; số liệu hiệu lực không đổi; KTT có thể lập hồ sơ điều chỉnh mới. |
| Luồng ngoại lệ | 2a. Chưa đăng nhập hoặc không phải GĐKD (kể cả KTT): từ chối duyệt hồ sơ.<br>3a. Hồ sơ không tồn tại hoặc không ở trạng thái chờ duyệt: từ chối.<br>4a. Người duyệt là người lập hồ sơ: từ chối.<br>5a. Hồ sơ vừa được xử lý bởi yêu cầu khác, hoặc lỗi khi lưu: hủy giao dịch, báo xung đột hoặc lỗi. |
