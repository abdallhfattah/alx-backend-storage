#!/usr/bin/env python3
"""
  module to get some content from web
  saves it in redis 
"""
import requests
import redis
from functools import wraps
from typing import Callable

redis_stroage = redis.Redis()


def cache(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(url: str) -> str:
        redis_stroage.incr(f"count:{url}")
        result = redis_stroage.get(f"result:{url}")
        if result:
            return result.decode("utf-8")
        result = method(url)
        redis_stroage.incr(f"count:{url}")
        redis_stroage.setex(f"result:{url}", 10, result)
        return result
    return wrapper


@cache
def get_page(url: str) -> str:
    return requests.get(url).text
