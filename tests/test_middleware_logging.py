import logging

import pytest
from requests import Request
from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.middleware import Middleware
from starlette.responses import PlainTextResponse
from starlette.testclient import TestClient

import layab.starlette


@pytest.fixture
def client():
    app = Starlette(
        middleware=[
            Middleware(layab.starlette.LoggingMiddleware, skip_paths=["/skipped"])
        ]
    )

    @app.route("/logging")
    class Logging(HTTPEndpoint):
        def get(self, request: Request):
            return PlainTextResponse("")

        def post(self, request: Request):
            return PlainTextResponse("")

        def put(self, request: Request):
            return PlainTextResponse("")

        def delete(self, request: Request):
            return PlainTextResponse("")

    @app.route("/logging_failure")
    class LoggingFailure(HTTPEndpoint):
        def get(self, request: Request):
            raise Exception("Error message")

        def post(self, request: Request):
            raise Exception("Error message")

        def put(self, request: Request):
            raise Exception("Error message")

        def delete(self, request: Request):
            raise Exception("Error message")

    @app.route("/skipped")
    class Skipped(HTTPEndpoint):
        def get(self, request: Request):
            return PlainTextResponse("")

        def post(self, request: Request):
            return PlainTextResponse("")

        def put(self, request: Request):
            return PlainTextResponse("")

        def delete(self, request: Request):
            return PlainTextResponse("")

    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def mock_uuid(monkeypatch):
    class UUIDMock:
        @staticmethod
        def uuid4():
            return "1-2-3-4-5"

    monkeypatch.setattr(layab.starlette, "uuid", UUIDMock)


def test_log_get_request_details(client, caplog, mock_uuid):
    caplog.set_level(logging.INFO)
    response = client.get("/logging")
    assert response.status_code == 200
    assert response.text == ""
    assert len(caplog.messages) == 2
    assert eval(caplog.messages[0]) == {
        "request_headers.accept": "*/*",
        "request_headers.accept-encoding": "gzip, deflate",
        "request_headers.connection": "keep-alive",
        "request_headers.host": "testserver",
        "request_headers.user-agent": "testclient",
        "request_id": "1-2-3-4-5",
        "request_method": "GET",
        "request_status": "start",
        "request_url.path": "/logging",
    }
    end_message = eval(caplog.messages[1])
    end_message.pop("request_processing_time")
    assert end_message == {
        "request_headers.accept": "*/*",
        "request_headers.accept-encoding": "gzip, deflate",
        "request_headers.connection": "keep-alive",
        "request_headers.host": "testserver",
        "request_headers.user-agent": "testclient",
        "request_id": "1-2-3-4-5",
        "request_method": "GET",
        "request_status": "success",
        "request_status_code": 200,
        "request_url.path": "/logging",
    }


def test_log_delete_request_details(client, caplog, mock_uuid):
    caplog.set_level(logging.INFO)
    response = client.delete("/logging")
    assert response.status_code == 200
    assert response.text == ""
    assert len(caplog.messages) == 2
    assert eval(caplog.messages[0]) == {
        "request_headers.accept": "*/*",
        "request_headers.accept-encoding": "gzip, deflate",
        "request_headers.connection": "keep-alive",
        "request_headers.content-length": "0",
        "request_headers.host": "testserver",
        "request_headers.user-agent": "testclient",
        "request_id": "1-2-3-4-5",
        "request_method": "DELETE",
        "request_status": "start",
        "request_url.path": "/logging",
    }
    end_message = eval(caplog.messages[1])
    end_message.pop("request_processing_time")
    assert end_message == {
        "request_headers.accept": "*/*",
        "request_headers.accept-encoding": "gzip, deflate",
        "request_headers.connection": "keep-alive",
        "request_headers.content-length": "0",
        "request_headers.host": "testserver",
        "request_headers.user-agent": "testclient",
        "request_id": "1-2-3-4-5",
        "request_method": "DELETE",
        "request_status": "success",
        "request_status_code": 200,
        "request_url.path": "/logging",
    }


def test_log_post_request_details(client, caplog, mock_uuid):
    caplog.set_level(logging.INFO)
    response = client.post("/logging")
    assert response.status_code == 200
    assert response.text == ""
    assert len(caplog.messages) == 2
    assert eval(caplog.messages[0]) == {
        "request_headers.accept": "*/*",
        "request_headers.accept-encoding": "gzip, deflate",
        "request_headers.connection": "keep-alive",
        "request_headers.content-length": "0",
        "request_headers.host": "testserver",
        "request_headers.user-agent": "testclient",
        "request_id": "1-2-3-4-5",
        "request_method": "POST",
        "request_status": "start",
        "request_url.path": "/logging",
    }
    end_message = eval(caplog.messages[1])
    end_message.pop("request_processing_time")
    assert end_message == {
        "request_headers.accept": "*/*",
        "request_headers.accept-encoding": "gzip, deflate",
        "request_headers.connection": "keep-alive",
        "request_headers.content-length": "0",
        "request_headers.host": "testserver",
        "request_headers.user-agent": "testclient",
        "request_id": "1-2-3-4-5",
        "request_method": "POST",
        "request_status": "success",
        "request_status_code": 200,
        "request_url.path": "/logging",
    }


def test_log_put_request_details(client, caplog, mock_uuid):
    caplog.set_level(logging.INFO)
    response = client.put("/logging")
    assert response.status_code == 200
    assert response.text == ""
    assert len(caplog.messages) == 2
    assert eval(caplog.messages[0]) == {
        "request_headers.accept": "*/*",
        "request_headers.accept-encoding": "gzip, deflate",
        "request_headers.connection": "keep-alive",
        "request_headers.content-length": "0",
        "request_headers.host": "testserver",
        "request_headers.user-agent": "testclient",
        "request_id": "1-2-3-4-5",
        "request_method": "PUT",
        "request_status": "start",
        "request_url.path": "/logging",
    }
    end_message = eval(caplog.messages[1])
    end_message.pop("request_processing_time")
    assert end_message == {
        "request_headers.accept": "*/*",
        "request_headers.accept-encoding": "gzip, deflate",
        "request_headers.connection": "keep-alive",
        "request_headers.content-length": "0",
        "request_headers.host": "testserver",
        "request_headers.user-agent": "testclient",
        "request_id": "1-2-3-4-5",
        "request_method": "PUT",
        "request_status": "success",
        "request_status_code": 200,
        "request_url.path": "/logging",
    }


def test_log_get_request_details_on_failure(client, caplog, mock_uuid):
    caplog.set_level(logging.INFO)
    response = client.get("/logging_failure")
    assert response.status_code == 500
    assert response.text == "Internal Server Error"
    assert len(caplog.messages) == 2
    assert eval(caplog.messages[0]) == {
        "request_headers.accept": "*/*",
        "request_headers.accept-encoding": "gzip, deflate",
        "request_headers.connection": "keep-alive",
        "request_headers.host": "testserver",
        "request_headers.user-agent": "testclient",
        "request_id": "1-2-3-4-5",
        "request_method": "GET",
        "request_status": "start",
        "request_url.path": "/logging_failure",
    }
    end_message = eval(caplog.messages[1])
    end_message.pop("error.traceback")
    assert end_message == {
        "error.class": "Exception",
        "error.msg": "Error message",
        "request.data": b"",
        "request_headers.accept": "*/*",
        "request_headers.accept-encoding": "gzip, deflate",
        "request_headers.connection": "keep-alive",
        "request_headers.host": "testserver",
        "request_headers.user-agent": "testclient",
        "request_id": "1-2-3-4-5",
        "request_method": "GET",
        "request_status": "error",
        "request_url.path": "/logging_failure",
    }


def test_log_delete_request_details_on_failure(client, caplog, mock_uuid):
    caplog.set_level(logging.INFO)
    response = client.delete("/logging_failure")
    assert response.status_code == 500
    assert response.text == "Internal Server Error"
    assert len(caplog.messages) == 2
    assert eval(caplog.messages[0]) == {
        "request_headers.accept": "*/*",
        "request_headers.accept-encoding": "gzip, deflate",
        "request_headers.connection": "keep-alive",
        "request_headers.content-length": "0",
        "request_headers.host": "testserver",
        "request_headers.user-agent": "testclient",
        "request_id": "1-2-3-4-5",
        "request_method": "DELETE",
        "request_status": "start",
        "request_url.path": "/logging_failure",
    }
    end_message = eval(caplog.messages[1])
    end_message.pop("error.traceback")
    assert end_message == {
        "error.class": "Exception",
        "error.msg": "Error message",
        "request.data": b"",
        "request_headers.accept": "*/*",
        "request_headers.accept-encoding": "gzip, deflate",
        "request_headers.connection": "keep-alive",
        "request_headers.content-length": "0",
        "request_headers.host": "testserver",
        "request_headers.user-agent": "testclient",
        "request_id": "1-2-3-4-5",
        "request_method": "DELETE",
        "request_status": "error",
        "request_url.path": "/logging_failure",
    }


def test_log_post_request_details_on_failure(client, caplog, mock_uuid):
    caplog.set_level(logging.INFO)
    response = client.post("/logging_failure")
    assert response.status_code == 500
    assert response.text == "Internal Server Error"
    assert len(caplog.messages) == 2
    assert eval(caplog.messages[0]) == {
        "request_headers.accept": "*/*",
        "request_headers.accept-encoding": "gzip, deflate",
        "request_headers.connection": "keep-alive",
        "request_headers.content-length": "0",
        "request_headers.host": "testserver",
        "request_headers.user-agent": "testclient",
        "request_id": "1-2-3-4-5",
        "request_method": "POST",
        "request_status": "start",
        "request_url.path": "/logging_failure",
    }
    end_message = eval(caplog.messages[1])
    end_message.pop("error.traceback")
    assert end_message == {
        "error.class": "Exception",
        "error.msg": "Error message",
        "request.data": b"",
        "request_headers.accept": "*/*",
        "request_headers.accept-encoding": "gzip, deflate",
        "request_headers.connection": "keep-alive",
        "request_headers.content-length": "0",
        "request_headers.host": "testserver",
        "request_headers.user-agent": "testclient",
        "request_id": "1-2-3-4-5",
        "request_method": "POST",
        "request_status": "error",
        "request_url.path": "/logging_failure",
    }


def test_log_put_request_details_on_failure(client, caplog, mock_uuid):
    caplog.set_level(logging.INFO)
    response = client.put("/logging_failure")
    assert response.status_code == 500
    assert response.text == "Internal Server Error"
    assert len(caplog.messages) == 2
    assert eval(caplog.messages[0]) == {
        "request_headers.accept": "*/*",
        "request_headers.accept-encoding": "gzip, deflate",
        "request_headers.connection": "keep-alive",
        "request_headers.content-length": "0",
        "request_headers.host": "testserver",
        "request_headers.user-agent": "testclient",
        "request_id": "1-2-3-4-5",
        "request_method": "PUT",
        "request_status": "start",
        "request_url.path": "/logging_failure",
    }
    end_message = eval(caplog.messages[1])
    end_message.pop("error.traceback")
    assert end_message == {
        "error.class": "Exception",
        "error.msg": "Error message",
        "request.data": b"",
        "request_headers.accept": "*/*",
        "request_headers.accept-encoding": "gzip, deflate",
        "request_headers.connection": "keep-alive",
        "request_headers.content-length": "0",
        "request_headers.host": "testserver",
        "request_headers.user-agent": "testclient",
        "request_id": "1-2-3-4-5",
        "request_method": "PUT",
        "request_status": "error",
        "request_url.path": "/logging_failure",
    }


def test_skip_log_get_request(client, caplog):
    caplog.set_level(logging.INFO)
    response = client.get("/skipped")
    assert response.status_code == 200
    assert response.text == ""
    assert len(caplog.messages) == 0


def test_skip_log_delete_request(client, caplog):
    caplog.set_level(logging.INFO)
    response = client.delete("/skipped")
    assert response.status_code == 200
    assert response.text == ""
    assert len(caplog.messages) == 0


def test_skip_log_post_request(client, caplog):
    caplog.set_level(logging.INFO)
    response = client.post("/skipped")
    assert response.status_code == 200
    assert response.text == ""
    assert len(caplog.messages) == 0


def test_skip_log_put_request(client, caplog):
    caplog.set_level(logging.INFO)
    response = client.put("/skipped")
    assert response.status_code == 200
    assert response.text == ""
    assert len(caplog.messages) == 0
