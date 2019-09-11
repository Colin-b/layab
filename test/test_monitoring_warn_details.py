import pytest
from flask import Flask
from flask_restplus import Api

import layab


@pytest.fixture
def app():
    application = Flask(__name__)
    application.testing = True
    api = Api(application, version="3.2.1")

    def warning_details():
        return "warn", {"toto2": {"status": "pass"}, "toto": {"status": "warn"}}

    layab.add_monitoring_namespace(api, warning_details)

    return application


def test_health_check_response_on_warning(client):
    response = client.get("/health")
    assert response.status_code == 429
    assert response.json == {
        "checks": {"toto2": {"status": "pass"}, "toto": {"status": "warn"}},
        "releaseId": "3.2.1",
        "status": "warn",
        "version": "3",
    }
