import os
import platform
from application import app
from application.logic import IndexLogic
from application.config.ServerConfig import ServerConfig


# 定义启动命令
command: str = f"gunicorn --log-level debug application:app -b {ServerConfig.host}:{ServerConfig.port} -w {ServerConfig.workers}"
# 获取系统类型
system: str = platform.system()

if __name__ == "__main__":
    with app.app_context():
        # 创建超级用户
        IndexLogic.create_admin_user()

    # 启动Flask服务器
    if system == "Linux":
        os.system(command=command)
    elif system == "Windows":
        app.run(host=ServerConfig.host, port=ServerConfig.port, debug=True)
    else:
        print("无法识别当前系统")
