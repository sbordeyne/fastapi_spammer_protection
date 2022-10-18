# fastapi_spammer_protection


[![PyPI](https://img.shields.io/pypi/v/fastapi_spammer_protection.svg)](https://pypi.python.org/pypi/fastapi_spammer_protection)
[![Documentation Status](https://readthedocs.org/projects/fastapi-spammer-protection/badge/?version=latest)](https://readthedocs.org/projects/fastapi-spammer-protection/badge/?version=latest)


Middleware to protect a FastAPI app against spammers that try to exploit known vulnerabilities


* Free software: MIT license
* Documentation: https://fastapi-spammer-protection.readthedocs.io.


## Usage

```python
from pathlib import Path

from fastapi_spammer_protection import SpammerProtection
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(SpammerProtection(Path('./banlist.txt')))
# ...
```

This simple middleware checks the incoming traffic for bots trying to exploit known
vulnerabilities. It is not made for security purposes, but to try to :

- mitigate log spam by setting iptables rules upstream of the HTTP server
- avoid overloading the ASGI runner by dumping requests early (and replying with a 403 status code)

There's also an element of security added : since te IP is blocked by trying to call
any of the known "bad" requests, subsequent requests by that same IP will never reach your source code,
even if there is a vulnerability in your app (not that you should rely solely on that, but it's an increase in protection)

## Script to add the IPs from the banlist to iptable rules

```bash
#!/usr/bin/env bash

for ip in $(cat data/blacklist.txt); do
    iptables -A INPUT -s $ip -j DROP
done
```

## NGINX configuration for the X-Forwarded-For header

Add the following to your configuration file :
```
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
```

