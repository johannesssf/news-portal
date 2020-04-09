"""New model
"""
import db
import unittest

from datetime import datetime


class NewsModel:

    def __init__(self, title, content, author_id):
        self.id = datetime.now().microsecond
        self.title = title
        self.content = content
        self.created_on = datetime.now().strftime('%d-%m-%Y')
        self.author_id = author_id

    @classmethod
    def find_all(cls):
        return db.NEWS_DB

    @classmethod
    def find_by_id(cls, _id):
        for news in db.NEWS_DB:
            if news['id'] == _id:
                obj = NewsModel(news['title'],
                                news['content'],
                                news['author_id'])
                obj.id = news['id']
                obj.created_on = news['created_on']
                return obj
        return None

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_on': self.created_on,
            'author_id': self.author_id
        }

    def save_to_db(self):
        db.NEWS_DB.append(
            {
                'id': self.id,
                'title': self.title,
                'content': self.content,
                'created_on': self.created_on,
                'author_id': self.author_id
            }
        )

    def delete_from_db(self):
        for news in NewsModel.find_all():
            if news['id'] == self.id:
                db.NEWS_DB.remove(news)
                return


class NewsModelTestCase(unittest.TestCase):
    def test_save_to_db(self):
        new_news1 = NewsModel('News 005', 'News 005 content', 3)
        new_news1.save_to_db()

        new_news2 = NewsModel('News 006', 'News 006 content', 1)
        new_news2.save_to_db()

        self.assertTrue(new_news1.json() in NewsModel.find_all())
        self.assertTrue(new_news2.json() in NewsModel.find_all())

        new_news1.delete_from_db()
        new_news2.delete_from_db()

    def test_find_by_id(self):
        new_news1 = NewsModel('Some News', 'Some News content', 3)
        new_news1.save_to_db()

        obj = NewsModel.find_by_id(new_news1.id)
        self.assertEqual(obj.title, new_news1.title)
        new_news1.delete_from_db()

        obj = NewsModel.find_by_id(0)
        self.assertIsNone(obj)
