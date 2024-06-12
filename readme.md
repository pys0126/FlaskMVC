# Flask MVC

Flask管理后台API开发模板，快速构建CRUD接口，采用MVC模式。

灵感源自[`SpringBoot`](https://spring.io/)，集成了`Flask、Flask-SQLAlchemy、Flask-Cors、Redis、HttpX、PIL、PyYaml`等框架。采用装饰器控制接口访问权限（基于角色的权限控制），会话管理采用`Token（JWT）` + `Redis`方式。另外集成了字符串、日期时间等工具包，方便快速开发。

## 简要说明

- 项目使用`Python>=3.9`，使用`hypercorn`作为HTTP服务器（ASGI异步高性能）。
 
- 强烈推荐使用`venv`或者`conda`虚拟环境，避免环境冲突。

- 整个项目应关注于`application`目录下的内容，其他模块为辅助工具。

### 一、配置项目

1. 编辑`config-template.yaml`配置模板。
2. 将配置信息复制到`config.yaml`（新建）中。

### 二、如何开发

1. 在`application/model`模块，创建ORM模型类，并在`application/model/__init__.py`导入。
2. 在`application/mapper`模块，创建ORM操作类。
3. 在`application/logic`模块，创建业务逻辑类。
4. 在`application/controller`模块，创建控制器类。
5. 注册蓝图、异常均在`application/__init__.py`。

**注意：** `mapper`、`logic`、`controller`模块的`__init__.py`中的基类都提供了基本CURD的实现方法，新建的类继承即可。

### 三、运行项目

- 终端运行：`python main.py`。

**注意：** Windows下使用Flask默认的HTTP服务器，Linux下将自动使用`hypercorn`作为HTTP服务器。

### 四、各模块说明

1. 在`application/config`自定义配置。
2. 在`application/enumeration`自定义枚举类型。
3. 在`application/util`自定义工具类。
4. 在`application/exception`自定义异常类。
5. 在`application/middleware`自定义中间件。