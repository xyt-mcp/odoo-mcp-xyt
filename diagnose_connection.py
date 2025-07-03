#!/usr/bin/env python3
"""
诊断 Odoo 连接问题的脚本
"""
import sys
import os
import json
import socket
import urllib.parse
import urllib.request
import ssl
import xmlrpc.client
from urllib.error import URLError, HTTPError

def test_basic_connectivity():
    """测试基本网络连接"""
    print("=== 基本网络连接测试 ===")
    
    config_file = "odoo_config.json"
    if not os.path.exists(config_file):
        print(f"✗ 配置文件 {config_file} 不存在")
        return False
        
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    url = config['url']
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.netloc
    port = parsed.port or (443 if parsed.scheme == 'https' else 80)
    
    print(f"目标服务器: {hostname}:{port}")
    
    # 1. DNS 解析测试
    try:
        ip = socket.gethostbyname(hostname)
        print(f"✓ DNS 解析成功: {hostname} -> {ip}")
    except socket.gaierror as e:
        print(f"✗ DNS 解析失败: {e}")
        return False
    
    # 2. TCP 连接测试
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((hostname, port))
        sock.close()
        if result == 0:
            print(f"✓ TCP 连接成功: {hostname}:{port}")
        else:
            print(f"✗ TCP 连接失败: {hostname}:{port}")
            return False
    except Exception as e:
        print(f"✗ TCP 连接测试异常: {e}")
        return False
    
    # 3. HTTP/HTTPS 请求测试
    try:
        print(f"\n--- HTTP 请求测试 ---")
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Odoo-MCP-Test/1.0')
        
        # 创建 SSL 上下文
        if parsed.scheme == 'https':
            ssl_context = ssl.create_default_context()
            # 如果需要忽略 SSL 验证，可以取消注释下面的行
            # ssl_context.check_hostname = False
            # ssl_context.verify_mode = ssl.CERT_NONE
        else:
            ssl_context = None
            
        with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
            status = response.getcode()
            headers = dict(response.headers)
            print(f"✓ HTTP 请求成功: 状态码 {status}")
            print(f"  服务器: {headers.get('Server', 'Unknown')}")
            print(f"  内容类型: {headers.get('Content-Type', 'Unknown')}")
            
            # 检查是否是 Odoo 服务器
            content = response.read(1024).decode('utf-8', errors='ignore')
            if 'odoo' in content.lower() or 'openerp' in content.lower():
                print("✓ 检测到 Odoo 服务器")
            else:
                print("⚠ 未检测到明显的 Odoo 标识")
                
    except HTTPError as e:
        print(f"✗ HTTP 请求失败: {e.code} {e.reason}")
        return False
    except URLError as e:
        print(f"✗ URL 请求失败: {e.reason}")
        return False
    except Exception as e:
        print(f"✗ HTTP 请求异常: {e}")
        return False
    
    return True

def test_xmlrpc_endpoints():
    """测试 XML-RPC 端点"""
    print("\n=== XML-RPC 端点测试 ===")
    
    with open("odoo_config.json", 'r') as f:
        config = json.load(f)
    
    url = config['url']
    
    # 测试 common 端点
    common_url = f"{url}/xmlrpc/2/common"
    print(f"测试 common 端点: {common_url}")
    
    try:
        # 创建简单的 XML-RPC 客户端
        common = xmlrpc.client.ServerProxy(common_url)
        
        # 测试 version 方法
        version_info = common.version()
        print(f"✓ Common 端点连接成功")
        print(f"  服务器版本: {version_info.get('server_version', 'Unknown')}")
        print(f"  协议版本: {version_info.get('protocol_version', 'Unknown')}")
        
        return True
        
    except xmlrpc.client.Fault as e:
        print(f"✗ XML-RPC 错误: {e}")
        return False
    except Exception as e:
        print(f"✗ XML-RPC 连接失败: {e}")
        return False

def test_authentication():
    """测试认证"""
    print("\n=== 认证测试 ===")
    
    with open("odoo_config.json", 'r') as f:
        config = json.load(f)
    
    try:
        common_url = f"{config['url']}/xmlrpc/2/common"
        common = xmlrpc.client.ServerProxy(common_url)
        
        print(f"尝试认证:")
        print(f"  数据库: {config['db']}")
        print(f"  用户名: {config['username']}")
        print(f"  密码: {'*' * len(config['password'])}")
        
        uid = common.authenticate(
            config['db'], 
            config['username'], 
            config['password'], 
            {}
        )
        
        if uid:
            print(f"✓ 认证成功! 用户 ID: {uid}")
            return True
        else:
            print("✗ 认证失败: 用户名或密码错误")
            return False
            
    except Exception as e:
        print(f"✗ 认证过程异常: {e}")
        return False

def check_proxy_settings():
    """检查代理设置"""
    print("\n=== 代理设置检查 ===")
    
    proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']
    proxy_found = False
    
    for var in proxy_vars:
        value = os.environ.get(var)
        if value:
            print(f"发现代理设置: {var} = {value}")
            proxy_found = True
    
    if not proxy_found:
        print("未发现系统代理设置")
    
    # 检查配置文件中是否有代理设置
    with open("odoo_config.json", 'r') as f:
        config = json.load(f)
    
    if 'proxy' in config:
        print(f"配置文件中的代理设置: {config['proxy']}")
    else:
        print("配置文件中未设置代理")

def main():
    """主函数"""
    print("🔍 Odoo 连接诊断工具")
    print("=" * 50)
    
    # 检查代理设置
    check_proxy_settings()
    
    # 基本连接测试
    if not test_basic_connectivity():
        print("\n❌ 基本连接测试失败，请检查网络设置")
        return False
    
    # XML-RPC 端点测试
    if not test_xmlrpc_endpoints():
        print("\n❌ XML-RPC 端点测试失败")
        return False
    
    # 认证测试
    if not test_authentication():
        print("\n❌ 认证测试失败")
        return False
    
    print("\n🎉 所有测试通过！连接配置正确。")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
