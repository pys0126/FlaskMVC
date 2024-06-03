from application.middleware.LoginMiddleware import login_required
from application.util.ResponseUtil import ResponseUtil
from application.logic import BaseLogic
from flask.blueprints import Blueprint
from flask import Response, request


class BaseController:
    """
    控制器基类 - 实现基本增删改查
    """

    def __init__(self) -> None:
        self.logic: BaseLogic = ...  # 逻辑类
        self.blue_print: Blueprint = ...  # 蓝图
        # 添加路由
        self.blue_print.add_url_rule("/add", view_func=self.add, methods=["POST"])
        self.blue_print.add_url_rule("/delete", view_func=self.delete, methods=["POST"])
        self.blue_print.add_url_rule("/update", view_func=self.update, methods=["POST"])
        self.blue_print.add_url_rule("/get_list", view_func=self.get_list, methods=["GET"])
        self.blue_print.add_url_rule("/get_by_id", view_func=self.get_by_id, methods=["GET"])

    @login_required
    def add(self) -> Response:
        """
        新增数据
        :return:
        """
        self.logic.add(data=request.get_json())
        return ResponseUtil().success()

    @login_required
    def delete(self) -> Response:
        """
        删除数据
        :return:
        """
        self.logic.delete_by_ids(id_list=request.args.get("ids").split(","))
        return ResponseUtil().success()

    @login_required
    def update(self) -> Response:
        """
        更新数据
        :return:
        """
        self.logic.update_by_id(data=request.get_json())
        return ResponseUtil().success()

    @login_required
    def get_by_id(self) -> Response:
        """
        根据ID获取单个数据
        :return:
        """
        return ResponseUtil(data=self.logic.get_info_by_id(data_id=int(request.args.get("id")))).success()

    @login_required
    def get_list(self) -> Response:
        """
        获取数据列表
        :return:
        """
        page_size: int = int(request.args.get("page_size", 10))
        current_page: int = int(request.args.get("current_page", 1))
        return ResponseUtil(data=self.logic.get_info_list(page_size=page_size,
                                                          current_page=current_page)).success()
