from http import HTTPStatus
from pathlib import Path
from typing import List, Optional, Union

from fastapi import Request, Response

from fastapi_spammer_protection import matcher


class SpammerProtection:
    def __init__(
        self, banlist_file_path: Union[str, Path],
        ip_header_name: str = 'X-Forwarded-For',
        whitelist: Optional[List[str]] = None,
    ):
        '''
        SpammerProtection is a protection mechanism as a middleware
        for FastAPI ASGI apps.

        :param banlist_file_path: Path to a banlist file
        :type banlist_file_path: str | Path
        :param ip_header_name: Name of the header containing the client's
                               IP address, defaults to 'X-Forwarded-For'
        :type ip_header_name: str, optional
        :param whitelist: List of IPs to whitelist regardless of the calls
                          made to the app, defaults to None
        :type whitelist: Optional[List[str]], optional
        '''
        self.banlist = []
        self.banlist_file_path = banlist_file_path
        self.ip_header_name = ip_header_name
        self.whitelist = whitelist
        self.load_banlist()

    async def __call__(self, request: Request, call_next):
        client_ip = request.headers.get(self.ip_header_name)
        if client_ip is None or client_ip in self.whitelist:
            # If we can't find the IP of the client, then just do nothing...
            # Same goes if explicitely set to be ignored by the middleware
            return await call_next(request)

        client_ip = self.parse_header(client_ip)

        if client_ip in self.banlist:
            # If the IP of the client is in the banlist,
            # return an Unauthorized response
            return Response('Banned', status_code=HTTPStatus.FORBIDDEN)

        for func_name in dir(matcher):
            # Does the matching against common vulnerable url patterns
            # It will add the IP of the user to the banlist if it's ever
            # found to be trying common exploits (trying to fetch .env files for instance)
            # see vulnerable_urls.py for a list of matched URI patterns
            func = getattr(matcher, func_name)
            if callable(func) and func(request):
                self.banlist.append(client_ip)
        self.save_banlist()
        response = await call_next(request)
        return response

    def save_banlist(self):
        '''
        Saves the banlist to the disk. The format is just the IPs separated by
        newline characters for easy parsing with third-party tools or scripts.
        '''
        with open(self.banlist_file_path, 'r') as file_handle:
            self.banlist.extend(file_handle.readlines())

    def load_banlist(self):
        '''
        Loads the banlist file.
        '''
        with open(self.banlist_file_path, 'w') as file_handle:
            file_handle.write('\n'.join(self.banlist))

    def parse_header(self, header_value: str):
        '''
        Parses a header in the format of the X-Forwarded-For header
        See https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For
        See https://www.nginx.com/resources/wiki/start/topics/examples/forwarded/
        '''
        return header_value.split(',')[0].split(';')[0]
