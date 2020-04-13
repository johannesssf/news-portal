import json
import pytest

from requests import get, post, put, delete
from models.author import AuthorModel
from models.news import NewsModel


APP_URL = 'http://localhost:5000'

AUTHORS = [
    {'name': 'Peter'},
    {'name': 'Linda'},
    {'name': 'Beth'},
    {'name': 'John'},
]


def test_create_authors():
    for author in AUTHORS:
        resp = post(f"{APP_URL}/author/{author['name']}")
        assert resp.status_code == 201

    assert len(json.loads(get(APP_URL + "/authors").content)) == len(AUTHORS)


def test_read_authors_ids():
    for author in AUTHORS:
        author['id'] = json.loads(
            get(f"{APP_URL}/author/{author['name']}").content)['id']


def test_create_news():
    for i in range(len(AUTHORS)):
        news = {
            'title': f'News00{i}',
            'content': f'News content00{i}',
            'author_id': AUTHORS[i]['id']
        }
        resp = post(APP_URL + '/news', news)
        assert resp.status_code == 201

    assert len(json.loads(get(APP_URL + '/news/search').content))


def test_update_news():
    for news in json.loads(get(APP_URL + '/news/search').content):
        news['title'] = news['title'] + ' updated'
        news['content'] = news['content'] + ' updated'
        put(APP_URL + f"/news/{news['id']}", news)

    for news in json.loads(get(APP_URL + '/news/search').content):
        assert 'updated' in news['title']
        assert 'updated' in news['content']


def test_search_news():
        assert len(json.loads(get(APP_URL + '/news/search?search_key=News000').content)) == 1
        assert len(json.loads(get(APP_URL + '/news/search?search_key=News001').content)) == 1
        assert len(json.loads(get(APP_URL + '/news/search?search_key=News').content)) == len(AUTHORS)

        assert len(json.loads(get(APP_URL + '/news/search?search_key=Peter').content)) == 1


def test_delete_news():
    for news in json.loads(get(APP_URL + '/news/search').content):
        delete(APP_URL + f"/news/{news['id']}")


def test_delete_authors():
    for author in AUTHORS:
        resp = delete(f"{APP_URL}/author/{author['name']}")
        assert resp.status_code == 200


if __name__ == "__main__":
    test_create_authors()
    test_read_authors_ids()
    test_create_news()
    test_update_news()
    test_search_news()
    test_delete_news()
    test_delete_authors()
