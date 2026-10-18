# AGENTS.md — 给 AI Agent 的工作指引

本文件面向自动化 AI Agent（编码助手、MCP 客户端、集成机器人）。人类读者请看 [README.md](README.md)。

## 这个仓库是什么

`synomosai-governance-mcp` 是一个 **Model Context Protocol (MCP) 服务器**（纯 Python 标准库、零依赖、零网络外发），为 AI 智能体及其构建者提供治理评估工具。核心文件是 `governance_mcp_server.py`（stdio 传输，6 个工具，可选 append-only JSONL 审计日志）。它输出的是**自评产物，不是第三方认证**。

## 可用的工作命令

```bash
# 初始化并列出工具
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python governance_mcp_server.py
echo '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' | python governance_mcp_server.py

# 跑一次治理扫描
echo '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"gov_scan","arguments":{"text":"contact user@example.com"}}}' | python governance_mcp_server.py

# 可选：开启 append-only 审计日志
# set SYNOSMOSAI_AUDIT_LOG=/path/audit.jsonl  (默认关闭)
```

前置依赖：Python ≥ 3.9，无第三方包。

## 约定（Do）

- 修改工具后保持 JSON-RPC 接口与 `tools/list` 描述稳定；每个响应仍带 `trace_id` 与时间戳。
- 新增工具时同步更新 `README.md` 的工具表、`llms.txt` 与 `llms-full.txt`。
- 保持「纯标准库、零网络外发」的设计纪律。

## 禁止（Don't）

- 不要改动 `LICENSE` 的版权主体或 README「Author & license」中的权属 / 许可口径（Code MIT / Docs CC BY 4.0 / UBIC 标识除外）。
- 不要把自评输出对外表述为「第三方认证」；这是自评工具。
- 不要在仓内提交任何密钥、令牌或真实个人数据。
- 不要新增网络外发行为；扫描器仅处理传入文本，不回传任何内容。

## 边界

本仓提供治理评估与文本体检工具；监管条款仅作定位参考，正式引用前须核对最新官方法条。安装采用「AI 请求、人批准」制（见 `INSTALL-REQUEST.md`）。
