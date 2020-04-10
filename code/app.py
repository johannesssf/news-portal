from flask import Flask
from flask_restful import Api

from resources.author import AuthorResource, AuthorList
from resources.news import NewsResource, NewsList


app = Flask(__name__)
app.secret_key = 'EV1}YJf,>i~S%1v:],jYijl^%4mG1q'
api = Api(app)

api.add_resource(AuthorList, '/authors')
api.add_resource(AuthorResource, '/author/<string:name>')

api.add_resource(NewsList, '/news/search')
api.add_resource(NewsResource, '/news',
                               '/news/<string:news_id>')


if __name__ == "__main__":
    app.run(debug=True)
