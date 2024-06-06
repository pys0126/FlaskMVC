from typing import Optional
from application.util.MysqlUtil import mysql_db


class BaseMapper:
    """
    Mapper基类 - 实现基本增删查改
    """
    model: mysql_db.Model = None

    @classmethod
    def count(cls) -> int:
        """
        数据总条数
        :return: 数据总条数
        """
        return cls.model.query.count()

    @classmethod
    def get_info_list(cls, page_size: int = 10, current_page: int = 1) -> list:
        """
        获取数据列表
        :param page_size: 每页条数
        :param current_page: 当前页
        :return: 数据列表
        """
        offset: int = (current_page - 1) * page_size
        return cls.model.query.limit(limit=page_size).offset(offset=offset).all()

    @classmethod
    def get_info_by_id(cls, model_id: int) -> Optional[mysql_db.Model]:
        """
        根据数据ID获取数据信息
        :param model_id: 数据ID
        :return: 数据信息 | None
        """
        return cls.model.query.filter_by(id=model_id).first()

    @classmethod
    def insert(cls, model: mysql_db.Model) -> bool:
        """
        插入一条数据
        :param model: 数据模型
        :return:
        """
        try:
            cls.model.add(instance=model)
            cls.model.commit()
            return True
        except Exception:
            cls.model.rollback()
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
            cls.model.query.filter_by(id=model_id).update(update_dict)
            cls.model.commit()
            return True
        except Exception:
            cls.model.rollback()
            return False

    @classmethod
    def delete_by_ids(cls, id_list: list) -> bool:
        """
        根据id删除数据信息
        :param id_list: 数据id列表
        :return: 是否删除成功
        """
        try:
            cls.model.query.filter(cls.model.id.in_(id_list)).delete()
            cls.model.commit()
            return True
        except Exception:
            cls.model.rollback()
            return False
