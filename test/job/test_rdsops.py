# Standars library imports
import asyncio
import logging
import sys

# Third-party library imports
import psycopg
import pytest
import sqlalchemy
from testcontainers.postgres import PostgresContainer

# Testing related imports
from src.include.rdsops import RDSOps

handler_print = logging.StreamHandler(sys.stdout)
handler_print.setLevel(logging.INFO)
for

def get_stmt(filename):
    with open(filename) as f:
        contents = f.read()
    return contents


async def initialize_database(db_name,
                              usern,
                              passwd,
                              db_host,
                              db_port,
                              schema_name_mig):
    try:
        conn = psycopg.connect(database=db_name,
                               user=usern,
                               password=passwd,
                               host=db_host,
                               port=db_port,
                               options=f'-c search_path={schema_name_mig}')
        cur = conn.cursor()

        create_role = 'CREATE ROLE ' + 'data_store_role' + ' WITH ADMIN ' + usern + ';'
    except Exception as E:
        raise E


