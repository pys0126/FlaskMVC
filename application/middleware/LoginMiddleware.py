"""
登录相关中间件
"""
from typing import Any
from functools import wraps
from flask import request, session
from application.config.ServerConfig import ServerConfig
from application.exception.BasicException import BasicException
from application.util.TokenUtil import verify_token, get_user_id
from application.enumeration.StatusCodeEnum import StatusCodeEnum


def login_required(func: Any) -> Any:
    @wraps(wrapped=func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            # 过滤掉Bearer 前缀
            token: str = request.headers.get(ServerConfig.token_name).split("Bearer ")[1]
            # 验证用户Token
            if not verify_token(token=token):
                raise BasicException(status_code=StatusCodeEnum.AUTHORITY_ERROR.value, error_message="非法访问，请先登录")
            # 存储Token到session
            session["user"] = get_user_id(token=token)
            session.permanent = True  # 设置session永久有效，除非被删除
            return func(*args, **kwargs)
        except IndexError:
            raise BasicException(status_code=StatusCodeEnum.AUTHORITY_ERROR.value, error_message="Token格式错误")
        except AttributeError:
            raise BasicException(status_code=StatusCodeEnum.AUTHORITY_ERROR.value,
                                 error_message=f"缺少{ServerConfig.token_name}")
    return wrapper
