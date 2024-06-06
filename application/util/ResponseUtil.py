from application.enumeration.StatusCodeEnum import StatusCodeEnum
from flask import Response, jsonify
from typing import Union


class ResponseUtil:
    """
    返回Response类
    """
    def __init__(self, code: int = StatusCodeEnum.SUCCESS.value, data: Union[dict, list, str, int, None] = None, message: str = "ok"):
        """
        构造方法
        :param code: 状态码
        :param data: 返回数据
        :param message: 返回信息
        """
        self.code: int = code
        self.data: Union[dict, list, str, None] = data
        self.message: str = message

    def success(self) -> Response:
        """
        成功Response
        :return: Response对象
        """
        response: Response = jsonify(code=self.code, data=self.data, message=self.message)
        response.status_code = 200
        return response

    def fail(self) -> Response:
        """
        失败Response
        :return: Response对象
        """
        response: Response = jsonify(code=self.code, message=self.message)
        response.status_code = 500
        return response
