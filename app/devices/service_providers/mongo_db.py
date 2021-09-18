from devices.models.devices import SensorValueNSQL


class Mongo:
    def __init__(self, client):
        self.db = client.irrigation_db
        self.sensors_collection = self.db.sensors

    async def _insert_document(self, collection, data):
        """ Function to insert a document into a collection and
        return the document's id.
        """

        return await collection.insert_one(data.dict())

    async def _find_document(self, collection, query):
        """ Function to retrieve single or multiple documents from a provided
        Collection using a dictionary containing a document's query.
        """
        data = []
        cursor = collection.find(query)
        for document in await cursor.to_list(length=500):
            data.append(SensorValueNSQL(**document))

        return data

    async def register_sensor_data(self, device_id, sensor_id, data):
        await self._insert_document(self.sensors_collection, SensorValueNSQL(
            device_id=device_id,
            sensor_id=sensor_id,
            data=data
        ))

    async def get_latest_sensor_data(self, device_id: str, sensor_id: str, minutes_from_now: int, function: str, sorting: str):
        return await self._find_document(self.sensors_collection, {'device_id': device_id, 'sensor_id': sensor_id})

