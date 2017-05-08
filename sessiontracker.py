import logging
import flask
from marshmallow import Schema, fields

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
    resolution = fields.Nested(Resolution, required=True)


@app.route('/track/<action>', methods=['POST'])
def track(action):
    (info, errors) = SessionAction().load(flask.request.get_json())
    if errors:
        return flask.jsonify({'errors': errors}), 422

    logger.info("Track: %r %r", action, info)

    location = {}
    return flask.jsonify(
        action=action,
        info=info,
        location=location,
    )
