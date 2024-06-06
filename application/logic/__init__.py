from typing import Optional
from application.mapper import BaseMapper
from application.util.MysqlUtil import mysql_db


class BaseLogic:
    """
    逻辑层基类 - 实现基本增删查改
    """
    mapper: BaseMapper = None
    model: mysql_db.Model = None

    @classmethod
    def add(cls, data: dict) -> None:
        """
        新增数据
        :param data: 数据字典
        :return: None
        """
        cls.mapper.insert(model=cls.model(**data))

    @classmethod
    def get_info_list(cls, page_size: int = 10, current_page: int = 1) -> dict:
        """
        获取数据列表
        :param page_size: 每页条数
        :param current_page: 当前页
        :return: {
                    items: [...],
                    total, page_size, current_page
                }
        """
        result: dict = dict(items=[model.to_dict() for model in cls.mapper.get_info_list(page_size=page_size,
                                                                                         current_page=current_page)],
                            total=cls.mapper.count(), page_size=page_size, current_page=current_page)
        return result

    @classmethod
    def get_info_by_id(cls, data_id: int) -> Optional[dict]:
        """
        根据id获取数据
        :param data_id: 数据id
        :return: 数据字典
        """
        return cls.mapper.get_info_by_id(model_id=data_id).to_dict()

    @classmethod
    def update_by_id(cls, data: dict) -> None:
        """
        根据ID更新数据
        :param data: 数据字典
        :return: None
        """
        cls.mapper.update_by_id(model_id=data.get("id"), update_dict=data)

    @classmethod
    def delete_by_ids(cls, id_list: list) -> None:
        """
        根据ID列表删除数据
        :param id_list: 数据ID列表
        :return: None
        """
        cls.mapper.delete_by_ids(id_list=id_list)
