'''
Middleware to protect a FastAPI app against spammers that try to exploit known vulnerabilities
'''
__version__ = '1.1.0'

from .middleware import SpammerProtection  # noqa
