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
        fun_name = method.__qualname__
        inputs = f"{fun_name}:inputs"
        outputs = f"{fun_name}:outputs"
        result = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(inputs, str(args))
            self._redis.rpush(outputs, result)
        return result

    return wrapper


def replay(fn: Callable) -> None:
    """replaying what was called from some function : fn"""
    if fn is None or not hasattr(fn, "__self__"):
        return

    redis_storage = getattr(fn.__self__, "_redis")

    if not isinstance(redis_storage, redis.Redis):
        return

    count = 0
    fun_name = fn.__qualname__

    if redis_storage.exists(fun_name):
        count = int(redis_storage.get(fun_name))

    inputs = redis_storage.lrange(f"{fun_name}:inputs", 0, -1)
    outputs = redis_storage.lrange(f"{fun_name}:outputs", 0, -1)

    print("{} was called {} times:".format(fun_name, count))

    for inp, out in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(fun_name, inp.decode("utf-8"), out))


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
