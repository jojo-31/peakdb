import logging
import traceback
from flask_restplus import Api

log = logging.getLogger(__name__)

api = Api(
    version="0.1", title="PeaksDB API", description="An API to retrieve world peaks"
)