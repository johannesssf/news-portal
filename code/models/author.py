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

    @classmethod
    def find_by_name(cls, name):
        for author in db.AUTHORS_DB:
            if author['name'].lower() == name.lower():
                new_author = AuthorModel(author['name'])
                new_author.id = author['id']
                return new_author
        return None

    @classmethod
    def find_by_id(cls, author_id):
        for author in db.AUTHORS_DB:
            if author['id'] == author_id:
                obj = AuthorModel(author['name'])
                obj.id = author['id']
                return obj
        return None

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
        new_author1 = AuthorModel('Any Author')
        new_author1.save_to_db()

        new_author2 = AuthorModel('New Author')
        new_author2.save_to_db()

        all_authors = AuthorModel.find_all()
        self.assertTrue(new_author1.json() in all_authors)
        self.assertTrue(new_author2.json() in all_authors)
        new_author1.delete_from_db()
        new_author2.delete_from_db()

    def test_find_by_name(self):
        new_author1 = AuthorModel('My Author')
        new_author1.save_to_db()

        author = AuthorModel.find_by_name('My Author')
        self.assertIsNotNone(author)
        self.assertEqual(author.name, 'My Author')

        new_author1.delete_from_db()
        author = AuthorModel.find_by_name('My Author')
        self.assertIsNone(author)

    def test_find_by_id(self):
        new_author1 = AuthorModel('Anonymous')
        new_author1.save_to_db()

        obj = AuthorModel.find_by_id(new_author1.id)
        self.assertEqual(obj.name, new_author1.name)
        new_author1.delete_from_db()

        obj = AuthorModel.find_by_id(0)
        self.assertIsNone(obj)
