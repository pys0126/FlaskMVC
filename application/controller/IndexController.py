from application.logic import IndexLogic
from flask import Blueprint, Response, request
from application.util.ResponseUtil import ResponseUtil
from application.middleware.LoginMiddleware import login_required


class IndexController:
    """
    杂项
    """

    def __init__(self) -> None:
        self.logic: IndexLogic = IndexLogic  # 逻辑层包，不需要实例化
        self.blue_print: Blueprint = Blueprint("index", __name__)
        self.blue_print.add_url_rule("/", view_func=self.home, methods=["GET", "POST"])
        self.blue_print.add_url_rule("/index", view_func=self.home, methods=["GET", "POST"])
        self.blue_print.add_url_rule("/verification_code", view_func=self.send_verification_code, methods=["POST"])

    @login_required
    def send_verification_code(self) -> Response:
        """
        发送验证码
        """
        IndexLogic.send_verification_code(email=request.args.get("email"))
        return ResponseUtil().success()

    def home(self) -> Response:
        """
        主页，无实际用途
        """
        return ResponseUtil().success()
