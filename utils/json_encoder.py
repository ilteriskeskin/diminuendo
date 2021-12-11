import json

from bson.objectid import ObjectId


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(JsonEncoder, self).default(obj)
