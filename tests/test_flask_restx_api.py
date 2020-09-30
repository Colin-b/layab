import flask
from layab.flask_restx import Api


def test_api():
    app = flask.Flask(__name__)
    Api(
        app,
        title="My API.",
        description="My description.",
        version="1.0.0",
        info={"x-test": "value"},
    )

    with app.test_client() as client:
        response = client.get("/swagger.json")
    assert response.json == {
        "basePath": "/",
        "consumes": ["application/json"],
        "info": {
            "description": "My description.",
            "title": "My API.",
            "version": "1.0.0",
            "x-test": "value",
        },
        "paths": {},
        "produces": ["application/json"],
        "responses": {
            "MaskError": {"description": "When any error occurs on mask"},
            "ParseError": {"description": "When a mask can't be parsed"},
        },
        "swagger": "2.0",
        "tags": [],
    }
