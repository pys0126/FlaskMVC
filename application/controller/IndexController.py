from application.logic import IndexLogic
from flask import Blueprint, Response, request
from application.util.ResponseUtil import ResponseUtil
from application.middleware.LoginMiddleware import login_required

# 主页蓝图
index: Blueprint = Blueprint("index", __name__)


@index.post("/verification_code")
@login_required
def send_verification_code() -> Response:
    """
    发送验证码
    """
    IndexLogic.send_verification_code(email=request.args.get("email"))
    return ResponseUtil().success()


@index.get("/")
@index.get("/index")
def home() -> Response:
    """
    主页，无实际用途
    """
    return ResponseUtil().success()
