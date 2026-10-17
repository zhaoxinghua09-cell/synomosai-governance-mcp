# INTEGRATION — 治理连接器 × 微信小程序 集成契约

> 读者：微信小程序开发会话 ｜ 版本：v1.0.0（连接器）｜ 2026-09-05 ｜ 治理线 SSOT 附属件
> 本契约回答：小程序云后端如何调用 `synomosai-governance-mcp` 的 5 个工具、响应结构、审计与红线约定。

---

## 一、调用方式（两阶段）

**阶段 1（现在就能联调）**：本地 stdio。连接器是「行式 JSON-RPC」进程——每行一个请求，每行一个响应。

```bash
python governance_mcp_server.py
```

```jsonc
// 请求（一行一个）
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"a3_assess","arguments":{"intent":4,"impact":2,"reversibility":5,"oversight":3}}}
```

**阶段 2（上线前）**：云函数/HTTP 包装。小程序 wx.request → 云函数拉起 stdio 子进程（或常驻进程池）→ 转发 JSON-RPC → 回传。包装器只做转发，不改语义。⚠️ 云端部署属联网动作，需持有人点头后另行实施。

## 二、响应结构（统一包装）

所有 `tools/call` 的 `result.content[0].text` 是一段 JSON 字符串，解析后：

```jsonc
{
  "result": { ...工具业务结果... },
  "trace_id": "c15670bf96aa",   // 12 位十六进制，每次调用唯一
  "ts": "2026-09-05T01:54:41.172965+00:00"
}
```

小程序侧**必须保存/透出 trace_id**——它是审计与纠纷取证的唯一关联键。

## 三、5 工具速查（小程序视角）

| 工具 | 入参 | 返回要点 | 小程序用法建议 |
|---|---|---|---|
| `a3_assess` | intent/impact/reversibility/oversight（各 1-5，越界自动 clamp，缺省 3） | scores/total(满分20)/verdict/reason/scope | 「AI 发布前自评」页：滑动条打分 → 展示放行/复核/拒绝 + 理由 |
| `audit_evidence_chain` | system_name（可选） | 六类证据工件模板 + generated_at | 「审计准备」页：按系统名生成六类模板清单 |
| `compliance_checklist` | 无 | 六项 checklist（均"待确认"）+ note（条款以官方文本为准） | 「合规自查」页：勾选式清单 |
| `passport_lookup` | skill（如 `example-ai-brand`） | found/fp/version/owner 或 not-found | 「身份查询」页：本地台账示例，未来接 UBIC 花名册 |
| `gov_scan` | text（必填）+ names（可选，逗号分隔指名清单） | findings[]（type/severity）/clean/verdict | 「文本体检」页：粘贴文本 → 高亮命中类型 |

错误：未知工具返回 `-32602`；内部异常 `-32603`。入参缺失/null 均有兜底，不会 500。

## 四、审计留痕（建议开启）

小程序云后端设置环境变量 `SYNOSMOSAI_AUDIT_LOG=/path/audit.jsonl` 后，每次调用追加一行 JSONL（ts/trace_id/tool/args/ok）。响应里的 trace_id 与日志行一一对应。默认不落盘（零副作用）。

## 五、红线（小程序侧必须遵守）

1. **只出公开层**：护照/花名册数据只展示 `display_flags.title=public` 的字段；`human_binding`（真人绑定）与 `ledger/health` 等私有字段**永不上小程序**。
2. **客户面向不出现个人姓名**（任何个人姓名一律禁止）；署名口径：治理线 SynomosAI。
3. **自评但书不可删**：凡展示 a3_assess / compliance_checklist 结果，页面须带"自评性质，非独立第三方认证"字样（工具返回的 `scope`/`note` 字段已内置，前端不得过滤）。
4. **评估≠认证**：不得在小程序使用"认证/背书/官方资质"等表述。
5. 法规条款展示保留"以官方最新文本为准"但书。

## 六、版本与指纹

- 连接器：synomosai-governance-mcp v1.0.0（发布打磨版）
- 指纹链：母版 `FP-GOV-6999EE1111DE`（2026-08-28）→ 发布版 `FP-4b74a77b6466bc10`（2026-09-05）
- 契约变更须同步升 version 并在双边（小程序会话 + 本会话）留痕

## 七、UBIC 数据接入（后续路线）

小程序不直读本地 roster-data.json。路线：本会话产出**公开快照**（仅 public 字段 + 指纹锚点值）→ 小程序侧随包/云端缓存只读展示。`passport_lookup` 未来由"本地台账示例"升级为"公开快照查询"，接口形态不变。
