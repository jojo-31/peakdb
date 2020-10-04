from pymongo import MongoClient, GEOSPHERE
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
import json
from typing import List, Union
import os
import logging

log = logging.getLogger(__name__)

PEAKS = [
    {"name": "Mont Valier", "altitude": 2838, "position": [42.79778, 1.08556]},
    {"name": "Pic de Maubermé", "altitude": 2880, "position": [42.79417, 0.91722]},
    {"name": "Pic de Crabère", "altitude": 2630, "position": [42.826039, 0.858633]},
]


class DB:
    def __init__(self):
        MONGO_URI = f"mongodb://{os.environ['MONGODB_HOSTNAME']}:{os.environ['MONGODB_PORT']}/{os.environ['MONGODB_DATABASE']}"

        try:
            client = MongoClient(MONGO_URI)
            self.db = client.peaks
            self.db.posts.delete_many({})
            self.db.posts.insert_many(PEAKS)
            self.db.posts.create_index([("position", GEOSPHERE)])
        except Exception as e:
            log.error(e)
            log.error("Connection to DB impossible. Continuing anyway...")

    def get_peaks(self) -> List[dict]:
        """Get all peaks currently in the DB"""
        peaks = list(self.db.posts.find())
        for peak in peaks:
            peak["id"] = peak["_id"]
            del peak["_id"]
        return peaks

    def add_peak(self, peak: dict) -> List[dict]:
        """Add a new peak to the DB,
        and return the created peak extracted from the DB

        Args:
            peak (dict): Peak to be inserted

        Returns:
            peak (dict): Created peak
        """
        if type(peak["position"]) == str:
            peak["position"] = json.loads(peak["position"])
        del peak["id"]
        result = self.db.posts.insert_one(peak)
        inserted_peak = self.db.posts.find_one({"_id": result.inserted_id})
        inserted_peak["id"] = inserted_peak["_id"]
        del inserted_peak["_id"]
        return inserted_peak

    def update_peak(self, peak_id: str, peak: dict) -> bool:
        """Update a peak existing in the DB

        Args:
            peak_id (str): ID of the peak to be updated
            peak (dict): Updated peak. ID cannot be modified.
        Returns:
            True if a peak has succesfully be modified
        """
        query = {"_id": ObjectId(peak_id)}
        del peak["id"]
        if type(peak["position"]) == str:
            peak["position"] = json.loads(peak["position"])
        result = self.db.posts.update_one(query, {"$set": peak})
        return result.modified_count == 1

    def remove_peak(self, peak_id: str) -> bool:
        """Removing a peak from the DB

        Args:
            peak_id (str): ID of the peak to be removed
        Returns:
            True if a peak has succesfully be modified
        """
        query = {"_id": ObjectId(peak_id)}
        result = self.db.posts.delete_one(query)
        return result.deleted_count == 1

    def get_peaks_in_bb(
        self, bottom_left: Union[str, list], upper_right: Union[str, list]
    ) -> List[dict]:
        """Get all peaks in BD that are contained in a bounding box.

        Args:
            bottom_left (str or list): Bottom left corner of the bounding box.
            upper_right (str or list): Upper right corner of the bounding box

        """
        if type(bottom_left) == str:
            bottom_left = json.loads(bottom_left)
        if type(upper_right) == str:
            upper_right = json.loads(upper_right)

        query = {"position": {"$within": {"$box": [bottom_left, upper_right]}}}

        peaks = list(self.db.posts.find(query))

        for peak in peaks:
            peak["id"] = peak["_id"]
            del peak["_id"]
        return peaks