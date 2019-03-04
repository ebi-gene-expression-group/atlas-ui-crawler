import requests


def get_request_status_code(url):
    return requests.head(url).status_code
