from datetime import datetime
from sqlalchemy import DateTime, String
from flask_sqlalchemy import SQLAlchemy
from application.util.TimeUtil import now_format_datetime
from sqlalchemy.orm import DeclarativeBase, scoped_session, Session, mapped_column, Mapped


class BaseModel(DeclarativeBase):
    """
    模型基类
    """
    # 更新时间，默认为now_format_datetime生成，更新时为now_format_datetime生成
    update_datetime: Mapped[datetime] = mapped_column(DateTime, insert_default=now_format_datetime(),
                                                      onupdate=now_format_datetime(),
                                                      nullable=True, comment="更新时间")
    # 创建时间，默认为now_format_datetime生成的
    create_datetime: Mapped[datetime] = mapped_column(DateTime, insert_default=now_format_datetime(), nullable=True,
                                                      comment="创建时间")
    # 备注
    remark: Mapped[str] = mapped_column(String(300), nullable=True, comment="备注")

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
