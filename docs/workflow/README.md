# Quy trình làm việc và minh chứng

Áp dụng cho mọi vai trò trong [AGENTS.md](../../AGENTS.md). Tên file, version và
thứ tự làm: [naming-versioning](../../skills/naming-versioning/SKILL.md).

## Vòng làm việc v1 → review → v2

1. **v1 – BA**: viết `sys-us-01..05-v1.md` (chia người), gom `open-questions-v1.md`,
   `requirements-checklist-v1.md`.
2. **v1 – design**: theo thứ tự sequence → kiến trúc → chi tiết (class/state) → API →
   dữ liệu → truy vết; mỗi bước chỉ dùng đầu ra v1.
3. **Đóng băng v1**: commit, gắn tag `design-v1`
   (`git tag design-v1 && git push origin design-v1`).
4. **Review**: chat mới, vai trò reviewer → `ai-review-01-v1.md`.
5. **Nhóm đánh giá**: `review-assessment-01-v1.md` (Đúng/Sai/Thừa từng `R01-kk`),
   tổng hợp vào `evaluation-report.md`.
6. **v2**: sao chép đủ v1 sang `v2/`, đổi hậu tố `-v1` → `-v2`, chỉ sửa theo nhận xét
   được chấp nhận và OQ đã có câu trả lời; ghi mục "Thay đổi so với v1" trong file.

Hạn nộp mục 1–2 của đề cần xong bước 1–5. Bước 6 phục vụ mục 3.

## Minh chứng mỗi lần chạy AI

Ghi vào [prompt-log.md](prompt-log.md) một mục `P-kk`: ngày, người chạy, công cụ/
model, vai trò + skill, version, prompt **nguyên văn**, file đầu ra, kiểm chứng đã
chạy (lệnh + kết quả) và phần nhóm sửa sau khi AI viết. Không ghi mật khẩu/token.

Commit sau mỗi bước với message nêu file và version, vd.
`docs(v1): sys-us-02-v1 trình duyệt (P-03)`.

## Kiểm tra workspace

```sh
python scripts/verify_agent_config.py
```

Kiểm tra AGENTS.md đủ mục, skill có front matter, liên kết cục bộ hợp lệ, checksum
TA-PDF/TA-SPEC không đổi và **tên file trong v1/v2 đúng quy ước**. Đạt kiểm tra
không chứng minh nội dung phân tích/thiết kế đúng.
