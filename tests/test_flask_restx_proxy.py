import flask
from layab.flask_restx import enrich_flask


def test_default():
    app = flask.Flask(__name__)
    enrich_flask(app, cors=False, compress_mimetypes=None, reverse_proxy=True)

    @app.route("/proxy")
    def proxy():
        return flask.jsonify(
            {"scheme": flask.request.scheme, "client": flask.request.remote_addr}
        )

    with app.test_client() as client:
        response = client.get("/proxy")
    assert response.status_code == 200
    assert response.json == {"client": "127.0.0.1", "scheme": "http"}


def test_forwarded_proto():
    app = flask.Flask(__name__)
    enrich_flask(app, cors=False, compress_mimetypes=None, reverse_proxy=True)

    @app.route("/proxy")
    def proxy():
        return flask.jsonify(
            {"scheme": flask.request.scheme, "client": flask.request.remote_addr}
        )

    with app.test_client() as client:
        response = client.get("/proxy", headers={"x-forwarded-proto": "https"})
    assert response.status_code == 200
    assert response.json == {"client": "127.0.0.1", "scheme": "https"}


def test_forwarded_for():
    app = flask.Flask(__name__)
    enrich_flask(app, cors=False, compress_mimetypes=None, reverse_proxy=True)

    @app.route("/proxy")
    def proxy():
        return flask.jsonify(
            {"scheme": flask.request.scheme, "client": flask.request.remote_addr}
        )

    with app.test_client() as client:
        response = client.get("/proxy", headers={"x-forwarded-for": "my_original_url"})
    assert response.status_code == 200
    assert response.json == {"client": "my_original_url", "scheme": "http"}


def test_forwarded_proto_and_for():
    app = flask.Flask(__name__)
    enrich_flask(app, cors=False, compress_mimetypes=None, reverse_proxy=True)

    @app.route("/proxy")
    def proxy():
        return flask.jsonify(
            {"scheme": flask.request.scheme, "client": flask.request.remote_addr}
        )

    with app.test_client() as client:
        response = client.get(
            "/proxy",
            headers={
                "x-forwarded-proto": "https",
                "x-forwarded-for": "my_original_url",
            },
        )
    assert response.status_code == 200
    assert response.json == {"client": "my_original_url", "scheme": "https"}
