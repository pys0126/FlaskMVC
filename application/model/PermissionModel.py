from sqlalchemy.orm import Mapped
from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column
from application.util.MysqlUtil import mysql_db


class PermissionModel(mysql_db.Model):
    __tablename__: str = "permission"
    # 主键
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True, comment="主键，自增")
    # 权限名称
    name: Mapped[str] = mapped_column(String(16), nullable=True, comment="权限名称，如“查看用户信息”、“修改用户信息”、“删除用户信息”，长度为16")
    # 权限模块
    module: Mapped[str] = mapped_column(String(16), nullable=True, comment="权限所属模块，如“用户管理”、“文章发布”等，长度为16")
    # 权限操作
    action: Mapped[str] = mapped_column(String(16), nullable=True, comment="权限操作，如“读取”、“写入”、“删除”，长度为16")
