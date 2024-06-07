from typing import Optional
from application.mapper import BaseMapper
from application.model.RoleModel import RoleModel
from application.model.UserModel import UserModel
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
        user_role_model: Optional[UserRoleModel] = cls.model.query.filter_by(user_id=user_id).first()
        return RoleModel.query.filter_by(id=user_role_model.role_id).first() if user_role_model else None

    @classmethod
    def get_user_info_list_by_role_id(cls, role_id: int) -> list:
        """
        根据角色id获取用户信息列表
        :param role_id: 角色ID
        :return: 用户模型列表
        """
        user_role_model_list: list = cls.model.query.filter_by(role_id=role_id).all()
        user_model_list: list = []
        for user_role_model in user_role_model_list:
            user_model_list.append(UserModel.query.filter_by(id=user_role_model.user_id).first())
        return user_model_list
