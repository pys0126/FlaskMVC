from application.model.RoleModel import RoleModel
from application import app
from application.util.MysqlUtil import mysql_session

with app.app_context():
    print(mysql_session.query(RoleModel).filter(RoleModel.id.in_([2, 3])).all())
