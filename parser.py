def detect_excel_type(file_bytes):
    if not file_bytes:
        return "carbon"
    content = str(file_bytes).lower()
    return "organic" if ("280" in content or "азотфиксац" in content or "органик" in content) else "carbon"
