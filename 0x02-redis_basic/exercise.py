#!/usr/bin/env python3

import redis
import uuid
from typing import Union


class Cache:
    """caching class"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: callable):
        obj = self._redis.get(key)
        if obj is None:
            return None
        return fn(obj) if fn else obj

    def get_str(self, key: str) -> str:
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        return self.get(key, int)
