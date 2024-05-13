from flask import Flask
from flask_cors import CORS
from sqlalchemy.engine import URL
from application.util.StringUtil import random_uuid
from werkzeug.exceptions import MethodNotAllowed
from application.controller.UserController import user
from application.controller.IndexController import index
from application.config.ServerConfig import ServerConfig
from application.config.DatabaseConfig import RedisConfig
from application.exception.TypeException import TypeException
from application.util.MysqlUtil import mysql_db, mysql_session
from application.exception.BasicException import BasicException
from application.enumeration.StatusCodeEnum import StatusCodeEnum
from application.exception.MethodException import MethodException
from application.config.DatabaseConfig import MysqlConfig, SqlalchemyConfig

# 创建Flask实例
app: Flask = Flask(__name__)
# 设置SECRET_KEY密钥，session用
app.config["SECRET_KEY"] = random_uuid()
CORS(app=app)  # 设置允许跨越
# 连接信息（使用URL构造对象，防止有非法字符导致连接出错）
app.config["SQLALCHEMY_DATABASE_URI"] = URL.create(drivername="mysql+pymysql", username=MysqlConfig.username,
                                                   password=MysqlConfig.password, host=MysqlConfig.host,
                                                   port=MysqlConfig.port, database=MysqlConfig.database_name)
# 配置是否打印SQL语句
app.config["SQLALCHEMY_ECHO"] = SqlalchemyConfig.on_echo
# 将Flask实例绑定到数据库
mysql_db.init_app(app=app)
# 创建数据表（如果不存在）
with app.app_context():
    # 导入所有待创建的数据表
    from application.model import *
    mysql_db.create_all()

# 异常注册
app.register_error_handler(BasicException, BasicException.exception_handle)
app.register_error_handler(Exception, BasicException.exception_handle)
app.register_error_handler(TypeError, TypeException.exception_handle)
app.register_error_handler(MethodNotAllowed, MethodException.exception_handle)

# 蓝图注册
app.register_blueprint(index, url_prefix="/")
app.register_blueprint(user, url_prefix="/user")
