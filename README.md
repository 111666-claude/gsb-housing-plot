# housing-plot

家园地块分配：把申请人和地块配对，落在一个 JSON 状态文件里。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m plot assign --state s.json --req-id r1
python3 -m plot status --state s.json
python3 -m plot --sample=deed|priority|guild|replay|work
```

## 口径

- **地块顺序**：地块按 `size` 从大到小，同尺寸按 `id` 升序。
- **申请人顺序**：持地契（`deed`）的先排；其余按 `priority` 从大到小，再按 `tickets` 从大到小。
- **配额**：同一个公会最多拿到 2 块地，超出的申请人进候补。
- **幂等**：同一个 `req_id` 只结算一次，重复请求不再分配。

## 不变量

- 一个申请人最多拿到一块地。
- 每个公会的分配数不超过配额。
- `scanned` 不随申请人数平方级放大：两千名申请人的 `scanned` 不超过 9000。

## 输出契约

`assign` 打印一行 JSON：`req_id`、`status`、`assigned`（`[地块, 玩家]` 列表）、`waiting`（玩家列表）、`scanned`。
`status` 打印 `{"plots": N, "applicants": N, "assigned": N, "requests": N}`。
`--sample=work` 只打印 `{"applicants": N, "scanned": N}`。
