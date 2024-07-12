from kink import inject
from persistance.datastore_postgres import PostgresDataStore
from models.bitarray import BitArray


@inject
class BitArrayDAO:
    def __init__(self, psqlDataStore: PostgresDataStore):
        self.psql = psqlDataStore
        self.create_bitarray_table()
        self.create_mask_table()

    def create_bitarray_table(self) -> bool:
        with self.psql.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('CREATE TABLE IF NOT EXISTS bitarray (id VARCHAR PRIMARY KEY, bitarray BYTEA);')
                conn.commit()
            self.psql.put_connection(conn)
        return True

    def create_mask_table(self) -> bool:
        with self.psql.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('CREATE TABLE IF NOT EXISTS mask (id VARCHAR PRIMARY KEY, mask BYTEA, FOREIGN KEY (id) REFERENCES bitarray(id))')
                conn.commit()
            self.psql.put_connection(conn)
        return True

    def get_bitarray(self, bitarray_id: str) -> BitArray:
        with self.psql.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM bitarray WHERE id = %s', (bitarray_id,))
                row = cur.fetchone()
                self.psql.put_connection(conn)
                if row is None:
                    return None
                return BitArray.decompress(row[1], id=row[0])

    def get_mask(self, mask_id: str) -> BitArray:
        with self.psql.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM mask WHERE id = %s', (mask_id,))
                row = cur.fetchone()
                self.psql.put_connection(conn)
                if row is None:
                    return None
                return BitArray.decompress(row[1], id=row[0])

    def set_bitarray(self, bitarray: BitArray) -> None:
        with self.psql.get_connection() as conn:
            with conn.cursor() as cur:
                compressed = bitarray.compress()
                result = cur.execute('INSERT INTO bitarray VALUES (%s, %s) ON CONFLICT (id) DO UPDATE SET bitarray = %s', (bitarray.id, compressed, compressed))
                conn.commit()
                if result is not None:
                    print(f"Result: {result}")
                    raise Exception("Error inserting bitarray")
                self.psql.put_connection(conn)

    def get_all_bitarrays(self) -> [BitArray]:
        with self.psql.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM bitarray')
                rows = cur.fetchall()
                self.psql.put_connection(conn)
                return [BitArray.decompress(row[1], id=row[0]) for row in rows]

    def set_mask(self, mask: BitArray) -> None:
        with self.psql.get_connection() as conn:
            with conn.cursor() as cur:
                compressed = mask.compress()
                cur.execute('INSERT INTO mask VALUES (%s, %s) ON CONFLICT (id) DO UPDATE SET mask = %s', (mask.id, compressed, compressed))
                conn.commit()
                self.psql.put_connection(conn)
