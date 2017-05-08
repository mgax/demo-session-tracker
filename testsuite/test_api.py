import pytest
import requests
import responses

@pytest.fixture
def app():
    from sessiontracker import app
    return app

@responses.activate
def test_homepage(client):
    def call_app(request):
        resp = client.get('/')
        return (resp.status_code, dict(resp.headers), resp.data)

    responses.add_callback(
        responses.GET,
        'http://example.com/',
        callback=call_app,
    )

    resp = requests.get('http://example.com/')
    assert resp.text == 'hi'
