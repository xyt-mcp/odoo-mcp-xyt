#!/usr/bin/env python3
"""
启动 MCP 服务器供 Inspector 使用
"""
import sys
import os
import asyncio

# 确保可以导入我们的模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from odoo_mcp.server import mcp

def main():
    """启动 MCP 服务器"""
    try:
        print("Starting Odoo MCP Server for Inspector...", file=sys.stderr)
        print(f"Python version: {sys.version}", file=sys.stderr)
        
        # 检查环境变量
        odoo_vars = {k: v for k, v in os.environ.items() if k.startswith('ODOO_')}
        if odoo_vars:
            print("Environment variables:", file=sys.stderr)
            for k, v in odoo_vars.items():
                if k == 'ODOO_PASSWORD':
                    print(f"  {k}: ***hidden***", file=sys.stderr)
                else:
                    print(f"  {k}: {v}", file=sys.stderr)
        
        # 使用 run() 方法启动服务器
        mcp.run()
        
    except KeyboardInterrupt:
        print("Server stopped by user", file=sys.stderr)
        return 0
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
