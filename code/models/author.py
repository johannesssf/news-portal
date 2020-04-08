"""Author model
"""
import db
import unittest

from datetime import datetime


class AuthorModel:

    def __init__(self, name):
        self.id = datetime.now().microsecond
        self.name = name

    @classmethod
    def find_all(cls):
        return db.AUTHORS_DB

    def json(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def save_to_db(self):
        db.AUTHORS_DB.append({'id': self.id, 'name': self.name})

    def delete_from_db(self):
        for author in db.AUTHORS_DB:
            if author['id'] == self.id:
                db.AUTHORS_DB.remove(author)
                break


class AuthorModelTestCase(unittest.TestCase):
    def test_find_all(self):
        new_author1 = AuthorModel({'id': 10, 'name': 'Any Author'})
        new_author1.save_to_db()

        new_author2 = AuthorModel({'id': 11, 'name': 'New Author'})
        new_author2.save_to_db()

        all_authors = AuthorModel.find_all()
        self.assertTrue(new_author1.json() in all_authors)
        self.assertTrue(new_author2.json() in all_authors)
        new_author1.delete_from_db()
        new_author2.delete_from_db()
