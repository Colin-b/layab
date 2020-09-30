import flask
import pytest

import layab.flask_restx


@pytest.fixture
def client():
    app = flask.Flask(__name__)

    @app.route("/standard_responses", methods=["POST"])
    def post():
        return layab.flask_restx.location_response("/standard_responses?id=42")

    with app.test_client() as client:
        yield client


def test_standard_post_response_without_reverse_proxy(client):
    response = client.post("/standard_responses")
    assert response.status_code == 201
    assert response.data == b""
    assert response.headers["location"] == "http://localhost/standard_responses?id=42"


def test_standard_post_response_with_reverse_proxy(client):
    response = client.post(
        "/standard_responses",
        headers={
            "X-Original-Request-Uri": "/reverse/standard_responses",
            "Host": "localhost",
        },
    )
    assert response.status_code == 201
    assert response.data == b""
    assert (
        response.headers["location"]
        == "http://localhost/reverse/standard_responses?id=42"
    )
