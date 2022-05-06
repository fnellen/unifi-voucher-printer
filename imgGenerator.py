from email.utils import localtime
from PIL import Image, ImageDraw, ImageFont

from uniFiVouchers import UniFiVoucher
from datetime import datetime
import tzlocal


class ImgDrawer:
    width = 696
    height = 271

    def __init__(self, uniFiVouchers: list[UniFiVoucher], ssid):
        self.uniFiVouchers = uniFiVouchers
        self.ssid = ssid

    def drawVouchers(self):
        for voucher in self.uniFiVouchers:
            self.drawVoucher(voucher)

    def drawVoucher(self, uniFiVoucher: UniFiVoucher):
        img1 = Image.new(mode="RGB", size=(
            self.width, self.height), color="white")
        img2 = Image.open("img/voucherLayout.png")
        img1.paste(img2, (0, 0))
        fntBold = ImageFont.truetype('/Library/Fonts/Arial Bold.ttf', 60)
        fnt25pt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 25)
        fnt20pt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 20)

        d = ImageDraw.Draw(img1)
        d.text((90, 17), self.ssid, font=fnt25pt, fill=(0, 0, 0))
        d.text((64, 80), str(int(uniFiVoucher.duration / 1440)) + " Days",
               font=fnt20pt, fill=(0, 0, 0))
        d.text((64, 142), str(uniFiVoucher.speedUp) + " Kbps",
               font=fnt20pt, fill=(0, 0, 0))
        d.text((64, 205), str(uniFiVoucher.speedDown) + " Kbps",
               font=fnt20pt, fill=(0, 0, 0))

        d.text((219, 223), str(uniFiVoucher.usageQuota),
               font=fnt25pt, fill=(0, 0, 0))
        localtimeZone = tzlocal.get_localzone()
        d.text((334, 223), datetime.fromtimestamp(uniFiVoucher.creationTime, localtimeZone).strftime('%d.%m.%Y at %H:%M'),
               font=fnt25pt, fill=(0, 0, 0))

        # https://github.com/python-pillow/Pillow/issues/5932
        gap = 5
        tuple_var = (239, 105)
        string_var = uniFiVoucher.code
        for char in string_var:
            d.text(tuple_var, char, (0, 0, 0), font=fntBold, align='center')
            width = d.textsize(char, font=fntBold)[0] + gap
            tuple_var = (tuple_var[0]+width, tuple_var[1])

        img1.save(f'tmp/{uniFiVoucher.id}.png')


if __name__ == '__main__':
    imgDrawer = ImgDrawer(
        [UniFiVoucher({"_id": "1", "code": "1234567890", "duration": 4320, "quota": 2, "note": "Zimmer 102", "create_time": 1651831339, "qos_rate_max_up": "1000",  "qos_rate_max_down": "1000"})], "Locanda Oca Bianca")
    imgDrawer.drawVouchers()
