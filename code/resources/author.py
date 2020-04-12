"""Author methors API
"""
from flask_restful import Resource

from models.author import AuthorModel


class AuthorResource(Resource):
    """Class responsible to handle the methods used to manage authors.
    """
    def get(self, name):
        for author in AuthorModel.find_by_name(name):
            if author.name == name:
                return author.json()
        return {'message': f"Author '{name}' not found."}, 404

    def post(self, name):
        for author in AuthorModel.find_by_name(name):
            if author.name == name:
                return {'message': f'User: {name} already exists.'}

        author = AuthorModel(name)
        author.save_to_db()

        return author.json(), 201

    def delete(self, name):
        authors = AuthorModel.find_by_name(name)
        for author in authors:
            if author.name == name:
                author.delete_from_db()
                return {'message': 'Author deleted.'}
        return {'message': f"Author '{name}' not found."}, 404


class AuthorList(Resource):
    """Class responsible to handle the methods used to visualize
    authors.
    """
    def get(self):
        return [a.json() for a in AuthorModel.find_all()]
