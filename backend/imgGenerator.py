from PIL import Image, ImageDraw, ImageFont

from uniFiVouchers import UniFiVoucher


class ImgDrawer:
    width = 696
    height = 271

    def __init__(self, uniFiVouchers: list[UniFiVoucher], ssid, gateCode):
        self.uniFiVouchers = uniFiVouchers
        self.ssid = ssid
        self.gateCode = gateCode

    def drawVouchers(self):
        for voucher in self.uniFiVouchers:
            self.drawVoucher(voucher)

    def drawGateCode(self):
        img = Image.new(mode="RGB", size=(
            self.width, self.height), color=(255, 255, 255))
        backgroundImage = Image.open("img/gateCodeLayout.png")
        img.paste(backgroundImage, (0, 0))
        fntBold = ImageFont.truetype('fonts/Arial Bold.ttf', 60)
        d = ImageDraw.Draw(img)

        gap = 5
        tuple_var = (227, 119)
        string_var = str(self.gateCode)
        for char in string_var:
            d.text(tuple_var, char, (0, 0, 0), font=fntBold, align='center')
            width = d.textsize(char, font=fntBold)[0] + gap
            tuple_var = (tuple_var[0]+width, tuple_var[1])

        img.save(f'tmp/gateCode.png')

    def drawVoucher(self, uniFiVoucher: UniFiVoucher):
        img1 = Image.new(mode="RGB", size=(
            self.width, self.height), color="white")
        img2 = Image.open("img/voucherLayoutV4.png")
        img1.paste(img2, (0, 0))
        fntBold = ImageFont.truetype('fonts/Arial Bold.ttf', 60)
        fnt25pt = ImageFont.truetype('fonts/Arial.ttf', 30)
        fnt25ptBold = ImageFont.truetype('fonts/Arial Bold.ttf', 30)
        d = ImageDraw.Draw(img1)
        # SSID
        d.text((146, 25), self.ssid, font=fnt25pt, fill=(0, 0, 0))
        # ROOM
        d.text((588, 25), uniFiVoucher.note, font=fnt25pt, fill=(0, 0, 0))
        # DURATION
        d.text((63, 210), str(int(uniFiVoucher.duration / 1440)) + " Days",
               font=fnt25pt, fill=(0, 0, 0))
        # QUANTITY
        d.text((234, 210), str(uniFiVoucher.usageQuota),
               font=fnt25pt, fill=(0, 0, 0))
        # GATE CODE
        d.text((452, 210), str(self.gateCode),
               font=fnt25ptBold, fill=(0, 0, 0))

        # https://github.com/python-pillow/Pillow/issues/5932
        gap = 5
        tuple_var = (158, 119)
        string_var = uniFiVoucher.code
        for char in string_var:
            d.text(tuple_var, char, (0, 0, 0), font=fntBold, align='center')
            width = d.textsize(char, font=fntBold)[0] + gap
            tuple_var = (tuple_var[0]+width, tuple_var[1])
        img1.save(f'tmp/{uniFiVoucher.id}.png')


if __name__ == '__main__':
    imgDrawer = ImgDrawer(
        [UniFiVoucher({"_id": "1", "code": "64728937", "duration": 4320, "quota": 10, "note": "102", "create_time": 1651831339, "qos_rate_max_up": "1000",  "qos_rate_max_down": "1000"})], "Locanda Oca Bianca", "19555A")
    # imgDrawer.drawVouchers()
    imgDrawer.drawGateCode()
