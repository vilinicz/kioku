import io
import os
import sqlite3

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


def connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    return con


def insert(name, encoding):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO faces (name, encoding) values (?, ?)',
                   (name, encoding))

    conn.commit()
    conn.close()


def update_face(fid, name):
    conn = connect()
    cursor = conn.cursor()

    query = """UPDATE faces set name = ? where id = ?"""
    values = (fid, name)
    cursor.execute(query, values)
    conn.commit()
    conn.close()


def faces():
    conn = connect()
    conn.row_factory = lambda c, r: dict(
        zip([col[0] for col in c.description], r))
    cursor = conn.cursor()

    cursor.execute('SELECT * from faces')
    data = cursor.fetchall()
    conn.commit()
    conn.close()

    return data


def faces_public():
    conn = connect()
    conn.row_factory = lambda c, r: dict(
        zip([col[0] for col in c.description], r))
    cursor = conn.cursor()

    cursor.execute('SELECT id, name from faces')
    data = cursor.fetchall()
    conn.commit()
    conn.close()

    return data


class Face:
    cache = list()

    @classmethod
    def all(cls):
        if not cls.cache:
            cls.load()
        return cls.cache

    @classmethod
    def all_public(cls):
        return faces_public()

    @classmethod
    def find(cls, fid: int):
        return next((f for f in cls.all_public() if f["id"] == fid), False)

    @classmethod
    def create(cls, name: str, encoding):
        insert(name, encoding)
        cls.load()

    @classmethod
    def update(cls, fid: int, name: str):
        update_face(fid, name)

    @classmethod
    def load(cls):
        cls.cache = faces()
