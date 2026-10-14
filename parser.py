"""Определение типа Excel-модуля по имени файла и листам."""

from __future__ import annotations

import io
from typing import BinaryIO


def detect_excel_type(file_bytes: bytes | None = None, filename: str = "") -> str:
    """Вернуть 'organic' или 'carbon'."""
    name = (filename or "").lower()
    if "органик" in name or "organic" in name:
        return "organic"
    if "углерод" in name or "carbon" in name or "нейтрал" in name:
        return "carbon"

    if not file_bytes:
        return "carbon"

    try:
        import openpyxl

        wb = openpyxl.load_workbook(io.BytesIO(file_bytes), read_only=True, data_only=False)
        names = " ".join(wb.sheetnames).lower()
        wb.close()
    except Exception:
        blob = file_bytes.decode("latin-1", errors="ignore").lower()
        if "органик" in blob or "азотфиксац" in blob or "фз-280" in blob or "280" in blob:
            return "organic"
        return "carbon"

    if (
        "главный" in names
        or "органик" in names
        or "планирование севооборота" in names
        or "планирования удобрений" in names
    ):
        return "organic"
    return "carbon"


def detect_excel_type_from_upload(upload: BinaryIO, filename: str = "") -> str:
    data = upload.read()
    if hasattr(upload, "seek"):
        upload.seek(0)
    return detect_excel_type(data, filename or getattr(upload, "name", ""))
