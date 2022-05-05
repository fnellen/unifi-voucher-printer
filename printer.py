from uniFiVouchers import UniFiVoucher
import subprocess
# https://github.com/pklaus/brother_ql


class PrinterSpooler:

    def __init__(self, bus, deviceModel, devicePort, imgSize):
        self.bus = bus
        self.deviceModel = deviceModel
        self.devicePort = devicePort
        self.imgSize = imgSize

    def printImgs(self, vouchers: list[UniFiVoucher]):
        for voucher in vouchers:
            process = subprocess.Popen(['brother_ql', '-b', self.bus, '-m', self.deviceModel, '-p', self.devicePort, 'print', '-l', self.imgSize, f'tmp/{voucher.id}.png'],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if "Printing was successful" in stdout.decode('utf-8'):
                print(f"Printing was successful for {voucher.id}")
            elif "Printing was successful" in stderr.decode('utf-8'):
                print(f"Printing was successful for {voucher.id}")
            else:
                # print(stderr)
                print(f"Printing failed for {voucher.id}")
