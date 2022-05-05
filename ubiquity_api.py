import requests
import json
import urllib3
from decouple import config
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# https://github.com/Art-of-WiFi/UniFi-API-client/blob/cbe89d913cc4dd3742d5fd35e201ec86bc8ccdc9/src/Client.php#L1919
# https://rtyley.github.io/bfg-repo-cleaner/


class UniFiVoucher:

    def __init__(self, id, adminName, code, creationTime, duration, note, speedUp, speedDown, usageQuota, siteId, status, used, statusExpires) -> None:
        self.id = id
        self.adminName = adminName
        self.code = code
        self.creationTime = creationTime
        self.duration = duration
        self.note = note
        self.speedUp = speedUp
        self.speedDown = speedDown
        self.usageQuota = usageQuota
        self.siteId = siteId
        self.status = status
        self.used = used
        self.statusExpires = statusExpires

    def __init__(self, json: dict):
        self.id = json.get("_id", None)
        self.adminName = json.get("admin_name", None)
        self.code = json.get("code", None)
        self.creationTime = json.get("create_time", None)
        self.duration = json.get("duration", None)
        self.note = json.get("note", None)
        self.speedUp = json.get("qos_rate_max_up", None)
        self.speedDown = json.get("qos_rate_max_down", None)
        self.usageQuota = json.get("qos_usage_quota", None)
        self.siteId = json.get("site_id", None)
        self.status = json.get("status", None)
        self.used = json.get("used", None)
        self.statusExpires = json.get("status_expires", None)

    def __str__(self) -> str:
        return f"ID: {self.id}, Created By: {self.adminName}, Code: {self.code}, Created At {self.creationTime}, Valid for: {self.duration}, Note: {self.note}, Upload Speed: {self.speedUp}, Download Speed {self.speedDown}, Quota: {self.usageQuota}, SiteId: {self.siteId}, Status: {self.status}, Used: {self.used}, Status Expires: {self.statusExpires}"


class UniFiClient:
    # set up connection parameters in a dictionary
    gateway = {"ip": "", "port": ""}
    csrf_token = ""
    session = None

    def __init__(self, gatewayIp, gatewayPort) -> None:
        self.gateway["ip"] = str(gatewayIp)
        self.gateway["gatewayPort"] = str(gatewayPort)
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
            "username": config("USERNAME"),
            "password": config("PASSWORD")
        }
        # Open a session for capturing cookies
        try:
            session = requests.Session()
            # login
            response = session.post(url, headers=headers,
                                    data=json.dumps(body), verify=False)
            response.raise_for_status()
            # Get CSRF token from response headers
            return response.headers["X-CSRF-Token"], session
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

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

    def createVoucher(self, minutes, count, quota, note, up=None, down=None, megabytes=None):
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
                                         data=json.dumps(body), verify=False)
            response.raise_for_status()
            api_data = response.json()
            vouchers = []
            for voucher in api_data["data"]:
                vouchers.append(UniFiVoucher(voucher))
            return vouchers
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

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
        response = self.session.post(url, headers=headers,
                                     data=json.dumps(body), verify=False)
        response.raise_for_status()
        try:
            api_data = response.json()
            vouchers = []
            for voucher in api_data["data"]:
                vouchers.append(UniFiVoucher(voucher))
            return vouchers
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    def retrieveAllVouchers(self) -> list:
        fetchVoucherUrl = f"proxy/network/api/s/default/stat/voucher"
        url = f"https://{self.gateway['ip']}:{self.gateway['port']}/{fetchVoucherUrl}"
        headers = {
            "Content-Type": "application/json",
            "x-csrf-token": self.csrf_token
        }
        body = {
        }
        response = self.session.post(url, headers=headers,
                                     data=json.dumps(body), verify=False)
        response.raise_for_status()
        try:
            api_data = response.json()
            vouchers = []
            for voucher in api_data["data"]:
                vouchers.append(UniFiVoucher(voucher))
            return vouchers
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

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
        response = self.session.post(url, headers=headers,
                                     data=json.dumps(body), verify=False)
        response.raise_for_status()
        try:
            return True
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)


if __name__ == "__main__":
    # create a new client
    client = UniFiClient("192.168.1.1", "443")
    # create a voucher
    voucherCreated = client.createVoucher(
        minutes=4320, count=5, quota=1, note="test 3 days", up=100, down=100, megabytes=100)
    voucherCreated = client.createVoucher(
        minutes=2880, count=10, quota=1, note="test 5 days", up=100, down=100, megabytes=100)
    # retrieve the voucher
    vouchers = client.retrieveAllVouchers()
    for v in vouchers:
        print(v)
    vouchers = client.retrieveVoucher(voucherCreated[0].creationTime)
    for voucher in vouchers:
        print(voucher.id)
        print(voucher.code)
        #print("Deleted: " + str(client.revokeVoucher(voucherId=voucher.id)))
