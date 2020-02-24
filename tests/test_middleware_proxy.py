import pytest
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

import layab.starlette


@pytest.fixture
def client():
    app = Starlette(middleware=[Middleware(layab.starlette.ProxyHeadersMiddleware)])

    @app.route("/proxy")
    def proxy(request):
        return JSONResponse(
            {"scheme": request.scope["scheme"], "client": request.scope["client"]}
        )

    return TestClient(app)


def test_default(client):
    response = client.get("/proxy")
    assert response.status_code == 200
    assert response.json() == {"client": ["testclient", 50000], "scheme": "http"}


def test_forwarded_proto(client):
    response = client.get("/proxy", headers={"x-forwarded-proto": "https"})
    assert response.status_code == 200
    assert response.json() == {"client": ["testclient", 50000], "scheme": "https"}


def test_forwarded_for(client):
    response = client.get("/proxy", headers={"x-forwarded-for": "my_original_url"})
    assert response.status_code == 200
    assert response.json() == {"client": ["my_original_url", 0], "scheme": "http"}


def test_forwarded_proto_and_for(client):
    response = client.get(
        "/proxy",
        headers={"x-forwarded-proto": "https", "x-forwarded-for": "my_original_url"},
    )
    assert response.status_code == 200
    assert response.json() == {"client": ["my_original_url", 0], "scheme": "https"}
