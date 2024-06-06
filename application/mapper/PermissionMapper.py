from application.model.PermissionModel import PermissionModel
from application.mapper import BaseMapper


class PermissionMapper(BaseMapper):
    """
    权限Mapper
    """
    model: PermissionModel = PermissionModel

