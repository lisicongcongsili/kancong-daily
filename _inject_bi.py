import sys, os, glob, json, time

local_data = os.path.expanduser("~/.local/share")
site = None
for m in sorted(glob.glob(os.path.join(local_data, "uv", "tools", "mt-data-cli", "lib", "python3.*", "site-packages")), reverse=True):
    if os.path.isdir(os.path.join(m, "meituan")):
        site = m; break
sys.path.insert(0, site)

from meituan.sso.browser_cookie_reader import BrowserCookieReader
from meituan.sso.secure_storage import EncryptedFileStorage
from meituan.sso.cookie_manager import APP_COOKIES_KEY
from meituan.data.bi.client import BI_CONFIG

jar = BrowserCookieReader().get_browser_cookiejar_from_default_browser("bi.sankuai.com")
val = next((c.value for c in jar if c.name == BI_CONFIG.ssoid_ck_name and c.value), None)
if not val:
    print("ERROR: cookie not found"); sys.exit(1)

storage = EncryptedFileStorage(keychain=None)
raw = storage.get(APP_COOKIES_KEY)
payload = json.loads(raw) if raw else {}
now = int(time.time())
payload[BI_CONFIG.client_id] = {"cookies": {BI_CONFIG.ssoid_ck_name: val}, "meta": {"source": "inject", "obtained_at": now, "last_validated_at": now}}
storage.set(APP_COOKIES_KEY, json.dumps(payload))
print("OK")
