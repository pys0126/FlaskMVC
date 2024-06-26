"""
数据库配置
"""
from application.config import YAML_CONTENT


# 获取数据库配置
DATABASE_CONFIG: dict = YAML_CONTENT.get("DatabaseConfig")


class MysqlConfig:
    """
    Mysql数据库配置
    """
    MYSQL_CONFIG: dict = DATABASE_CONFIG.get("MysqlConfig")  # 获取Mysql数据库配置项
    host: str = MYSQL_CONFIG.get("host", "127.0.0.1")  # 数据库主机名
    port: int = int(MYSQL_CONFIG.get("port", 3306))  # 数据库端口
    username: str = MYSQL_CONFIG.get("username", "root")  # 数据库用户名
    password: str = MYSQL_CONFIG.get("password", "root")  # 数据库密码
    database_name: str = MYSQL_CONFIG.get("database_name", "task_system")  # 数据库名称


class SqlalchemyConfig:
    """
    Sqlalchemy配置
    """
    SQLALCHEMY_CONFIG: dict = DATABASE_CONFIG.get("SqlalchemyConfig")  # 获取Mysql数据库配置项
    on_echo: bool = SQLALCHEMY_CONFIG.get("on_echo")  # 是否开启查询日志


class RedisConfig:
    """
    Redis配置
    """
    REDIS_CONFIG: dict = DATABASE_CONFIG.get("RedisConfig")  # 获取Redis配置项
    host: str = REDIS_CONFIG.get("host", "127.0.0.1")  # Redis主机名
    port: int = int(REDIS_CONFIG.get("port", 6379))  # Redis端口
    password: str = REDIS_CONFIG.get("password", "")  # Redis密码
    db: int = REDIS_CONFIG.get("db", 0)  # Redis数据库


