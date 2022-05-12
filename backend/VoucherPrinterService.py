from ubiquityApi import UniFiClient
from imgGenerator import ImgDrawer
from printer import PrinterSpooler
from decouple import config


class VoucherPrinterService:

    def __init__(self):
        self.bus = config('BUS')
        self.deviceModel = config('DEVICE_MODEL')
        self.devicePort = config('DEVICE_PORT')
        self.imgSize = config('IMG_SIZE')
        self.ssid = config('SSID')
        try:
            self.printer = PrinterSpooler(
                self.bus, self.deviceModel, self.devicePort, self.imgSize)
        except:
            self.printer = None
        try:
            self.client = UniFiClient(
                config('GATEWAY_IP'), config('GATEWAY_PORT'))
        except Exception as err:
            raise err

    def printVouchers(self, minutes, count, quota, note, up=None, down=None, megabytes=None):
        voucherCreated = self.client.createVoucher(
            minutes=minutes, count=count, quota=quota, note=note, up=up, down=down, megabytes=megabytes)
        if len(voucherCreated) == 0:
            return False, []
        vouchers = self.client.retrieveVoucher(voucherCreated[0].creationTime)
        imgDrawer = ImgDrawer(vouchers, self.ssid)
        imgDrawer.drawVouchers()
        if self.printer == None:
            return False, "Printer not online", vouchers
        try:
            self.printer.printImgs(vouchers)
            return True, None, vouchers
        except:
            return False, "Failed printing vouchers", vouchers
