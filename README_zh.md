# Odoo MCP 服务器

一个与 Odoo ERP 系统集成的 MCP 服务器实现，使 AI 助手能够通过模型上下文协议（Model Context Protocol）与 Odoo 数据和功能进行交互。

## 快速开始

1. **安装 Python 3.10+** 并创建虚拟环境
2. **克隆并安装** 项目：
   ```bash
   git clone <repository-url>
   cd odoo-mcp-xyt
   pip install -e .
   ```
3. **配置 Odoo 连接** 在 `odoo_config.json` 中：
   ```json
   {
     "url": "https://your-odoo-instance.com",
     "db": "your-database-name",
     "username": "your-username",
     "password": "your-password-or-api-key"
   }
   ```
4. **运行服务器**：
   ```bash
   python -m odoo_mcp
   ```
5. **使用 MCP Inspector 测试**：
   ```bash
   npx @modelcontextprotocol/inspector
   ```

## 功能特性

- **全面的 Odoo 集成**：完全访问 Odoo 模型、记录和方法
- **XML-RPC 通信**：通过 XML-RPC 安全连接到 Odoo 实例
- **灵活配置**：支持配置文件和环境变量
- **资源模式系统**：基于 URI 的 Odoo 数据结构访问
- **错误处理**：为常见 Odoo API 问题提供清晰的错误消息
- **无状态操作**：干净的请求/响应周期，确保可靠集成

## 工具

- **execute_method**

  - 在 Odoo 模型上执行自定义方法
  - 输入参数：
    - `model` (字符串): 模型名称（例如 'res.partner'）
    - `method` (字符串): 要执行的方法名称
    - `args` (可选数组): 位置参数
    - `kwargs` (可选对象): 关键字参数
  - 返回：包含方法结果和成功指示器的字典

- **search_employee**

  - 按姓名搜索员工
  - 输入参数：
    - `name` (字符串): 要搜索的姓名（或姓名的一部分）
    - `limit` (可选数字): 返回结果的最大数量（默认 20）
  - 返回：包含成功指示器、匹配员工姓名和 ID 列表以及任何错误消息的对象

- **search_holidays**
  - 在指定日期范围内搜索假期
  - 输入参数：
    - `start_date` (字符串): 开始日期，格式为 YYYY-MM-DD
    - `end_date` (字符串): 结束日期，格式为 YYYY-MM-DD
    - `employee_id` (可选数字): 可选的员工 ID 来过滤假期
  - 返回：包含成功指示器、找到的假期列表以及任何错误消息的对象

## 资源

- **odoo://models**

  - 列出 Odoo 系统中所有可用的模型
  - 返回：模型信息的 JSON 数组

- **odoo://model/{model_name}**

  - 获取特定模型的信息，包括字段
  - 示例：`odoo://model/res.partner`
  - 返回：包含模型元数据和字段定义的 JSON 对象

- **odoo://record/{model_name}/{record_id}**

  - 通过 ID 获取特定记录
  - 示例：`odoo://record/res.partner/1`
  - 返回：包含记录数据的 JSON 对象

- **odoo://search/{model_name}/{domain}**
  - 搜索匹配域条件的记录
  - 示例：`odoo://search/res.partner/[["is_company","=",true]]`
  - 返回：匹配记录的 JSON 数组（默认限制为 10 条）

## 配置

### Odoo 连接设置

1. 创建名为 `odoo_config.json` 的配置文件：

```json
{
  "url": "https://your-odoo-instance.com",
  "db": "your-database-name",
  "username": "your-username",
  "password": "your-password-or-api-key"
}
```

2. 或者，使用环境变量：
   - `ODOO_URL`: 你的 Odoo 服务器 URL
   - `ODOO_DB`: 数据库名称
   - `ODOO_USERNAME`: 登录用户名
   - `ODOO_PASSWORD`: 密码或 API 密钥
   - `ODOO_TIMEOUT`: 连接超时时间（秒，默认：30）
   - `ODOO_VERIFY_SSL`: 是否验证 SSL 证书（默认：true）
   - `HTTP_PROXY`: 强制 ODOO 连接使用 HTTP 代理

### 与 Claude Desktop 一起使用

将以下内容添加到你的 `claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "odoo": {
      "command": "python",
      "args": ["-m", "odoo_mcp"],
      "env": {
        "ODOO_URL": "https://your-odoo-instance.com",
        "ODOO_DB": "your-database-name",
        "ODOO_USERNAME": "your-username",
        "ODOO_PASSWORD": "your-password-or-api-key"
      }
    }
  }
}
```

## 安装和设置

### 前置要求

- Python 3.10+（MCP 兼容性要求）
- Node.js（用于 MCP Inspector）

### 1. 环境设置

创建 Python 3.10+ 环境：

```bash
# 使用 conda
conda create -n odoo-mcp python=3.10 -y
conda activate odoo-mcp

# 或使用 venv
python3.10 -m venv odoo-mcp
source odoo-mcp/bin/activate  # Windows: odoo-mcp\Scripts\activate
```

### 2. 安装依赖

```bash
# 以开发模式安装项目
pip install -e .

# 安装 MCP CLI 工具用于调试
pip install 'mcp[cli]'
```

### 3. 配置

使用你的 Odoo 连接详情创建 `odoo_config.json`：

```json
{
  "url": "https://your-odoo-instance.com",
  "db": "your-database-name",
  "username": "your-username",
  "password": "your-password-or-api-key"
}
```

## 运行和调试

### 方法 1：直接 Python 执行（推荐）

```bash
# 使用已安装的包命令
/path/to/your/python/bin/odoo-mcp-xyt

# 使用 Python 模块
/path/to/your/python/bin/python -m odoo_mcp

# 使用详细日志脚本
/path/to/your/python/bin/python run_server.py
```

### 方法 2：用于开发和测试的 MCP Inspector

#### 步骤 1：启动 MCP Inspector

```bash
# 启动 inspector
npx @modelcontextprotocol/inspector
```

这将输出类似以下内容：

```
⚙️ Proxy server listening on 127.0.0.1:6277
🔑 Session token: your-session-token-here
🔗 Open inspector with token pre-filled:
   http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=your-session-token-here
🔍 MCP Inspector is up and running at http://127.0.0.1:6274 🚀
```

#### 步骤 2：在 Inspector 中配置服务器

1. 在浏览器中打开 Inspector URL
2. 如果提示，输入会话令牌
3. 点击 "Add Server" 并使用此配置：

```json
{
  "name": "Odoo MCP Server",
  "command": "/path/to/your/python/bin/python",
  "args": ["/path/to/your/project/start_for_inspector.py"],
  "env": {}
}
```

**实际路径示例：**

```json
{
  "name": "Odoo MCP Server",
  "command": "/Users/username/miniconda3/envs/odoo-mcp/bin/python",
  "args": ["/Users/username/code/odoo-mcp-xyt/start_for_inspector.py"],
  "env": {}
}
```

### 方法 3：使用 MCP 开发工具（备选）

```bash
# 基本用法
mcp dev src/odoo_mcp/server.py

# 带额外依赖
mcp dev src/odoo_mcp/server.py --with pandas --with numpy

# 挂载本地代码用于开发
mcp dev src/odoo_mcp/server.py --with-editable .
```

**注意：** 如果遇到 `uv` 相关错误，请使用方法 1 或 2。

## 故障排除

### 常见问题

1. **Python 版本错误**：确保使用 Python 3.10+

   ```bash
   python --version  # 应显示 3.10 或更高版本
   ```

2. **连接错误**：测试你的 Odoo 连接

   ```bash
   python diagnose_connection.py
   ```

3. **MCP Inspector JSON 错误**：使用方法 2（手动 Inspector 设置）而不是 `mcp dev`

4. **导入错误**：确保所有依赖都已安装
   ```bash
   pip install -e .
   pip install 'mcp[cli]'
   ```

### 调试工具

- **连接诊断**：`python diagnose_connection.py`
- **详细日志**：`python run_server.py`（在 `logs/` 目录中创建日志）
- **MCP Inspector**：用于交互式测试和调试

## 使用示例

一旦你的服务器运行起来，你可以使用 MCP Inspector 测试它或将其与 Claude Desktop 集成。以下是一些示例操作：

### 在 MCP Inspector 中测试工具

1. **搜索员工**：

   ```json
   {
     "name": "search_employee",
     "arguments": {
       "name": "张三",
       "limit": 10
     }
   }
   ```

2. **执行自定义方法**：

   ```json
   {
     "name": "execute_method",
     "arguments": {
       "model": "res.partner",
       "method": "search_read",
       "args": [[["is_company", "=", true]], ["name", "email"]]
     }
   }
   ```

3. **搜索假期**：

   ```json
   {
     "name": "search_holidays",
     "arguments": {
       "start_date": "2024-01-01",
       "end_date": "2024-12-31",
       "employee_id": 1
     }
   }
   ```

### 在 MCP Inspector 中测试资源

1. **列出所有模型**：`odoo://models`
2. **获取合作伙伴模型信息**：`odoo://model/res.partner`
3. **获取特定合作伙伴**：`odoo://record/res.partner/1`
4. **搜索公司**：`odoo://search/res.partner/[["is_company","=",true]]`

## 参数格式指南

在使用 Odoo 的 MCP 工具时，请注意以下参数格式指南：

1. **域参数**：

   - 支持以下域格式：
     - 列表格式：`[["field", "operator", value], ...]`
     - 对象格式：`{"conditions": [{"field": "...", "operator": "...", "value": "..."}]}`
     - 以上任一格式的 JSON 字符串
   - 示例：
     - 列表格式：`[["is_company", "=", true]]`
     - 对象格式：`{"conditions": [{"field": "date_order", "operator": ">=", "value": "2025-03-01"}]}`
     - 多条件：`[["date_order", ">=", "2025-03-01"], ["date_order", "<=", "2025-03-31"]]`

2. **字段参数**：
   - 应该是字段名称的数组：`["name", "email", "phone"]`
   - 服务器会尝试将字符串输入解析为 JSON

## UVX 方式安装

如果你想使用 UVX 方式安装，可以在 Claude Desktop 配置中使用：

```json
{
  "mcpServers": {
    "odoo-mcp-xyt": {
      "command": "uvx",
      "args": ["odoo-mcp-xyt==2.0.0.0"],
      "env": {
        "ODOO_URL": "",
        "ODOO_DB": "",
        "ODOO_USERNAME": "",
        "ODOO_PASSWORD": ""
      }
    }
  }
}
```

### Docker 使用

```json
{
  "mcpServers": {
    "odoo": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "ODOO_URL",
        "-e",
        "ODOO_DB",
        "-e",
        "ODOO_USERNAME",
        "-e",
        "ODOO_PASSWORD",
        "mcp/odoo"
      ],
      "env": {
        "ODOO_URL": "https://your-odoo-instance.com",
        "ODOO_DB": "your-database-name",
        "ODOO_USERNAME": "your-username",
        "ODOO_PASSWORD": "your-password-or-api-key"
      }
    }
  }
}
```

## 构建

Docker 构建：

```bash
docker build -t mcp/odoo:latest -f Dockerfile .
```

## 许可证

此 MCP 服务器采用 MIT 许可证。
