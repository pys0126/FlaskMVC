"""
服务器配置
"""
import os
from datetime import timedelta
from application.config import YAML_CONTENT


class ServerConfig:
    SERVER_CONFIG: dict = YAML_CONTENT.get("ServerConfig")  # 获取服务器配置
    # 服务器配置项
    host: str = SERVER_CONFIG.get("host", "0.0.0.0")  # 服务访问地址
    port: int = int(SERVER_CONFIG.get("port", 6868))  # 服务访问端口
    workers: int = int(SERVER_CONFIG.get("workers", 1))  # 服务的进程数

    # 其他配置项
    log_dir: str = SERVER_CONFIG.get("log_path", "logs")  # 日志目录路径
    # Token过期时间，默认7天
    token_expire: int = int(SERVER_CONFIG.get("token_expire", int(timedelta(days=7).total_seconds())))
    token_name: str = "Authorization"  # Token在Header中的名称和session的键名
    secret_key: str = SERVER_CONFIG.get("secret_key", os.urandom(16).hex())  # Token加密密钥

    file_max_size: int = int(SERVER_CONFIG.get("file_max_size", 1024 * 1024 * 3))  # 文件最大上传大小（字节），默认3M

    # 默认超级管理员
    super_admin_username: str = SERVER_CONFIG.get("super_admin_username", "admin")  # 用户名
    super_admin_password: str = SERVER_CONFIG.get("super_admin_password", "admin")  # 密码

