## Demo project that implements a session-tracking Swagger API

API spec: [swagger.yaml](docs/swagger.yaml)

### Setup
* Create a virtualenv and activate it
* Install dependencies: `pip install -r requirements.txt`

### Development
Dependencies are tracked using
[pip-tools](https://github.com/jazzband/pip-tools). To add a new dependency,
add it to `requirements.in`, then run `pip-compile` and `pip-sync`.
