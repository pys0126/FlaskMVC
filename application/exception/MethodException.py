from typing import Union, Any
from flask import Response
from werkzeug.exceptions import MethodNotAllowed
from application.util.ResponseUtil import ResponseUtil
from application.enumeration.StatusCodeEnum import StatusCodeEnum
from application.util.TimeUtil import now_format_datetime


class MethodException(MethodNotAllowed):
    """
    请求方法异常
    """
    def __init__(self, status_code: Union[int, Any] = StatusCodeEnum.METHOD_ERROR.value,
                 error_message: str = "请求方法错误，请检查") -> None:
        """
        构造方法
        :param status_code: 异常码
        :param error_message: 异常消息
        """
        self.status_code: int = status_code
        self.error_message: str = error_message

    @staticmethod
    def exception_handle(exception: MethodNotAllowed) -> Response:
        """
        异常钩子
        :param exception: 异常类
        :return:
        """
        type_exception: MethodException = MethodException()
        # 打印异常堆栈信息
        print(f"{now_format_datetime()}\tErrorInfo => ", exception)
        # 返回Response
        return ResponseUtil(code=type_exception.status_code, message=type_exception.error_message).fail()
