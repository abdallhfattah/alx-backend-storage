#!/usr/bin/env python3

import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        returns the given method after incrementing its call counter.
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Returns the method's output after storing its inputs and output."""
        func_name = method.__qualname__
        inputs_key = f"{func_name}:inputs"
        outputs_key = f"{func_name}:outputs"
        result = method(*args, **kwargs)

        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(inputs_key, str(args))
            self._redis.r.rpush(outputs_key, str(result))
        return result

    return wrapper


class Cache:
    """caching class"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self,
        key: str,
        fn: Callable = None,
    ) -> Union[str, bytes, int, float]:
        obj = self._redis.get(key)
        if obj is None:
            return None
        return fn(obj) if fn else obj

    def get_str(self, key: str) -> str:
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        return self.get(key, lambda x: int(x))
