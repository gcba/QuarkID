import psycopg2 as pg
import psycopg2.pool
import sys


class PostgresDataStore():
    def __init__(self, dbname: str, dbuser: str, dbpassword: str, dbhost: str, dbport: str):
        self.dbname = dbname
        self.dbuser = dbuser
        self.dbpassword = dbpassword
        self.dbhost = dbhost
        self.dbport = dbport
        self.pool = None

    def init_connections(self, minconn: int = 1, maxconn: int = 3) -> None:
        try:
            self.pool = pg.pool.ThreadedConnectionPool(minconn=minconn, maxconn=maxconn, database=self.dbname, user=self.dbuser, password=self.dbpassword, host=self.dbhost, port=self.dbport)
            return True
        except Exception:
            print("Unable to connect to postgres", file=sys.stderr)
            return False

    def get_connection(self):
        return self.pool.getconn()

    def put_connection(self, conn):
        self.pool.putconn(conn)
