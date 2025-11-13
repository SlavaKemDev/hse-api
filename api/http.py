import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional, Dict, Any, Callable
from .exceptions import ApiError, AuthError, NetworkError
from . import config


class HttpClient:
    def __init__(self, access_token: str, refresh_fn: Callable[[], str]):
        self._access_token = access_token
        self._refresh_fn = refresh_fn
        self._session = requests.Session()
        retry = Retry(total=3, backoff_factor=0.3, status_forcelist=[502, 503, 504])
        self._session.mount("https://", HTTPAdapter(max_retries=retry))

    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self._access_token}"}

    def _request(self, method: str, url: str, *, params=None, data=None, json=None, timeout=config.DEFAULT_TIMEOUT):
        try:
            resp = self._session.request(method, url, headers=self._headers(),
                                         params=params, data=data, json=json, timeout=timeout)
        except requests.RequestException as e:
            raise NetworkError(str(e)) from e

        if resp.status_code == 401:
            self._access_token = self._refresh_fn()
            resp = self._session.request(method, url, headers=self._headers(),
                                         params=params, data=data, json=json, timeout=timeout)

        if resp.status_code == 401:
            raise AuthError("Unauthorized after token refresh")

        if not resp.ok:
            raise ApiError(f"{resp.status_code}: {resp.text}")

        return resp.json()

    def get(self, url: str, params: Optional[Dict[str, Any]] = None):
        return self._request("GET", url, params=params)

    def post(self, url: str, data: Optional[Dict[str, Any]] = None, json=None):
        return self._request("POST", url, data=data, json=json)
