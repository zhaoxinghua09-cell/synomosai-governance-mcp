# SynomosAI Governance MCP v1.1.0 — 零依赖容器（仅 Python 标准库）
FROM python:3.12-slim
WORKDIR /app
COPY governance_mcp_server.py openapi.yaml ./
# 签证门禁（可选）：挂载签证文件并启用环境变量
#   docker run -e SYNOSMOSAI_REQUIRE_VISA=/app/visa.json -v ./visa.json:/app/visa.json ...
ENV PYTHONUNBUFFERED=1
# MCP over stdio（容器内以 stdin/stdout 通信）；HTTP 桥接时自行映射端口并加载 openapi.yaml
ENTRYPOINT ["python", "governance_mcp_server.py"]
