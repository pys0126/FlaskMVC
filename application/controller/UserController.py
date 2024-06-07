from application.controller import BaseController
from application.logic.UserLogic import UserLogic
from application.util.ResponseUtil import ResponseUtil
from flask import Blueprint, Response, request, session
from application.middleware.AuthMiddleware import auth_required


class UserController(BaseController):
    """
    用户控制器
    """
    def __init__(self) -> None:
        self.logic: UserLogic = UserLogic()  # 实例化逻辑层
        self.blue_print: Blueprint = Blueprint("user", __name__)  # 实例化蓝图
        super().__init__(logic=self.logic, blue_print=self.blue_print)  # 继承父类方法，注入依赖
        # 注册路由
        self.blue_print.add_url_rule("/login", view_func=self.login, methods=["POST"])
        self.blue_print.add_url_rule("/logout", view_func=self.logout, methods=["POST"])
        self.blue_print.add_url_rule("/now_user_info", view_func=self.now_user_info, methods=["GET"])
        self.blue_print.add_url_rule("/change_avatar", view_func=self.change_avatar, methods=["POST"])
        self.blue_print.add_url_rule("/change_password", view_func=self.change_password, methods=["POST"])
        self.blue_print.add_url_rule("/change_nickname", view_func=self.change_nickname, methods=["POST"])
        self.blue_print.add_url_rule("/change_email", view_func=self.change_email, methods=["POST"])

    @auth_required
    def get_list(self) -> Response:
        """
        获取所有用户信息
        """
        return ResponseUtil(data=UserLogic.get_info_list(
            page_size=int(request.args.get("page_size", 10)),
            current_page=int(request.args.get("current_page", 1))
        )).success()

    @auth_required
    def now_user_info(self) -> Response:
        """
        获取当前用户信息
        """
        return ResponseUtil(data=UserLogic.now_user_info(user_id=session.get("user"))).success()

    def login(self) -> Response:
        """
        登录
        """
        return ResponseUtil(data=UserLogic.login(data=request.get_json())).success()

    @auth_required
    def logout(self) -> Response:
        """
        退出登录
        """
        UserLogic.logout(user_id=session.get("user"))
        session.clear()  # 清除session
        return ResponseUtil().success()

    @auth_required
    def change_avatar(self) -> Response:
        """
        更改头像
        """
        UserLogic.change_avatar(avatar_url=request.args.get("avatar_url"), user_id=session.get("user"))
        return ResponseUtil(message="修改头像成功").success()

    @auth_required
    def change_password(self) -> Response:
        """
        更改密码
        """
        UserLogic.change_password(old_password=request.args.get("old_password"),
                                  new_password=request.args.get("new_password"), user_id=session.get("user"))
        return ResponseUtil(message="修改密码成功").success()

    @auth_required
    def change_nickname(self) -> Response:
        """
        更改昵称
        """
        UserLogic.change_nickname(nickname=request.args.get("nickname"), user_id=session.get("user"))
        return ResponseUtil(message="修改昵称成功").success()

    @auth_required
    def change_email(self) -> Response:
        """
        更改邮箱
        """
        UserLogic.change_email(email=request.args.get("email"), valid_code=request.args.get("valid_code"),
                               user_id=session.get("user"))
        return ResponseUtil(message="修改邮箱成功").success()
