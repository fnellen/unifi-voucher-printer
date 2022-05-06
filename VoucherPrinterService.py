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
        self.printer = PrinterSpooler(
            self.bus, self.deviceModel, self.devicePort, self.imgSize)
        try:
            self.client = UniFiClient(
                config('GATEWAY_IP'), config('GATEWAY_PORT'))
        except Exception as err:
            raise SystemExit(err)

    def printVouchers(self, minutes, count, quota, note, up=None, down=None, megabytes=None):
        voucherCreated = self.client.createVoucher(
            minutes=minutes, count=count, quota=quota, note=note, up=up, down=down, megabytes=megabytes)
        vouchers = self.client.retrieveVoucher(voucherCreated[0].creationTime)
        imgDrawer = ImgDrawer(vouchers, config('SSID'))
        imgDrawer.drawVouchers()
        self.printer.printImgs(vouchers)


if __name__ == '__main__':
    voucherPrinterService = VoucherPrinterService()
    voucherPrinterService.printVouchers(
        minutes=4320, count=1, quota=3, note="Zimmer 102", up=2000, down=5000)
