"""Database
"""
from pymongo import MongoClient


class NewsPortalDB:
    """MongoDB connection class.
    """
    def __init__(self, collection):
        mongo = MongoClient("mongodb://localhost:27017")
        self.newsdb = mongo.newsportal[collection]
