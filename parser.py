import io
import re

def detect_excel_type(file_bytes):
    """Определяет режим (carbon или organic) по содержимому файла"""
    if file_bytes is None:
        return "carbon"
    try:
        # Быстрый поиск маркеров в байтах книги XLSX
        content = file_bytes.decode('latin-1', errors='ignore').lower()
        if '280' in content or 'азотфиксац' in content or 'органик' in content or 'птичий помет' in content:
            return "organic"
        if 'cseq' in content or 'углерод' in content or 'севооборот' in content or 'cnet' in content or 'f6' in content:
            return "carbon"
        return "carbon"
    except Exception:
        return "carbon"