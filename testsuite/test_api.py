import pytest
import requests
import responses

RESP_LOCATION = {
    'city': 'Mountain View',
    'continent': 'America',
    'country': 'United States',
    'country_iso2': 'US',
    'latitude': 37.386,
    'longitude': -122.0838,
    'postal': '94035',
    'state': 'California',
}

FREEGEOIP_MOCK_RESPONSE = {
    'ip': '8.8.8.8',
    'country_code': 'US',
    'country_name': 'United States',
    'region_code': 'CA',
    'region_name': 'California',
    'city': 'Mountain View',
    'zip_code': '94035',
    'time_zone': 'America/Los_Angeles',
    'latitude': 37.386,
    'longitude': -122.0838,
    'metro_code': 807,
}

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

    responses.add(
        responses.GET,
        'http://freegeoip.net/json/{}'.format(info['ip']),
        json=FREEGEOIP_MOCK_RESPONSE,
    )

    return requests.post(
        'http://example.com/track/{}'.format(action),
        json=info,
    )

def test_login(client):
    info = {
        'ip': '8.8.8.8',
        'browser': 'chrome',
        'browser_version': '58.0.3029.96',
        'os': 'OSX',
        'os_version': '10.11.6',
        'resolution': {'width': 200, 'height': 100},
    }
    resp = _call_api(client, 'login', info)
    assert resp.json() == {
        'action': 'login',
        'info': info,
        'location': RESP_LOCATION,
    }
