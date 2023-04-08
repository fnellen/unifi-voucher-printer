from flask import Flask
from flask import request
from VoucherPrinterService import VoucherPrinterService
from flask import abort
from flask_cors import CORS
from decouple import config
from werkzeug import secure_filename
import os
app = Flask(__name__)
cors = CORS(app, resources={
            r"/*": {"origins": config('FRONTEND_URL', default="*")}})


@app.route("/", methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/print-gate-code", methods=['POST'])
def printGateCode():
    voucherPrinterService = VoucherPrinterService()
    successfull, message = voucherPrinterService.printGateCode()
    resp = {}
    if successfull:
        resp["message"] = "Gate code printed successfully!"
        return resp, 200
    else:
        resp["error"] = message
        return resp, 500


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
            success, ErrorMessage, vouchers = voucherPrinterService.printVouchers(
                minutes=int(minutes), count=int(count), quota=int(quota), note=note, up=up, down=down, megabytes=megabytes)
            resp = {"vouchers": []}
            for v in vouchers:
                resp["vouchers"].append(
                    v.toDict())
                sf = secure_filename(f'tmp/{v.id}.png')
                os.remove(sf)
            if not success:
                resp["error"] = ErrorMessage
            return resp, 200
        except:
            return {"error": "Internal server errror", "vouchers": []}, 500
    else:
        abort(400)
