from typing import Optional
from application.mapper import BaseMapper
from application.model.RoleModel import RoleModel
from application.model.UserModel import UserModel
from application.util.MysqlUtil import mysql_session
from application.model.UserRoleModel import UserRoleModel


class UserRoleMapper(BaseMapper):
    """
    用户-角色Mapper
    """
    model: UserRoleModel = UserRoleModel

    @classmethod
    def get_role_info_by_user_id(cls, user_id: int) -> Optional[RoleModel]:
        """
        根据用户id获取角色信息
        :param user_id: 用户ID
        :return: 角色模型
        """
        return mysql_session.query(cls.model).join(target=UserRoleModel,
                                                   onclause=RoleModel.id == UserRoleModel.role_id
                                                   ).filter(UserRoleModel.user_id == user_id).first()

    @classmethod
    def get_user_info_list_by_role_id(cls, role_id: int) -> list:
        """
        根据角色id获取用户信息列表
        :param role_id: 角色ID
        :return: 用户模型列表
        """
        return mysql_session.query(cls.model).join(target=UserRoleModel,
                                                   onclause=UserModel.id == UserRoleModel.user_id
                                                   ).filter(UserRoleModel.role_id == role_id).all()
