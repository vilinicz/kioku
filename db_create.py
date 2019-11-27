#!/usr/bin/env python3

import db

conn = db.connect()

cur = conn.cursor()

create_db = """
CREATE TABLE faces (
    id INTEGER,
    name VARCHAR,
    encoding array,
    PRIMARY KEY (id));
"""

cur.executescript(create_db)

conn.commit()
conn.close()