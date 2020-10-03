import logging

from flask import request, jsonify
import flask_cors
from flask_restplus import Resource
from api import restplus
from database import db_instance
from api import serializers

log = logging.getLogger(__name__)

ns = restplus.api.namespace("peaks", description="Operations related to peaks")


@ns.route("/")
class PeakCollection(Resource):
    @restplus.api.marshal_list_with(serializers.peak)
    def get(self):
        """Returns the list of all peaks"""
        return db_instance.get_peaks()

    @restplus.api.response(204, "Peak successfully created.")
    @restplus.api.expect(serializers.peak)
    def post(self):
        """Add a new peak"""
        inserted_peak = db_instance.add_peak(request.json)
        return inserted_peak, 204


@ns.route("/<string:peak_id>")
@restplus.api.response(404, "Peak not found.")
class PeakItem(Resource):
    @restplus.api.expect(serializers.peak)
    @restplus.api.response(204, "Peak successfully updated.")
    def put(self, peak_id: str):
        """Update a peak

        Args:
            peak_id (str): ID of the peak
        """
        db_instance.update_peak(peak_id, request.json)
        return None, 204

    @restplus.api.response(204, "Peak successfully deleted.")
    def delete(self, peak_id: str):
        """Delete a peak

        Args:
            peak_id (str): ID of the peak
        """
        db_instance.remove_peak(peak_id)
        return None, 204


@ns.route("/<string:bottom_left>/<string:upper_right>")
class PeakSearch(Resource):
    @restplus.api.marshal_list_with(serializers.peak)
    def get(self, bottom_left: str, upper_right: str):
        """Get all peaks within the given bounding box
        The given bounding box points should be a list of lon / lat,
        in decimal degrees, eg: [40.2, 12.5]

        Args:
            bottom_left (str): Bottom left point of the bounding box
            upper_right (str): Upper right point of the bounding box

        """
        return db_instance.get_peaks_in_bb(bottom_left, upper_right)
