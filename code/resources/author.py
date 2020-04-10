"""Author methord API
"""
from flask_restful import Resource

from models.author import AuthorModel


class AuthorResource(Resource):

    def get(self, name):
        author = AuthorModel.find_by_name(name)
        if author is not None:
            return author.json()
        return {'message': f"Author '{name}' not found."}, 404

    def post(self, name):
        author = AuthorModel.find_by_name(name)
        if author is None:
            author = AuthorModel(name)
            author.save_to_db()
        return author.json(), 201

    def delete(self, name):
        author = AuthorModel.find_by_name(name)
        if author is not None:
            author.delete_from_db()
            return {'message': 'Author deleted.'}
        return {'message': f"Author '{name}' not found."}, 404


class AuthorList(Resource):

    def get(self):
        return [a.json() for a in AuthorModel.find_all()]
