import copy
import logging
import uuid
from typing import List, Any
import time
import traceback
import functools
from urllib.parse import urlparse

import flask
import flask_restx
import werkzeug
from werkzeug.middleware.proxy_fix import ProxyFix


logger = logging.getLogger(__name__)


class Api(flask_restx.Api):
    def __init__(self, *args, **kwargs):
        self.extra_info = kwargs.pop("info", {})
        super().__init__(*args, **kwargs)

    @werkzeug.utils.cached_property
    def __schema__(self):
        schema = super().__schema__
        schema.setdefault("info", {}).update(self.extra_info)
        return schema


def enrich_flask(
    application: flask.Flask,
    *,
    cors: bool = True,
    compress_mimetypes: List[str] = None,
    reverse_proxy: bool = True,
):
    if cors:
        import flask_cors

        flask_cors.CORS(application)

    if compress_mimetypes:
        import flask_compress

        application.config["COMPRESS_MIMETYPES"] = compress_mimetypes
        flask_compress.Compress(application)

    if reverse_proxy:
        application.wsgi_app = ProxyFix(
            application.wsgi_app, x_proto=1, x_host=1, x_prefix=1
        )


class _Statistics:
    def __init__(self, request: flask.Request):
        request_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
        # Store the request ID so that it can be accessed to use in application logs
        flask.g.request_id = request_id
        args = {arg: [] for arg in request.args}
        for arg, value in request.args.items(multi=True):
            args[arg].append(value)

        self.stats = {
            "request": {
                "url.path": request.path,
                "method": request.method,
                "id": request_id,
                "args": args,
                "headers": dict(request.headers),
                "status": "start",
            },
        }
        logger.info(copy.deepcopy(self.stats))
        self.start = time.perf_counter()

    def response(self, response: Any):
        self.stats["request"]["processing_time"] = time.perf_counter() - self.start
        self.stats["request"]["status"] = "end"
        self.stats["request"]["status_code"] = (
            response.status_code if isinstance(response, flask.Response) else 200
        )
        logger.info(self.stats)

    def exception_occurred(self, exception: Exception):
        self.stats["request"]["processing_time"] = time.perf_counter() - self.start
        self.stats["request"]["status"] = "error"
        self.stats["error"] = {
            "class": type(exception).__name__,
            "msg": str(exception),
            "traceback": traceback.format_exc(),
        }
        logger.critical(self.stats)


def log_requests(skip_paths: List[str] = None):
    skip_paths = skip_paths or []

    def _log_request_details(func):
        @functools.wraps(func)
        def wrapper(*func_args, **func_kwargs):
            if not flask.has_request_context() or (flask.request.path in skip_paths):
                return func(*func_args, **func_kwargs)

            statistics = _Statistics(flask.request)
            try:
                ret = func(*func_args, **func_kwargs)
                statistics.response(ret)
                return ret
            except Exception as e:
                statistics.exception_occurred(e)
                raise

        return wrapper

    flask_restx.Resource.method_decorators.append(_log_request_details)


def _base_path() -> str:
    """
    Return service base path (handle the fact that client may be behind a reverse proxy).
    """
    if "X-Original-Request-Uri" in flask.request.headers:
        service_path = (
            "/"
            + flask.request.headers["X-Original-Request-Uri"].split("/", maxsplit=2)[1]
        )
        return f'{flask.request.scheme}://{flask.request.headers["Host"]}{service_path}'
    parsed = urlparse(flask.request.base_url)
    return f"{parsed.scheme}://{parsed.netloc}"


def location_response(url: str) -> flask.Response:
    """
    Create a response to return to the client in case of a successful POST or PUT request.

    :param url: Server relative URL returning the created/updated resource(s).
    :return: Response containing the resource location.
    """
    return flask.Response(
        b"",
        status=201,
        headers={"location": f"{_base_path()}{url}"},
        content_type="text/plain",
    )
