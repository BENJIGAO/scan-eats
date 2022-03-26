from multiprocessing.sharedctypes import Value
from requests import get

# Revese proxy for use with webpack-dev-server.
def proxy_request(host, path):
    response = get(host + path)

    excluded_headers = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection",
    ]

    headers = {
        name: value
        for name, value in response.raw.headers.items()
        if name.lower() not in excluded_headers
    }
    return (response.content, response.status_code, headers)