from uniFiVouchers import UniFiVoucher
import subprocess
import usb.core
import usb.util
# https://github.com/pklaus/brother_ql


class PrinterSpooler:

    def __init__(self, bus, deviceModel, device_specifier, imgSize):
        if bus == 'pyusb':
            self.bus = bus
        else:
            raise ValueError("Not yet implemented other than pyusb")
        if deviceModel == 'QL-570':
            self.deviceModel = deviceModel
        else:
            raise ValueError("Not yet implemented other than QL-570")
        self.imgSize = imgSize
        self.dev = None
        if device_specifier.startswith('usb://'):
            device_specifier = device_specifier[6:]
            vendor_product, _, serial = device_specifier.partition('/')
            vendor, _, product = vendor_product.partition(':')
            vendor, product = int(vendor, 16), int(product, 16)
            for result in self.list_available_devices():
                printer = result['instance']
                if printer.idVendor == vendor and printer.idProduct == product or (serial and printer.iSerialNumber == serial):
                    self.dev = printer["identifier"]
                    break
            if self.dev is None:
                raise ValueError('Device not found')

    def list_available_devices(self):
        """
        List all available devices for the respective backend

        returns: devices: a list of dictionaries with the keys 'identifier' and 'instance': \
            [ {'identifier': 'usb://0x04f9:0x2015/C5Z315686', 'instance': pyusb.core.Device()}, ]
            The 'identifier' is of the format idVendor:idProduct_iSerialNumber.
        """
        class find_class(object):
            def __init__(self, class_):
                self._class = class_

            def __call__(self, device):
                # first, let's check the device
                if device.bDeviceClass == self._class:
                    return True
                # ok, transverse all devices to find an interface that matches our class
                for cfg in device:
                    # find_descriptor: what's it?
                    intf = usb.util.find_descriptor(
                        cfg, bInterfaceClass=self._class)
                    if intf is not None:
                        return True
                return False

        # only Brother printers
        printers = usb.core.find(
            find_all=1, custom_match=find_class(7), idVendor=0x04f9)

        def identifier(dev):
            try:
                serial = usb.util.get_string(dev, 256, dev.iSerialNumber)
                return 'usb://0x{:04x}:0x{:04x}_{}'.format(dev.idVendor, dev.idProduct, serial)
            except:
                return 'usb://0x{:04x}:0x{:04x}'.format(dev.idVendor, dev.idProduct)

        return [{'identifier': identifier(printer), 'instance': printer} for printer in printers]

    def printImgs(self, vouchers: list[UniFiVoucher]):
        for voucher in vouchers:
            process = subprocess.Popen(['brother_ql', '-b', self.bus, '-m', self.deviceModel, '-p', self.dev, 'print', '-l', self.imgSize, f'tmp/{voucher.id}.png'],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if "Printing was successful" not in stdout.decode('utf-8') or "Printing was successful" not in stderr.decode('utf-8'):
                raise SystemError(f"Printing failed for {voucher.id}")
