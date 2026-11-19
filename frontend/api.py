import os

import requests

# the frontend NEVER touches the database. every bit of data goes through
# the FastAPI backend with normal http requests, all from this file.
API_URL = os.environ.get("API_URL", "http://localhost:8000")


def get(path, **params):
    return requests.get(API_URL + path, params=params, timeout=5)


def post(path, data):
    return requests.post(API_URL + path, json=data, timeout=5)


def patch(path, data):
    return requests.patch(API_URL + path, json=data, timeout=5)


def delete(path):
    return requests.delete(API_URL + path, timeout=5)


def error_messages(response):
    """Turn a 422 from FastAPI into readable messages like 'rating: must be <= 10'."""
    detail = response.json().get("detail")
    if isinstance(detail, str):
        return [detail]
    # validation errors come back as a list, each with the field name in "loc"
    return [f"{err['loc'][-1]}: {err['msg']}" for err in detail]
