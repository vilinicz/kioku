import sqlite3
import numpy as np
import io
import os


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

    cursor.execute('INSERT INTO faces (name, encoding) values (?, ?)', (name, encoding))

    conn.commit()
    conn.close()


def faces():
    conn = connect()
    conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
    cursor = conn.cursor()

    cursor.execute('SELECT * from faces')
    data = cursor.fetchall()

    conn.commit()
    conn.close()

    return data


def faces_public():
    conn = connect()
    conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
    cursor = conn.cursor()

    cursor.execute('SELECT id, name from faces')
    data = cursor.fetchall()

    conn.commit()
    conn.close()

    return data