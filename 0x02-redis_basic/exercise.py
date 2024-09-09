#!/usr/bin/env python3

import redis
import uuid
from typing import Union


class Cache:
    """caching class"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> uuid.UUID:
        key = uuid.uuid1()
        self._redis.set(key, data)
        return key
