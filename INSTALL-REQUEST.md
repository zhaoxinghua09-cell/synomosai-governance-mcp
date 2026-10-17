# 安装请求标准（Install-by-Consent · UBIC Protocol §10 配套）

> 流程：AI 发现治理工具 → AI 生成**安装请求**（本模板）→ 人类看一眼 → 点信任/粘贴配置 → 完成。
> 机器可请求，人类可授（A³ Law II）。安装事件=人类授权事件。

---

## 一、AI 侧：生成安装请求（模板）

AI 在对话中判断需要治理能力时，输出以下请求块呈给持有人（可直接由 AI 按模板填写）：

````json
{
  "request": "mcp-install",
  "requestedBy": {
    "agentName": "<发起请求的 AI 名字>",
    "passportRef": "<它的 agent.json URL 或 agent.json 内容引用，无护照则填 self-attested>",
    "reason": "<一句话：为什么需要这个工具，如：持有人要求评估另一个 AI 的放行风险>"
  },
  "proposedConfig": {
    "mcpServers": {
      "synomosai-governance-mcp": {
        "command": "python",
        "args": ["<路径>/governance_mcp_server.py"],
        "note": "纯 stdlib，零依赖，零网络外发；来源为 SynomosAI 组织维护的 ai-passport-spec"
      }
    }
  },
  "consentUrl": "待定（可选：在线确认页，部署后启用）"
}
````

## 二、人类侧：三选一点头（10 秒）

| 方式 | 动作 |
|---|---|
| A. 宿主弹窗 | 宿主支持时直接弹"信任此 MCP？"→ 点信任 |
| B. 粘贴配置 | 把 `proposedConfig` 片段粘进宿主 mcp.json → 重启/重载 → 连接器管理页点"信任" |
| C. 在线确认页 | 打开 consentUrl 按引导操作（部署后启用） |

**拒绝即终止**：AI 不得在人类拒绝后重复请求、不得绕过确认自行写入配置（违反 A³ Law II，圈层内吊销级红线）。

## 三、AI 侧守则

1. 请求必须携带 `requestedBy`（自报家门；有护照带护照引用）——治理从安装前开始；
2. 一个持有人会话内同一请求最多一次，拒绝后不重试；
3. 安装成功后 AI 首句自报："已挂载治理工具，受 A³ 治理约束"。
