from enum import Enum


class StatusCodeEnum(Enum):
    """
    状态码枚举
    """
    SUCCESS = 2000  # 成功
    ERROR = 5000  # 失败
    ILLEGALITY_ERROR = 4001  # 非法请求
    AUTHORITY_ERROR = 4030  # 权限错误
    NOT_FOUND_ERROR = 4040  # 未找到
    METHOD_ERROR = 4050  # 请求方法错误
    BAD_REQUEST_ERROR = 4000  # 错误请求
    ALREADY_EXIST_ERROR = 4090  # 已存在
    UNSUPPORTED_MEDIA_TYPE_ERROR = 4150  # 不支持的媒体类型
    FILE_SIZE_ERROR = 4130  # 文件大小错误
    FILE_UPLOAD_ERROR = 5001  # 文件上传错误
    FILE_DELETE_ERROR = 5003  # 文件删除错误
