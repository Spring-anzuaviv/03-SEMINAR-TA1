# Rule – Quy tắc chung

> Áp dụng cho mọi vai trò.
> Tách nguyên văn từ AGENTS.md ngày 09/11/2026 (P-23); sửa rule tại file này.

## Dẫn nguồn và phân loại kết luận

- Mỗi yêu cầu, vai trò, quyền, trạng thái, điều kiện, con số và nhận xét review
  phải có mã nguồn + trang/mục/US/PAY/AC cụ thể trong tài liệu cục bộ.
  Ví dụ: [ĐẶC TẢ] [TA-SPEC §4.2, US-PAY-02; TA-PDF tr.2].
- Phân biệt [ĐẶC TẢ], [THAM KHẢO], [ĐỀ XUẤT KỸ THUẬT],
  [GIẢ ĐỊNH – Cần xác nhận] và [QUYẾT ĐỊNH ĐÃ XÁC NHẬN].
  Nếu đối chiếu tài liệu đồ án tổng thể, ghi rõ mã nguồn từng phía.
- Acceptance criteria do phân tích suy ra phải ghi AC dẫn xuất và nối yêu cầu
  gốc; điều kiện bổ sung phải chờ xác nhận. Mã tự đặt không phải mã trong đề.
- Đề xuất kỹ thuật phải nêu mục đích, yêu cầu liên quan, lựa chọn thay thế,
  lý do và tác động nghiệp vụ nếu có; không trình bày như business rule gốc.

## Không tự chốt nghiệp vụ chưa rõ

- Mâu thuẫn/mơ hồ/thiếu phải thành Open Question (OQ), có ID ổn định, vị trí
  mọi nguồn, loại, mô tả, lý do cần xác nhận, lựa chọn nếu có và ảnh hưởng.
- Giữ trạng thái Cần xác nhận đến khi người phụ trách trả lời rõ. Reviewer AI
  không có quyền duyệt nghiệp vụ. Khi có xác nhận, ghi người, ngày, nội dung
  và tham chiếu câu trả lời; không sửa hồi tố đặc tả.
- Không tự chọn một phía của mâu thuẫn hoặc dùng tài liệu ngoài phạm vi làm
  đáp án. Tiếp tục phần độc lập; phần phụ thuộc ghi Blocked by OQ-....
- Nếu cần trình bày phương án giả định, gắn nhãn và OQ. Không coi đó là thiết kế
  cuối cùng hoặc truyền sang vai trò tiếp theo như sự thật đã duyệt.
- Không thêm vai trò, trạng thái, thuế, ngưỡng, SLA, công thức hoặc quy trình
  chưa có nguồn. Không mở rộng phạm vi để tự lấp chỗ thiếu.

Mẫu Open Questions:

| ID | Vị trí mọi nguồn | Loại Mâu thuẫn/Mơ hồ/Thiếu | Mô tả | Lý do cần xác nhận | Lựa chọn | Ảnh hưởng | Trạng thái | Người/ngày/câu trả lời và tham chiếu |
|---|---|---|---|---|---|---|---|---|

## Làm việc đúng phạm vi và kiểm chứng

- Chỉ làm công việc được giao. Không sửa mã ứng dụng khi chỉ được giao
  phân tích/thiết kế/review; tuân thủ giới hạn ghi file của từng vai trò.
- Nêu giả định, chỗ chưa rõ và phương án đơn giản hơn khi phù hợp. Thiết kế
  vừa đủ; không thêm tính năng, abstraction, cấu hình hoặc xử lý lỗi giả định.
- Thay đổi tối thiểu, giữ conventions có sẵn, không refactor hoặc xóa phần
  không liên quan. Dọn phần thừa do chính thay đổi của mình tạo ra.
- Xác định tiêu chí hoàn thành và chạy kiểm tra phù hợp với thay đổi. Ghi lệnh,
  kết quả và phần chưa kiểm chứng; không nói đã chạy/render/đạt hiệu năng/phê
  duyệt khi chưa có bằng chứng.
- Không ghi bí mật vào prompt/nhật ký. Ghi nguồn, công cụ/phiên bản, prompt
  thực tế, đầu ra, kiểm chứng và phần AI viết/nhóm sửa theo
  [quy trình minh chứng](../docs/workflow/README.md).
