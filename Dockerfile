# SynomosAI Governance MCP v1.2.0 — 零依赖容器（仅 Python 标准库）
# 默认以 Streamable HTTP 模式启动（POST /mcp，端口 8080）；也支持 stdio（--stdio）
FROM python:3.12-slim
WORKDIR /app
COPY governance_mcp_server.py openapi.yaml ./
# 签证门禁（可选）：挂载签证文件并启用环境变量
#   docker run -e SYNOSMOSAI_REQUIRE_VISA=/app/visa.json -v ./visa.json:/app/visa.json ...
ENV PYTHONUNBUFFERED=1
ENV MCP_HTTP_PORT=8080
EXPOSE 8080
# Streamable HTTP（云端托管/远程调用）：POST /mcp
# 本地 stdio 模式：docker run ... <image> --stdio（或 python governance_mcp_server.py）
ENTRYPOINT ["python", "governance_mcp_server.py"]
CMD ["--http"]
