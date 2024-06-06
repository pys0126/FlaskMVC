from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer, Text
from application.util.MysqlUtil import mysql_db


class UserModel(mysql_db.Model):
    __tablename__: str = "user"
    # 主键
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True, comment="主键，自增")
    # 昵称
    nickname: Mapped[str] = mapped_column(String(8), nullable=True, comment="昵称，长度为8")
    # 用户名
    username: Mapped[str] = mapped_column(String(16), nullable=True, unique=True, comment="用户名，长度为16，唯一")
    # 密码，32位长度md5加密
    password: Mapped[str] = mapped_column(String(32), nullable=True, comment="密码，md5加密，长度32")
    # 邮箱
    email: Mapped[str] = mapped_column(String(32), nullable=True, comment="邮箱，长度为32")
    # 头像URL
    avatar: Mapped[str] = mapped_column(Text, nullable=True,
                                        default="https://c-ssl.duitang.com/uploads/blog/202206/12/"
                                                "20220612164733_72d8b.jpg", comment="头像URL")
