import importlib.util
import sys
import traceback
import os

app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app.py'))
spec = importlib.util.spec_from_file_location('app_mod', app_path)
app_mod = importlib.util.module_from_spec(spec)
sys.modules['app_mod'] = app_mod
# Ensure project root is on sys.path so relative imports (like `from config import *`) work
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

spec.loader.exec_module(app_mod)

app = getattr(app_mod, 'app')

with app.test_client() as c:
    try:
        resp = c.get('/')
        print('STATUS', resp.status_code)
        print(resp.data.decode()[:1000])
    except Exception:
        traceback.print_exc()
