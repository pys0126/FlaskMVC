from application import app
from application.util.MysqlUtil import mysql_session


# 自动清理每次请求数据库会话
@app.teardown_appcontext
def shutdown_session(exception=None):
    if exception:
        mysql_session.rollback()
    mysql_session.remove()
