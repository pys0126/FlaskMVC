"""
Token工具包
"""
import jwt
from typing import Optional
from application.util.TimeUtil import now_timestamp
from application.util.RedisUtil import RedisUtil
from application.config.ServerConfig import ServerConfig
from application.util.StringUtil import base64_encode, random_uuid

# redis客户端
redis_client: RedisUtil = RedisUtil()


def generate_token(user_id: int) -> str:
    """
    根据用ID生成token
    :param user_id: 用户id
    :return: token
    """
    # 其他参数：Base64(UUID + 用户id + 时间戳)
    other_str: str = base64_encode(text=f"{random_uuid()}{user_id}{now_timestamp()}")
    payload: dict = {
        "user_id": user_id,
        "baby": other_str
    }
    # 生成Token
    token: str = jwt.encode(payload=payload, key=ServerConfig.secret_key, algorithm="HS256")
    # 删除该用户ID旧的token
    delete_exist_token(user_id=user_id)
    # 缓存Token，Token作为key，值为用户id
    redis_client.set_value(key=str(user_id), value=token, ex=ServerConfig.token_expire)
    return token


def verify_token(token: str) -> bool:
    """
    根据token和用户id验证token是否正确
    :param token: token
    :return: bool
    """
    try:
        payload: dict = jwt.decode(jwt=token, key=ServerConfig.secret_key, algorithms=["HS256"])
        user_id: int = payload.get("user_id")
        # 从redis中获取token
        redis_token: Optional[str] = redis_client.get_value(key=str(user_id))
        if redis_token != token:
            return False
        return True
    except Exception:
        return False


def clear_token(user_id: int) -> bool:
    """
    清除token
    :param user_id: user_id
    :return: None
    """
    try:
        user_id: str = str(user_id)
        # 从redis中获取token
        redis_token: Optional[str] = redis_client.get_value(key=user_id)
        if redis_token is None:
            return False
        redis_client.delete_by_key(key=user_id)  # 删除redis缓存的token
        return True
    except Exception:
        return False


def delete_exist_token(user_id: int) -> None:
    """
    删除同一个用户的token，保证用户只能有一个token
    :param user_id: 用户ID
    :return: None
    """
    redis_client.delete_by_key(key=str(user_id))  # 删除token


def get_user_id(token: str) -> int:
    """
    获取用户id
    :param token: token
    :return: 用户id | 0
    """
    try:
        payload: dict = jwt.decode(jwt=token, key=ServerConfig.secret_key, algorithms=["HS256"])
        user_id: int = payload.get("user_id")
        # 从redis中获取token
        redis_token: Optional[str] = redis_client.get_value(key=str(user_id))
        if redis_token != token:
            return 0
        return user_id
    except Exception:
        return 0
