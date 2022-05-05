from PIL import Image, ImageDraw, ImageFont


class ImgDrawer:
    width = 696
    height = 271

    def __init__(self, id, code, ssid, daysValid, amountDevices):
        self.id = id
        self.code = code
        self.ssid = ssid
        self.daysValid = daysValid
        self.amountDevices = amountDevices

    def drawVoucher(self):
        img = Image.new(mode="RGB", size=(
            self.width, self.height), color="white")

        fntBold = ImageFont.truetype('/Library/Fonts/Arial Bold.ttf', 60)
        fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 40)
        d = ImageDraw.Draw(img)
        d.text((157, 26), self.ssid, font=fnt, fill=(0, 0, 0))
        d.text((167, 96), self.code, font=fntBold, fill=(0, 0, 0))
        d.text((77, 192), "Valid for " + self.daysValid + " days and " +
               self.amountDevices + " devices", font=fnt, fill=(0, 0, 0))

        img.save('save.png')
