import time
import traceback
import logging
import uuid
from typing import List

from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


logger = logging.getLogger(__name__)


def middleware(
    *, cors: bool = True, compress: bool = False, reverse_proxy: bool = True
) -> List[Middleware]:
    """
    Create a default Starlette middleware stack.

    :param cors: If CORS (Cross Resource) should be enabled. Activated by default.
    :param compress: If responses should be compressed. No compression by default.
    :param reverse_proxy: If server should handle reverse-proxy configuration. Enabled by default.
    :return: all created middleware
    """
    middleware = [Middleware(LoggingMiddleware, skip_paths=["/health"])]
    if cors:
        middleware.append(
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_methods=["*"],
                allow_headers=["*"],
            )
        )

    if compress:
        middleware.append(Middleware(GZipMiddleware))

    if reverse_proxy:
        middleware.append(Middleware(ProxyHeadersMiddleware))

    return middleware


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Always log the following attributes:
        - request_url.path: The URL path according to the server (such as /health)
        - request_method: The HTTP method (GET, POST, PUT, DELETE, PATCH)
        - request_id: Unique identifier of the request
        - request_path.*: Path arguments
        - request_args.*: Query arguments
        - request_headers.*: Headers

    Perform 2 logging per request:
        * Upon reception the following additional attributes will be log:
            - request_status: start
        * Upon success (if a response is returned) the following additional attributes will be log:
            - request_status: success
            - request_processing_time: The time it took to process the request
            - request_status_code: The HTTP status code of the response
        * Upon failure (if an exception is raised) the following additional attributes will be log:
            - request_status: error
            - request.data: The request body
            - error.class: exception class name
            - error.msg: str representation of the exception instance
            - error.traceback: exception trace
    """

    def __init__(self, app: ASGIApp, skip_paths: List[str] = None):
        super().__init__(app)
        self.skip_paths = skip_paths or []

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if request.url.path in self.skip_paths:
            return await call_next(request)

        statistics = _Statistics(request)
        try:
            response = await call_next(request)
        except Exception as e:
            await statistics.exception_occurred(e)
            raise

        statistics.success(response)
        return response


class _Statistics:
    def __init__(self, request: Request):
        self.request = request
        original_request_id = request.headers.get("X-Request-Id")
        request_id = (
            f"{original_request_id},{uuid.uuid4()}"
            if original_request_id
            else str(uuid.uuid4())
        )
        self.stats = {
            "request_url.path": request.url.path,
            "request_method": request.method,
            "request_id": request_id,
        }
        self.stats.update(
            {
                f"request_path.{param_name}": param_value
                for param_name, param_value in request.path_params.items()
            }
        )
        self.stats.update(
            {
                f"request_args.{param_name}": (
                    param_value[0] if len(param_value) == 1 else param_value
                )
                for param_name, param_value in request.query_params.items()
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

    def success(self, response: Response):
        self.stats.update(
            {
                "request_processing_time": time.perf_counter() - self.start,
                "request_status": "success",
                "request_status_code": response.status_code,
            }
        )
        logger.info(self.stats)

    async def exception_occurred(self, exception: Exception):
        self.stats.update(
            {
                "request.data": await self.request.body(),
                "error.class": type(exception).__name__,
                "error.msg": str(exception),
                "error.traceback": traceback.format_exc(),
                "request_status": "error",
            }
        )
        logger.critical(self.stats)


# Original: https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py
# TODO Check if the missing X-Forwarded-Prefix handling will have an impact
class ProxyHeadersMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] in ("http", "websocket"):
            headers = dict(scope["headers"])

            if b"x-forwarded-proto" in headers:
                # Determine if the incoming request was http or https based on
                # the X-Forwarded-Proto header.
                x_forwarded_proto = headers[b"x-forwarded-proto"].decode("ascii")
                scope["scheme"] = x_forwarded_proto.strip()

            if b"x-forwarded-for" in headers:
                # Determine the client address from the last trusted IP in the
                # X-Forwarded-For header. We've lost the connecting client's port
                # information by now, so only include the host.
                x_forwarded_for = headers[b"x-forwarded-for"].decode("ascii")
                host = x_forwarded_for.split(",")[-1].strip()
                port = 0
                scope["client"] = (host, port)

        return await self.app(scope, receive, send)


# TODO Check if we can use request.url_for with the Proxy middleware
def _base_path(request: Request) -> str:
    """
    Return service base path (handle the fact that client may be behind a reverse proxy).
    If X-Original-Request-Uri is in headers, use it to create the base path assuming that:
        X-Original-Request-Uri is formatted as "/reverse_proxy_entry/service_path"
    and that Host is also in headers.

    The resulting base path would then be: scheme://host/reverse_proxy_entry

    In case X-Original-Request-Uri is not in headers, scheme://hostname or scheme://host:port will be used.
    """
    if "X-Original-Request-Uri" in request.headers:
        service_path = (
            "/" + request.headers["X-Original-Request-Uri"].split("/", maxsplit=2)[1]
        )
        return f'{request.url.scheme}://{request.headers["Host"]}{service_path}'
    return f"{request.base_url.scheme}://{request.base_url.netloc}"


class LocationResponse(Response):
    """
    Response containing by default:
     * location header linking to provided path.
     * Status code set to 201.
     * Content type set to text/plain.
    """

    def __init__(self, request: Request, path: str, *args, **kwargs) -> None:
        kwargs.setdefault("status_code", 201)
        kwargs.setdefault("headers", {}).setdefault(
            "location", f"{_base_path(request)}{path}"
        )
        kwargs.setdefault("media_type", "text/plain")
        Response.__init__(self, *args, **kwargs)
