import logging

from flask import request, jsonify
import flask_cors
from flask_restplus import Resource
from api import restplus
from database import db_instance
from api import serializers, utilities

log = logging.getLogger(__name__)

ns_ips = restplus.api.namespace("ips", description="Operations related to black IPs")


@ns_ips.route("/")
class IpsCollection(Resource):
    @restplus.api.marshal_list_with(serializers.ip)
    def get(self):
        """Returns the list of all blacked IPs"""
        return db_instance.get_black_ips()