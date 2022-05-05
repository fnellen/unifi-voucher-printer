from PIL import Image, ImageDraw, ImageFont

from uniFiVouchers import UniFiVoucher


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
        img = Image.new(mode="RGB", size=(
            self.width, self.height), color="white")

        fntBold = ImageFont.truetype('/Library/Fonts/Arial Bold.ttf', 60)
        fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 40)
        d = ImageDraw.Draw(img)
        d.text((157, 26), self.ssid, font=fnt, fill=(0, 0, 0))
        d.text((167, 96), uniFiVoucher.code[: 5] + " " +
               uniFiVoucher.code[5:], font=fntBold, fill=(0, 0, 0))
        d.text((77, 192), "Valid for " + str(uniFiVoucher.duration / 1440) +
               " days and " + str(uniFiVoucher.usageQuota) + " Devices", font=fnt, fill=(0, 0, 0))

        img.save(f'tmp/{uniFiVoucher.id}.png')
