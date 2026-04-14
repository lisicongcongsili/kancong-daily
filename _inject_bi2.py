import sys, os, glob, json, time

local_data = os.path.expanduser("~/.local/share")
site = None
for m in sorted(glob.glob(os.path.join(local_data, "uv", "tools", "mt-data-cli", "lib", "python3.*", "site-packages")), reverse=True):
    if os.path.isdir(os.path.join(m, "meituan")):
        site = m; break
sys.path.insert(0, site)

from meituan.sso.secure_storage import EncryptedFileStorage
from meituan.sso.cookie_manager import APP_COOKIES_KEY
from meituan.data.bi.client import BI_CONFIG

# 直接使用从浏览器 CDP 获取的 ssoid 值
ssoid_val = "eAGFzrtKA0EUgGEGm5BKLK2mlBTL3OccK02CV5CQCF66ncvqEjeLRMV3EEJMaSEiiE0aK8XSxkawVLAVH0BfQPME9j8_X4VMP30-V-n44Wf8LsWsL4ukn_a6x2meZPHIJ0VwebJfFnGeSi5To0NAK63KJAcRsprWUsQ0Mm5kfUhmaAMbyJCBbi7WtWUMhBLGIjSbRvIlBvTx8uz7Q84R8e8PJrKFqZX7we3dm2y9nH_dvMoRqWxF1_GxF68JRQPWMeW5twGC8B6YNyKg4lnKrRG7FK3ziApQ15TCoMEB9-6v0lpzcGJEaOFB8faq2jk86awtd1uqDAW0NzbX-8psm1O8INWDvJ_7srfH1BUZDyecXyxTYic**eAEFwQkBwDAIBDBLcPxyYAX_EpYEkcG2ISWdd5jVuuIONDGLOO0rvhHfC8TAn440vlRL3A8ldhEc**dG3u7E1znIuQKAwMgzo1y5wrLNOnZaESMj5wqZ-VxnIaC2hvLzhx3ZLV5F63oHaeEh5CYDa4Tji5seJGZJ6oGw**MjIxNDc2NTAsbGlzaWNvbmcwNCzmnY7mgJ3ogaosbGlzaWNvbmcwNEBtZWl0dWFuLmNvbSwxLGVkY18yMjE0NzY1MCwxNzc2MDYzMTQyOTU2"

storage = EncryptedFileStorage(keychain=None)
raw = storage.get(APP_COOKIES_KEY)
payload = json.loads(raw) if raw else {}
now = int(time.time())
payload[BI_CONFIG.client_id] = {
    "cookies": {BI_CONFIG.ssoid_ck_name: ssoid_val},
    "meta": {"source": "inject", "obtained_at": now, "last_validated_at": now}
}
storage.set(APP_COOKIES_KEY, json.dumps(payload))
print("OK")
