"""News API
"""
from flask import jsonify
from flask_restful import Resource, reqparse
from models.news import NewsModel


class NewsResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('content',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('author_id',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")

    def post(self):
        # TODO: Block if the author id is unknown???
        reqdata = NewsResource.parser.parse_args()
        news = NewsModel(reqdata['title'],
                         reqdata['content'],
                         reqdata['author_id'])
        news.save_to_db()
        return news.json()

    def put(self, news_id):
        # TODO: PUT is creating a new news.
        reqdata = NewsResource.parser.parse_args()

        news_obj = NewsModel.find_by_id(news_id)
        if news_obj is not None:
            news_obj.title = reqdata['title']
            news_obj.content = reqdata['content']
            news_obj.author_id = reqdata['author_id']
            news_obj.save_to_db()
            return {'msg': 'News updated.'}

        return {'message': 'News not found.'}, 404

    def delete(self, news_id):
        news_obj = NewsModel.find_by_id(news_id)
        if news_obj is not None:
            news_obj.delete_from_db()
            return {'msg': 'News deleted'}

        return {'message': 'News not found.'}, 404


class NewsList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('search_key',
                        type=str,
                        required=False)

    def get(self):
        reqdata = NewsList.parser.parse_args()

        if reqdata['search_key'] is None:
            return [n.json() for n in NewsModel.find_all()]

        # TODO: Create filter
        return {'msg': f"Filtered news by: {reqdata['search_key']}"}
