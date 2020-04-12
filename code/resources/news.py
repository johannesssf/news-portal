"""News methods API
"""
from flask_restful import Resource, reqparse
from models.news import NewsModel
from models.author import AuthorModel


class NewsResource(Resource):
    """Class responsible to handle the methods used to manage news.
    """
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
        reqdata = NewsResource.parser.parse_args()
        news = NewsModel(reqdata['title'],
                         reqdata['content'],
                         reqdata['author_id'])
        news.save_to_db()
        return news.json(), 201

    def put(self, news_id):
        reqdata = NewsResource.parser.parse_args()

        news_obj = NewsModel.find_by_id(news_id)
        if news_obj is not None:
            if len(reqdata['title']):
                news_obj.title = reqdata['title']
            if len(reqdata['content']):
                news_obj.content = reqdata['content']
            if len(reqdata['author_id']):
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
    """Class responsible to handle the methods used to search and
    visualize news.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('search_key',
                        type=str,
                        required=False)

    def get(self):
        reqdata = NewsList.parser.parse_args()

        if reqdata['search_key'] is None:
            return [n.json() for n in NewsModel.find_all()]

        found_news = NewsModel.find_any(reqdata['search_key'])
        authors_news = []
        for author in AuthorModel.find_by_name(reqdata['search_key']):
            authors_news += NewsModel.find_by_author(author.id)

        for news in authors_news:
            if news in found_news:
                found_news.remove(found_news.index(news))


        return [n.json() for n in found_news + authors_news]
