from application.model.RolePermissionModel import RolePermissionModel
from application.model.PermissionModel import PermissionModel
from application.model.RoleModel import RoleModel
from application.mapper import BaseMapper


class RolePermissionMapper(BaseMapper):
    """
    角色权限Mapper
    """
    model: RolePermissionModel = RolePermissionModel

    @classmethod
    def get_permission_info_list_by_role_id(cls, role_id: int) -> list:
        """
        根据角色id获取权限信息列表
        :param role_id: 角色id
        :return: 权限信息列表
        """
        return cls.model.query.join(target=PermissionModel,
                                    onclause=cls.model.permission_id == PermissionModel.id
                                    ).filter_by(role_id=role_id).all()

    @classmethod
    def get_role_info_list_by_permission_id(cls, permission_id: int) -> list:
        """
        根据权限id获取角色信息列表
        :param permission_id: 权限id
        :return: 角色信息列表
        """
        return cls.model.query.join(target=RoleModel,
                                    onclause=cls.model.role_id == RoleModel.id
                                    ).filter_by(permission_id=permission_id).all()
