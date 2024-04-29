"""
登录相关中间件
"""
from functools import wraps
from typing import Any
from flask import request
from application.exception.BasicException import BasicException
from application.enumeration.StatusCodeEnum import StatusCodeEnum
from application.util.TokenUtil import verify_token
from application.config.ServerConfig import ServerConfig


def login_required(func: Any):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # 过滤掉Bearer 前缀
            token: str = request.headers.get(ServerConfig.token_name).split("Bearer ")[1]
            # 验证用户Token
            if not verify_token(token=token):
                raise BasicException(status_code=StatusCodeEnum.AUTHORITY_ERROR.value, error_message="非法访问，请先登录")
            return func(token=token, *args, **kwargs)
        except IndexError:
            raise BasicException(status_code=StatusCodeEnum.AUTHORITY_ERROR.value, error_message="Token格式错误")
        except AttributeError:
            raise BasicException(status_code=StatusCodeEnum.AUTHORITY_ERROR.value,
                                 error_message=f"缺少{ServerConfig.token_name}")
    return wrapper
