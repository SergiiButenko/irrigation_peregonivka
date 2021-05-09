from pymongo import MongoClient


class Mongo:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client['SensorsDB']
        self.sensors_collection = self.db['sensors']

    def register_sensor_data(self, sensor_id, data):
        self.insert_document(self.sensors_collection, dict(
            sensor_id=sensor_id,
            data=data
        ))

    def get_latest_sensor_data(self, sensor_id):
        return self.find_document(self.sensors_collection, {'sensor_id': sensor_id})

    def insert_document(self, collection, data):
        """ Function to insert a document into a collection and
        return the document's id.
        """
        return collection.insert_one(data).inserted_id

    def find_document(collection, elements, multiple=False):
        """ Function to retrieve single or multiple documents from a provided
        Collection using a dictionary containing a document's elements.
        """
        if multiple:
            results = collection.find(elements)
            return [r for r in results]
        else:
            return collection.find_one(elements)