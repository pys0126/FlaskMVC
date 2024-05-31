"""
用户逻辑
"""
from flask import session
from typing import Optional
from application.util.RedisUtil import RedisUtil
from application.model.UserModel import UserModel
from application.mapper.UserMapper import UserMapper
from application.exception.BasicException import BasicException
from application.enumeration.StatusCodeEnum import StatusCodeEnum
from application.util.TokenUtil import clear_token, generate_token
from application.util.StringUtil import random_uuid, md5_encode, is_valid_url, is_valid_password, is_valid_email


# 实例化redis客户端
redis_client: RedisUtil = RedisUtil()


def now_user_info(user_id: int) -> Optional[dict]:
    """
    获取当前用户信息
    :param user_id: user_id
    :return:
    """
    user_model: Optional[UserModel] = UserMapper.get_info_by_id(model_id=user_id)
    if user_model is None:
        raise BasicException(status_code=StatusCodeEnum.BAD_REQUEST_ERROR.value, error_message="用户不存在")
    user_info: dict = user_model.to_dict()
    user_info.pop("password")  # 删除密码字段
    return user_info


def get_info_list() -> list:
    """
    获取用户信息列表
    :return:
    """
    result: list[Optional[dict]] = []
    for user_model in UserMapper.get_info_list():
        user_info: dict = user_model.to_dict()
        user_info.pop("password")  # 删除密码字段
        result.append(user_info)
    return result


def registered(data: dict, valid_code: str) -> None:
    """
    注册/新增用户
    :param data: 用户信息字典
    :param valid_code: 邮箱验证码
    :return:
    """
    # 检查必填项
    if not all([data.get("username"), data.get("password"), data.get("nickname"), data.get("email"), valid_code]):
        raise BasicException(status_code=StatusCodeEnum.BAD_REQUEST_ERROR.value, error_message="请完善内容")
    # 检查用户名是否已存在
    if UserMapper.get_info_by_username(username=data.get("username")):
        raise BasicException(status_code=StatusCodeEnum.ALREADY_EXIST_ERROR.value, error_message="该用户已存在")
    # 检查密码是否符合规范
    if not is_valid_password(text=str(data.get("password"))):
        raise BasicException(status_code=StatusCodeEnum.BAD_REQUEST_ERROR.value,
                             error_message="密码不符合规范（至少一个字母，至少一个数字，至少为6位）")
    # 检查邮箱格式
    if not is_valid_email(text=data.get("email")):
        raise BasicException(status_code=StatusCodeEnum.BAD_REQUEST_ERROR.value, error_message="请输入正确邮箱")
    # 验证邮箱验证码
    cache_code: Optional[str] = redis_client.get_value(key=data.get("email"))
    if not cache_code or cache_code != valid_code:
        raise BasicException(status_code=StatusCodeEnum.AUTHORITY_ERROR.value, error_message="邮箱验证码错误")
    # 删除Redis中的邮箱验证码
    redis_client.delete_by_key(key=data.get("email"))
    data["password"] = md5_encode(text=str(data.get("password")))  # md5加密密码，先转为字符串
    user_model: UserModel = UserModel(**data)
    user_model.id = random_uuid()  # 随机生成ID
    if not UserMapper.insert(model=user_model):
        raise BasicException(status_code=StatusCodeEnum.ERROR.value, error_message="内部错误，请稍后再试")


def login(data: dict) -> str:
    """
    登录
    :param data: 用户信息字典
    :return: user_id
    """
    # 检查必填项
    if not all([data.get("username"), data.get("password")]):
        raise BasicException(status_code=StatusCodeEnum.BAD_REQUEST_ERROR.value, error_message="请完善内容")
    # 检查密码是否符合规范
    if not is_valid_password(text=str(data.get("password"))):
        raise BasicException(status_code=StatusCodeEnum.BAD_REQUEST_ERROR.value,
                             error_message="密码不符合规范（至少一个字母，至少一个数字，至少为6位）")
    user_model: Optional[UserModel] = UserMapper.get_info_by_username(username=data.get("username"))
    # 检查用户是否存在
    if not user_model:
        raise BasicException(status_code=StatusCodeEnum.NOT_FOUND_ERROR.value, error_message="该用户不存在")
    # 检查密码是否正确
    if md5_encode(text=data.get("password")) != user_model.password:
        raise BasicException(status_code=StatusCodeEnum.AUTHORITY_ERROR.value, error_message="密码错误")
    return generate_token(user_id=user_model.id)


def logout(user_id: int) -> None:
    """
    退出登录
    :param user_id: user_id
    :return:
    """
    if not clear_token(user_id=user_id):  # 清空token
        raise BasicException(status_code=StatusCodeEnum.BAD_REQUEST_ERROR.value, error_message="用户会话异常")
    session.clear()  # 清空Session


def change_avatar(avatar_url: str, user_id: int) -> None:
    """
    修改头像
    :param avatar_url: 头像URL
    :param user_id: user_id
    :return:
    """
    user_model: Optional[UserModel] = UserMapper.get_info_by_id(model_id=user_id)
    # 检查用户是否存在
    if not user_model:
        raise BasicException(status_code=StatusCodeEnum.NOT_FOUND_ERROR.value, error_message="该用户不存在")
    # 检查是否为URL
    if not avatar_url or not is_valid_url(text=avatar_url):
        raise BasicException(status_code=StatusCodeEnum.BAD_REQUEST_ERROR.value, error_message="请输入正确URL")
    # 修改头像
    if not UserMapper.update_by_id(model_id=user_id, update_dict={"avatar": avatar_url}):
        raise BasicException(status_code=StatusCodeEnum.ERROR.value, error_message="内部错误，请稍后再试")


def change_password(old_password: str, new_password: str, user_id: int) -> None:
    """
    修改密码
    :param old_password: 旧密码
    :param new_password: 新密码
    :param user_id: user_id
    :return:
    """
    user_model: Optional[UserModel] = UserMapper.get_info_by_id(model_id=user_id)
    # 检查用户是否存在
    if not user_model:
        raise BasicException(status_code=StatusCodeEnum.NOT_FOUND_ERROR.value, error_message="该用户不存在")
    # 检查是否为空
    if not all([old_password, new_password]):
        raise BasicException(status_code=StatusCodeEnum.BAD_REQUEST_ERROR.value, error_message="请完善内容")
    # 检查密码是否正确
    if user_model.password != md5_encode(text=old_password):
        raise BasicException(status_code=StatusCodeEnum.AUTHORITY_ERROR.value, error_message="旧密码错误")
    # 检查密码是否符合规范
    if not is_valid_password(text=new_password):
        raise BasicException(status_code=StatusCodeEnum.BAD_REQUEST_ERROR.value,
                             error_message="密码不符合规范（至少一个字母，至少一个数字，至少为6位）")
    # 修改密码
    if not UserMapper.update_by_id(model_id=user_id, update_dict={"password": md5_encode(text=new_password)}):
        raise BasicException(status_code=StatusCodeEnum.ERROR.value, error_message="内部错误，请稍后再试")


def change_nickname(nickname: str, user_id: int) -> None:
    """
    修改昵称
    :param nickname: 昵称
    :param user_id: user_id
    :return:
    """
    user_model: Optional[UserModel] = UserMapper.get_info_by_id(model_id=user_id)
    # 检查用户是否存在
    if not user_model:
        raise BasicException(status_code=StatusCodeEnum.NOT_FOUND_ERROR.value, error_message="该用户不存在")
    # 检查是否为空
    if not nickname:
        raise BasicException(status_code=StatusCodeEnum.BAD_REQUEST_ERROR.value, error_message="请完善内容")
    # 修改昵称
    if not UserMapper.update_by_id(model_id=user_id, update_dict={"nickname": nickname}):
        raise BasicException(status_code=StatusCodeEnum.ERROR.value, error_message="内部错误，请稍后再试")


def change_email(email: str, valid_code: str, user_id: int) -> None:
    """
    修改邮箱
    :param email: 邮箱
    :param valid_code: 邮箱验证码
    :param user_id: user_id
    :return:
    """
    user_model: Optional[UserModel] = UserMapper.get_info_by_id(model_id=user_id)
    # 检查用户是否存在
    if not user_model:
        raise BasicException(status_code=StatusCodeEnum.NOT_FOUND_ERROR.value, error_message="该用户不存在")
    # 检查必填项
    if not all([email, valid_code]):
        raise BasicException(status_code=StatusCodeEnum.BAD_REQUEST_ERROR.value, error_message="请完善内容")
    # 检查邮箱格式
    if not is_valid_email(text=email):
        raise BasicException(status_code=StatusCodeEnum.BAD_REQUEST_ERROR.value, error_message="请输入正确邮箱")
    # 验证邮箱验证码
    cache_code: Optional[str] = redis_client.get_value(key=email)
    if not cache_code or cache_code != valid_code:
        raise BasicException(status_code=StatusCodeEnum.AUTHORITY_ERROR.value, error_message="邮箱验证码错误")
    # 删除Redis中的邮箱验证码
    redis_client.delete_by_key(key=email)
    # 修改邮箱
    if not UserMapper.update_by_id(model_id=user_id, update_dict={"email": email}):
        raise BasicException(status_code=StatusCodeEnum.ERROR.value, error_message="内部错误，请稍后再试")
