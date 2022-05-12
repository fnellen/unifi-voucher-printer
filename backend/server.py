from waitress import serve
import views
from decouple import config
serve(views.app, host='0.0.0.0', port=config(
    "FLASK_RUN_PORT"), url_scheme="http")
