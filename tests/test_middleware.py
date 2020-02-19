from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

import layab
from layab._middleware import LoggingMiddleware


def test_minimal_middleware():
    middleware = layab.middleware(cors=False, reverse_proxy=False)
    assert len(middleware) == 1
    assert middleware[0].cls == LoggingMiddleware
    assert middleware[0].options == {'skip_paths': ['/health']}


def test_cors_middleware():
    middleware = layab.middleware(reverse_proxy=False)
    assert len(middleware) == 2
    assert middleware[0].cls == LoggingMiddleware
    assert middleware[1].cls == CORSMiddleware
    assert middleware[1].options == {'allow_origins': ['*'], 'allow_methods': ['*'], 'allow_headers': ['*']}


def test_compress_middleware():
    middleware = layab.middleware(
        cors=False,
        reverse_proxy=False,
        compress=True,
    )
    assert len(middleware) == 2
    assert middleware[0].cls == LoggingMiddleware
    assert middleware[1].cls == GZipMiddleware
    assert middleware[1].options == {}


def test_reverse_proxy_middleware():
    middleware = layab.middleware(
        cors=False
    )
    assert len(middleware) == 2
    assert middleware[0].cls == LoggingMiddleware
    assert middleware[1].cls == ProxyHeadersMiddleware
    assert middleware[1].options == {'trusted_hosts': '*'}
