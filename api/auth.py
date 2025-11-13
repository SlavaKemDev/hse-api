import requests
from . import config
from .exceptions import AuthError, NetworkError


def password_grant(email: str, password: str):
    data = {
        "client_id": "app-x-ios",
        "username": email,
        "password": password,
        "grant_type": "password",
    }
    try:
        r = requests.post(config.OIDC_TOKEN_URL, data=data, timeout=10)
    except requests.RequestException as e:
        raise NetworkError(str(e)) from e

    if r.status_code != 200:
        raise AuthError("Invalid credentials")

    j = r.json()
    return j["access_token"], j["refresh_token"]


def refresh_grant(refresh_token: str) -> str:
    data = {
        "client_id": "app-x-ios",
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    r = requests.post(config.OIDC_TOKEN_URL, data=data, timeout=10)
    if r.status_code != 200:
        raise AuthError("Refresh failed")
    return r.json()["access_token"]
