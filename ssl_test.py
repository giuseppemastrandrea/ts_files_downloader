import ssl
import platform
import requests
import urllib3

print("OS", platform.system(), platform.version())
print("Python", platform.python_version())
print("OpenSSL", ssl.OPENSSL_VERSION)
print("Requests", requests.__version__)
print("Urllib3", urllib3.__version__)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
s = requests.Session()
s.verify = False
try:
    s.request("GET", "https://expired.badssl.com")
except Exception as e:
    print("Issue detected")
    print(e)
else:
    print("Issue not detected")

pools = s.adapters["https://"].poolmanager.pools
key = pools.keys()[0]
cp = pools[key]
conn = cp._get_conn()
print("SSLContext", conn.ssl_context.verify_mode, conn.ssl_context.check_hostname)