import os
import requests
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")


def _url(path: str) -> str:
    if not path.startswith("/"):
        path = "/" + path
    return f"{BACKEND_URL}{path}"


def _raise_clean_error(resp: requests.Response):
    """Try to show backend error JSON/text nicely."""
    try:
        data = resp.json()
        raise RuntimeError(f"{resp.status_code} {resp.reason}: {data}")
    except Exception:
        raise RuntimeError(f"{resp.status_code} {resp.reason}: {resp.text[:300]}")


def get(path: str, params: dict | None = None, timeout: int = 20) -> dict:
    resp = requests.get(_url(path), params=params, timeout=timeout)
    if not resp.ok:
        _raise_clean_error(resp)
    return resp.json()


def post(path: str, payload: dict, timeout: int = 25) -> dict:
    resp = requests.post(_url(path), json=payload, timeout=timeout)
    if not resp.ok:
        _raise_clean_error(resp)
    return resp.json()