from fastapi import Request
from .vulnerable_urls import urls


def dotenv(request: Request):
    return request.url.path.endswith('.env')


def php(request: Request):
    return '.php' in request.url.path


def default_matcher(request: Request):
    for url in urls:
        if (
            request.method == url.method and
            request.url.path == url.path and
            request.url.query == url.query
        ):
            return True
    return False
