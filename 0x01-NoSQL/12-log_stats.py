#!/usr/bin/env python3
"""log stats"""

from pymongo import MongoClient

def nginx_stats():
    """
    Connects to the MongoDB logs database and retrieves statistics about the nginx logs.
    """
    # Connect to MongoDB
    client = MongoClient()

    # Access the 'logs' database and 'nginx' collection
    db = client.logs
    nginx_collection = db.nginx

    # Count the total number of logs
    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")

    # Count the number of logs for each HTTP method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        method_count = nginx_collection.count_documents({"method": method})
        print(f"\t{method}: {method_count}")

    # Count the number of GET requests to the /status path
    status_check = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )
    print(f"{status_check} status check")


if __name__ == "__main__":
    nginx_stats()
