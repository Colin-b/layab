import logging

import pytest
import flask
import flask_restplus

import layab._monitoring


@pytest.fixture
def app():
    application = flask.Flask(__name__)
    application.testing = True
    application.config["PROPAGATE_EXCEPTIONS"] = False
    api = flask_restplus.Api(application)

    @api.route("/logging")
    class Logging(flask_restplus.Resource):
        @layab._monitoring._log_request_details
        def get(self):
            return ""

        @layab._monitoring._log_request_details
        def post(self):
            return ""

        @layab._monitoring._log_request_details
        def put(self):
            return ""

        @layab._monitoring._log_request_details
        def delete(self):
            return ""

    @api.route("/logging_failure")
    class LoggingFailure(flask_restplus.Resource):
        @layab._monitoring._log_request_details
        def get(self):
            raise Exception("Error message")

        @layab._monitoring._log_request_details
        def post(self):
            raise Exception("Error message")

        @layab._monitoring._log_request_details
        def put(self):
            raise Exception("Error message")

        @layab._monitoring._log_request_details
        def delete(self):
            raise Exception("Error message")

    return application


def test_generated_swagger(client):
    response = client.get("/swagger.json")
    assert response.status_code == 200
    assert response.json == {
        "swagger": "2.0",
        "basePath": "/",
        "paths": {
            "/logging": {
                "delete": {
                    "responses": {"200": {"description": "Success"}},
                    "operationId": "delete_logging",
                    "tags": ["default"],
                },
                "get": {
                    "responses": {"200": {"description": "Success"}},
                    "operationId": "get_logging",
                    "tags": ["default"],
                },
                "post": {
                    "responses": {"200": {"description": "Success"}},
                    "operationId": "post_logging",
                    "tags": ["default"],
                },
                "put": {
                    "responses": {"200": {"description": "Success"}},
                    "operationId": "put_logging",
                    "tags": ["default"],
                },
            },
            "/logging_failure": {
                "delete": {
                    "responses": {"200": {"description": "Success"}},
                    "operationId": "delete_logging_failure",
                    "tags": ["default"],
                },
                "get": {
                    "responses": {"200": {"description": "Success"}},
                    "operationId": "get_logging_failure",
                    "tags": ["default"],
                },
                "post": {
                    "responses": {"200": {"description": "Success"}},
                    "operationId": "post_logging_failure",
                    "tags": ["default"],
                },
                "put": {
                    "responses": {"200": {"description": "Success"}},
                    "operationId": "put_logging_failure",
                    "tags": ["default"],
                },
            }
        },
        "info": {"title": "API", "version": "1.0"},
        "produces": ["application/json"],
        "consumes": ["application/json"],
        "tags": [{"name": "default", "description": "Default namespace"}],
        "responses": {
            "ParseError": {"description": "When a mask can't be parsed"},
            "MaskError": {"description": "When any error occurs on mask"},
        },
    }


def test_log_get_request_details(client, caplog):
    caplog.set_level(logging.INFO)
    response = client.get("/logging")
    assert response.status_code == 200
    assert response.json == ""
    assert len(caplog.messages) == 2
    assert eval(caplog.messages[0]) == {'func_name': 'Logging.get', 'request_headers.User-Agent': 'werkzeug/0.16.0', 'request_headers.Host': 'localhost', 'request_status': 'start'}
    end_message = eval(caplog.messages[1])
    end_message.pop('request_processing_time')
    assert end_message == {'func_name': 'Logging.get', 'request_headers.User-Agent': 'werkzeug/0.16.0', 'request_headers.Host': 'localhost', 'request_status': 'success', 'request_status_code': 200}


def test_log_delete_request_details(client, caplog):
    caplog.set_level(logging.INFO)
    response = client.delete("/logging")
    assert response.status_code == 200
    assert response.json == ""
    assert len(caplog.messages) == 2
    assert eval(caplog.messages[0]) == {'func_name': 'Logging.delete', 'request_headers.User-Agent': 'werkzeug/0.16.0', 'request_headers.Host': 'localhost', 'request_status': 'start'}
    end_message = eval(caplog.messages[1])
    end_message.pop('request_processing_time')
    assert end_message == {'func_name': 'Logging.delete', 'request_headers.User-Agent': 'werkzeug/0.16.0', 'request_headers.Host': 'localhost', 'request_status': 'success', 'request_status_code': 200}


def test_log_post_request_details(client, caplog):
    caplog.set_level(logging.INFO)
    response = client.post("/logging")
    assert response.status_code == 200
    assert response.json == ""
    assert len(caplog.messages) == 2
    assert eval(caplog.messages[0]) == {'func_name': 'Logging.post', 'request_headers.User-Agent': 'werkzeug/0.16.0', 'request_headers.Host': 'localhost', 'request_status': 'start'}
    end_message = eval(caplog.messages[1])
    end_message.pop('request_processing_time')
    assert end_message == {'func_name': 'Logging.post', 'request_headers.User-Agent': 'werkzeug/0.16.0', 'request_headers.Host': 'localhost', 'request_status': 'success', 'request_status_code': 200}


def test_log_put_request_details(client, caplog):
    caplog.set_level(logging.INFO)
    response = client.put("/logging")
    assert response.status_code == 200
    assert response.json == ""
    assert len(caplog.messages) == 2
    assert eval(caplog.messages[0]) == {'func_name': 'Logging.put', 'request_headers.User-Agent': 'werkzeug/0.16.0', 'request_headers.Host': 'localhost', 'request_status': 'start'}
    end_message = eval(caplog.messages[1])
    end_message.pop('request_processing_time')
    assert end_message == {'func_name': 'Logging.put', 'request_headers.User-Agent': 'werkzeug/0.16.0', 'request_headers.Host': 'localhost', 'request_status': 'success', 'request_status_code': 200}


def test_log_get_request_details_on_failure(client, caplog):
    caplog.set_level(logging.INFO)
    response = client.get("/logging_failure")
    assert response.status_code == 500
    assert response.json == {'message': 'Internal Server Error'}
    assert len(caplog.messages) == 3
    assert eval(caplog.messages[0]) == {'func_name': 'LoggingFailure.get', 'request_headers.User-Agent': 'werkzeug/0.16.0', 'request_headers.Host': 'localhost', 'request_status': 'start'}
    end_message = eval(caplog.messages[1])
    end_message.pop('error.traceback')
    assert end_message == {'error.class': 'Exception', 'error.msg': 'Error message', 'error.summary': 'test_monitoring_logging.get/_monitoring.wrapper', 'func_name': 'LoggingFailure.get', 'request.data': b'', 'request_headers.Host': 'localhost', 'request_headers.User-Agent': 'werkzeug/0.16.0', 'request_status': 'error'}
    assert caplog.messages[2] == "Exception on /logging_failure [GET]"


def test_log_delete_request_details_on_failure(client, caplog):
    caplog.set_level(logging.INFO)
    response = client.delete("/logging_failure")
    assert response.status_code == 500
    assert response.json == {'message': 'Internal Server Error'}
    assert len(caplog.messages) == 3
    assert eval(caplog.messages[0]) == {'func_name': 'LoggingFailure.delete', 'request_headers.User-Agent': 'werkzeug/0.16.0', 'request_headers.Host': 'localhost', 'request_status': 'start'}
    end_message = eval(caplog.messages[1])
    end_message.pop('error.traceback')
    assert end_message == {'error.class': 'Exception', 'error.msg': 'Error message', 'error.summary': 'test_monitoring_logging.delete/_monitoring.wrapper', 'func_name': 'LoggingFailure.delete', 'request.data': b'', 'request_headers.Host': 'localhost', 'request_headers.User-Agent': 'werkzeug/0.16.0', 'request_status': 'error'}
    assert caplog.messages[2] == "Exception on /logging_failure [DELETE]"


def test_log_post_request_details_on_failure(client, caplog):
    caplog.set_level(logging.INFO)
    response = client.post("/logging_failure")
    assert response.status_code == 500
    assert response.json == {'message': 'Internal Server Error'}
    assert len(caplog.messages) == 3
    assert eval(caplog.messages[0]) == {'func_name': 'LoggingFailure.post', 'request_headers.User-Agent': 'werkzeug/0.16.0', 'request_headers.Host': 'localhost', 'request_status': 'start'}
    end_message = eval(caplog.messages[1])
    end_message.pop('error.traceback')
    assert end_message == {'error.class': 'Exception', 'error.msg': 'Error message', 'error.summary': 'test_monitoring_logging.post/_monitoring.wrapper', 'func_name': 'LoggingFailure.post', 'request.data': b'', 'request_headers.Host': 'localhost', 'request_headers.User-Agent': 'werkzeug/0.16.0', 'request_status': 'error'}
    assert caplog.messages[2] == "Exception on /logging_failure [POST]"


def test_log_put_request_details_on_failure(client, caplog):
    caplog.set_level(logging.INFO)
    response = client.put("/logging_failure")
    assert response.status_code == 500
    assert response.json == {'message': 'Internal Server Error'}
    assert len(caplog.messages) == 3
    assert eval(caplog.messages[0]) == {'func_name': 'LoggingFailure.put', 'request_headers.User-Agent': 'werkzeug/0.16.0', 'request_headers.Host': 'localhost', 'request_status': 'start'}
    end_message = eval(caplog.messages[1])
    end_message.pop('error.traceback')
    assert end_message == {'error.class': 'Exception', 'error.msg': 'Error message', 'error.summary': 'test_monitoring_logging.put/_monitoring.wrapper', 'func_name': 'LoggingFailure.put', 'request.data': b'', 'request_headers.Host': 'localhost', 'request_headers.User-Agent': 'werkzeug/0.16.0', 'request_status': 'error'}
    assert caplog.messages[2] == "Exception on /logging_failure [PUT]"
