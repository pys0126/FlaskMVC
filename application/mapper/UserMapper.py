from typing import Optional
from application.mapper import BaseMapper
from application.model.UserModel import UserModel


class UserMapper(BaseMapper):
    """
    用户Mapper
    """
    model: UserModel = UserModel

    @classmethod
    def get_info_by_username(cls, username: str) -> Optional[UserModel]:
        """
        根据用户名获取用户信息
        :param username: 用户名
        :return: 用户信息 | None
        """
        return cls.model.query.filter_by(username=username).first()
