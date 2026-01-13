import urllib.request

urls = ['http://127.0.0.1:10000/', 'http://127.0.0.1:10000/test']
for u in urls:
    try:
        r = urllib.request.urlopen(u, timeout=5)
        body = r.read().decode(errors='replace')
        print(f"URL: {u}\nSTATUS: {getattr(r, 'status', '?')}\nBODY:\n{body[:500]}\n---")
    except urllib.error.HTTPError as he:
        # Read body from error response for debugging
        try:
            err_body = he.read().decode(errors='replace')
        except Exception:
            err_body = '<no body>'
        print(f"URL: {u}\nERROR HTTP {he.code}\nBODY:\n{err_body[:1000]}\n---")
    except Exception as e:
        print(f'URL: {u}\nERROR: {e}')
