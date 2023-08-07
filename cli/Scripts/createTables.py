import os
import asyncio
from Data_Objects.dbdo import PlantSpecies, Pests, Hardiness
from Data_Objects.dbdo import Images, ScientificName, Soil, Sunlight, Base, metadata
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
print(f"connection string: {ENGINE}")

Session = sessionmaker(bind=ENGINE)
session = Session()
try:
    Base.metadata.create_all(ENGINE)
except (Exception) as e:
    print(f"\n\terror: {e} \n")