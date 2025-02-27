from urllib.parse import urlparse, urlunparse

import validators


def to_short_url(url):
    parsed_url = urlparse(url)
    short_url = (parsed_url.scheme, parsed_url.netloc, '', '', '', '')
    return urlunparse(short_url)


def is_valid(url):
    try:
        validators.url(url)
        return False
    except validators.ValidationError:
        return True
