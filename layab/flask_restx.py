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
        self.request = request
        original_request_id = request.headers.get("X-Request-Id")
        request_id = (
            f"{original_request_id},{uuid.uuid4()}"
            if original_request_id
            else str(uuid.uuid4())
        )
        # Store the request ID so that it can be accessed to use in application logs
        flask.g.request_id = request_id
        self.stats = {
            "request_url.path": request.path,
            "request_method": request.method,
            "request_id": request_id,
        }
        self.stats.update(
            {
                f"request_args.{param_name}": (
                    param_value[0] if len(param_value) == 1 else param_value
                )
                for param_name, param_value in request.args.items()
            }
        )
        self.stats.update(
            {
                f"request_headers.{header_name}": header_value
                for header_name, header_value in request.headers.items()
            }
        )
        logger.info({**self.stats, "request_status": "start"})
        self.start = time.perf_counter()

    def success(self, response: Any):
        self.stats.update(
            {
                "request_processing_time": time.perf_counter() - self.start,
                "request_status": "success",
                "request_status_code": response.status_code
                if isinstance(response, flask.Response)
                else 200,
            }
        )
        logger.info(self.stats)

    def exception_occurred(self, exception: Exception):
        self.stats.update(
            {
                "request.data": self.request.data,
                "error.class": type(exception).__name__,
                "error.msg": str(exception),
                "error.traceback": traceback.format_exc(),
                "request_status": "error",
            }
        )
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
                statistics.success(ret)
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
