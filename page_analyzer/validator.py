from urllib.parse import urlparse, urlunparse

import validators


def to_short_url(url):
    parsed_url = urlparse(url)
    short_url = (parsed_url.scheme, parsed_url.netloc, '', '', '', '')
    return urlunparse(short_url)


def validate(url):
    if not validators.url(url):
        return 'Некорректный URL'

