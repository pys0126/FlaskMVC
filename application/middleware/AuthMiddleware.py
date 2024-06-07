"""
权限相关中间件
"""
from typing import Any
from functools import wraps
from flask import session, request
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


def auth_required(roles: list = None, exclude_roles: list = None) -> Any:
    """
    权限验证装饰器
    :param roles: 允许的角色列表
    :param exclude_roles: 排除的角色列表
    :return:
    """
    # 默认为空列表
    if roles is None:
        roles = []
    if exclude_roles is None:
        exclude_roles = []

    def decorator(func):
        @wraps(wrapped=func)
        @login_required
        def wrapper(*args, **kwargs) -> Any:
            user_id: int = session.get("user")
            role_info: RoleModel = UserRoleMapper.get_role_info_by_user_id(user_id=user_id)
            # 如果没有角色信息/角色不在允许的角色列表/角色在排除的角色列表，则没有权限访问
            if not role_info or role_info.name not in roles or role_info.name in exclude_roles:
                raise BasicException(status_code=StatusCodeEnum.AUTHORITY_ERROR.value,
                                     error_message="该帐号没有权限访问")
            return func(*args, **kwargs)

        return wrapper

    return decorator
