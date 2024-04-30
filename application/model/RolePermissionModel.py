from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from application.util.MysqlUtil import mysql_db
from application.util.TimeUtil import now_timestamp


class RolePermissionModel(mysql_db.Model):
    """
    角色-权限关联表
    """
    __tablename__: str = "role_permission"
    # 主键
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True, comment="主键，自增")
    # 角色ID
    role_id: Mapped[int] = mapped_column(Integer, nullable=True, comment="角色ID")
    # 权限ID
    permission_id: Mapped[int] = mapped_column(Integer, nullable=True, comment="权限ID")
    # 更新时间，默认为now_timestamp生成，更新时为now_timestamp生成
    update_timestamp: Mapped[int] = mapped_column(Integer, insert_default=now_timestamp(), onupdate=now_timestamp(),
                                                  nullable=True, comment="更新时间戳")
    # 创建时间，默认为now_timestamp生成的
    create_timestamp: Mapped[int] = mapped_column(Integer, insert_default=now_timestamp(), nullable=True,
                                                  comment="创建时间戳")
