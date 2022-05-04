from http import cookies
import requests
import json
import urllib3
from pprint import pprint
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class UbiquitiClient:
    # set up connection parameters in a dictionary
    gateway = {"ip": ""}
    csrf_token = ""
    session = None

    def __init__(self, gateway_ip) -> None:
        self.gateway["ip"] = str(gateway_ip)
        self.csrf_token, self.session = self.getCsrfToken()

    def getCsrfToken(self):
        # set REST API headers
        headers = {"Accept": "application/json",
                   "Content-Type": "application/json"}
        # set URL parameters
        loginUrl = 'api/auth/login'
        url = f"https://{self.gateway['ip']}/{loginUrl}"
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

        # Get CSRF token from response headers
        return response.headers["X-CSRF-Token"], session

    # https://github.com/Art-of-WiFi/UniFi-API-client/blob/cbe89d913cc4dd3742d5fd35e201ec86bc8ccdc9/src/Client.php#L1919

    def createVoucher(self, minutes, count, quota, note, up=None, down=None, megabytes=None):
        createVoucherUrl = f"proxy/network/api/s/default/cmd/hotspot"
        url = f"https://{self.gateway['ip']}/{createVoucherUrl}"
        headers = {
            "Content-Type": "application/json",
            "x-csrf-token": self.csrf_token
        }
        body = {
            "cmd": "create-voucher",
            "expire": minutes,
            "n": count,
            "quota": quota,
            "note": note,
            "up": up,
            "down": down,
            "bytes": megabytes,
        }
        response = self.session.post(url, headers=headers,
                                     data=json.dumps(body), verify=False)
        api_data = response.json()
        return api_data["data"]

    def retrieveVoucher(self, create_time):
        fetchVoucherUrl = f"proxy/network/api/s/default/stat/voucher"
        url = f"https://{self.gateway['ip']}/{fetchVoucherUrl}"
        headers = {
            "Content-Type": "application/json",
            "x-csrf-token": self.csrf_token
        }
        body = {
            "create_time": str(create_time),
        }
        response = self.session.post(url, headers=headers,
                                     data=json.dumps(body), verify=False)
        api_data = response.json()
        return api_data["data"]

    def revokeVoucher(self, voucherId):
        deleteVoucherUrl = f"proxy/network/api/s/default/cmd/hotspot"
        url = f"https://{self.gateway['ip']}/{deleteVoucherUrl}"
        headers = {
            "Content-Type": "application/json",
            "x-csrf-token": self.csrf_token
        }
        body = {
            "_id": voucherId,
            "cmd": "delete-voucher",
        }
        response = self.session.post(url, headers=headers,
                                     data=json.dumps(body), verify=False)
        api_data = response.json()
        pprint(api_data)


if __name__ == "__main__":
    # create a new client
    client = UbiquitiClient("192.168.1.1")
    # create a voucher
    voucherCreated = client.createVoucher(
        minutes=4320, count=5, quota=1, note="test 3 days", up=100, down=100, megabytes=100)
    pprint(voucherCreated)
    # retrieve the voucher
    vouchers = client.retrieveVoucher(voucherCreated[0]["create_time"])
    for voucher in vouchers:
        print("Voucher ID: " + voucher["_id"])
        print("Voucher Code: " + voucher["code"])
        print(voucher["quota"])
        print(voucher["note"])
        print(voucher["qos_rate_max_up"])
        print(voucher["qos_rate_max_down"])
        print(voucher["qos_usage_quota"])
