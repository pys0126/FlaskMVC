from sqlalchemy import Integer
from flask_sqlalchemy import SQLAlchemy
from application.util.TimeUtil import now_timestamp
from sqlalchemy.orm import DeclarativeBase, scoped_session, Session, mapped_column, Mapped


class BaseModel(DeclarativeBase):
    """
    模型基类
    """
    # 更新时间，默认为now_timestamp生成，更新时为now_timestamp生成
    update_timestamp: Mapped[int] = mapped_column(Integer, insert_default=now_timestamp(), onupdate=now_timestamp(),
                                                  nullable=True, comment="更新时间戳")
    # 创建时间，默认为now_timestamp生成的
    create_timestamp: Mapped[int] = mapped_column(Integer, insert_default=now_timestamp(), nullable=True,
                                                  comment="创建时间戳")

    def to_dict(self) -> dict:
        """
        转为字典
        :return:
        """
        # 去除_sa_instance_state字段
        self.__dict__.pop("_sa_instance_state")
        return self.__dict__


# 初始化SQLAlchemy
mysql_db: SQLAlchemy = SQLAlchemy(model_class=BaseModel)
# 获得会话
mysql_session: scoped_session[Session] = mysql_db.session
