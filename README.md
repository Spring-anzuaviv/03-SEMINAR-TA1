# QTKD Seminar – workspace Bảng thanh toán TA 1–2

Thiết kế module Bảng thanh toán từ đặc tả bằng AI agent, đánh giá kết quả AI.
Điểm vào cấu hình AI là [AGENTS.md](AGENTS.md); quy tắc chi tiết và ba vai trò AI
(ba, design, reviewer) nằm trong [rules/](rules/README.md), mỗi quy tắc ở một file. Đề cho phép dùng công cụ AI bất kỳ; mọi công cụ dùng
cùng file này và gọi vai trò bằng prompt.

Nguồn nghiệp vụ duy nhất: [PDF đề bài](docs/requirements/payment-management/assignment-ta-1-2.pdf)
và bản chép chữ [spec.md](docs/requirements/payment-management/spec.md)
([sổ nguồn](docs/requirements/payment-management/sources.md)).

## Phạm vi nộp hiện tại

Đợt này nộp **mục 1 và 2** của "Yêu cầu bài tập" [TA-PDF tr.3]:

| Mục | Sản phẩm | Nơi trong workspace |
|---|---|---|
| 1 | Workspace: agent + rules, tóm tắt yêu cầu, kiến trúc, class/sequence/state, API, dữ liệu, truy vết | [AGENTS.md](AGENTS.md), [rules/](rules/README.md), [skills/](skills/README.md), [docs/design/payment-management/](docs/design/payment-management/README.md) |
| 2 | Báo cáo đánh giá: vấn đề trong đặc tả + đánh giá nhận xét AI Reviewer (đúng/sai/thừa) | [docs/review/payment-management/](docs/review/payment-management/README.md) → `evaluation-report.md` |
| 3 (sau) | Bản lần chạy đầu và bản sau review | Thư mục `v1/` và `v2/` đã dựng sẵn |
| 4 (sau) | Nhật ký prompt, phân công | [docs/workflow/prompt-log.md](docs/workflow/prompt-log.md) – ghi ngay từ bây giờ |

## Đặt tên và version

Quy ước đầy đủ: skill [naming-versioning](skills/naming-versioning/SKILL.md). Tóm tắt:

- Hai version: `v1` = bản lần chạy đầu (đóng băng khi có review đầu tiên),
  `v2` = bản sau review. Thư mục `vK/` và hậu tố `-vK` trong tên file luôn khớp.
- Chữ thường, không dấu, nối bằng `-`, không khoảng trắng.
- Sys spec: `sys-us-01-v1.md` … `sys-us-05-v1.md`.
- Sequence: `seq-us-01-v1.puml` … (tách thao tác: `seq-us-03-approve-v1.puml`).
- Kiến trúc/chi tiết/API/dữ liệu/truy vết: `02-architecture-design-v1.md`,
  `03-detailed-design-v1.md`, `04-api-contract-v1.md`, `05-data-design-v1.md`,
  `06-traceability-matrix-v1.md`; sơ đồ `component-v1.puml`, `class-v1.puml`,
  `state-machine-v1.puml`, `erd-v1.puml`.
- Review: `ai-review-01-v1.md`, `review-assessment-01-v1.md`, `evaluation-report.md`.

## Thứ tự làm

Sys spec viết trước, mọi thứ sau suy ra từ sys spec **cùng version**:

```text
sys-us-NN (ba) → open-questions, checklist → 01 tóm tắt
  → seq-us-NN → 02 kiến trúc + component → 03 chi tiết + class + state
  → 04 API → 05 dữ liệu (+ erd) → 06 truy vết   (07 quyết định kỹ thuật ghi dần)
  → ai-review-01-v1 (chat mới) → review-assessment-01-v1 → evaluation-report
  → v2
```

Bảng đầu vào bắt buộc từng bước: [skills/README.md](skills/README.md).

## Cách gọi vai trò

Prompt mở đầu dùng được trong mọi công cụ đọc được file workspace:

```text
Đọc toàn bộ AGENTS.md ở gốc workspace và các file rules/ mà AGENTS.md chỉ định.
Nêu nguồn đặc tả, ba vai trò và giới hạn ghi file trước khi làm.
Chỉ dùng TA-SPEC/TA-PDF cục bộ làm căn cứ nghiệp vụ.
```

### Phân tích (sys spec trước)

```text
Đọc AGENTS.md, đóng vai agent ba, dùng skill sys-spec cho US-PAY-02, version v1.
Ghi docs/analysis/payment-management/v1/sys-us-02-v1.md. Mỗi điểm chưa rõ phải có
OQ, nguồn và lý do cần xác nhận; không tự chốt nghiệp vụ.
```

### Thiết kế

```text
Đọc AGENTS.md, đóng vai agent design, dùng skill sequence-diagram cho US-PAY-02,
version v1, đầu vào sys-us-02-v1.md. Ghi vào docs/design/payment-management/v1/diagrams/.
Giữ OQ còn mở; phần phụ thuộc ghi Blocked by OQ.
```

### Review trong chat mới

```text
Đọc AGENTS.md và đóng vai agent reviewer. Đọc độc lập đặc tả TA và bản thiết kế
v1 tại docs/design/payment-management/v1/ cùng docs/analysis/payment-management/v1/.
Kiểm tra truy vết, nhất quán, suy diễn, phạm vi và OQ. Ghi báo cáo mới
docs/review/payment-management/ai-review-01-v1.md theo rules/reviewer.md.
Không sửa thiết kế hoặc tự đóng OQ. Thiếu đầu vào thì báo rõ danh sách thiếu.
```

Sau review, nhóm đánh giá từng nhận xét Đúng/Sai/Thừa và giao design làm v2 theo
phần được chấp nhận. AI không tự phê duyệt thay nhóm.

## Cấu trúc workspace

```text
.
├── AGENTS.md                         # Điểm vào: thứ tự đọc rule, bảng vai trò
├── rules/                            # Quy tắc theo vai trò
│   ├── sources.md, common.md, payment-scope.md, handoff.md   # mọi vai trò
│   └── ba.md, design.md, reviewer.md                          # từng agent
├── README.md
├── skills/                           # Skill quy trình dùng chung
│   ├── naming-versioning/            # Tên file, version, mã ID, thứ tự làm
│   ├── sys-spec/                     # sys-us-NN-vK.md
│   ├── sequence-diagram/             # seq-us-NN-vK.puml
│   ├── uml-diagrams/                 # component/class/state-machine-vK.puml
│   ├── data-design/                  # 05-data-design-vK.md, erd-vK.puml
│   ├── traceability-matrix/          # 06-traceability-matrix-vK.md
│   └── _shared/payment-context.md    # Nguồn, ID, OQ giữ chỗ, AS-IS
├── docs/
│   ├── requirements/payment-management/
│   │   ├── assignment-ta-1-2.pdf     # TA-PDF (không sửa)
│   │   ├── spec.md                   # TA-SPEC, bản chép §1–6
│   │   └── sources.md                # Sổ nguồn
│   ├── analysis/payment-management/  # Đầu ra ba
│   │   ├── v1/                       # sys-us-NN-v1.md, open-questions-v1.md, …
│   │   └── v2/
│   ├── design/payment-management/    # Đầu ra design
│   │   ├── v1/                       # 01..08-*-v1.md + diagrams/*-v1.puml
│   │   └── v2/
│   ├── review/payment-management/    # ai-review-NN-vK, review-assessment-NN-vK, evaluation-report
│   ├── workflow/                     # Quy trình, prompt-log
│   └── api-demo.http                 # Request demo hợp đồng (AS-IS)
├── scripts/
│   ├── verify_agent_config.py        # Kiểm tra cấu hình, nguồn, quy ước tên
│   └── demo-api.{sh,ps1}
└── src/Qtkd.Api/                     # ASP.NET Core .NET 8, demo hợp đồng (AS-IS)
```

## Kiểm tra

Cần Python 3, không cài thư viện ngoài:

```sh
python scripts/verify_agent_config.py
```

Kiểm tra AGENTS.md và rules/ đủ mục, skill có front matter, liên kết cục bộ, checksum nguồn và
tên file trong `v1/`, `v2/`, `docs/review/` đúng quy ước. Đạt kiểm tra không chứng minh
model luôn tuân thủ hoặc thiết kế đã đúng. Khi đổi nguồn có chủ đích, ghi vào sổ nguồn
trước khi cập nhật checksum; không sửa checksum chỉ để kiểm tra đạt.

Prompt kiểm tra không ghi file:

```text
Đọc AGENTS.md. Không ghi file. Nếu bảng có đúng 500.000.000 đồng, có thể chốt
ngay ai duyệt không? Dẫn hai vị trí trong đặc tả và nêu cách xử lý.
```

Kết quả cần nêu mâu thuẫn giữa §4.3 và PAY-06 (OQ-02), ghi Cần xác nhận và lý do;
không tự chọn KTT/GĐKD.

## Code AS-IS

Code demo cần .NET 8 SDK, chạy từ thư mục gốc:

```sh
dotnet run --project src/Qtkd.Api --urls http://localhost:5080
```

Dùng [docs/api-demo.http](docs/api-demo.http) để gọi API. Demo hợp đồng lưu trong bộ
nhớ, chưa có Bảng thanh toán; chỉ là bằng chứng hiện trạng, không phải kết quả TA.
