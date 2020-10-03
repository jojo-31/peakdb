import logging
import traceback
from flask_restplus import Api
import settings


log = logging.getLogger(__name__)

api = Api(
    version="0.1", title="PeaksDB API", description="An API to retrieve world peaks"
)


@api.errorhandler
def default_error_handler(e):
    message = "An unhandled exception occurred."
    log.exception(message)

    if not settings.DEBUG:
        return {"message": message}, 500
