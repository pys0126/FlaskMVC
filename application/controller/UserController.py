from application.logic.UserLogic import UserLogic
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
    return ResponseUtil(data=UserLogic.get_info_list(
        page_size=int(request.args.get("page_size", 10)),
        current_page=int(request.args.get("current_page", 1))
    )).success()


@user.get("/now_user_info")
@login_required
def now_user_info() -> Response:
    """
    获取当前用户信息
    """
    return ResponseUtil(data=UserLogic.now_user_info(user_id=session.get("user"))).success()


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
    UserLogic.logout(user_id=session.get("user"))
    session.pop(ServerConfig.token_name)  # 删除session中的token
    return ResponseUtil().success()


@user.post("/change_avatar")
@login_required
def change_avatar() -> Response:
    """
    更改头像
    """
    UserLogic.change_avatar(avatar_url=request.args.get("avatar_url"), user_id=session.get("user"))
    return ResponseUtil(message="修改头像成功").success()


@user.post("/change_password")
@login_required
def change_password() -> Response:
    """
    更改密码
    """
    UserLogic.change_password(old_password=request.args.get("old_password"),
                              new_password=request.args.get("new_password"), user_id=session.get("user"))
    return ResponseUtil(message="修改密码成功").success()


@user.post("/change_nickname")
@login_required
def change_nickname() -> Response:
    """
    更改昵称
    """
    UserLogic.change_nickname(nickname=request.args.get("nickname"), user_id=session.get("user"))
    return ResponseUtil(message="修改昵称成功").success()


@user.post("/change_email")
@login_required
def change_email() -> Response:
    """
    更改邮箱
    """
    UserLogic.change_email(email=request.args.get("email"), valid_code=request.args.get("valid_code"),
                           user_id=session.get("user"))
    return ResponseUtil(message="修改邮箱成功").success()
