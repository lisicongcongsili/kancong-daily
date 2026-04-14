import sys, os, glob
local_data = os.path.expanduser('~/.local/share')
for m in sorted(glob.glob(os.path.join(local_data, 'uv', 'tools', 'mt-data-cli', 'lib', 'python3.*', 'site-packages')), reverse=True):
    if os.path.isdir(os.path.join(m, 'meituan')):
        sys.path.insert(0, m); break
from meituan.data.bi.client import BI_CONFIG
print('ssoid_ck_name:', BI_CONFIG.ssoid_ck_name)
print('client_id:', BI_CONFIG.client_id)
