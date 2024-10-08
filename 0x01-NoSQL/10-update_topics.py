#!/usr/bin/env python3
"""Updating topics"""


def update_topics(mongo_collection, name, topics):
    """updating topics using name"""
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
