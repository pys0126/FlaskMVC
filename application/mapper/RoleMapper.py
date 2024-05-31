from typing import Optional
from application.mapper import BaseMapper
from application.model.RoleModel import RoleModel
from application.util.MysqlUtil import mysql_session


class RoleMapper(BaseMapper):
    """
    角色Mapper
    """
    model: RoleModel = RoleModel
