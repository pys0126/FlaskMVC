from flask import Flask, Blueprint

app = Flask(__name__)

test = Blueprint('test', __name__)


# 定义一个带参数的装饰器
def log_request(logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(logger)
            return func(*args, **kwargs)

        return wrapper

    return decorator


# 使用带参数的装饰器
@test.route('/')
@log_request("xxx")
def index():
    return "Hello, World!"


if __name__ == '__main__':
    app.register_blueprint(test, url_prefix='/')
    app.run(debug=True)
