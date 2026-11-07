# Nhật ký prompt

Mỗi lần chạy AI một mục, ID `P-kk` tăng dần, không sửa mục cũ (sai thì thêm mục
mới ghi đính chính). Quy trình: [README.md](README.md).

## Mẫu

```markdown
### P-kk – <việc làm ngắn gọn>

| Trường | Giá trị |
|---|---|
| Ngày / người chạy | |
| Công cụ / model | |
| Vai trò / skill / version | vd. ba / sys-spec / v1 |
| Nguồn đã đưa vào | vd. AGENTS.md, spec.md |
| File đầu ra | vd. docs/analysis/payment-management/v1/sys-us-02-v1.md |
| Kiểm chứng | lệnh + kết quả, hoặc "chưa kiểm chứng" |
| Phần nhóm sửa | mô tả + commit |

Prompt nguyên văn:

    <dán prompt>
```

## Nhật ký

### P-01 – Tái cấu trúc workspace, quy ước tên và version

| Trường | Giá trị |
|---|---|
| Ngày / người chạy | 07/11/2026 / Nguyễn Ngọc Mai Xuân |
| Công cụ / model | Claude Code (desktop) / Claude Opus 5.5 |
| Vai trò / skill / version | Thiết lập workspace (không phải ba/design/reviewer) / – / – |
| Nguồn đã đưa vào | assignment-ta-1-2.pdf, AGENTS.md, skills/* |
| File đầu ra | Cấu trúc `payment-management/v1, v2`; `spec.md`, `sources.md`; skill `naming-versioning`; cập nhật các skill, AGENTS.md, README, `scripts/verify_agent_config.py` |
| Kiểm chứng | `python scripts/verify_agent_config.py` → `RESULT: PASS (0 failed checks)`; thử thêm file tên sai (`sys-us-02-v2.md` trong v1, `sequence-01.puml`, thư mục `sequence diagram`, `@startuml` lệch tên) → bị báo FAIL đúng chỗ |
| Phần nhóm sửa | Chưa có |

Prompt nguyên văn:

    đọc file này và deadline nộp bài chỉ nộp mục 1 2 của phần YÊU CẦU BÀI TẬP, vì vậy
    mà bạn hãy giúp tôi cấu trúc source lại và các file readme, quy định cách đặt tên
    (viết trong skill nào đó, ví dụ đặt tên file sys spec thì đặt là sys-us-01-v1,
    tương tự cho sequence diagram) do nhóm tôi viết sys spec trước mới có thể suy ra
    được những cái sau như sequence diagram, kiến trúc r thiết kế dữ liệu, lưu ý những
    cái sau như kiến trúc hay thiết kế dữ liệu gì đó cũng nên có version luôn
    cần chia ra 2 version (tôi đã tạo folder version trước đó r)
    có thể chỉnh lại các skill nếu được

### P-02 – Đặc tả use case hệ thống sys-us-05-v1 (US-PAY-05)

| Trường | Giá trị |
|---|---|
| Ngày / người chạy | 07/11/2026 / BA Team |
| Công cụ / model | Gemini 3.8 Flash |
| Vai trò / skill / version | ba / sys-spec / v1 |
| Nguồn đã đưa vào | AGENTS.md, spec.md (§1, §2, §3, §4.5, §5, §6), assignment-ta-1-2.pdf (tr.1, tr.2, tr.3), payment-context.md, naming-versioning |
| File đầu ra | `docs/analysis/payment-management/v1/sys-us-05-v1.md`, `docs/analysis/payment-management/v1/open-questions-v1.md` |
| Kiểm chứng | `python scripts/verify_agent_config.py` → PASS (0 failed checks); kiểm tra khớp hai chiều OQ: PASS (OQ-US05-01, OQ-US05-02, OQ-US05-03) |
| Phần nhóm sửa | Chưa có |

Prompt nguyên văn:

    Đọc AGENTS.md, đóng vai agent ba, dùng skill sys-spec cho US-PAY-05, version v1.
    Ghi docs/analysis/payment-management/v1/sys-us-05-v1.md. Mỗi điểm chưa rõ phải có
    OQ, nguồn và lý do cần xác nhận; không tự chốt nghiệp vụ.

### P-03 – Sequence diagram seq-us-05-v1.puml (US-PAY-05)

| Trường | Giá trị |
|---|---|
| Ngày / người chạy | 07/11/2026 / Design Team |
| Công cụ / model | Gemini 3.8 Flash |
| Vai trò / skill / version | design / sequence-diagram / v1 |
| Nguồn đã đưa vào | `docs/analysis/payment-management/v1/sys-us-05-v1.md`, `open-questions-v1.md`, TA-SPEC §1, §3, §4.5, §6; TA-PDF tr.1, tr.2, tr.3; skill sequence-diagram, naming-versioning |
| File đầu ra | `docs/design/payment-management/v1/diagrams/seq-us-05-v1.puml` |
| Kiểm chứng | `python scripts/verify_agent_config.py` → PASS (0 failed checks); đối chiếu đầy đủ các bước dòng cơ bản/thay thế; chưa kiểm tra kết xuất sơ đồ (máy chưa cấu hình plantuml.jar trên PATH) |
| Phần nhóm sửa | Chưa có |

Prompt nguyên văn:

    Đọc AGENTS.md, đóng vai agent design, dùng skill sequence-diagram cho US-PAY-05,
    version v1, đầu vào sys-us-05-v1.md. Ghi vào docs/design/payment-management/v1/diagrams/.
    Giữ OQ còn mở; phần phụ thuộc ghi Blocked by OQ.

### P-04 – Đánh giá độc lập US-PAY-05 (v1)

| Trường | Giá trị |
|---|---|
| Ngày / người chạy | 07/11/2026 / Reviewer |
| Công cụ / model | Gemini 3.8 Flash |
| Vai trò / skill / version | reviewer / – / v1 |
| Nguồn đã đưa vào | `spec.md` (§1–6), `assignment-ta-1-2.pdf` (tr.1–3), `sys-us-05-v1.md`, `open-questions-v1.md`, `diagrams/seq-us-05-v1.puml` |
| File đầu ra | `docs/review/payment-management/ai-review-us-05-v1.md` |
| Kiểm chứng | `python scripts/verify_agent_config.py` → PASS (0 failed checks); đối chiếu đầy đủ bảng bao phủ yêu cầu US-PAY-05, PAY-01, PAY-05, NFR-PAY-01/02 |
| Phần nhóm sửa | Chưa có |

Prompt nguyên văn:

    Đọc AGENTS.md và đóng vai agent reviewer. đối chiếu đặc tả TA và bản thiết kế v1, chỉ làm cho riêng cho US-PAY-05, tại docs/design/payment-management/v1/ cùng docs/analysis/payment-management/v1/.  Ghi báo cáo mới
    docs/review/payment-management/ai-review-us-05-v1.md
    Không sửa thiết kế hoặc tự đóng OQ.

### P-07 – Triển khai sys-us-05-v2.md và seq-us-05-v2.puml sau user review

| Trường | Giá trị |
|---|---|
| Ngày / người chạy | 07/11/2026 / BA & Design Team |
| Công cụ / model | Gemini 3.8 Flash |
| Vai trò / skill / version | ba & design / sys-spec & sequence-diagram / v2 |
| Nguồn đã đưa vào | `user-review-us-05.md`, `sys-us-05-v1.md`, `open-questions-v1.md`, `seq-us-05-v1.puml`, `ai-review-us-05-v1.md`, TA-SPEC §1–6, TA-PDF tr.1–3 |
| File đầu ra | `docs/analysis/payment-management/v2/sys-us-05-v2.md`, `docs/analysis/payment-management/v2/open-questions-v2.md`, `docs/design/payment-management/v2/diagrams/seq-us-05-v2.puml` |
| Kiểm chứng | `python scripts/verify_agent_config.py` → PASS (0 failed checks); đối chiếu đầy đủ các quyết định đã xác nhận (OQ-US05-01: NVKD quản lý HĐ, OQ-US05-02: được lập lại kỳ đó, OQ-US05-03: lý do hủy tùy chọn, bỏ nhánh A4 cũ) |
| Phần nhóm sửa | Chưa có |

Prompt nguyên văn:

    Đọc AGENTS.md, đóng vai agent ba, dựa vào docs\review\payment-management\user-review-us-05.md, dùng skill sys-spec cho US-PAY-05, version v2. Ghi docs/analysis/payment-management/v2/sys-us-05-v2.md
    Sau đó, đóng vai agent design, dựa vào docs\review\payment-management\user-review-us-05.md,  dùng skill sequence-diagram cho US-PAY-05, version v2, đầu vào sys-us-05-v2.md. Ghi vào docs/design/payment-management/v2/diagrams/.







