from sqlalchemy.orm import Mapped
from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column
from application.util.MysqlUtil import mysql_db
from application.util.TimeUtil import now_timestamp


class RoleModel(mysql_db.Model):
    __tablename__: str = "role"
    # 主键
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True, comment="主键，自增")
    # 角色名称
    name: Mapped[str] = mapped_column(String(16), nullable=True, comment="角色名称，长度为16")
    # 角色描述
    description: Mapped[str] = mapped_column(String(32), nullable=True, comment="角色描述，长度为32")
    # 更新时间，默认为now_timestamp生成，更新时为now_timestamp生成
    update_timestamp: Mapped[int] = mapped_column(Integer, insert_default=now_timestamp(), onupdate=now_timestamp(),
                                                  nullable=True, comment="更新时间戳")
    # 创建时间，默认为now_timestamp生成的
    create_timestamp: Mapped[int] = mapped_column(Integer, insert_default=now_timestamp(), nullable=True,
                                                  comment="创建时间戳")
