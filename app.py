from flask import Flask
from flask import request
from VoucherPrinterService import VoucherPrinterService
from flask import abort
import json
app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/create-voucher", methods=["POST"])
def createVoucher():
    if request.method == "POST":
        try:
            minutes = request.args.get('minutes', '')
            count = request.args.get('count', '')
            quota = request.args.get('quota', '')
            note = request.args.get('note', '')
            up = request.args.get('up', None)
            down = request.args.get('down', None)
            megabytes = request.args.get('megabytes', None)
            print(minutes, count, quota, note, up, down, megabytes)
            if minutes == '' or count == '' or quota == '' or note == '':
                abort(400)
            if up is None:
                up = 5000
            if down is None:
                down = 2000
            voucherPrinterService = VoucherPrinterService()
            success, vouchers = voucherPrinterService.printVouchers(
                minutes=int(minutes), count=int(count), quota=int(quota), note=note, up=up, down=down, megabytes=megabytes)
            if success:
                resp = {"vouchers": []}
                for v in vouchers:
                    resp["vouchers"].append(v.toDict())
                return json.dumps(resp)
            else:
                abort(500)
        except KeyError as err:
            return "Error: " + str(err)
