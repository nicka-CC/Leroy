import os
from typing import Optional
from fastapi import UploadFile

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")


def ensure_upload_dir() -> None:
    os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_upload(file: UploadFile, prefix: Optional[str] = None) -> str:
    ensure_upload_dir()
    filename = file.filename or "upload.bin"
    safe_name = filename.replace("/", "_").replace("\\", "_")
    if prefix:
        safe_name = f"{prefix}_{safe_name}"
    file_path = os.path.join(UPLOAD_DIR, safe_name)
    with open(file_path, "wb") as out:
        out.write(file.file.read())
    return f"/uploads/{safe_name}"
