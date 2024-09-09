#!/usr/bin/env python3
"""
Caching request module with Redis
This module provides a way to cache HTTP responses and track
the number of times a URL is accessed.
"""

import redis
import requests
from functools import wraps
from typing import Callable


def track_get_page(fn: Callable[[str], str]) -> Callable[[str], str]:
    """
    Decorator for get_page that tracks URL access count and caches
    the response for 10 seconds.

    Args:
        fn: The function to wrap, expects a URL string as an argument.

    Returns:
        The wrapped function.
    """

    @wraps(fn)
    def wrapper(url: str) -> str:
        """
        Wrapper function that:
        - Increments the access count for the URL in Redis.
        - Checks the cache for an existing response.
        - If a cached response exists, it returns it.
        - Otherwise, it makes a request, caches the result for 10 seconds
          and returns the response.

        Args:
            url: The URL to fetch the page from.

        Returns:
            The HTML content of the page as a string.
        """
        client = redis.Redis()

        # Increment the access count for the URL
        client.incr(f"count:{url}")

        # Check if the page is already cached
        cached_page = client.get(f"{url}")
        if cached_page:
            return cached_page.decode("utf-8")

        # Fetch the page from the web
        response = fn(url)

        # Cache the response for 10 seconds
        client.setex(f"{url}", 10, response)

        return response

    return wrapper


@track_get_page
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a webpage.

    Args:
        url: The URL of the webpage to fetch.

    Returns:
        The HTML content of the page as a string.
    """
    response = requests.get(url)
    return response.text
