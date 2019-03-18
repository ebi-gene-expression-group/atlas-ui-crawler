import requests


def get_request_status_code(url):
    request = requests.get(url)

    return request.status_code
