from http import cookies
import requests
import json
import urllib3
from pprint import pprint
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# set up connection parameters in a dictionary
gateway = {"ip": "192.168.1.1"}

# set REST API headers
headers = {"Accept": "application/json",
           "Content-Type": "application/json"}
# set URL parameters
loginUrl = 'api/auth/login'
url = f"https://{gateway['ip']}/{loginUrl}"
# set username and password
body = {
    "username": "***REMOVED***",
    "password": "***REMOVED***"
}
# Open a session for capturing cookies
session = requests.Session()
# login
response = session.post(url, headers=headers,
                        data=json.dumps(body), verify=False)

# parse response data into a Python object
api_data = response.json()
# Get CSRF token from response headers
csrf_token = response.headers["X-CSRF-Token"]

# https://github.com/Art-of-WiFi/UniFi-API-client/blob/cbe89d913cc4dd3742d5fd35e201ec86bc8ccdc9/src/Client.php#L1919

createVoucherUrl = f"proxy/network/api/s/default/cmd/hotspot"
url = f"https://{gateway['ip']}/{createVoucherUrl}"
headers = {
    "Content-Type": "application/json",
    "x-csrf-token": csrf_token
}
body = {
    "cmd": "create-voucher",
    "expire": 2880,
    "n": 1,
    "qouta": 0,
    "note": "test"
}
response = session.post(url, headers=headers,
                        data=json.dumps(body), verify=False)
api_data = response.json()
pprint(api_data)
