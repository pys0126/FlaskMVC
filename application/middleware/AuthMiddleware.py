"""
权限相关中间件
"""
from typing import Any
from flask import session
from functools import wraps
from application.mapper.UserRoleMapper import UserRoleMapper
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
            # 查询当用户的所有角色
            role_list: list = UserRoleMapper.get_role_info_by_user_id(user_id=user_id)
            for role_info in role_list:
                # 如果当前角色在允许的角色列表中，则通过
                if role_info.name in roles:
                    return func(*args, **kwargs)
                # 如果当前角色在排除的角色列表中，则跳出循环
                elif role_info.name in exclude_roles:
                    break
            raise BasicException(status_code=StatusCodeEnum.AUTHORITY_ERROR.value,
                                 error_message=f"该帐号没有权限访问，ID：{user_id}")

        return wrapper

    return decorator
