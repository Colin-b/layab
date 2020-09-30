import flask
from layab.flask_restx import enrich_flask


def test_minimal_enrich():
    app = flask.Flask(__name__)
    original_app = app.wsgi_app
    enrich_flask(app, cors=False, compress_mimetypes=None, reverse_proxy=False)
    assert app.wsgi_app == original_app


def test_cors_enrich():
    app = flask.Flask(__name__)
    before = len(app.after_request_funcs)
    enrich_flask(app, cors=True, compress_mimetypes=None, reverse_proxy=False)
    assert len(app.after_request_funcs) == before + 1


def test_compress_enrich():
    app = flask.Flask(__name__)
    before = len(app.after_request_funcs)
    enrich_flask(app, cors=False, compress_mimetypes=["text/csv"], reverse_proxy=False)
    assert len(app.after_request_funcs) == before + 1
