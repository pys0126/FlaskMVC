# Flask后端快速开发模板

项目使用`Python>=3.7`，将`Flask、Flask-SQLAlchemy、Flask-Cors、Redis、HttpX、PIL、PyYaml`集成，包含各种工具包，方便快速开发。

## 简要说明

强烈推荐使用`venv`环境，避免环境冲突；整个项目应关注于`application`目录下的内容，其他目录为辅助工具。

### 一、配置项目

1. 编辑`config-template.yaml`配置模板。
2. 将配置信息复制到`config.yaml`（新建）中。

### 二、开发顺序（推荐）

1. 在`application/model`目录，创建数据库模型，并在`application/model/__init__.py`导入。
2. 在`application/mapper`目录，创建表操作。 
3. 在`application/logic`目录，创建业务逻辑。
4. 在`application/controller`目录，创建控制器。
5. 注册蓝图、异常均在`application/__init__.py`。

### 三、运行项目

**注意：** Windows下自动使用Flask默认的HTTP服务器，Linux下将自动使用`gunicorn`作为HTTP服务器。

1. Run：`python main.py`。

### 四、扩展

1. 在`application/config`自定义配置。
2. 在`application/enumeration`自定义枚举类型。
3. 在`application/util`自定义工具类。
4. 在`application/exception`自定义异常类。
5. 在`application/middleware`自定义中间件。