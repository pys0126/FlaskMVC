from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from application.util.MysqlUtil import mysql_db
from application.util.TimeUtil import now_timestamp


class UserRoleModel(mysql_db.Model):
    """
    用户-角色关联表
    """
    __tablename__: str = "user_role"
    # 主键
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True, comment="主键，自增")
    # 用户ID
    user_id: Mapped[int] = mapped_column(Integer, nullable=True, comment="用户ID")
    # 角色ID
    role_id: Mapped[int] = mapped_column(Integer, nullable=True, comment="角色ID")
    # 更新时间，默认为now_timestamp生成，更新时为now_timestamp生成
    update_timestamp: Mapped[int] = mapped_column(Integer, insert_default=now_timestamp(), onupdate=now_timestamp(),
                                                  nullable=True, comment="更新时间戳")
    # 创建时间，默认为now_timestamp生成的
    create_timestamp: Mapped[int] = mapped_column(Integer, insert_default=now_timestamp(), nullable=True,
                                                  comment="创建时间戳")
