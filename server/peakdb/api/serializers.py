from flask_restplus import fields
from api.restplus import api

peak = api.model(
    "peak",
    {
        "id": fields.String(
            readOnly=True, description="The unique identifier of a peak"
        ),
        "name": fields.String(required=True, description="Name of the peak"),
        "altitude": fields.Integer(required=True, description="Altitude of the peak"),
        "position": fields.List(
            fields.Float(),
            description="Position of the peak, in lon / lat decimal degrees",
        ),
    },
)
ip = api.model(
    "ip",
    {
        "ip": fields.String(required=True, description="Black IP"),
        "date": fields.String(required=True, description="Date of the request"),
    },
)
