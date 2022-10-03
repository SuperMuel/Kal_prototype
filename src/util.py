import re
from typing import TypeVar, List, Iterable


import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

url_validation_regexp = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def is_url_valid(url:str):
    return re.match(url_validation_regexp, url) is not None


T = TypeVar('T')
def group_elements_by(n: int, elements: List[T]) -> Iterable[List[T]]:
    if n < 1:
        raise RuntimeError(f"n should be > 1")
    k = len(elements) // n
    for i in range(k):
        yield elements[n * i:n * (i + 1)]
    yield elements[k * n:]


def robust_request(url) -> requests.Response:
    s = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])

    s.mount("https://", HTTPAdapter(max_retries=retries))
    return s.get(url)
