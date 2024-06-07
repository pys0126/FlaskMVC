import jwt
from application.config.ServerConfig import ServerConfig

payload: dict = {
    "user_id": 1,
    "baby": "x"
}

token: str = jwt.encode(payload=payload, key=ServerConfig.secret_key, algorithm="HS256")
print(token)

decode_str: str = jwt.decode(jwt=token, key=ServerConfig.secret_key, algorithms=["HS256"])
print(decode_str)
