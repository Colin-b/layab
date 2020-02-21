import pytest
from starlette.applications import Starlette
from starlette.testclient import TestClient

import layab


@pytest.fixture
def client():
    app = Starlette()

    @app.route("/standard_responses", methods=["POST"])
    def post(request):
        return layab.LocationResponse(request, "/standard_responses?id=42")

    return TestClient(app)


def test_standard_post_response_without_reverse_proxy(client):
    response = client.post("/standard_responses")
    assert response.status_code == 201
    assert response.text == ""
    assert response.headers["location"] == "http://testserver/standard_responses?id=42"


def test_standard_post_response_with_reverse_proxy(client):
    response = client.post(
        "/standard_responses",
        headers={
            "X-Original-Request-Uri": "/reverse/standard_responses",
            "Host": "localhost",
        },
    )
    assert response.status_code == 201
    assert response.text == ""
    assert (
        response.headers["location"]
        == "http://localhost/reverse/standard_responses?id=42"
    )
