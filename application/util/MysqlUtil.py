from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, scoped_session, Session


class BaseModel(DeclarativeBase):
    """
    模型基类
    """

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
