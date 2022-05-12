from waitress import serve
import app
from decouple import config
serve(app.app, host='0.0.0.0', port=config(
    "FLASK_RUN_PORT"), url_scheme="http")
