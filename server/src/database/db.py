from pymongo import MongoClient
from bson.json_util import dumps, loads
import json
PEAKS = [
    {
        'name': 'Mont Valier',
        'altitude': 2838,
    },
    {
        'name': 'Pic de Maubermé',
        'altitude': 2880,
    },
    {
        'name': 'Pic de Crabère',
        'altitude': 2630,
    },
]
class DB():
    def __init__(self):
        client = MongoClient("mongodb://localhost")
        self.db = client.peaks
        self.db.posts.delete_many({})
        self.db.posts.insert_many(PEAKS)

    def get_peaks(self):
        peaks = list(self.db.posts.find())
        for peak in peaks:
            peak["id"] = dumps(peak["_id"])
            del peak["_id"]
        return peaks

    def add_peak(self, peak: dict):
        self.db.posts.insert_one(peak)

    def update_peak(self, peak_id: int, peak: dict):
        print(peak)
        _id = loads(peak_id)
        del peak["id"]
        query = {"_id": _id}
        self.db.posts.update_one(query, {"$set": peak})

    def remove_peak(self, peak_id: int):
        _id = loads(peak_id)
        query = {"_id": _id}
        self.db.posts.delete_one(query)