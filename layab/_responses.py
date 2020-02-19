from starlette.requests import Request
from starlette.responses import Response


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
