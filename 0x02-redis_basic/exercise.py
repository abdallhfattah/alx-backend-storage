#!/usr/bin/env python3

import redis
import uuid
from typing import Union


class Cache:
    """caching class"""

    def __init__(self):
        _redis = redis.Redis()
        _redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> uuid.UUID:
        random_key = uuid.uuid1()
        _redis.set(random_key, data)
        return random_key
