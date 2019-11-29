import pytest
from flask import Flask
from flask_restplus import Api

import layab


@pytest.fixture
def app():
    application = Flask(__name__)
    application.testing = True
    api = Api(application, version="3.2.1")

    def failure_details():
        return "fail", None

    layab.add_monitoring_namespace(api, failure_details)

    return application


def test_health_check_response_on_exception(client):
    response = client.get("/health")
    assert response.status_code == 400
    assert response.json == {
        "checks": None,
        "releaseId": "3.2.1",
        "status": "fail",
        "version": "3",
    }
