#!/usr/bin/env python3

from db import database

with database() as db:
    create_db = """
        CREATE TABLE faces (
        id INTEGER,
        name VARCHAR,
        room INTEGER,
        note TEXT,
        encoding array,
        PRIMARY KEY (id));
    """
    db.executescript(create_db)
