"""Optional S3 asset uploads for generated models."""
from __future__ import annotations

import os
import gzip
import mimetypes
import shutil
import tempfile
from pathlib import Path
from typing import Iterable, Tuple

S3_BUCKET = os.getenv("S3_BUCKET")
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
S3_URL_PREFIX = os.getenv("S3_URL_PREFIX")

try:  # Lazy optional dependency
    import boto3
except Exception:  # pragma: no cover - optional
    boto3 = None  # type: ignore


def _client():
    if not boto3:
        raise RuntimeError("boto3 not installed")
    return boto3.client("s3", endpoint_url=S3_ENDPOINT_URL)


def upload(path: Path, key: str) -> str:
    """Upload a file to S3 and return the public URL."""
    if not S3_BUCKET:
        raise RuntimeError("S3_BUCKET not configured")
    client = _client()
    extra = {}
    tmp_name = None
    try:
        if os.getenv("COMPRESS_UPLOADS", "1") == "1":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".gz") as tmp:
                with open(path, "rb") as src, gzip.GzipFile(fileobj=tmp, mode="wb") as gz:
                    shutil.copyfileobj(src, gz)
                tmp_name = tmp.name
            ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
            extra = {"ContentType": ctype, "ContentEncoding": "gzip"}
            upload_path = tmp_name
        else:
            upload_path = str(path)
        client.upload_file(upload_path, S3_BUCKET, key, ExtraArgs=extra)  # type: ignore[arg-type]
    finally:
        if tmp_name:
            os.unlink(tmp_name)
    base = S3_URL_PREFIX.rstrip("/") if S3_URL_PREFIX else f"https://{S3_BUCKET}.s3.amazonaws.com"
    return f"{base}/{key}"


def maybe_upload_assets(paths: Iterable[Path]) -> Tuple[list[str], bool]:
    """Upload multiple files if S3 is configured.

    Returns list of URLs and a flag indicating whether upload occurred.
    """
    if not S3_BUCKET:
        return [str(p) for p in paths], False
    urls: list[str] = []
    for p in paths:
        key = f"{p.parent.name}/{p.name}"
        urls.append(upload(p, key))
    return urls, True
