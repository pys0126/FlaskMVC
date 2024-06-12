from asgiref.wsgi import WsgiToAsgi
from application import app

asgi_app: WsgiToAsgi = WsgiToAsgi(app)
