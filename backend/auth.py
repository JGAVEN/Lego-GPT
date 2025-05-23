from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from typing import Any, Dict


def _b64url(data: bytes) -> bytes:
    return base64.urlsafe_b64encode(data).rstrip(b"=")


def _b64url_decode(data: str | bytes) -> bytes:
    if isinstance(data, str):
        data = data.encode()
    padding = b"=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def encode(payload: Dict[str, Any], secret: str, exp: int | None = None) -> str:
    msg = payload.copy()
    if exp is not None:
        msg["exp"] = int(exp)
    header = _b64url(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
    body = _b64url(json.dumps(msg).encode())
    signing_input = b".".join([header, body])
    sig = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    return b".".join([header, body, _b64url(sig)]).decode()


def decode(token: str, secret: str) -> Dict[str, Any]:
    try:
        header_b64, payload_b64, sig_b64 = token.split(".")
    except ValueError as exc:  # pragma: no cover
        raise ValueError("Invalid token") from exc
    signing_input = f"{header_b64}.{payload_b64}".encode()
    sig = _b64url_decode(sig_b64)
    expected = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    if not hmac.compare_digest(sig, expected):
        raise ValueError("Bad signature")
    payload = json.loads(_b64url_decode(payload_b64))
    exp = payload.get("exp")
    if exp is not None and time.time() > exp:
        raise ValueError("Token expired")
    return payload
