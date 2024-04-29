from flask import Blueprint, Response, request
from application.logic.IndexLogic import IndexLogic
from application.util.ResponseUtil import ResponseUtil
from application.middleware.LoginMiddleware import login_required


# 主页蓝图
index: Blueprint = Blueprint("index", __name__)


@index.post("/verification_code")
@login_required
def send_verification_code(token: str) -> Response:
    """
    发送验证码
    :param token: Token
    """
    IndexLogic.send_verification_code(email=request.args.get("email"))
    return ResponseUtil().success()
