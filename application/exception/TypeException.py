import traceback
from flask import Response
from typing import Union, Any
from application.util.LogUtil import write_error_log
from application.util.ResponseUtil import ResponseUtil
from application.enumeration.StatusCodeEnum import StatusCodeEnum
from application.util.TimeUtil import now_format_datetime


class TypeException(TypeError):
    """
    类型错误异常
    """
    def __init__(self, status_code: Union[int, Any] = StatusCodeEnum.BAD_REQUEST_ERROR.value,
                 error_message: str = "参数格式/类型错误") -> None:
        """
        构造方法
        :param status_code: 异常码
        :param error_message: 异常消息
        """
        self.status_code: int = status_code
        self.error_message: str = error_message

    @staticmethod
    def exception_handle(exception: TypeError) -> Response:
        """
        异常钩子
        :param exception: 异常类
        :return:
        """
        type_exception: TypeException = TypeException()
        # 打印、写入异常堆栈信息
        print(f"{now_format_datetime()}\tErrorInfo => ", exception)
        write_error_log(traceback.format_exc())
        # 返回Response
        return ResponseUtil(code=type_exception.status_code, message=type_exception.error_message).fail()
