from urllib.parse import urlparse

import validators


def to_short_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}/"


def validate(url, max_length=255):
    if len(url) > max_length or not validators.url(url):
        return 'Некорректный URL'

