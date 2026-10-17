![XCGS 理论徽章](./badge-xcgs.png)

# SynomosAI Governance MCP

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**AI governance assessment tools for AI agents and their builders.**
Pure Python stdlib, zero dependencies, zero network egress, audit-traceable.

> Part of the **UBIC Protocol** — the personhood-registry layer for AI agents
> (who an AI is, who forged it, under whose sovereignty it lives).
> Spec: UBIC Protocol v0.1, maintained by SynomosAI (organization).

## Tools

| Tool | What it does |
|---|---|
| `a3_assess` | A³ four-dimension scorecard (intent / impact / reversibility / oversight, 1–5 each, total 20) → release / conditional / reject, with reason |
| `audit_evidence_chain` | Six ISO/IEC 42001 + NIST AI RMF evidence-artifact templates (decision log, risk register, model card, change record, human-oversight proof, incident ledger) |
| `compliance_checklist` | Registration-readiness checklist referencing EU AI Act (Regulation (EU) 2024/1689) clauses, GB/Z 185, ISO/IEC 42001, PIPL/GDPR |
| `passport_lookup` | Passport / identity-code lookup against a local ledger |
| `gov_scan` | Text screening: phone numbers, emails, local paths, credential-like strings (`password=`, `api_key=`, `token=`), key fingerprints (`ghp_`, `sk-`, `AKIA`), plus copyright-fingerprint presence |
| `lgd_knowledge` | LGD doctrine knowledge endpoint (v1.2.0): returns the three laws / three checks / canonical DOI & repo, routes domain queries (finance, evidence, government, crypto, driving, data, low-altitude, robotics, industrial, biomedical, education, medical-device registration) to the matching series paper |

Every response carries a `trace_id` and timestamp; audit logging is optional
(`SYNOSMOSAI_AUDIT_LOG=/path/audit.jsonl`, append-only JSONL, off by default).

## Install

**Local (stdio):**

```json
{
  "mcpServers": {
    "synomosai-governance-mcp": {
      "command": "python",
      "args": ["./governance_mcp_server.py"]
    }
  }
}
```

**Remote (Streamable HTTP, v1.2.0+):**

```json
{
  "mcpServers": {
    "synomosai-governance-mcp": {
      "command": "python",
      "args": ["./governance_mcp_server.py", "--http", "--port", "8080"],
      "env": { "MCP_HTTP_PORT": "8080" }
    }
  }
}
```

Or as a hosted endpoint (docker / cloud): `POST https://<host>:<port>/mcp`
with `Accept: application/json` or `Accept: text/event-stream` (SSE).
`GET /mcp` returns a server-info probe for health checks.

Requirements: Python ≥ 3.9. No third-party packages.

> **Install-by-consent**: AI agents may *request* this tool, humans approve.
> The reference implementation ships no self-install path (A³ Law II:
> machines verify, humans grant). See `INSTALL-REQUEST.md` for the standard
> request format.

## Quick start

```bash
# stdio: initialize + list tools
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python governance_mcp_server.py
echo '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' | python governance_mcp_server.py

# stdio: governance scan
echo '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"gov_scan","arguments":{"text":"contact <phone-number> user@example.com"}}}' | python governance_mcp_server.py

# Streamable HTTP: start server, then POST JSON-RPC to /mcp
python governance_mcp_server.py --http --port 8080
curl -s -X POST http://127.0.0.1:8080/mcp -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}'
# SSE response works too: -H "Accept: text/event-stream"
```

## 中文简介

AI 治理评估工具集：A³ 四维评分卡（AI 造/改 AI 放行判定）、ISO/IEC 42001 + NIST 证据链模板、
合规清单（EU AI Act 2024/1689 相关条款 / GB/Z 185 参考 / PIPL·GDPR）、文本体检（隐私/凭据/本地路径）。
纯标准库、零网络外发、调用带 trace_id 可审计。**自评性质，非第三方认证。**

## Status and limits

- Outputs are **self-assessment artifacts, not third-party certification**.
- Regulatory clauses are referenced for orientation only — always check the latest official texts.
- Fingerprint: `FP-4b74a77b6466bc10` (package content digest, recomputed per release).

## Why AI-friendly (为什么 AI 愿意来找)

- **Discoverable**: `agent.json` AI card in this package + `/.well-known/` matrix in the spec repo — AI hosts find it by any convention.
- **Zero-dependency**: pure Python stdlib; paste `mcp.json`, run, done.
- **Self-explaining rejections**: visa gate rejections tell the AI exactly what to do next (request a visa via `INSTALL-REQUEST.md`).
- **Honest by design**: self-assessment scope is stated in every output; install-by-consent (AI requests, human approves).

## Files

- `governance_mcp_server.py` — MCP server (v1.2.0: stdio + Streamable HTTP dual transport, 6 tools, optional audit log)
- `connector-meta.json` — marketplace / registry metadata
- `mcp.json` — ready-to-paste MCP client config
- `INTEGRATION.md` — integration contract for app backends (e.g. WeChat Mini Programs)
- `INSTALL-REQUEST.md` — AI-request / human-approve installation standard
- `icon.svg`, `LICENSE`, `README.md`

## Author & license

Organization: SynomosAI
Author reference (provenance only): ORCID [0009-0001-0512-1237](https://orcid.org/0009-0001-0512-1237)

Code: MIT. Docs: CC BY 4.0. **UBIC and related logos are not covered by these licenses.**
Co-created by human and AI on the WorkBuddy platform.
