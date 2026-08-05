import sys

# 1. ЖЕСТКИЙ ПАТЧ СИСТЕМНОГО БАГА STARLETTE
try:
    import starlette.middleware.gzip as st_gzip
    orig_init = st_gzip.GZipResponder.__init__
    def patched_init(self, *args, **kwargs):
        kwargs.setdefault('thread_minimum_size', 1024 * 1024)
        return orig_init(self, *args, **kwargs)
    st_gzip.GZipResponder.__init__ = patched_init
except Exception:
    pass

# 2. ПЕРЕНАПРАВЛЕНИЕ НА ТВОЙ РАБОЧИЙ APP4.PY
with open("app4.py", "r", encoding="utf-8") as f:
    code = f.read()
exec(code, globals())
