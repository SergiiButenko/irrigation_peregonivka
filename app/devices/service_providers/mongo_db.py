from pymongo import MongoClient
import json
from bson import ObjectId

from fastapi import Depends


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class Mongo:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client.irrigation_db
        self.sensors_collection = self.db.sensors

    async def register_sensor_data(self, device_id, sensor_id, data):
        await self._insert_document(self.sensors_collection, dict(
            device_id=device_id,
            sensor_id=sensor_id,
            data=data
        ))

    async def get_latest_sensor_data(self, device_id: str, sensor_id: str, minutes_from_now: int, function: str, sorting: str):
        return await self._find_document(self.sensors_collection, {'device_id': device_id, 'sensor_id': sensor_id})

    async def _insert_document(self, collection, data):
        """ Function to insert a document into a collection and
        return the document's id.
        """
        return await collection.insert_one(data).inserted_id

    async def _find_document(self, collection, elements, multiple=False):
        """ Function to retrieve single or multiple documents from a provided
        Collection using a dictionary containing a document's elements.
        """
        if multiple:
            results = collection.find(elements)
            return [JSONEncoder().encode(r) for r in results]
        else:
            return JSONEncoder().encode(collection.find_one(elements))
