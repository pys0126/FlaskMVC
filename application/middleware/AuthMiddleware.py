"""
权限相关中间件
"""
from typing import Any
from functools import wraps
from flask import session
from application.model.UserModel import UserModel
from application.mapper.UserMapper import UserMapper
from application.model.RoleModel import RoleModel
from application.mapper.RoleMapper import RoleMapper
from application.model.PermissionModel import PermissionModel
from application.mapper.PermissionMapper import PermissionModel
from application.model.UserRoleModel import UserRoleModel
from application.mapper.UserRoleMapper import UserRoleMapper
from application.model.RolePermissionModel import RolePermissionModel
from application.mapper.RolePermissionMapper import RolePermissionModel
from application.middleware.LoginMiddleware import login_required
from application.exception.BasicException import BasicException
from application.enumeration.StatusCodeEnum import StatusCodeEnum


def auth_required(func: Any) -> Any:
    @wraps(wrapped=func)
    @login_required
    def wrapper(*args, **kwargs) -> Any:
        user_id: int = session.get("user")
        role_info: RoleModel = UserRoleMapper.get_role_info_by_user_id(user_id=user_id)
        # 如果没有角色信息，则没有权限
        if not role_info:
            raise BasicException(status_code=StatusCodeEnum.AUTHORITY_ERROR.value, error_message="该帐号没有权限")
        return func(*args, **kwargs)
    return wrapper
