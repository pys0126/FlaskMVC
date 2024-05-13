from application.logic import UserLogic
from application.util.ResponseUtil import ResponseUtil
from flask import Blueprint, Response, request, session
from application.config.ServerConfig import ServerConfig
from application.middleware.LoginMiddleware import login_required

# 用户蓝图
user: Blueprint = Blueprint("user", __name__)


@user.get("/user_info_list")
@login_required
def user_info_list() -> Response:
    """
    获取所有用户信息
    """
    return ResponseUtil(data=UserLogic.info_list()).success()


@user.get("/now_user_info")
@login_required
def now_user_info() -> Response:
    """
    获取当前用户信息
    """
    token: str = session.get(ServerConfig.token_name)
    return ResponseUtil(data=UserLogic.now_user_info(token=token)).success()


@user.post("/login")
def login() -> Response:
    """
    登录
    """
    return ResponseUtil(data=UserLogic.login(data=request.get_json())).success()


@user.post("/logout")
@login_required
def logout() -> Response:
    """
    退出登录
    """
    token: str = session.get(ServerConfig.token_name)
    UserLogic.logout(token=token)
    session.pop(ServerConfig.token_name)  # 删除session中的token
    return ResponseUtil().success()


@user.post("/change_avatar")
@login_required
def change_avatar() -> Response:
    """
    更改头像
    """
    token: str = session.get(ServerConfig.token_name)
    UserLogic.change_avatar(avatar_url=request.args.get("avatar_url"), token=token)
    return ResponseUtil(message="修改头像成功").success()


@user.post("/change_password")
@login_required
def change_password() -> Response:
    """
    更改密码
    """
    token: str = session.get(ServerConfig.token_name)
    UserLogic.change_password(old_password=request.args.get("old_password"),
                              new_password=request.args.get("new_password"), token=token)
    return ResponseUtil(message="修改密码成功").success()


@user.post("/change_nickname")
@login_required
def change_nickname() -> Response:
    """
    更改昵称
    """
    token: str = session.get(ServerConfig.token_name)
    UserLogic.change_nickname(nickname=request.args.get("nickname"), token=token)
    return ResponseUtil(message="修改昵称成功").success()


@user.post("/change_email")
@login_required
def change_email() -> Response:
    """
    更改邮箱
    """
    token: str = session.get(ServerConfig.token_name)
    UserLogic.change_email(email=request.args.get("email"), valid_code=request.args.get("valid_code"), token=token)
    return ResponseUtil(message="修改邮箱成功").success()
