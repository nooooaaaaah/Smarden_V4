import argparse
import asyncio
import datetime
import time
from Scripts.deletetables import deleteAllTables, deleteTable
from Scripts.fetchPlants import fetch_all_plants
import Scripts.createTables as createTables

# Define command line arguments
parser = argparse.ArgumentParser(description='CLI Database Migration Utility')

parser.add_argument('--fetch', action='store_true',
                    help='Fetch all plants data')
parser.add_argument('--create-tables', action='store_true',
                    help='Create tables in database')
parser.add_argument('--delete-all-tables', action='store_true',
                    help='drop all tables in database')
parser.add_argument('--delete-table', nargs=1,
                    help='Drop table by name')

args = parser.parse_args()

# CLI Database Migration utility for perennialAPI
print("CLI Database Migration utility for perennialAPI")
print("")

# commands
async def drop_table(table_name):
    print(f"Dropping table with Name: {table_name[0]}")
    deleteTable(table_name[0])
    
async def drop_all_tables():
    print("Dropping all the tables in the DB")
    deleteAllTables()

async def fetch_data():
    curr_time = datetime.datetime.now().strftime("%I:%M %p")
    start_time = time.monotonic()
    print(f"Started fetch and insert. {curr_time}")
    await fetch_all_plants()
    end_time = time.monotonic()
    elapsed_time = end_time - start_time
    elapsed_time = elapsed_time / 60.0
    curr_time = datetime.datetime.now().strftime("%I:%M %p")
    print(f"Data fetched successfully. {curr_time}")
    print(f"It took {elapsed_time}")


async def create_database():
    createTables.create_tables()
    print("Tables created successfully.")

# Run the appropriate function based on command line arguments
if args.fetch:
    asyncio.run(fetch_data())
elif args.create_tables:
    asyncio.run(create_database())
elif args.delete_all_tables:
    asyncio.run(drop_all_tables())
elif args.delete_table:
    asyncio.run(drop_table(args.delete_table))
else:
    print("No command specified. Please specify a command to run.")
    parser.print_help()
