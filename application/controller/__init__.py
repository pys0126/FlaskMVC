from application.logic import BaseLogic


class BaseController:
    """
    控制器基类 - 实现基本增删改查
    """
    logic: BaseLogic = None
