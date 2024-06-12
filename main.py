import os
import platform
from application.logic import IndexLogic
from application.config.ServerConfig import ServerConfig
from asgiref.wsgi import WsgiToAsgi
from application import app

# 将app转换为asgi
asgi_app: WsgiToAsgi = WsgiToAsgi(app)


# 定义启动命令
command: str = (f"hypercorn main:asgi_app --log-level debug -b {ServerConfig.host}:{ServerConfig.port} -w "
                f"{ServerConfig.workers}")
# 获取系统类型
system: str = platform.system()

if __name__ == "__main__":
    with app.app_context():
        # 创建超级用户及其角色
        IndexLogic.create_admin_user()

    # 启动hypercorn服务器
    os.system(command=command)
