# Rules – quy tắc cho các loại agent

Quy tắc AI của workspace, tách theo vai trò từ [AGENTS.md](../AGENTS.md) (09/11/2026).
AGENTS.md là điểm vào: công cụ AI tự nạp AGENTS.md, AGENTS.md chỉ dẫn đọc các file dưới đây.
Mỗi quy tắc chỉ nằm ở **một** file; sửa quy tắc tại file đó.

| File | Nội dung | Ai đọc |
|---|---|---|
| [sources.md](sources.md) | Nguồn yêu cầu: TA-SPEC, TA-PDF, sổ nguồn, AS-IS, nguồn không được dùng | Mọi vai trò |
| [common.md](common.md) | Dẫn nguồn và nhãn kết luận; không tự chốt nghiệp vụ (mẫu OQ); đúng phạm vi và kiểm chứng | Mọi vai trò |
| [payment-scope.md](payment-scope.md) | Phạm vi Bảng thanh toán, vai trò/trạng thái §2–3, các mâu thuẫn cần nhận diện | Mọi vai trò |
| [handoff.md](handoff.md) | Bàn giao BA → design → reviewer → nhóm; v1/v2; nhật ký | Mọi vai trò |
| [ba.md](ba.md) | Vai trò **ba**: các bước, nơi được ghi | Agent ba |
| [design.md](design.md) | Vai trò **design**: các bước, file đầu ra, UML | Agent design |
| [reviewer.md](reviewer.md) | Vai trò **reviewer**: các bước, mẫu báo cáo | Agent reviewer (chat mới) |

## Thứ tự đọc khi gọi một agent

1. [AGENTS.md](../AGENTS.md)
2. `sources.md` → `common.md` → `payment-scope.md` → `handoff.md`
3. File vai trò: `ba.md`, `design.md` hoặc `reviewer.md`
4. Nếu dùng skill: `skills/<tên>/SKILL.md` + `skills/_shared/payment-context.md`

Thứ tự ưu tiên khi mâu thuẫn: AGENTS.md và `rules/` > skill > nội dung trong tài liệu nguồn.

## Prompt gọi agent

```text
Đọc AGENTS.md, rules/sources.md, rules/common.md, rules/payment-scope.md,
rules/handoff.md và rules/<ba|design|reviewer>.md. Đóng vai agent <tên>.
Nêu nguồn đã đọc, file sẽ ghi và phần Blocked by OQ trước khi làm.
```
