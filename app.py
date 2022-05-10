from urllib import response
from flask import Flask, make_response
from flask import request
from VoucherPrinterService import VoucherPrinterService
from flask import abort
import json
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
            r"/create-voucher/*": {"origins": "localhost:3000"}})


@app.route("/", methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/create-voucher", methods=["POST"])
def createVoucher():
    if request.method == "POST":
        try:
            minutes = request.args.get('minutes', 0)
            count = request.args.get('count', 0)
            quota = request.args.get('quota', 0)
            note = request.args.get('note', '')
            up = request.args.get('up', None)
            down = request.args.get('down', None)
            megabytes = request.args.get('megabytes', None)
            if minutes == 0 or count == 0 or quota == 0 or note == '':
                abort(400)
            if up is None:
                up = 5000
            if down is None:
                down = 2000
            voucherPrinterService = VoucherPrinterService()
            success, vouchers = voucherPrinterService.printVouchers(
                minutes=int(minutes), count=int(count), quota=int(quota), note=note, up=up, down=down, megabytes=megabytes)
            resp = {"vouchers": []}
            for v in vouchers:
                resp["vouchers"].append(v.toDict())
            return resp, 200
        except Exception as err:
            return {"Fehler": str(err)}, 500
    else:
        abort(400)
