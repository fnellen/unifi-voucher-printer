from fpdf import FPDF


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


if __name__ == "__main__":
    pdf = VoucherPdfTemplate(orientation='l', unit='mm', format=(29.0, 62.0))
    pdf.addVoucher(voucherCode="1234567890",
                   ssid="Locanda Oca Bianca", daysValid=30, amountDevices=2)
    pdf.output("voucher.pdf", "F")
