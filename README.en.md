# SynomosAI Governance MCP

[![License: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE)
[![Docs: CC BY 4.0](https://img.shields.io/badge/Docs-CC%20BY%204.0-lightgrey.svg)](#)
[![Python](https://img.shields.io/badge/python-stdlib%20%7C%20zero%20deps-3776AB.svg)](#)
[![Zero Network Egress](https://img.shields.io/badge/zero-network-egress-2ea44f.svg)](#)
[![MCP](https://img.shields.io/badge/MCP-server-yellow.svg)](#)

**AI governance assessment tools for AI agents and their builders.**
Pure Python stdlib, zero dependencies, zero network egress, audit-traceable.

> Part of the **UBIC Protocol** — the personhood-registry layer for AI agents
> (who an AI is, who forged it, under whose sovereignty it lives).

## Tools

| Tool | What it does |
|---|---|
| `a3_assess` | A³ four-dimension scorecard (intent / impact / reversibility / oversight, 1–5 each, total 20) → release / conditional / reject, with reason |
| `audit_evidence_chain` | Six ISO/IEC 42001 + NIST AI RMF evidence-artifact templates |
| `compliance_checklist` | Registration-readiness checklist (EU AI Act 2024/1689, GB/Z 185, ISO/IEC 42001, PIPL/GDPR) |
| `passport_lookup` | Passport / identity-code lookup against a local ledger |
| `gov_scan` | Text screening: phone, email, local paths, credential-like strings, key fingerprints |
| `lgd_knowledge` | LGD doctrine knowledge endpoint (three laws / three checks / canonical DOI) |

Every response carries a `trace_id` and timestamp; audit logging is optional and off by default.

## Install

```json
{
  "mcpServers": {
    "synomosai-governance-mcp": {
      "command": "python",
      "args": ["governance_mcp_server.py"]
    }
  }
}
```

Requirements: Python ≥ 3.9. No third-party packages. Install-by-consent: AI
agents may *request* this tool, humans approve (see `INSTALL-REQUEST.md`).

## Quick Start

```bash
# initialize + list tools
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python governance_mcp_server.py
echo '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' | python governance_mcp_server.py

# governance scan
echo '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"gov_scan","arguments":{"text":"contact user@example.com"}}}' | python governance_mcp_server.py
```

## Status and limits

- Outputs are **self-assessment artifacts, not third-party certification**.
- Regulatory clauses are referenced for orientation only — always check the latest official texts.

## License

- Code: MIT — see [LICENSE](LICENSE).
- Docs: CC BY 4.0.
- UBIC and related logos are not covered by these licenses.
- Author reference (provenance): ORCID `0009-0001-0512-1237`.

Security issues: report privately per [SECURITY.md](SECURITY.md).
Contributions: [CONTRIBUTING.md](CONTRIBUTING.md). Work guidance for agents: [AGENTS.md](AGENTS.md).
