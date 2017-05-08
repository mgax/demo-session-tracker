import logging
import flask
from marshmallow import Schema, fields
import requests

ACTIONS = ['login', 'logout', 'buy', 'review', 'shopping-cart']

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
app = flask.Flask(__name__)

@app.route('/')
def homepage():
    return 'hi'

class Resolution(Schema):
    width = fields.Int(required=True)
    height = fields.Int(required=True)

class SessionAction(Schema):
    ip = fields.Str(required=True)
    browser = fields.Str(required=True)
    browser_version = fields.Str()
    os = fields.Str()
    os_version = fields.Str()
    resolution = fields.Nested(Resolution, required=True)

def geolocate(ip):
    resp = requests.get('http://freegeoip.net/json/{}'.format(ip)).json()
    return {
        'longitude': resp['longitude'],
        'latitude': resp['latitude'],
        'city': resp['city'],
        'state': resp['region_name'],
        'country': resp['country_name'],
        'country_iso2': resp['country_code'],
        'postal': resp['zip_code'],
        'continent': resp['time_zone'].split('/')[0],
    }

@app.route('/track/<action>', methods=['POST'])
def track(action):
    if action not in ACTIONS:
        flask.abort(404)

    (info, errors) = SessionAction().load(flask.request.get_json())
    if errors:
        return flask.jsonify({'errors': errors}), 400

    logger.info("Track: %r %r", action, info)

    location = geolocate(info['ip'])

    return flask.jsonify(
        action=action,
        info=info,
        location=location,
    )

if __name__ == '__main__':
    app.run(debug=True)
