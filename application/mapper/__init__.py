from typing import Optional
from application.util.MysqlUtil import mysql_session, mysql_db


class BaseMapper:
    """
    Mapper基类 - 实现增删查改
    """
    model: mysql_db.Model = None

    @classmethod
    def get_info_list(cls) -> list:
        """
        获取数据列表
        :return: 数据列表
        """
        return mysql_session.query(cls.model).all()

    @classmethod
    def get_info_by_id(cls, model_id: int) -> Optional[mysql_db.Model]:
        """
        根据数据ID获取数据信息
        :param model_id: 数据ID
        :return: 数据信息 | None
        """
        return mysql_session.query(cls.model).filter_by(id=model_id).first()

    @classmethod
    def insert(cls, model: mysql_db.Model) -> bool:
        """
        插入一条数据
        :param model: 数据模型
        :return:
        """
        try:
            mysql_session.add(instance=model)
            mysql_session.commit()
            return True
        except Exception:
            mysql_session.rollback()
            return False

    @classmethod
    def update_by_id(cls, model_id: int, update_dict: dict) -> bool:
        """
        根据ID更新数据
        :param model_id: 数据ID
        :param update_dict: 更新的数据
        :return:
        """
        try:
            mysql_session.query(cls.model).filter_by(id=model_id).update(update_dict)
            mysql_session.commit()
            return True
        except Exception:
            mysql_session.rollback()
            return False

    @classmethod
    def delete_by_ids(cls, id_list: list) -> bool:
        """
        根据id删除数据信息
        :param id_list: 数据id列表
        :return: 是否删除成功
        """
        try:
            mysql_session.query(cls.model).filter(cls.model.id.in_(id_list)).delete()
            mysql_session.commit()
            return True
        except Exception:
            mysql_session.rollback()
            return False
