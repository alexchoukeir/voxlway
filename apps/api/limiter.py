from slowapi import Limiter
from fastapi import Request

def get_remote_address(request: Request) -> str:
    """
    Get the remote address.

    Args:
        request (Request): The incoming request.

    Returns:
        str: The remote address.
    """
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.client.host

limiter = Limiter(key_func=get_remote_address)
