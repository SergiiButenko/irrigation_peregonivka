from databases import Database
from devices.config.config import Config

psql_db = Database(Config.PSQL_DATABASE_URI)
