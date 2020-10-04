import os
from pathlib import Path
import logging.config
from flask_cors import CORS
from flask import (
    Flask,
    jsonify,
    request,
    Blueprint,
    cli,
    render_template,
    abort,
)
from flask import send_from_directory, url_for
from jinja2 import TemplateNotFound

dir_path = Path(os.path.realpath(__file__)).parent / ".env"
cli.load_dotenv(dir_path)

from api import restplus
from api.peaks.endpoints import ns_peaks
from api.black_ips.endpoints import ns_ips

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

logging_conf_path = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "../logging.conf")
)
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

sample_page = Blueprint("", "", template_folder="templates")

def create_blueprints(app):
    blueprint = Blueprint("peaks", __name__, url_prefix="/peaks")
    restplus.api.init_app(blueprint)
    restplus.api.add_namespace(ns_peaks)
    CORS(blueprint, resources={r"*": {"origins": "*"}})
    app.register_blueprint(blueprint)

    blueprint = Blueprint("ips", __name__, url_prefix="/ips")
    restplus.api.init_app(blueprint)
    restplus.api.add_namespace(ns_ips)
    CORS(blueprint, resources={r"*": {"origins": "*"}})
    app.register_blueprint(blueprint)

    app.register_blueprint(sample_page, url_prefix="/")

@app.after_request
def after_request(response):
    response.headers.set("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    return response


def main():
    create_blueprints(app)
    app.run(debug=os.environ["APP_DEBUG"])


if __name__ == "__main__":
    main()
