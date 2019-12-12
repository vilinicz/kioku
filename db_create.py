#!/usr/bin/env python3

import db

with db.database() as db:
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
