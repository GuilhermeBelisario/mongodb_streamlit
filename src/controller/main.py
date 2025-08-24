from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from src.tools.mongo_connection import MongoConnection

# Connect to an in-memory MongoDB database
engine = create_engine("mongodb:///:memory:")

# Define a metadata object
metadata = MetaData()

conn_mongodb = MongoConnection.connect()

# Define the 'users' table
users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("email", String(100)),
)

# Create the table in the database
metadata.create_all(engine)
