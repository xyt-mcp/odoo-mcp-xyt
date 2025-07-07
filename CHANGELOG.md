# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0.0] - 2025-01-07

### Added

- 完整的运行和调试指南
- 中文版 README 文档 (README_zh.md)
- MCP Inspector 配置和使用说明
- 连接诊断工具 (diagnose_connection.py)
- Inspector 专用启动脚本 (start_for_inspector.py)
- 新增合作伙伴搜索工具 (search_partner, search_partner_by_name)
- 新增日历创建工具 (create_calendar)
- 三种运行方式：直接执行、MCP Inspector、开发工具
- 故障排除指南和使用示例
- 详细的安装和环境设置指南

### Enhanced

- 更新了 README.md 添加详细的安装、运行和调试指南
- 增强了服务器功能，支持更多 Odoo 操作
- 改进了错误处理和日志记录
- 优化了 Docker 支持

### Fixed

- 解决了 MCP Inspector 的 JSON 解析错误
- 修复了 Python 版本兼容性问题
- 改进了连接稳定性和错误提示

## [0.0.3] - 2025-03-18

### Fixed

- Fixed `OdooClient` class by adding missing methods: `get_models()`, `get_model_info()`, `get_model_fields()`, `search_read()`, and `read_records()`
- Ensured compatibility with different Odoo versions by using only basic fields when retrieving model information

### Added

- Support for retrieving all models from an Odoo instance
- Support for retrieving detailed information about specific models
- Support for searching and reading records with various filtering options

## [0.0.2] - 2025-03-18

### Fixed

- Added missing dependencies in pyproject.toml: `mcp>=0.1.1`, `requests>=2.31.0`, `xmlrpc>=0.4.1`

## [0.0.1] - 2025-03-18

### Added

- Initial release with basic Odoo XML-RPC client support
- MCP Server integration for Odoo
- Command-line interface for quick setup and testing
