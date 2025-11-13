class ApiError(Exception):
    pass


class AuthError(ApiError):
    pass


class NetworkError(ApiError):
    pass
