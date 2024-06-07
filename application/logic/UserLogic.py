"""
用户逻辑
"""
from flask import session
from typing import Optional
from application.logic import BaseLogic
from application.util.RedisUtil import RedisUtil
from application.model.UserModel import UserModel
from application.mapper.UserMapper import UserMapper
from application.exception.BasicException import BasicException
from application.enumeration.StatusCodeEnum import StatusCodeEnum
from application.util.TokenUtil import clear_token, generate_token
from application.util.StringUtil import (random_uuid, md5_encode, sha1_encode, is_valid_url, is_valid_password,
                                         is_valid_email)


class UserLogic(BaseLogic):
    """
    用户逻辑层
    """
    model: UserModel = UserModel  # 定义模型
    mapper: UserMapper = UserMapper  # 定义mapper
    # 实例化redis客户端
    redis_client: RedisUtil = RedisUtil()

    @classmethod
    def now_user_info(cls, user_id: int) -> Optional[dict]:
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

    @classmethod
    def get_info_list(cls, page_size: int = 10, current_page: int = 1) -> dict:
        """
        获取用户信息列表
        :param page_size: 每页条数
        :param current_page: 当前页
        :return: {
                    items: [...],
                    total, page_size, current_page
                }
        """
        result: dict = dict(items=[], total=cls.mapper.count(), page_size=page_size, current_page=current_page)
        for user_model in UserMapper.get_info_list(page_size=page_size, current_page=current_page):
            user_info: dict = user_model.to_dict()
            user_info.pop("password")  # 删除密码字段
            result["items"].append(user_info)  # 添加用户信息到items列表中
        return result

    @classmethod
    def registered(cls, data: dict, valid_code: str) -> None:
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
        cache_code: Optional[str] = cls.redis_client.get_value(key=data.get("email"))
        if not cache_code or cache_code != valid_code:
            raise BasicException(status_code=StatusCodeEnum.AUTHORITY_ERROR.value, error_message="邮箱验证码错误")
        # 删除Redis中的邮箱验证码
        cls.redis_client.delete_by_key(key=data.get("email"))
        data["password"] = sha1_encode(text=md5_encode(text=str(data.get("password"))))  # md5 + sha1 加密密码
        user_model: UserModel = UserModel(**data)
        user_model.id = random_uuid()  # 随机生成ID
        if not UserMapper.insert(model=user_model):
            raise BasicException(status_code=StatusCodeEnum.ERROR.value, error_message="内部错误，请稍后再试")

    @classmethod
    def login(cls, data: dict) -> str:
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
        if sha1_encode(text=md5_encode(text=str(data.get("password")))) != user_model.password:
            raise BasicException(status_code=StatusCodeEnum.AUTHORITY_ERROR.value, error_message="密码错误")
        return generate_token(user_id=user_model.id)

    @classmethod
    def logout(cls, user_id: int) -> None:
        """
        退出登录
        :param user_id: user_id
        :return:
        """
        if not clear_token(user_id=user_id):  # 清空token
            raise BasicException(status_code=StatusCodeEnum.BAD_REQUEST_ERROR.value, error_message="用户会话异常")
        session.clear()  # 清空Session

    @classmethod
    def change_avatar(cls, avatar_url: str, user_id: int) -> None:
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

    @classmethod
    def change_password(cls, old_password: str, new_password: str, user_id: int) -> None:
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
        if user_model.password != sha1_encode(text=md5_encode(text=old_password)):
            raise BasicException(status_code=StatusCodeEnum.AUTHORITY_ERROR.value, error_message="旧密码错误")
        # 检查密码是否符合规范
        if not is_valid_password(text=new_password):
            raise BasicException(status_code=StatusCodeEnum.BAD_REQUEST_ERROR.value,
                                 error_message="密码不符合规范（至少一个字母，至少一个数字，至少为6位）")
        # 修改密码
        if not UserMapper.update_by_id(model_id=user_id,
                                       update_dict={"password": sha1_encode(text=md5_encode(text=new_password))}):
            raise BasicException(status_code=StatusCodeEnum.ERROR.value, error_message="内部错误，请稍后再试")

    @classmethod
    def change_nickname(cls, nickname: str, user_id: int) -> None:
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

    @classmethod
    def change_email(cls, email: str, valid_code: str, user_id: int) -> None:
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
        cache_code: Optional[str] = cls.redis_client.get_value(key=email)
        if not cache_code or cache_code != valid_code:
            raise BasicException(status_code=StatusCodeEnum.AUTHORITY_ERROR.value, error_message="邮箱验证码错误")
        # 删除Redis中的邮箱验证码
        cls.redis_client.delete_by_key(key=email)
        # 修改邮箱
        if not UserMapper.update_by_id(model_id=user_id, update_dict={"email": email}):
            raise BasicException(status_code=StatusCodeEnum.ERROR.value, error_message="内部错误，请稍后再试")
