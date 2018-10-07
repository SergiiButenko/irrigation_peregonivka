import psycopg2
import psycopg2.extras
import logging

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)


class Database(object):
    """docstring for Database"""
    HOST = '127.0.0.1'
    DB = 'irrigation'
    USER = 'postgres'
    PASSWORD = 'postgres'
    PORT = 5467

    def __init__(self, arg):
        super(Database, self).__init__()
        self.arg = arg
        self.connection = self._connect()

    def _connect():
        conn = None
        try:
            conn = psycopg2.connect(dbname=DB, user=USER, host=HOST, password=PASSWORD)
        except Exception as e:
            logging.error("Unable to connect to database")
            logging.exception(e)
            raise e

        return conn

    def select(self, query, values=None, method="fetchall"):
        """Use this method in case you need to get info from database."""

        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            # execute our Query
            cursor.execute(query) if values is None else cursor.execute(query, values)

            logging.debug("db request '{}' executed".format(cursor.statement))
            return getattr(cursor, method)()
        except Exception as e:
            logging.exception(e)
            logging.error(
                "Error while performing operation with database. Query: '{}'".format(
                    query
                )
            )
            raise e

    # executes query and returns fetch* result
    def update(self, query, values=None):
        """Doesn't have fetch* methods. Returns lastrowid after database insert command."""
        lastrowid = -1
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            # execute our Query
            cursor.execute(query) if values is None else cursor.execute(query, values)

            self.connection.commit()
            logging.debug("db request '{0}' executed".format(cursor.statement))
            lastrowid = cursor.fetchone()[0]

            return lastrowid
        except Exception as e:
                logging.exception(e)
                logging.error(
                    "Error while performing operation with database. Query: '{}'".format(
                        query
                    )
                )
                raise e

    def get_next_active_rule(line_id):
        """Return nex active rule."""
        query = """SELECT * rules_line rl
        """


        'SELECT l.id, l.line_id, l.rule_id, l.timer as "[timestamp]", l.interval_id, l.time, li.name '
                "FROM life AS l, lines as li "
                "WHERE l.state = 1 AND l.active=1 AND l.line_id=%s AND li.number = l.line_id AND timer>=datetime('now', 'localtime', '-30 seconds') "
                "ORDER BY timer LIMIT 1"
        res = select(query, values=(line_id,), "fetchone")
        if res is None:
            return None

        logging.debug("Next active rule retrieved for line id {}".format(line_id))

        return {
            "id": res[0],
            "line_id": res[1],
            "rule_id": res[2],
            "user_friendly_name": res[6],
            "timer": res[3],
            "interval_id": res[4],
            "time": res[5],
        }
