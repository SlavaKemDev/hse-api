from urllib.parse import urljoin

API_V2_URL = "https://api.hseapp.ru/v2/"
API_V3_URL = "https://api.hseapp.ru/v3/"
API_DEFAULT_URL = "https://api.hseapp.ru/"
OIDC_TOKEN_URL = "https://saml.hse.ru/realms/hse/protocol/openid-connect/token"


def url(base: str, path: str) -> str:
    return urljoin(base, path)


DEFAULT_TIMEOUT = 10  # seconds
