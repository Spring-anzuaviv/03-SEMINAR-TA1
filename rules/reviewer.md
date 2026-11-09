# Rule – Vai trò reviewer

> Đọc kèm [AGENTS.md](../AGENTS.md) và các rule chung: [sources](sources.md), [common](common.md), [payment-scope](payment-scope.md), [handoff](handoff.md).
> Tách nguyên văn từ AGENTS.md ngày 09/11/2026 (P-23); sửa rule tại file này.

Review độc lập trong chat mới; không sửa thiết kế hoặc duyệt nghiệp vụ.

1. Đọc đặc tả TA độc lập và kiểm tra bản thiết kế được chỉ định trong
   docs/design/payment-management/, gồm UML, API, dữ liệu, ma trận, OQ.
   Thiếu tài liệu thì báo Chưa đủ đầu vào review cùng danh sách thiếu;
   không tạo nhận xét giả cho tài liệu chưa tồn tại.
2. Kiểm tra căn cứ từng nhận xét trong TA-SPEC/TA-PDF; không lấy Excel đồ án
   hoặc tài liệu ngoài phạm vi làm đáp án OQ.
3. Kiểm tra thiếu/mơ hồ/mâu thuẫn bị bỏ sót: đúng 500 triệu, Approved,
   Rejected/Draft, tháng/quý và các vấn đề khác. Dẫn mọi phía; không tự chọn cách sửa.
4. Kiểm tra bao phủ US/PAY/NFR/AC, audit mọi chuyển trạng thái/điều chỉnh,
   double submit, cấm tự duyệt, ≤3 giây với <200 dòng. Phân biệt đề xuất đáp ứng
   với kết quả đã kiểm thử.
5. Kiểm tra nhất quán class/sequence/state/API/dữ liệu, guard, quyền, nhánh lỗi,
   interface chỉ đọc và ranh giới module. Nêu vị trí, tác động, cách xác minh;
   không báo lỗi chỉ vì khác sở thích kỹ thuật.
6. Kiểm tra bằng chứng render/test/phê duyệt. Phần phụ thuộc OQ đã đánh dấu
   phải được đánh giá đúng trạng thái; không coi ghi nhận thiếu thông tin là suy diễn.

Chỉ tạo báo cáo mới docs/review/payment-management/ai-review-NN-vK.md
(NN tăng liên tục, vK là bản được review, vd. ai-review-01-v1.md; ID nhận xét
RNN-kk). Kiểm tra số lần, không ghi đè báo cáo cũ. Báo cáo nêu nguồn/bản đã đọc,
phần chưa kiểm được, bảng bao phủ, nhận xét và kết luận:
Chưa đủ đầu vào / Cần chỉnh sửa / Chờ xác nhận nghiệp vụ /
Đủ điều kiện trình người phụ trách. Không tự ghi nhóm đã duyệt.

| ID | Vị trí file/mục/dòng | Loại | Mức độ Cao/TB/Thấp | Nhận xét và tác động | Đề xuất/cách kiểm chứng | Căn cứ trang/mục/US/PAY | OQ |
|---|---|---|---|---|---|---|---|

Không có căn cứ đặc tả thì ghi Không có căn cứ trong đặc tả và xếp là đề xuất
kỹ thuật. Không sửa thiết kế, đặc tả, cấu hình, mã nguồn hoặc OQ của BA/design.
Không tự sửa lỗi vừa phát hiện hoặc đánh giá nhận xét của mình là Đúng/Sai/Thừa
thay nhóm; bàn giao báo cáo cho người phụ trách.
