from sre_constants import SUCCESS
from uniFiVouchers import UniFiVoucher
import os
# https://github.com/pklaus/brother_ql


class PrinterSpooler:

    def __init__(self, bus, deviceModel, devicePort, imgSize):
        self.bus = bus
        self.deviceModel = deviceModel
        self.devicePort = devicePort
        self.imgSize = imgSize

    def printImgs(self, vouchers: list[UniFiVoucher]):
        for voucher in vouchers:
            # Save pages as images in the pdf
            # brother_ql -b pyusb -m 'QL-570' -p usb://0x04f9:0x2028 print -l '62x29' {voucher.id}
            stream = os.popen(
                f"brother_ql -b {self.bus} -m '{self.deviceModel}' -p {self.devicePort} print -l '{self.imgSize}' tmp/{voucher.id}.png")
            output = stream.read()
            # if "Printing was successful" in output:
            #     print(SUCCESS)
            # else:
            #     print(f"Error while printing voucher {voucher.id}")
            #     break
