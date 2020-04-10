"""Author model
"""
import unittest

from bson.objectid import ObjectId
from pymongo.errors import InvalidId

from db import NewsPortalDB


class AuthorModel:
    db = NewsPortalDB('authors')

    def __init__(self, name, _id=None):
        self.id = _id
        self.name = name

    @classmethod
    def find_all(cls):
        """Find all authors into database.

        Returns:
            List[AuthorModel] -- All available authors objects
        """
        return [AuthorModel(a['name'], str(a['_id']))
                for a in cls.db.newsdb.find()]

    @classmethod
    def find_by_name(cls, name):
        """Find an author filtering by its name.

        Arguments:
            name {str} -- Name to be searched

        Returns:
            AuthorModel -- A matching author with the name, None otherwise
        """
        author = cls.db.newsdb.find_one({'name': name})

        if author is not None:
            author = AuthorModel(author['name'], str(author['_id']))

        return author

    @classmethod
    def find_by_id(cls, author_id):
        """Find an author filtering by its id.

        Arguments:
            name {str} -- id to be searched

        Returns:
            AuthorModel -- A matching author with the id, None otherwise
        """
        try:
            author = cls.db.newsdb.find_one({'_id': ObjectId(str(author_id))})
            if author is not None:
                author = AuthorModel(author['name'], str(author['_id']))
        except InvalidId:
            author = None

        return author

    def json(self):
        """A JSON representation of the AuthorModel object with dict.

        Returns:
            dict -- JSON representation
        """
        return {
            'id': self.id,
            'name': self.name
        }

    def save_to_db(self):
        """Save the current object to the database.
        """
        result = self.db.newsdb.insert_one({"name": self.name})
        self.id = str(result.inserted_id)

    def delete_from_db(self):
        """Delete the current object from the database.
        """
        self.db.newsdb.delete_one({'_id': ObjectId(self.id)})


class AuthorModelTestCase(unittest.TestCase):
    def test_find_all(self):
        new_author1 = AuthorModel('Any Author')
        new_author1.save_to_db()

        new_author2 = AuthorModel('New Author')
        new_author2.save_to_db()

        all_authors = [a.json() for a in AuthorModel.find_all()]
        self.assertTrue(new_author1.json() in all_authors)
        self.assertTrue(new_author2.json() in all_authors)
        new_author1.delete_from_db()
        new_author2.delete_from_db()

    def test_find_by_name(self):
        new_author1 = AuthorModel('My Author')
        new_author1.save_to_db()

        author = AuthorModel.find_by_name('My Author')
        self.assertIsNotNone(author)
        self.assertEqual(author.name, new_author1.name)

        new_author1.delete_from_db()
        author = AuthorModel.find_by_name('My Author')
        self.assertIsNone(author)

    def test_find_by_id(self):
        new_author1 = AuthorModel('Anonymous')
        new_author1.save_to_db()

        obj = AuthorModel.find_by_id(new_author1.id)
        self.assertEqual(obj.name, new_author1.name)
        new_author1.delete_from_db()

        obj = AuthorModel.find_by_id('a1b2c3d4')
        self.assertIsNone(obj)

        obj = AuthorModel.find_by_id(123)
