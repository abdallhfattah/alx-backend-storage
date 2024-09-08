#!/usr/bin/env python3
""" 12. Log stats
"""


from pymongo import MongoClient


def log_stats():
    """log_stats."""
    client = MongoClient("mongodb://127.0.0.1:27017")
    logs_collection = client.logs.nginx
    total = logs_collection.count_documents({})
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        result = logs_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {result}")

    path = logs_collection.count_documents({"method": "GET",
                                           "path": "/status"})
    print(f"{total} logs")
    print(f"{path} status check")


if __name__ == "__main__":
    log_stats()
