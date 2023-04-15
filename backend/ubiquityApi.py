import requests
import json
import urllib3
from uniFiVouchers import UniFiVoucher
from decouple import config
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Inspiered by: https://github.com/Art-of-WiFi/UniFi-API-client/blob/cbe89d913cc4dd3742d5fd35e201ec86bc8ccdc9/src/Client.php#L1919


class UniFiClient:
    # set up connection parameters in a dictionary
    gateway = {"ip": "", "port": ""}
    csrf_token = ""
    session = None

    def __init__(self, gatewayIp, gatewayPort) -> None:
        self.gateway["ip"] = str(gatewayIp)
        self.gateway["gatewayPort"] = str(gatewayPort)
        csrf_token, session = self.getCsrfToken()
        if csrf_token is None:
            raise SystemExit("Could not get CSRF token")
        self.csrf_token = csrf_token
        self.session = session

    def getCsrfToken(self):
        # set REST API headers
        headers = {"Accept": "application/json",
                   "Content-Type": "application/json"}
        # set URL parameters
        loginUrl = 'api/auth/login'
        url = f"https://{self.gateway['ip']}/{loginUrl}"
        # set username and password
        body = {
            "username": config("USERNAME"),
            "password": config("PASSWORD")
        }
        # Open a session for capturing cookies
        try:
            session = requests.Session()
            # login
            response = session.post(url, headers=headers,
                                    data=json.dumps(body))
            # Get CSRF token from response headers
            return response.headers["X-CSRF-Token"], session
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    def createVoucher(self, minutes: int, count: int, quota: int, note: str, up: int = None, down: int = None, megabytes: int = None):
        """
     Create voucher(s)

     NOTES: please use the retrieveVoucher() method/function to retrieve the newly created voucher(s) by create_time

     @param int    minutes   minutes the voucher is valid after activation (expiration time)
     @param int    count     number of vouchers to create, default value is 1
     @param int    quota     single-use or multi-use vouchers, value '0' is for multi-use, '1' is for single-use,
                              'n' is for multi-use n times
     @param string note      note text to add to voucher when printing
     @param int    up        upload speed limit in kbps
     @param int    down      download speed limit in kbps
     @param int    megabytes data transfer limit in MB
     @return array containing a single object which contains voucher createtime
     */
     """
        createVoucherUrl = f"proxy/network/api/s/default/cmd/hotspot"
        url = f"https://{self.gateway['ip']}:{self.gateway['port']}/{createVoucherUrl}"
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
        try:
            response = self.session.post(url, headers=headers,
                                         data=json.dumps(body))
            api_data = response.json()
            vouchers = []
            # vouchers = [UniFiVoucher(x) for x in api_data["data"]]
            for voucher in api_data["data"]:
                vouchers.append(UniFiVoucher(voucher))
            return vouchers
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def retrieveVoucher(self, create_time):
        fetchVoucherUrl = f"proxy/network/api/s/default/stat/voucher"
        url = f"https://{self.gateway['ip']}:{self.gateway['port']}/{fetchVoucherUrl}"
        headers = {
            "Content-Type": "application/json",
            "x-csrf-token": self.csrf_token
        }
        body = {
            "create_time": str(create_time),
        }
        try:
            response = self.session.post(url, headers=headers,
                                         data=json.dumps(body))
            api_data = response.json()
            vouchers = []
            for voucher in api_data["data"]:
                vouchers.append(UniFiVoucher(voucher))
            return vouchers
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def retrieveAllVouchers(self) -> list:
        fetchVoucherUrl = f"proxy/network/api/s/default/stat/voucher"
        url = f"https://{self.gateway['ip']}:{self.gateway['port']}/{fetchVoucherUrl}"
        headers = {
            "Content-Type": "application/json",
            "x-csrf-token": self.csrf_token
        }
        body = {
        }
        try:
            response = self.session.post(url, headers=headers,
                                         data=json.dumps(body))
            api_data = response.json()
            vouchers = []
            for voucher in api_data["data"]:
                vouchers.append(UniFiVoucher(voucher))
            return vouchers
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def revokeVoucher(self, voucherId):
        deleteVoucherUrl = f"proxy/network/api/s/default/cmd/hotspot"
        url = f"https://{self.gateway['ip']}:{self.gateway['port']}/{deleteVoucherUrl}"
        headers = {
            "Content-Type": "application/json",
            "x-csrf-token": self.csrf_token
        }
        body = {
            "_id": voucherId,
            "cmd": "delete-voucher",
        }
        try:
            response = self.session.post(url, headers=headers,
                                         data=json.dumps(body))
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
