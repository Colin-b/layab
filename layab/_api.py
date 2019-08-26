from typing import List
import os.path
import importlib

import flask
import flask_restplus
import flask_cors
import flask_compress
import werkzeug
from werkzeug.middleware.proxy_fix import ProxyFix

from layab import get_environment


class _Api(flask_restplus.Api):
    @werkzeug.cached_property
    def __schema__(self):
        schema = super().__schema__
        schema["info"]["x-server-environment"] = get_environment()
        return schema


def create_api(
    file_path: str,
    cors: bool = True,
    compress_mimetypes: List[str] = None,
    reverse_proxy: bool = True,
    **kwargs,
) -> (flask.Flask, flask_restplus.Api):
    """
    Create Flask application and related Flask-RestPlus API instance.

    :param file_path: server.py __file__ variable.
    :param cors: If CORS (Cross Resource) should be enabled. Activated by default.
    :param compress_mimetypes: List of mime-types that should be compressed. No compression by default.
    :param reverse_proxy: If server should handle reverse-proxy configuration. Enabled by default.
    :param kwargs: Additional Flask-RestPlus API arguments.
    :return: A tuple with 2 elements: Flask application, Flask-RestPlus API
    """
    service_package = os.path.basename(os.path.dirname(file_path))
    application = flask.Flask(service_package)

    if cors:
        flask_cors.CORS(application)

    if compress_mimetypes:
        compress = flask_compress.Compress()
        compress.init_app(application)
        application.config["COMPRESS_MIMETYPES"] = compress_mimetypes

    if reverse_proxy:
        application.wsgi_app = ProxyFix(application.wsgi_app, x_proto=1, x_host=1, x_prefix=1)

    version = importlib.import_module(f"{service_package}.version").__version__

    return application, _Api(application, version=version, **kwargs)
