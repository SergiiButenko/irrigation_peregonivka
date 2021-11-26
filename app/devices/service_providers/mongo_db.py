from devices.models.devices import SensorValueNSQL
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import DESCENDING, ASCENDING
from devices.config.config import Config


class Mongo:
    def __init__(self):
        self.client = AsyncIOMotorClient(Config.MONGO_DATABASE_URI)
        self.db = self.client.irrigation_db
        self.sensors_collection = self.db.sensors

    async def _insert_document(self, collection, data):
        """Function to insert a document into a collection and
        return the document's id.
        """

        return await collection.insert_one(data.dict())

    async def _transform_sort(self, input_sort):
        SORTING_MAP = {"ASC": ASCENDING, "DESC": DESCENDING}

        new_sort = []
        for _sort in input_sort:
            _new_sort = (_sort[0], SORTING_MAP[_sort[1]])
            new_sort.append(_new_sort)

        return new_sort

    async def _find_document(self, collection, query=None, sorting=None):
        """Function to retrieve single or multiple documents from a provided
        Collection using a dictionary containing a document's query.
        """

        data = []
        cursor = collection.find(query)
        if sorting is not None:
            sorting = await self._transform_sort(sorting)
            cursor.sort(sorting)

        for document in await cursor.to_list(length=500):
            data.append(SensorValueNSQL(**document))

        return data

    async def register_sensor_data(self, component_id, data):
        await self._insert_document(
            self.sensors_collection,
            SensorValueNSQL(component_id=component_id, data=data),
        )

    async def get_latest_sensor_data(
        self, component_id: str, filter: dict = None, sorting: list = None
    ):

        query = {"component_id": component_id, **filter}
        return await self._find_document(
            self.sensors_collection,
            query,
            sorting,
        )


mongo_db = Mongo()
