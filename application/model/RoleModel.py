from sqlalchemy.orm import Mapped
from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column
from application.util.MysqlUtil import mysql_db


class RoleModel(mysql_db.Model):
    __tablename__: str = "role"
    # 主键
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True, comment="主键，自增")
    # 角色名称
    name: Mapped[str] = mapped_column(String(16), nullable=True, comment="角色名称，长度为16")
    # 角色描述
    description: Mapped[str] = mapped_column(String(32), nullable=True, comment="角色描述，长度为32")
