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
formatter = logging.Formatter("%(asctime)s %(levelname)s - %(message)s")
handler_print.setFormatter(formatter)

log = logging.getLogger("RDS_TEST")
log.addHandler(handler_print)
log.setLevel(logging.info)

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

        role = 'data_store_role'
        create_role = 'CREATE ROLE ' + role + ' WITH ADMIN ' + usern + ';'
        log.info("Create role: " + create_role)
        cur.execute()
        log.info(f'Role {role} created successfully!')

        schema = 'data_store'
        create_schema = 'CREATE SCHEMA IF NOT EXISTS ' + 'data_store' + ' AUTHORIZATION ' + role + ' ;'
        log.info("Create SCHEMA: " + create_schema)
        cur.execute()
        log.info(f'Schema {schema} created successfully!')

        mock_create_scripts_paths = ['test/mocks/create_file_audit.sql']
        for create_script in mock_create_scripts_paths:
            create_table = get_stmt(create_script)
            cur.execute(create_table)
        log.info(f'Tables created successfully!')

        # Insert scripts as/if needed
        log.info(f'No insert scripts defined yet. Nothing to INSERT.')

        cur.close()
        conn.commit()
        conn.close() 
        
    except Exception as err:
        log.info(f"Oops! An error has occured: {err}")
        log.info(f"Exception type:  {type(err)}")
        exit(err)

def start_postgres_container(datastore, user_name, pass_nm):
    postgres_container = PostgresContainer('postgres:15',
                                           port=5432,
                                           user=user_name,
                                           password=pass_nm,
                                           dbname=datastore)
    postgres_container.start()
    # postgres_container.with_bind_ports(5432)
    db_url = postgres_container.get_connection_url()
    db_port = postgres_container.get_exposed_port()
    db_host = postgres_container. get_container_host_ip()

    print('DB created for testing')
    print('HOST: ' + db_host)
    print('PORT: ' + db_port)
    print('URL: ' + db_url)

    db_uri = f"postgresql://admin:secret@{db_host}:{db_port}/{datastore}"

    with postgres_container as postgres:
        engine = sqlalchemy.create_engine(db_uri,
                                          connect_args={'options': '-csearch_path={}'.format('initial')}:)


