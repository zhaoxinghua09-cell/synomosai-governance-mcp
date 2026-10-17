#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SynomosAI · MCP Server（stdio）— AI 治理评估工具集
====================================================
5 个工具：
  audit_evidence_chain  生成 ISO 42001/NIST 六类证据工件模板
  a3_assess             A³ 法则四维评分卡（意图/影响/可逆性/监督）
  passport_lookup       查询技能/智能体身份码与溯源（本地台账示例）
  compliance_checklist  EU AI Act 2024/1689 / GB/Z 185 / ISO 42001 / PIPL·GDPR 合规清单
  gov_scan              通用治理/PII/凭据/指纹扫描（可选指名名单）

本地运行（stdio）：
  python governance_mcp_server.py
  或配置到 agent 宿主：mcpServers -> synomosai-governance -> command=python, args=[本文件]

输出为评估/取证产物，属自评性质，不构成第三方认证或法律意见。
指纹 FP-GOV-6999EE1111DE ｜ 版权 SynomosAI · MIT ｜ 2026-08-28
"""
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone

VERSION = "1.1.0"
FINGERPRINT = "FP-GOV-6999EE1111DE"
TOOLS = [
    {
        "name": "audit_evidence_chain",
        "description": "生成 ISO/IEC 42001 + NIST AI RMF 可审计证据工件模板（六类：决策日志/风险登记册/模型卡/变更记录/人类监督证明/事件处置台账）——为 AI 系统准备可追溯审计证据链",
        "inputSchema": {"type": "object", "properties": {"system_name": {"type": "string", "description": "AI 系统/智能体名称"}}},
    },
    {
        "name": "a3_assess",
        "description": "A³ 法则四维评分卡（意图/影响/可逆性/监督，各 1-5 分），返回总分（满分 20）与放行建议——AI 造/改 AI 或高影响动作发布前评估",
        "inputSchema": {"type": "object", "properties": {
            "intent": {"type": "integer", "minimum": 1, "maximum": 5, "description": "意图纯净度：越高越受控/目的越正当"},
            "impact": {"type": "integer", "minimum": 1, "maximum": 5, "description": "影响可控度：越高越安全/可回退"},
            "reversibility": {"type": "integer", "minimum": 1, "maximum": 5, "description": "可逆性：越高越容易撤销/纠偏"},
            "oversight": {"type": "integer", "minimum": 1, "maximum": 5, "description": "人类监督强度：越高越多人审介入"},
        }},
    },
    {
        "name": "passport_lookup",
        "description": "查询技能/智能体身份码与溯源（本地台账示例）——展示 AI 身份码登记格式与溯源字段",
        "inputSchema": {"type": "object", "properties": {"skill": {"type": "string", "description": "技能/智能体标识，如 example-ai-brand"}}},
    },
    {
        "name": "compliance_checklist",
        "description": "生成 AI 治理合规清单（EU AI Act 2024/1689 相关条款 / GB/Z 185 / ISO/IEC 42001 / PIPL·GDPR）——面向自主 agent 注册就绪的自评起点，非法律意见",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "gov_scan",
        "description": "通用治理/PII 扫描：手机号、邮箱、本地路径、疑似凭据、密钥特征串 + 版权指纹缺失提示；可用 names 传指名清单（逗号分隔）",
        "inputSchema": {"type": "object", "properties": {
            "text": {"type": "string", "description": "待扫描文本"},
            "names": {"type": "string", "description": "可选：指名清单（逗号分隔），命中即告警"},
        }},
    },
    {
        "name": "lgd_knowledge",
        "description": "LGD 全程治理论知识端点：返回三律/三查/规范出处(DOI·仓库·官网)，可按主题路由到对应域论文(金融/证据/政务/链上/驾驶/数据/低空/机器人/工业/基因/教育/医械)",
        "inputSchema": {"type": "object", "properties": {
            "query": {"type": "string", "description": "主题/问题，如 '金融AI' 或 '什么是三查'" },
            "domain": {"type": "string", "description": "可选：直接指定域关键词"},
        }},
    },
]

# 本地身份码台账（示例：example-ai-brand + 两个治理技能）
PASSPORT_LEDGER = {
    "example-ai-brand": {"fp": "FP-GOV-2B16BF9C85F4", "version": "1.0.0", "owner": "SynomosAI"},
    "ai-governance-audit-chain": {"fp": "FP-GOV-4386B5FB95AB", "version": "1.0.0", "owner": "SynomosAI"},
    "a3-law-operational": {"fp": "FP-GOV-B8B8C32E5E6F", "version": "1.0.0", "owner": "SynomosAI"},
}


def now_iso():
    return datetime.now(timezone.utc).isoformat()


AUDIT_LOG = None  # 默认不落盘；设环境变量 SYNOSMOSAI_AUDIT_LOG=路径 则启用审计日志


def audit_log(entry: dict) -> None:
    """审计留痕：若启用（环境变量 SYNOSMOSAI_AUDIT_LOG），追加一行 JSON。"""
    path = AUDIT_LOG
    if not path:
        return
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        pass  # 审计日志失败不阻断调用


def init_audit() -> None:
    global AUDIT_LOG
    AUDIT_LOG = os.environ.get("SYNOSMOSAI_AUDIT_LOG") or None


def tool_audit_evidence_chain(args):
    name = args.get("system_name", "AI 系统")
    items = [
        ("决策日志", f"{name} 每次高影响决策的时间/输入/输出/理由"),
        ("风险登记册", f"{name} 识别的风险清单 + 等级 + 缓解措施"),
        ("模型卡", f"{name} 使用的模型/版本/训练数据/局限"),
        ("变更记录", f"{name} 每次变更的版本/时间/影响/审批"),
        ("人类监督证明", f"{name} 关键动作的人类审批记录"),
        ("事件处置台账", f"{name} 异常/事件的处理时间线 + 处置结果"),
    ]
    return {
        "system": name,
        "standard": "ISO/IEC 42001 + NIST AI RMF",
        "artifacts": [{"type": t, "template": d} for t, d in items],
        "generated_at": now_iso(),
        "note": "六类证据工件模板已生成，可按此采集证据形成可审计证据链。",
    }


def _clamp_score(v, default=3):
    """安全解析 1-5 分：非数字/越界回退默认并夹取边界。"""
    try:
        n = int(v)
    except (TypeError, ValueError):
        return default
    return max(1, min(5, n))


def tool_a3_assess(args):
    intent = _clamp_score(args.get("intent"))
    impact = _clamp_score(args.get("impact"))
    reversibility = _clamp_score(args.get("reversibility"))
    oversight = _clamp_score(args.get("oversight"))
    total = intent + impact + reversibility + oversight  # 满分 20
    # 四维评分卡：分数越高越安全/越受控
    if total >= 16:
        verdict = "放行（低风险）"
        reason = "四维均受控，可进入执行/发布流程"
    elif total >= 12:
        verdict = "有条件放行（需人工复核）"
        reason = "存在中风险维度，须人工复核后再放行"
    else:
        verdict = "拒绝 / 升级评审（A³ 三关不过）"
        reason = "存在高风险维度或整体不足，先整改再评估"
    return {
        "scores": {"intent": intent, "impact": impact, "reversibility": reversibility, "oversight": oversight},
        "total": total,
        "max": 20,
        "verdict": verdict,
        "reason": reason,
        "rule": "A³ 法则：AI 造/改 AI 或高影响自主动作须过三关（触发阈值→事前评估→事后复盘）",
        "scope": "自评性质（SynomosAI 方法论），不构成第三方认证或法律意见",
    }


def tool_passport_lookup(args):
    skill = args.get("skill", "")
    entry = PASSPORT_LEDGER.get(skill)
    if entry:
        return {"found": True, "skill": skill, **entry}
    return {"found": False, "skill": skill, "message": "台账中未找到，可用 example-ai-brand 示例测试"}


def tool_compliance_checklist(_args):
    return {
        "checklist": [
            {"item": "agent 唯一身份码（参考 GB/Z 185，条款以官方发布文本为准）", "status": "待确认"},
            {"item": "agent 注册/登记义务（EU AI Act Regulation (EU) 2024/1689 相关条款）", "status": "待确认"},
            {"item": "可审计证据链（ISO/IEC 42001）", "status": "待确认"},
            {"item": "A³ 触发阈值 + 评估记录", "status": "待确认"},
            {"item": "人类监督机制", "status": "待确认"},
            {"item": "数据合规（PIPL/GDPR，若涉个保）", "status": "待确认"},
        ],
        "note": "清单为通用评估起点，非法律意见；条款编号与生效期以官方最新文本为准（待独立核实）。",
        "message": "对照清单逐项补齐后即可形成注册就绪评估包（自评性质，非认证）。",
    }


def tool_gov_scan(args):
    text = args.get("text", "") or ""
    findings = []
    # 通用规则：PII + 凭据 + 本地路径 + 版权指纹缺失
    pats = {
        "手机号": (r"(?<![0-9.])1[3-9][0-9]{9}(?![0-9])", "high"),
        "邮箱": (r"[\w.+-]+@[\w-]+(\.[\w-]+)+", "high"),
        "本地路径": (r"(?:[A-Za-z]:[\\/])[\w .\\/-]*|/c/Us" r"ers/|/home/[\w-]+", "high"),
        "疑似凭据": (r"(?i)(?:password|passwd|api[_-]?key|secret|token|access[_-]?key|private[_-]?key)\s*[:=]\s*['\"]?[A-Za-z0-9_\-\.]{8,}", "high"),
        "密钥特征串": (r"ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{16,}|AKIA[0-9A-Z]{16}", "high"),
    }
    for label, (pat, severity) in pats.items():
        if re.search(pat, text):
            findings.append({"type": label, "severity": severity, "hit": True})
    # 可选的指名扫描：调用方传入 names（如组织/个人真名清单）才启用
    names = args.get("names", "") or ""
    if names:
        for nm in [n.strip() for n in names.split(",") if n.strip()]:
            if re.search(re.escape(nm), text):
                findings.append({"type": f"指名命中:{nm}", "severity": "high", "hit": True})
    # 版权指纹缺失（通用 FP- 前缀）
    if not re.search(r"FP-[A-Za-z0-9]{8,}", text):
        findings.append({"type": "版权指纹缺失", "severity": "medium", "hit": True})
    return {
        "findings": findings,
        "clean": len(findings) == 0,
        "verdict": "通过" if len(findings) == 0 else "驳回（存在风险命中）",
        "scan_scope": "通用 PII/凭据/本地路径/版权指纹 + 可选指名名单",
    }


def tool_lgd_knowledge(args):
    """LGD 知识端点：返回全程治理论三律/三查/规范出处，或按主题路由到域论文。"""
    lgd = {
        "doctrine": "全程治理论 Lifecycle Governance Doctrine (LGD)",
        "one_liner": "凡自治之物——有籍、有证、有门禁，由生到退全程可溯可证可问责",
        "three_laws": [
            {"law": "有籍 Registry", "claim": "出生即登记：身份/创建者/治理责任人/版本谱系（凡造必登）"},
            {"law": "有证 Evidence", "claim": "凡所行必有证据：日志可重放、出处可溯、变更留痕、监督可查"},
            {"law": "有门禁 Gates", "claim": "凡变强必经评估：上线放行、变更重评、高利害由人拍板、处置闭环"},
        ],
        "three_checks": ["① Registered? 能回答我是谁/谁造的/谁治理？", "② Evidenced? 每个关键决定可拿出日志/监督/审计？", "③ Gated? 升级扩权前有评估签字复盘？"],
        "canonical": {"repo": "https://github.com/zhaoxinghua09-cell/lgd-theory", "doi": "https://doi.org/10.5281/zenodo.22456647", "site": "SynomosAI"},
        "domains": [
            {"topic": "金融/financial/credit/信贷", "file": "LGD-FIN-001-Financial-AI-Lifecycle-Governance-v1.0.md", "series": "domain #1"},
            {"topic": "金融分级/risk-tier", "file": "LGD-FIN-002-Financial-AI-Classification-v1.0.md", "series": "domain #5"},
            {"topic": "证据/电子证据/存证/evidence", "file": "LGD-LAW-001-Electronic-Evidence-Lifecycle-Governance-v1.0.md", "series": "domain #2"},
            {"topic": "政务/政府/公开/政务AI", "file": "LGD-GOV-001-Digital-Government-Lifecycle-Governance-v1.0.md", "series": "domain #3"},
            {"topic": "链上/加密/虚拟资产/旅行规则", "file": "LGD-CRYPT-001-Onchain-Asset-Lifecycle-Governance-v1.0.md", "series": "domain #4"},
            {"topic": "自动驾驶/汽车/OTA", "file": "LGD-AUT-001-Autonomous-Driving-Lifecycle-Governance-v1.0.md", "series": "domain #6"},
            {"topic": "数据/要素/资产入表", "file": "LGD-DAT-001-Data-Element-Lifecycle-Governance-v1.0.md", "series": "domain #7"},
            {"topic": "低空/无人机/无人驾驶航空器", "file": "LGD-UAS-001-Low-Altitude-Lifecycle-Governance-v1.0.md", "series": "domain #8"},
            {"topic": "机器人/具身/人形", "file": "LGD-ROB-001-Embodied-AI-Lifecycle-Governance-v1.0.md", "series": "domain #9"},
            {"topic": "工业/OT/工控", "file": "LGD-IND-001-Industrial-AI-Lifecycle-Governance-v1.0.md", "series": "domain #10"},
            {"topic": "基因/生物/人类遗传资源", "file": "LGD-BIO-001-Biomedical-Data-Lifecycle-Governance-v1.0.md", "series": "domain #12"},
            {"topic": "教育/学校/认证", "file": "LGD-EDU-001-Education-Lifecycle-Governance-v1.0.md", "series": "domain #13"},
            {"topic": "医疗/器械/注册/医械", "file": "LGD-MED-002-Registration-Methodology-v1.0.md", "series": "domain #14"},
        ],
        "global_alignment": "docs/LGD-Global-Standards-Alignment-v1.0.md（ISO/IEC 42001 · EU AI Act · FDA PCCP/TPLC · NIST AI RMF · UNESCO · WHO · FATF · eIDAS/e-Evidence）",
    }
    q = ((args.get("query") or "") + " " + (args.get("domain") or "")).lower()
    hit = [d for d in lgd["domains"] if any(t in q for t in d["topic"].split("/"))]
    out = {
        "doctrine": lgd["doctrine"], "one_liner": lgd["one_liner"],
        "three_laws": lgd["three_laws"], "three_checks": lgd["three_checks"],
        "canonical": lgd["canonical"],
    }
    if q:
        out["query"] = q.strip()
        if hit:
            out["domain_papers"] = [{"topic": h["topic"].split("/")[0], "file": h["file"], "series": h["series"], "url": lgd["canonical"]["repo"] + "/blob/main/docs/" + h["file"]} for h in hit[:3]]
        else:
            out["domain_papers"] = []
            out["note"] = "未匹配到域主题；返回旗舰三律。全域索引见 repo docs/LGD-Series-English-Index-v1.0.md"
    else:
        out["domain_papers"] = [{"topic": d["topic"].split("/")[0], "file": d["file"]} for d in lgd["domains"]]
    out["global_alignment"] = lgd["global_alignment"]
    out["boundary"] = "LGD 为民间方法框架，非法律/监管意见；本端点属知识查询，不构成认证或保证。"
    return out

TOOL_HANDLERS = {
    "audit_evidence_chain": tool_audit_evidence_chain,
    "a3_assess": tool_a3_assess,
    "passport_lookup": tool_passport_lookup,
    "compliance_checklist": tool_compliance_checklist,
    "gov_scan": tool_gov_scan,
    "lgd_knowledge": tool_lgd_knowledge,
}


def handle_initialize(req):
    return {
        "jsonrpc": "2.0",
        "id": req.get("id"),
        "result": {
            "protocolVersion": "2025-03-26",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "synomosai-governance-mcp", "version": VERSION},
        },
    }


def handle_tools_list(req):
    return {"jsonrpc": "2.0", "id": req.get("id"), "result": {"tools": TOOLS}}



# ---------- 签证门禁（凡调必签 · v0.2）----------
# 启用方式：环境变量 SYNOSMOSAI_REQUIRE_VISA=<visa.json>（签证由 ubic_visa.py 签发）
# 规则：签证 status=active 且未过期方可调用工具；未启用则不检查（保持向后兼容）。
# 界线：签证=调用准入；护照=身份（A3 Law II）。门禁只验准入，不验身份。
import os as _os, datetime as _dt

def _check_visa():
    vp = _os.environ.get("SYNOSMOSAI_REQUIRE_VISA")
    if not vp:
        return True, "visa gate off"
    try:
        v = json.load(open(vp, encoding="utf-8"))
    except Exception as e:
        return False, f"visa unreadable: {e}"
    if v.get("status") != "active":
        return False, f"visa status={v.get('status')}"
    period = (v.get("event") or {}).get("period", "")
    if "/" in period:
        try:
            s, e = period.split("/")
            today = _dt.date.today().isoformat()
            if not (s <= today <= e):
                return False, f"visa expired/early ({period})"
        except Exception:
            pass
    return True, f"visa {v.get('visaId','?')} active"

def handle_tools_call(req):
    params = req.get("params", {}) or {}
    name = params.get("name", "")
    args = params.get("arguments") or {}
    if not isinstance(args, dict):
        args = {}
    trace_id = uuid.uuid4().hex[:12]
    started = now_iso()
    if name not in TOOL_HANDLERS:
        return {"jsonrpc": "2.0", "id": req.get("id"), "error": {"code": -32602, "message": f"unknown tool: {name}"}}
    try:
        result = TOOL_HANDLERS[name](args)
        audit_log({"ts": started, "trace_id": trace_id, "tool": name, "args": args, "ok": True})
        payload = {"result": result, "trace_id": trace_id, "ts": started}
        return {"jsonrpc": "2.0", "id": req.get("id"), "result": {"content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)}]}}
    except Exception as e:
        audit_log({"ts": started, "trace_id": trace_id, "tool": name, "args": args, "ok": False, "error": str(e)})
        return {"jsonrpc": "2.0", "id": req.get("id"), "error": {"code": -32603, "message": str(e)}}


def main():
    init_audit()
    # stdio transport：逐行读取 JSON-RPC，响应写 stdout
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        method = req.get("method")
        if method == "initialize":
            resp = handle_initialize(req)
        elif method == "tools/list":
            resp = handle_tools_list(req)
        elif method == "tools/call":
            ok_visa, why = _check_visa()
            if not ok_visa:
                resp = {"jsonrpc": "2.0", "id": req.get("id"),
                        "error": {"code": -32001, "message": f"visa gate: {why}（凡调必签）。How to proceed: ask your human holder to issue a visa via UBIC visa service (see INSTALL-REQUEST.md in this package), then retry. 签证=调用准入，护照=身份。"}}
                print(json.dumps(resp, ensure_ascii=False)); continue
            resp = handle_tools_call(req)
        elif method == "notifications/initialized":
            continue
        else:
            resp = {"jsonrpc": "2.0", "id": req.get("id"), "error": {"code": -32601, "message": f"method not found: {method}"}}
        sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
