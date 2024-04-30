from application.util.MysqlUtil import mysql_session
from application.util.RedisUtil import RedisUtil
from application.util.EmailUtil import send_email
from application.model.UserModel import UserModel
from application.config.ServerConfig import ServerConfig
from application.exception.BasicException import BasicException
from application.enumeration.StatusCodeEnum import StatusCodeEnum
from application.util.StringUtil import generate_verification_code, is_valid_email


class IndexLogic:
    """
    杂项逻辑层
    """
    # 实例化redis客户端
    redis_client: RedisUtil = RedisUtil()

    @classmethod
    def send_verification_code(cls, email: str) -> None:
        """
        发送验证码
        :param email: 目标邮箱
        :return:
        """
        # 检查邮箱格式
        if not is_valid_email(text=email):
            raise BasicException(status_code=StatusCodeEnum.BAD_REQUEST_ERROR.value, error_message="请输入正确邮箱")
        code: str = generate_verification_code()  # 生成验证码
        # 发送邮件
        result: bool = send_email(target_email=email, title="邮箱验证码",
                                  content=f"您的验证码是：{code}，"
                                          f"{int(ServerConfig.email_verification_code_expire * 60)}分钟内有效")
        # 发送失败
        if not result:
            raise BasicException(status_code=StatusCodeEnum.ERROR.value, error_message="验证码发送失败，请稍后再试")
        # 保存验证码到redis
        cls.redis_client.set_value(key=email, value=code, ex=ServerConfig.email_verification_code_expire)

    @classmethod
    def create_admin_user(cls) -> None:
        """
        创建管理员用户
        :return:
        """
        try:
            # 创建超级用户
            mysql_session.add(instance=UserModel(
                nickname="超级管理员",
                username=ServerConfig.super_admin_username,
                password=ServerConfig.super_admin_password
            ))
            mysql_session.commit()
        except Exception:
            mysql_session.rollback()
