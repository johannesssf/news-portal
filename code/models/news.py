"""New model
"""
import unittest

from bson.objectid import ObjectId
from pymongo.errors import InvalidId

from db import NewsPortalDB


class NewsModel:
    db = NewsPortalDB('news')

    def __init__(self, title, content, author_id, _id=None):
        self.id = _id
        self.title = title
        self.content = content
        self.author_id = author_id

    @classmethod
    def find_all(cls):
        """Find all news into database.

        Returns:
            List[NewsModel] -- All available news objects
        """
        return [
            NewsModel(title=n['title'],
                      content=n['content'],
                      author_id=str(n['author_id']),
                      _id=str(n['_id']))
            for n in cls.db.newsdb.find()]

    @classmethod
    def find_by_id(cls, news_id):
        """Find a news filtering by its id.

        Arguments:
            name {str} -- id to be searched

        Returns:
            NewsModel -- A matching news with the id, None otherwise
        """
        try:
            news = cls.db.newsdb.find_one({'_id': ObjectId(str(news_id))})
            if news is not None:
                news = NewsModel(title=news['title'],
                                 content=news['content'],
                                 author_id=str(news['author_id']),
                                 _id=str(news['_id']))
        except InvalidId:
            news = None

        return news

    def json(self):
        """A JSON representation of the NewsModel object with dict.

        Returns:
            dict -- JSON representation
        """
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author_id': self.author_id
        }

    def save_to_db(self):
        """Save the current object to the database.
        """
        result = self.db.newsdb.insert_one(
            {
                'title': self.title,
                'content': self.content,
                'author_id': ObjectId(self.author_id)
            }
        )
        self.id = str(result.inserted_id)

    def delete_from_db(self):
        """Delete the current object from the database.
        """
        self.db.newsdb.delete_one({'_id': ObjectId(self.id)})


class NewsModelTestCase(unittest.TestCase):
    def test_save_to_db(self):
        new_news1 = NewsModel('News 005',
                              'News 005 content',
                              '5e90b342364975e5081a5555')
        new_news1.save_to_db()

        new_news2 = NewsModel('News 006',
                              'News 006 content',
                              '5e90b342364975e5081a7777')
        new_news2.save_to_db()

        all_news = [n.json() for n in NewsModel.find_all()]
        self.assertTrue(new_news1.json() in all_news)
        self.assertTrue(new_news2.json() in all_news)

        new_news1.delete_from_db()
        new_news2.delete_from_db()

    def test_find_by_id(self):
        new_news1 = NewsModel('Some News',
                              'Some News content',
                              '5e90b342364975e5081a7777')
        new_news1.save_to_db()

        obj = NewsModel.find_by_id(new_news1.id)
        self.assertEqual(obj.title, new_news1.title)
        new_news1.delete_from_db()

        obj = NewsModel.find_by_id('5e90b342364975e5081a0000')
        self.assertIsNone(obj)
