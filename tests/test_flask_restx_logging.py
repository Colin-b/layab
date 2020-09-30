import logging

import flask
import flask_restx
import pytest

import layab.flask_restx


@pytest.fixture
def client():
    app = flask.Flask(__name__)
    layab.flask_restx.log_requests(skip_paths=["/skipped"])
    api = flask_restx.Api(app)

    @api.route("/logging")
    class Logging(flask_restx.Resource):
        def get(self):
            return flask.Response(b"")

        def post(self):
            return flask.Response(b"")

        def put(self):
            return flask.Response(b"")

        def delete(self):
            return flask.Response(b"")

    @api.route("/logging_failure")
    class LoggingFailure(flask_restx.Resource):
        def get(self):
            raise Exception("Error message")

        def post(self):
            raise Exception("Error message")

        def put(self):
            raise Exception("Error message")

        def delete(self):
            raise Exception("Error message")

    @api.route("/skipped")
    class Skipped(flask_restx.Resource):
        def get(self):
            return flask.Response(b"")

        def post(self):
            return flask.Response(b"")

        def put(self):
            return flask.Response(b"")

        def delete(self):
            return flask.Response(b"")

    with app.test_client() as client:
        yield client

    flask_restx.Resource.method_decorators.clear()


@pytest.fixture
def mock_uuid(monkeypatch):
    class UUIDMock:
        @staticmethod
        def uuid4():
            return "1-2-3-4-5"

    monkeypatch.setattr(layab.flask_restx, "uuid", UUIDMock)


def test_log_get_request_details(client, caplog, mock_uuid):
    caplog.set_level(logging.INFO)
    response = client.get("/logging")
    assert response.status_code == 200
    assert response.data == b""
    assert len(caplog.messages) == 2
    assert eval(caplog.messages[0]) == {
        "request_headers.Host": "localhost",
        "request_headers.User-Agent": "werkzeug/1.0.1",
        "request_id": "1-2-3-4-5",
        "request_method": "GET",
        "request_status": "start",
        "request_url.path": "/logging",
    }
    end_message = eval(caplog.messages[1])
    end_message.pop("request_processing_time")
    assert end_message == {
        "request_headers.Host": "localhost",
        "request_headers.User-Agent": "werkzeug/1.0.1",
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
    assert response.data == b""
    assert len(caplog.messages) == 2
    assert eval(caplog.messages[0]) == {
        "request_headers.Host": "localhost",
        "request_headers.User-Agent": "werkzeug/1.0.1",
        "request_id": "1-2-3-4-5",
        "request_method": "DELETE",
        "request_status": "start",
        "request_url.path": "/logging",
    }
    end_message = eval(caplog.messages[1])
    end_message.pop("request_processing_time")
    assert end_message == {
        "request_headers.Host": "localhost",
        "request_headers.User-Agent": "werkzeug/1.0.1",
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
    assert response.data == b""
    assert len(caplog.messages) == 2
    assert eval(caplog.messages[0]) == {
        "request_headers.Host": "localhost",
        "request_headers.User-Agent": "werkzeug/1.0.1",
        "request_id": "1-2-3-4-5",
        "request_method": "POST",
        "request_status": "start",
        "request_url.path": "/logging",
    }
    end_message = eval(caplog.messages[1])
    end_message.pop("request_processing_time")
    assert end_message == {
        "request_headers.Host": "localhost",
        "request_headers.User-Agent": "werkzeug/1.0.1",
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
    assert response.data == b""
    assert len(caplog.messages) == 2
    assert eval(caplog.messages[0]) == {
        "request_headers.Host": "localhost",
        "request_headers.User-Agent": "werkzeug/1.0.1",
        "request_id": "1-2-3-4-5",
        "request_method": "PUT",
        "request_status": "start",
        "request_url.path": "/logging",
    }
    end_message = eval(caplog.messages[1])
    end_message.pop("request_processing_time")
    assert end_message == {
        "request_headers.Host": "localhost",
        "request_headers.User-Agent": "werkzeug/1.0.1",
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
    assert response.data == b'{"message": "Internal Server Error"}\n'
    assert len(caplog.messages) == 3
    assert eval(caplog.messages[0]) == {
        "request_headers.Host": "localhost",
        "request_headers.User-Agent": "werkzeug/1.0.1",
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
        "request_headers.Host": "localhost",
        "request_headers.User-Agent": "werkzeug/1.0.1",
        "request_id": "1-2-3-4-5",
        "request_method": "GET",
        "request_status": "error",
        "request_url.path": "/logging_failure",
    }


def test_log_delete_request_details_on_failure(client, caplog, mock_uuid):
    caplog.set_level(logging.INFO)
    response = client.delete("/logging_failure")
    assert response.status_code == 500
    assert response.data == b'{"message": "Internal Server Error"}\n'
    assert len(caplog.messages) == 3
    assert eval(caplog.messages[0]) == {
        "request_headers.Host": "localhost",
        "request_headers.User-Agent": "werkzeug/1.0.1",
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
        "request_headers.Host": "localhost",
        "request_headers.User-Agent": "werkzeug/1.0.1",
        "request_id": "1-2-3-4-5",
        "request_method": "DELETE",
        "request_status": "error",
        "request_url.path": "/logging_failure",
    }


def test_log_post_request_details_on_failure(client, caplog, mock_uuid):
    caplog.set_level(logging.INFO)
    response = client.post("/logging_failure")
    assert response.status_code == 500
    assert response.data == b'{"message": "Internal Server Error"}\n'
    assert len(caplog.messages) == 3
    assert eval(caplog.messages[0]) == {
        "request_headers.Host": "localhost",
        "request_headers.User-Agent": "werkzeug/1.0.1",
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
        "request_headers.Host": "localhost",
        "request_headers.User-Agent": "werkzeug/1.0.1",
        "request_id": "1-2-3-4-5",
        "request_method": "POST",
        "request_status": "error",
        "request_url.path": "/logging_failure",
    }


def test_log_put_request_details_on_failure(client, caplog, mock_uuid):
    caplog.set_level(logging.INFO)
    response = client.put("/logging_failure")
    assert response.status_code == 500
    assert response.data == b'{"message": "Internal Server Error"}\n'
    assert len(caplog.messages) == 3
    assert eval(caplog.messages[0]) == {
        "request_headers.Host": "localhost",
        "request_headers.User-Agent": "werkzeug/1.0.1",
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
        "request_headers.Host": "localhost",
        "request_headers.User-Agent": "werkzeug/1.0.1",
        "request_id": "1-2-3-4-5",
        "request_method": "PUT",
        "request_status": "error",
        "request_url.path": "/logging_failure",
    }


def test_skip_log_get_request(client, caplog):
    caplog.set_level(logging.INFO)
    response = client.get("/skipped")
    assert response.status_code == 200
    assert response.data == b""
    assert len(caplog.messages) == 0


def test_skip_log_delete_request(client, caplog):
    caplog.set_level(logging.INFO)
    response = client.delete("/skipped")
    assert response.status_code == 200
    assert response.data == b""
    assert len(caplog.messages) == 0


def test_skip_log_post_request(client, caplog):
    caplog.set_level(logging.INFO)
    response = client.post("/skipped")
    assert response.status_code == 200
    assert response.data == b""
    assert len(caplog.messages) == 0


def test_skip_log_put_request(client, caplog):
    caplog.set_level(logging.INFO)
    response = client.put("/skipped")
    assert response.status_code == 200
    assert response.data == b""
    assert len(caplog.messages) == 0
