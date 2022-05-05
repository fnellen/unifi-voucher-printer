class UniFiVoucher:

    def __init__(self, json: dict):
        self.id = json.get("_id", None)
        self.adminName = json.get("admin_name", None)
        self.code = json.get("code", None)
        self.creationTime = json.get("create_time", None)
        self.duration = json.get("duration", None)
        self.note = json.get("note", None)
        self.speedUp = json.get("qos_rate_max_up", None)
        self.speedDown = json.get("qos_rate_max_down", None)
        self.usageQuota = json.get("quota", None)
        self.siteId = json.get("site_id", None)
        self.status = json.get("status", None)
        self.used = json.get("used", None)
        self.statusExpires = json.get("status_expires", None)

    def __str__(self) -> str:
        return f"ID: {self.id}, Created By: {self.adminName}, Code: {self.code}, Created At {self.creationTime}, Valid for: {self.duration}, Note: {self.note}, Upload Speed: {self.speedUp}, Download Speed {self.speedDown}, Quota: {self.usageQuota}, SiteId: {self.siteId}, Status: {self.status}, Used: {self.used}, Status Expires: {self.statusExpires}"
