import io
import os
import sqlite3
from contextlib import contextmanager

import numpy as np

# create a default path to connect to and create (if necessary) a database
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'kioku.db')


def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())


def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


sqlite3.register_adapter(np.ndarray, adapt_array)
sqlite3.register_converter("array", convert_array)


@contextmanager
def database(db_path=DEFAULT_PATH):
    conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = lambda c, r: dict(
        zip([col[0] for col in c.description], r))

    yield conn.cursor()

    conn.commit()
    conn.close()


class Face:
    cache = list()

    @classmethod
    def all(cls):
        if not cls.cache:
            cls.load()
        return cls.cache

    @classmethod
    def all_public(cls):
        with database() as db:
            db.execute('SELECT id, name, room, note from faces')
            return db.fetchall()

    @classmethod
    def find(cls, fid: int):
        return next((f for f in cls.all_public() if f["id"] == fid), False)

    @classmethod
    def create(cls, name: str, encoding):
        with database() as db:
            db.execute('INSERT INTO faces (name, encoding) values (?, ?)',
                       (name, encoding))
        cls.load()

    @classmethod
    def update(cls, fid: int, name: str, room: int, note: str):
        query = 'UPDATE faces set name = ?, room = ?, note = ? where id = ?'
        values = (name, room, note, fid)
        with database() as db:
            db.execute(query, values)
        cls.load()
        return cls.find(fid)

    @classmethod
    def load(cls):
        with database() as db:
            db.execute('SELECT * from faces')
            cls.cache = db.fetchall()

    @classmethod
    def create_table(cls):
        with database() as db:
            create_db = """
                CREATE TABLE IF NOT EXISTS faces (
                id INTEGER,
                name VARCHAR,
                room INTEGER,
                note TEXT,
                encoding array,
                PRIMARY KEY (id));
            """
            db.executescript(create_db)
