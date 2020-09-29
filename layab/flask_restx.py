import logging
import uuid
from typing import List, Any
import time
import traceback
import functools

import flask
import flask_restx
from werkzeug.middleware.proxy_fix import ProxyFix


logger = logging.getLogger(__name__)


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
    def _log_request_details(func):
        @functools.wraps(func)
        def wrapper(*func_args, **func_kwargs):
            skip_path = False
            for path in skip_paths:
                skip_path |= path in func.__qualname__
            if (
                skip_path
                or (func_args and isinstance(func_args[0], flask_restx.Resource))
                or not flask.has_request_context()
            ):
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
