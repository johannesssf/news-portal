"""News model
"""
import pymongo
import unittest

from bson.objectid import ObjectId
from pymongo.errors import InvalidId

from db import NewsPortalDB


class NewsModel:
    db = NewsPortalDB('news')
    db.newsdb.create_index(
        [('title', pymongo.TEXT), ('content', pymongo.TEXT)],
        name='news_title_content_index'
    )

    def __init__(self, title, content, author_id, _id=None):
        self.id = _id
        self.title = title
        self.content = content
        self.author_id = author_id

    def __eq__(self, news_obj):
        return all([
            self.id == news_obj.id,
            self.title == news_obj.title,
            self.content == news_obj.content,
            self.author_id == news_obj.author_id,
        ])

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

    @classmethod
    def find_any(cls, keyword):
        """Find all news with the matching keyword.

        Returns:
            list[NewsModel] -- A list of news with a matching keyword
            in its title or content
        """
        news = []
        for n in cls.db.newsdb.find({'$text': {'$search': keyword}}):
            news.append(
                NewsModel(title=n['title'],
                          content=n['content'],
                          author_id=str(n['author_id']),
                          _id=str(n['_id']))
            )

        return news

    @classmethod
    def find_by_author(cls, author_id):
        """Find all news with matching author_id.

        Arguments:
            author_id {str} -- Author id

        Returns:
            list[NewsModel] -- List with all news matching the author id
        """
        news = []
        all_news = cls.db.newsdb.find({'author_id': ObjectId(author_id)})
        for n in all_news:
            news.append(
                NewsModel(title=n['title'],
                          content=n['content'],
                          author_id=str(n['author_id']),
                          _id=str(n['_id']))
            )

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
        if self.id is None:
            result = self.db.newsdb.insert_one(
                {
                    'title': self.title,
                    'content': self.content,
                    'author_id': ObjectId(self.author_id)
                }
            )
            self.id = str(result.inserted_id)
        else:
            self.db.newsdb.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': {
                    'title': self.title,
                    'content': self.content,
                    'author_id': ObjectId(self.author_id)
                }}
            )

    def delete_from_db(self):
        """Delete the current object from the database.
        """
        self.db.newsdb.delete_one({'_id': ObjectId(self.id)})


class NewsModelTestCase(unittest.TestCase):
    def test_save_to_db_create(self):
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

    def test_save_to_db_update(self):
        new_news1 = NewsModel('News 007',
                              'News 007 content',
                              '5e90b342364975e5081a3333')
        new_news1.save_to_db()
        new_news1_id = new_news1.id

        new_news1.title = 'News 007 updated'
        new_news1.content = 'News 007 content updated'
        new_news1.save_to_db()

        self.assertEqual(new_news1_id, new_news1.id)
        new_news1.delete_from_db()

    def test_find_by_id(self):
        new_news1 = NewsModel('Some News',
                              'Some News content',
                              '5e90b342364975e5081a7777')
        new_news1.save_to_db()

        obj = NewsModel.find_by_id(new_news1.id)
        self.assertEqual(obj, new_news1)
        new_news1.delete_from_db()

        obj = NewsModel.find_by_id('5e90b342364975e5081a0000')
        self.assertIsNone(obj)

        obj = NewsModel.find_by_id(1234)
        self.assertIsNone(obj)

    def test_find_any(self):
        new_news1 = NewsModel('News 005',
                              'News 005 content',
                              '5e90b342364975e5081a5555')
        new_news1.save_to_db()

        new_news2 = NewsModel('News 006',
                              'News 006 content',
                              '5e90b342364975e5081a7777')
        new_news2.save_to_db()

        found_news = NewsModel.find_any('News')
        self.assertTrue(len(found_news) == 2)

        found_news = NewsModel.find_any('content')
        self.assertTrue(len(found_news) == 2)

        found_news = NewsModel.find_any('005')
        self.assertTrue(len(found_news) == 1)

        new_news1.delete_from_db()
        new_news2.delete_from_db()

    def test_find_by_author(self):
        new_news1 = NewsModel('News 111',
                              'News 111 content',
                              '5e90b342364975e5081a5555')
        new_news1.save_to_db()

        new_news2 = NewsModel('News 222',
                              'News 222 content',
                              '5e90b342364975e5081a7777')
        new_news2.save_to_db()

        new_news3 = NewsModel('News 333',
                              'News 333 content',
                              '5e90b342364975e5081a7777')
        new_news3.save_to_db()

        found_news = NewsModel.find_by_author('5e90b342364975e5081a7777')
        self.assertTrue(len(found_news) == 2)
        self.assertFalse(new_news1 in found_news)
        self.assertTrue(new_news2 in found_news)
        self.assertTrue(new_news3 in found_news)

        found_news = NewsModel.find_by_author('5e90b342364975e5081a5555')
        self.assertTrue(len(found_news) == 1)
        self.assertTrue(new_news1 in found_news)

        found_news = NewsModel.find_by_author('5e90b342364975e5081a1111')
        self.assertTrue(len(found_news) == 0)

        new_news1.delete_from_db()
        new_news2.delete_from_db()
        new_news3.delete_from_db()
