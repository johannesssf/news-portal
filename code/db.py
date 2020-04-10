"""Database
"""
from pymongo import MongoClient


class NewsPortalDB:

    def __init__(self, collection):
        mongo = MongoClient("mongodb://localhost:27017")
        self.newsdb = mongo.newsportal[collection]


NEWS_DB = [
    {
        'id': 1,
        'title': 'News 01',
        'content': 'News 01 content',
        'created_on': '01-12-19',
        'author_id': 1
    },
    {
        'id': 2,
        'title': 'News 02',
        'content': 'News 02 content',
        'created_on': '02-12-19',
        'author_id': 1
    },
    {
        'id': 3,
        'title': 'News 03',
        'content': 'News 03 content',
        'created_on': '03-12-19',
        'author_id': 2
    },
    {
        'id': 4,
        'title': 'News 04',
        'content': 'News 04 content',
        'created_on': '04-12-19',
        'author_id': 2
    },
]

AUTHORS_DB = [
        {
            'id': 1,
            'name': 'Johannes',
        },
        {
            'id': 2,
            'name': 'Rafaella',
        },
        {
            'id': 3,
            'name': 'Peter',
        },
    ]
