import requests


def get_request_status_code(url):
    return requests.get(url).status_code
