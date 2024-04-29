from typing import Optional
from application.model.UserModel import UserModel
from application.util.MysqlUtil import mysql_session


def info_list() -> list:
    """
    获取数据列表
    :return: 数据列表
    """
    result: list = mysql_session.query(UserModel).all()
    return result


def get_info_by_username(username: str) -> Optional[UserModel]:
    """
    根据用户名获取用户信息
    :param username: 用户名
    :return: 用户信息 | None
    """
    user_model: Optional[UserModel] = mysql_session.query(UserModel).filter_by(username=username).first()
    result: Optional[UserModel] = user_model if user_model else None
    return result


def get_info_by_id(user_id: str) -> Optional[UserModel]:
    """
    根据用户ID获取用户信息
    :param user_id: 用户ID
    :return: 用户信息 | None
    """
    user_model: Optional[UserModel] = mysql_session.query(UserModel).filter_by(id=user_id).first()
    result: Optional[UserModel] = user_model if user_model else None
    return result


def insert(user_model: UserModel) -> bool:
    """
    插入一条数据
    :param user_model: 用户模型
    :return:
    """
    try:
        mysql_session.add(instance=user_model)
        mysql_session.commit()
        return True
    except Exception:
        mysql_session.rollback()
        return False


def update_by_id(user_id: str, update_dict: dict) -> bool:
    """
    根据ID更新数据
    :param user_id: 用户ID
    :param update_dict: 更新的数据
    :return:
    """
    try:
        mysql_session.query(UserModel).filter_by(id=user_id).update(update_dict)
        mysql_session.commit()
        return True
    except Exception:
        mysql_session.rollback()
        return False

