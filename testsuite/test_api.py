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

@responses.activate
def _call_api(client, action, info):
    def call_app(request):
        resp = client.post(
            '/track/{}'.format(action),
            data=request.body,
            content_type='application/json',
        )
        return (resp.status_code, dict(resp.headers), resp.data)

    responses.add_callback(
        responses.POST,
        'http://example.com/track/{}'.format(action),
        callback=call_app,
    )

    return requests.post(
        'http://example.com/track/{}'.format(action),
        json=info,
    )

def test_login(client):
    info = {'ip': '8.8.8.8', 'resolution': {'width': 200, 'height': 100}}
    expected_location = {}
    resp = _call_api(client, 'login', info)
    assert resp.json() == {
        'action': 'login',
        'info': info,
        'location': expected_location,
    }
