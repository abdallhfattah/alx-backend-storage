#!/usr/bin/env python3
"""
List all documents in Python
"""


def list_all(mongo_collection):
    """listing all mongo collections"""
    return mongo_collection.find()
