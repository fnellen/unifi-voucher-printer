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
            # Save pages as images in the pdf
            # brother_ql -b pyusb -m 'QL-570' -p usb://0x04f9:0x2028 print -l '62x29' {voucher.id}
            # successfull = os.system(
            #    f"brother_ql -b {self.bus} -m '{self.deviceModel}' -p {self.devicePort} print -l '{self.imgSize}' tmp/{voucher.id}.png")
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
