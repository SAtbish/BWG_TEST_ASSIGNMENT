"""
CREATE TABLE currency_pairs (id SERIAL PRIMARY KEY, symbol VARCHAR NOT NULL, price FLOAT NOT NULL, time TIMESTAMP NOT NULL);
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        "CREATE TABLE currency_pairs ("
        "id SERIAL PRIMARY KEY, "
        "symbol VARCHAR NOT NULL, "
        "price FLOAT NOT NULL, "
        "time TIMESTAMP NOT NULL"
        ");"
    )
]
