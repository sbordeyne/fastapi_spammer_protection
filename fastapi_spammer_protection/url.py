import typing
from urllib.parse import urlsplit, SplitResult, urljoin

from fastapi import Request


class URL:
    def __init__(self, method: str, url: str):
        self.method = method
        self._raw_url = url
        self._url = urljoin('https://hostname:8080', url)

    def __eq__(self, other: Request):
        return (
            other.method == self.method and
            other.url.path == self.path and
            other.url.query == self.query
        )

    def __hash__(self):
        return hash(f'{self.method} {self._url}')

    @property
    def components(self) -> SplitResult:
        if not hasattr(self, "_components"):
            self._components = urlsplit(self._url)
        return self._components

    @property
    def scheme(self) -> str:
        return self.components.scheme

    @property
    def netloc(self) -> str:
        return self.components.netloc

    @property
    def path(self) -> str:
        return self.components.path

    @property
    def query(self) -> str:
        return self.components.query

    @property
    def fragment(self) -> str:
        return self.components.fragment

    @property
    def username(self) -> typing.Union[None, str]:
        return self.components.username

    @property
    def password(self) -> typing.Union[None, str]:
        return self.components.password

    @property
    def hostname(self) -> typing.Union[None, str]:
        return self.components.hostname

    @property
    def port(self) -> typing.Optional[int]:
        return self.components.port
