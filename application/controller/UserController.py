from flask import Blueprint, Response, request
from application.logic.UserLogic import UserLogic
from application.util.ResponseUtil import ResponseUtil
from application.middleware.LoginMiddleware import login_required

# 用户蓝图
user: Blueprint = Blueprint("user", __name__)


@user.get("/user_info_list")
@login_required
def user_info_list(token: str) -> Response:
    """
    获取所有用户信息
    :param token: Token
    """
    return ResponseUtil(data=UserLogic.info_list()).success()


@user.get("/now_user_info")
@login_required
def now_user_info(token: str) -> Response:
    """
    获取当前用户信息
    :param token: Token
    """
    return ResponseUtil(data=UserLogic.now_user_info(token=token)).success()


@user.post("/login")
def login() -> Response:
    """
    登录
    """
    return ResponseUtil(data=UserLogic.login(data=request.get_json())).success()


@user.post("/logout")
@login_required
def logout(token: str) -> Response:
    """
    退出登录
    :param token: Token
    """
    UserLogic.logout(token=token)
    return ResponseUtil().success()


@user.post("/change_avatar")
@login_required
def change_avatar(token: str) -> Response:
    """
    更改头像
    :param token: Token
    """
    UserLogic.change_avatar(avatar_url=request.args.get("avatar_url"), token=token)
    return ResponseUtil(message="修改头像成功").success()


@user.post("/change_password")
@login_required
def change_password(token: str) -> Response:
    """
    更改密码
    :param token: Token
    """
    UserLogic.change_password(old_password=request.args.get("old_password"),
                              new_password=request.args.get("new_password"), token=token)
    return ResponseUtil(message="修改密码成功").success()


@user.post("/change_nickname")
@login_required
def change_nickname(token: str) -> Response:
    """
    更改昵称
    :param token: Token
    """
    UserLogic.change_nickname(nickname=request.args.get("nickname"), token=token)
    return ResponseUtil(message="修改昵称成功").success()


@user.post("/change_email")
@login_required
def change_email(token: str) -> Response:
    """
    更改邮箱
    :param token: Token
    """
    UserLogic.change_email(email=request.args.get("email"), valid_code=request.args.get("valid_code"), token=token)
    return ResponseUtil(message="修改邮箱成功").success()
