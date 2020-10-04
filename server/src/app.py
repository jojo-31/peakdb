import logging.config
from flask_cors import CORS
from flask import Flask, jsonify, request, Blueprint, cli

cli.load_dotenv()

from database.db import DB
import uuid
import os
from api import restplus
from api.peaks.endpoints import ns as peaks_ns

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

logging_conf_path = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "../logging.conf")
)
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


def create_blueprint(app):
    blueprint = Blueprint("peaks", __name__, url_prefix="/peaks")
    restplus.api.init_app(blueprint)
    restplus.api.add_namespace(peaks_ns)

    CORS(blueprint, resources={r"*": {"origins": "*"}})
    app.register_blueprint(blueprint)


@app.after_request
def after_request(response):
    response.headers.set("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    return response


def main():
    create_blueprint(app)
    app.run(debug=os.environ["APP_DEBUG"])


if __name__ == "__main__":
    main()