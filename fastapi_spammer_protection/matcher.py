from fastapi import Request
from .vulnerable_urls import urls


def dotenv(request: Request):
    return request.url.path.endswith('.env')


def php(request: Request):
    return '.php' in request.url.path


def default_matcher(request: Request):
    return request in urls
