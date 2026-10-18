# 贡献指南 / Contributing

欢迎为本治理 MCP 服务器提改进。请保持「纯标准库、零网络外发、自评非认证」的设计纪律。

## 提交流程

1. fork 本仓或在分支上改动；
2. 保持 JSON-RPC 接口与 `tools/list` 描述向后兼容；
3. 新增工具时同步更新 `README.md` 工具表与 `llms.txt` / `llms-full.txt`；
4. 自测 `initialize` / `tools/list` / 目标 `tools/call` 均返回合法 JSON-RPC；
5. 提交 Pull Request，说明改动了哪个工具或文档。

## 不要做的事

- 不要新增任何网络外发行为。
- 不要把自评输出表述为第三方认证。
- 不要改 `LICENSE` 与 README「Author & license」中的权属 / 许可口径。
- 不要提交密钥、令牌或真实个人数据。

安全问题请走 [SECURITY.md](SECURITY.md) 的私下报告渠道。

联系：zhaoxinghua09@gmail.com ｜ ORCID `0009-0001-0512-1237`
