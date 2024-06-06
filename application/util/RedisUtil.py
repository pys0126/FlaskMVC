from redis import Redis
from typing import Optional, Any
from application.config.DatabaseConfig import RedisConfig


class RedisUtil:
    def __init__(self) -> None:
        self.redis_client: Redis = Redis(host=RedisConfig.host, port=RedisConfig.port, password=RedisConfig.password,
                                         db=RedisConfig.db)

    def set_value(self, key: str, value: str, ex: int) -> None:
        """
        设置缓存值
        :param key: 键名
        :param value: 值
        :param ex: 存储时间，单位秒
        :return:
        """
        self.redis_client.set(name=key, value=value, ex=ex)

    def set_list_value(self, key: str, value: Any) -> None:
        """
        设置List的缓存值
        :param key: 键名
        :param value: 值
        :return:
        """
        self.redis_client.rpush(key, *value)

    def get_list_value(self, key: str) -> list:
        """
        获取List的缓存值
        :param key: 键名
        :return: 值
        """
        return self.redis_client.lrange(key, 0, -1)

    def get_value(self, key: str) -> Optional[str]:
        """
        获取缓存值
        :param key: 键名
        :return: 值
        """
        try:
            return self.redis_client.get(name=key).decode()
        except AttributeError:
            return None

    def get_keys(self) -> list:
        """
        获取所有键名
        :return: 键名列表
        """
        return [key.decode("u8") for key in self.redis_client.keys()]

    def delete_by_key(self, key: str) -> None:
        """
        根据Key删除值
        :param key: 键名
        :return:
        """
        self.redis_client.delete(key)

    def __del__(self) -> None:
        self.redis_client.close()
