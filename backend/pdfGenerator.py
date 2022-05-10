from fpdf import FPDF
from uniFiVouchers import UniFiVoucher
from decouple import config


class VoucherPdfTemplate(FPDF):

    def ssid(self, ssid):
        self.set_font('Arial', '', 8)
        self.set_xy(0, 6)
        self.cell(w=62, h=0, txt=ssid, border=0, align="C")

    def voucherCode(self, voucherCode):
        self.set_font('Arial', 'B', 15)
        self.set_xy(0, 14.5)
        self.cell(w=62, h=0, txt=voucherCode[: 5] + " " +
                  voucherCode[5:], border=0, align="C")

    def validity(self, daysValid, amountDevices):
        self.set_font('Arial', '', 8)
        self.set_xy(0, 23)
        self.cell(w=62, h=0, txt="Valid for " + str(daysValid) +
                  " days and " + str(amountDevices) + " Devices", border=0, align="C")

    def addVoucher(self, voucherCode, ssid, daysValid, amountDevices):
        self.set_auto_page_break(auto=False, margin=0.0)
        self.add_page()
        self.ssid(ssid)
        self.voucherCode(voucherCode)
        self.validity(daysValid, amountDevices)


class VoucherPdfGenerator:
    pdf: VoucherPdfTemplate
    ssid = config("SSID")

    def __init__(self, ssid):
        self.pdf = VoucherPdfTemplate(
            orientation='l', unit='mm', format=(29.0, 62.0))
        self.ssid = ssid

    def drawVouchers(self, vouchers: UniFiVoucher):
        for voucher in vouchers:
            self.appendVoucher(voucherCode=voucher.code,
                               ssid=self.ssid, daysValid=voucher.duration / 60, amountDevices=voucher.usageQuota)
        self.exportVoucher()

    def appendVoucher(self, voucherCode, ssid, daysValid, amountDevices):
        self.pdf.addVoucher(voucherCode=voucherCode,
                            ssid=ssid, daysValid=daysValid, amountDevices=amountDevices)

    def exportVoucher(self):
        self.pdf.output("voucher.pdf", "S")
