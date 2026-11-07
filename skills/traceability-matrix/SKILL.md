---
name: traceability-matrix
description: Lập 06-traceability-matrix-vK.md nối từng US/PAY/NFR/AC và nguồn TA-SPEC tới thành phần, UML, API/class/dữ liệu, cách kiểm chứng và trạng thái/OQ; kiểm tra không bỏ sót ID và không đánh dấu đáp ứng phần bị chặn.
---

# Skill: traceability-matrix – Ma trận truy vết

Vai trò: **design** trong [AGENTS.md](../../AGENTS.md) (bước 7). Đọc AGENTS.md và
[ngữ cảnh dùng chung](../_shared/payment-context.md) và
[naming-versioning](../naming-versioning/SKILL.md). Chạy **sau cùng** (bước 10),
khi các file thiết kế khác cùng version đã có.

## Đầu vào

Đọc thực tế (không giả định tồn tại) các file **cùng version vK**:
`docs/analysis/payment-management/vK/*` (sys-us, AC, OQ),
`docs/design/payment-management/vK/01..05, 07`, `vK/diagrams/*.puml`.
File chưa có → ô tương ứng ghi `Chưa có <file>`; không bịa tên thành phần.

## Đầu ra

`docs/design/payment-management/vK/06-traceability-matrix-vK.md`.

## Cấu trúc

1. **Nguồn và bản đã đọc** – danh sách file + commit (`git log -1 --format=%h -- <file>`).
2. **Ma trận chính** – một dòng cho mỗi US-PAY-01..05, PAY-01..08, NFR-PAY-01..02
   và **mỗi AC** (`AC-USNN-kk`):

   | ID | Loại | Nguồn | Nội dung rút gọn | SYS (sys-us) | Thành phần (02) | UML (file/phần tử) | API (04) | Class/method (03) | Dữ liệu (05) | Cách kiểm chứng | Trạng thái | OQ/DD |
   |---|---|---|---|---|---|---|---|---|---|---|---|---|

   - Nguồn: `TA-SPEC §x, ID; TA-PDF tr.y`.
   - UML: tên file + phần tử cụ thể (transition, alt, class), không chỉ tên file.
   - Cách kiểm chứng: kiểm thử đề xuất (unit/integration/API), vd. "Gọi submit 2 lần
     cùng Idempotency-Key → 1 chuyển trạng thái, 1 audit". Đây là kế hoạch, không phải
     kết quả đã chạy.
3. **Ma trận ngược** – thành phần/endpoint/entity → ID yêu cầu; phần tử không truy
   được về yêu cầu nào là dấu hiệu vượt phạm vi, ghi chú để design xem lại.
4. **Phần bị chặn** – mọi dòng `Blocked by OQ-…`, phần nào làm được và phần nào chờ.
5. **Tổng hợp bao phủ** – số ID theo từng trạng thái.

## Giá trị cột Trạng thái (chỉ dùng các giá trị này)

| Giá trị | Khi dùng |
|---|---|
| `Đã thiết kế – chưa kiểm thử` | Có thành phần/UML/API/dữ liệu đầy đủ, không phụ thuộc OQ mở |
| `Thiết kế một phần` | Thiếu ít nhất một cột thiết kế; ghi thiếu gì |
| `Blocked by OQ-…` | Phụ thuộc OQ chưa trả lời (vẫn điền phần đã làm) |
| `Chưa thiết kế` | Chưa có phần nào |

Không dùng "Đạt", "Đã đáp ứng", "Đã kiểm thử" khi chưa có bằng chứng chạy test/đo;
NFR-PAY-02 chỉ là phương án đáp ứng cho đến khi có kết quả đo ghi lệnh/số liệu.
Mọi trạng thái kèm `Design Pending Approval` cho tới khi người phụ trách duyệt.

## Bắt buộc soát

- PAY-04 (tổng âm, dòng bắt buộc – Blocked, chống trình trùng), PAY-07 cấm tự duyệt,
  NFR-PAY-01 audit cho **mọi** chuyển trạng thái và mọi điều chỉnh (liệt kê từng chuyển).
- Mâu thuẫn: tháng/quý (OQ-01), 500 triệu (OQ-02), Approved (OQ-03),
  Rejected/Draft (OQ-04), dòng bắt buộc (OQ-05) – các dòng liên quan không được
  ở `Đã thiết kế`.
- Tên ở các cột khớp danh mục tên dùng chung; lệch thì ghi vào mục 3 để sửa.

## Kiểm chứng tự động tối thiểu

Chạy từ gốc workspace, đặt `V` = `v1` hoặc `v2`, ghi lệnh + kết quả vào cuối file:

```sh
python - <<'EOF'
import re, pathlib
V = "v1"  # đổi thành "v2" khi lập ma trận v2
t = pathlib.Path(f"docs/design/payment-management/{V}/06-traceability-matrix-{V}.md").read_text(encoding="utf-8")
ids = [f"US-PAY-0{i}" for i in range(1, 6)] + [f"PAY-0{i}" for i in range(1, 9)] + ["NFR-PAY-01", "NFR-PAY-02"]
missing = [i for i in ids if not re.search(r"\|\s*" + re.escape(i) + r"\s*\|", t)]
acs = set(re.findall(r"AC-US0\d-\d+", "".join(p.read_text(encoding="utf-8") for p in pathlib.Path(f"docs/analysis/payment-management/{V}").glob("*.md"))))
missing += sorted(a for a in acs if a not in t)
print("MISSING:", missing or "none")
EOF
```

Kết quả `none` chỉ chứng minh đủ dòng, không chứng minh thiết kế đúng.
Ghi prompt-log; không sửa `src/` hoặc OQ của BA.
