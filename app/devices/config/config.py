import os


class Config:
    PSQL_DATABASE_URI = os.environ['PSQL_DATABASE_URI']
    MONGO_DATABASE_URI = os.environ['MONGO_DATABASE_URI']
    SCENARIOS_PATH = os.path.join('devices', 'scenarios_library')
