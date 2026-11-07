---
name: sys-spec
description: Viết đặc tả use case hệ thống sys-us-NN-vK.md (actor, tiền/hậu điều kiện, dòng cơ bản/thay thế, NFR, AC dẫn xuất, Open Questions) cho một US-PAY của module Bảng thanh toán, bám TA-SPEC và dẫn nguồn từng dòng. Là bước đầu tiên; sequence, kiến trúc và dữ liệu đều suy ra từ file này.
---

# Skill: sys-spec – Đặc tả use case hệ thống

Vai trò: **ba** trong [AGENTS.md](../../AGENTS.md). Đọc AGENTS.md,
[ngữ cảnh dùng chung](../_shared/payment-context.md) và
[naming-versioning](../naming-versioning/SKILL.md) trước khi làm.

## Đầu vào

- Tham số: số US (01..05) và version, vd. "dùng skill sys-spec cho US-PAY-02, v1".
  Không nêu version thì hỏi lại; mặc định chỉ được ghi v1 khi v1 chưa đóng băng.
- Đọc toàn bộ [TA-SPEC](../../docs/requirements/payment-management/spec.md),
  không chỉ mục của US được giao (quy tắc PAY và §3/§6 tác động chéo).
- Đọc nếu có (cùng version): `open-questions-vK.md` và các `sys-us-*-vK.md` khác
  để tái sử dụng OQ/AC, không đặt mã trùng nghĩa.
- v2: đọc `sys-us-NN-v1.md`, `review-assessment-*-v1.md` (chỉ nhận xét được chấp
  nhận) và câu trả lời OQ đã ghi người/ngày.

## Đầu ra

`docs/analysis/payment-management/vK/sys-us-NN-vK.md`, vd. `v1/sys-us-01-v1.md`.
File đã tồn tại thì chỉ bổ sung phần thiếu/sai có căn cứ, không viết lại toàn bộ;
nêu thay đổi trong câu trả lời. Không ghi vào `v1/` khi đã có `ai-review-01-v1.md`.

## Cấu trúc file

```markdown
# SYS-US-NN – <Tên US theo TA-SPEC> (vK)

> Phiên bản / Ngày / Người phụ trách / Đầu vào / AI + Prompt / Trạng thái
> (khối thông tin theo naming-versioning §5)
> Nhãn: [ĐẶC TẢ] … [AC dẫn xuất] … [ĐỀ XUẤT KỸ THUẬT] … [GIẢ ĐỊNH – Cần xác nhận]

## 1. Use case
## 2. Điểm cần xác nhận
## 3. Acceptance criteria
## Thay đổi so với v1   (chỉ ở v2)
```

## Các bước

1. **Liệt kê căn cứ**: câu nguyên văn của US, mọi PAY liên quan, §2/§3/§6.
   Bảng gợi ý ở [ngữ cảnh chung §2](../_shared/payment-context.md#2-danh-mục-id-phải-bao-phủ)
   – phải kiểm tra lại trên đặc tả.
2. **Phần 1 – bảng use case** gồm các hàng: Tên (SYS-US-NN), Tác nhân
   (chính/liên quan), Mục tiêu, Kích hoạt, Tiền điều kiện (P1..), Hậu điều kiện
   (thành công/thất bại), Dòng cơ bản (đánh số), Dòng thay thế, Yêu cầu phi chức năng.
   - Mỗi bước/điều kiện kết thúc bằng nhãn + dẫn nguồn.
   - Dòng thay thế đặt tên theo bước rẽ nhánh (A4 rẽ từ bước 4); nhánh con A4.2.
   - Bắt buộc có nhánh: sai trạng thái, sai quyền, dữ liệu không hợp lệ, thao tác
     đồng thời/trùng (nếu đề có yêu cầu), lỗi lưu kể cả lỗi audit.
   - Bước UI/điều hướng không có trong đề → `[ĐỀ XUẤT KỸ THUẬT]`.
   - NFR: nêu NFR-PAY-01/02 áp dụng hay **không áp dụng** và vì sao; không tự
     thêm SLA cho chức năng khác ngoài lập bảng.
   - Dòng cơ bản/thay thế phải đủ chi tiết để vẽ sequence (ai gửi gì cho hệ thống,
     hệ thống kiểm tra gì, kết quả gì) – sequence ở bước sau chỉ được vẽ từ đây.
3. **Phần 2 – Điểm cần xác nhận**: bảng OQ theo mẫu AGENTS.md (ID, Vị trí mọi
   nguồn kèm trích dẫn ngắn, Loại, Mô tả, Lý do, Lựa chọn, Ảnh hưởng tới Phần 1,
   Trạng thái `Cần xác nhận`, Người/ngày/câu trả lời). Dùng `OQ-01..05` cho vấn đề
   đã giữ chỗ; vấn đề mới đặt `OQ-USNN-kk`. Mỗi `Blocked by OQ-…` ở Phần 1 phải có
   dòng tương ứng ở Phần 2 và ngược lại. Sau đó chép OQ mới vào `open-questions-vK.md`.
4. **Phần 3 – Acceptance criteria**: bảng `ID | Given/When/Then | Nhãn | Nguồn | OQ`.
   - `[ĐẶC TẢ]` khi gần nguyên văn; còn lại `[AC dẫn xuất]` nối về câu gốc.
   - AC phụ thuộc OQ vẫn ghi, cột OQ điền `Blocked by OQ-…`, không chọn phía.
   - Mã `AC-USNN-kk` là mã tự đặt; ghi chú điều đó ở đầu bảng.

## Không được

- Thêm vai trò, trạng thái, ngưỡng, thuế, SLA, kênh thông báo, công thức không có nguồn.
- Chọn KTT/GĐKD cho đúng 500 triệu, chọn Rejected/Draft, chọn cách điều chỉnh Approved,
  chốt kỳ tháng/quý, liệt kê "dòng dịch vụ bắt buộc".
- Chốt endpoint/schema/class (việc của design); chỉ được gợi ý có nhãn.
- Dùng tài liệu ngoài TA-SPEC/TA-PDF làm đáp án.

## Tự kiểm trước khi trả lời

- [ ] Tên file, hậu tố version và khối thông tin đúng naming-versioning.
- [ ] Mọi hàng Phần 1 có nhãn + nguồn; không còn câu khẳng định không dẫn nguồn.
- [ ] Mọi PAY liên quan ở bước 1 xuất hiện ít nhất một lần.
- [ ] Mọi `Blocked by OQ-…` ↔ dòng OQ khớp hai chiều
  (`grep -o "OQ-[0-9A-Z-]*" sys-us-NN-vK.md | sort -u`).
- [ ] Mỗi dòng cơ bản/thay thế có ít nhất một AC; mỗi AC có nguồn.
- [ ] Tên trạng thái đúng 5 giá trị §3.
- Ghi lần chạy vào [prompt-log](../../docs/workflow/prompt-log.md) theo
  [quy trình](../../docs/workflow/README.md).
