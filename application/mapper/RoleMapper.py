from application.mapper import BaseMapper
from application.model.RoleModel import RoleModel


class RoleMapper(BaseMapper):
    """
    角色Mapper
    """
    model: RoleModel = RoleModel

    @classmethod
    def get_role_name_list(cls) -> list:
        """
        获取角色名称列表
        :return:
        """
        return [role.name for role in cls.model.query.all()]
