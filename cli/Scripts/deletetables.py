from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import create_engine, MetaData, Table, inspect
from dotenv import load_dotenv
import logging
import os

logging.basicConfig(filename='Errors.log', level=logging.DEBUG)

load_dotenv()
# Connecting
CONNECTION_PARAMS = {
    'host': os.environ.get('HOST'),
    'port': int(os.environ.get('PORT')),
    'database': os.environ.get('DATABASE'),
    'user': os.environ.get('USER'),
    'password': os.environ.get('PASSWORD')
}
API_Key = os.environ.get('API_KEY')
ENGINE = create_engine(
    f'postgresql://{CONNECTION_PARAMS["user"]}:{CONNECTION_PARAMS["password"]}@{CONNECTION_PARAMS["host"]}:{CONNECTION_PARAMS["port"]}/{CONNECTION_PARAMS["database"]}')

METADATA = MetaData()


def deleteAllTables():
    try:
        with ENGINE.connect() as conn:
            inspector = inspect(conn)
            tables = inspector.get_table_names()
            for table in tables:
                print("not doing anything atm")
                # ENGINE.execute(table.delete())
        print("Dropped all tables")
    except(Exception) as e:
        logging.debug(e)
        print(f'error: {e}')

def deleteTable(table_name):
    METADATA.reflect(bind=ENGINE)
    try:
        table = METADATA.tables.get(table_name)
        # print("not doing anything atm")
        table.drop(bind=ENGINE)
        print(f"Dropped Table: {table}")
    except(Exception) as e:
        logging.debug(e)
        print(f'error: {e}')


