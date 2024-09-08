#!/usr/bin/env python3
"""schools  by topic"""


def schools_by_topic(mongo_collection, topic):
    """school by topics"""
    mongo_collection.find({"topic": topic})
