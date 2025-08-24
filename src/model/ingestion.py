import time
from src.tools.mongo_connection import MongoConnection
import random
import Faker
import duckdb


############################################################################################################
# Objetivo é a criação de um processo de injestão de dados em "tempo real" para que use em seguida do dados#
# no monogodb para atualizar a visualização no streamlit.                                                  #
############################################################################################################

conn_duckdb = duckdb.connect()
conn_mongo = MongoConnection()


while True:

    number = random.randint(1,3)

    if number == 1:
        fake = Faker()
        fake_dictionary = {
            "name": fake.name(),
            "age": random.randint(18, 30),
            "email": fake.email(),
            "address": fake.address(),
            "phone": fake.phone_number(),
            "company": fake.company(),
            "Avg. Salary per Year": random.randint(40000, 70000),
            "job": fake.job()
        }

    elif number == 2:
        fake = Faker()
        fake_dictionary = {
            "name": fake.name(),
            "age": random.randint(6, 18),
            "address": fake.address()
        }

    elif number == 3:
        fake = Faker()
        fake_dictionary = {
            "name": fake.name(),
            "age": random.randint(30, 65),
            "email": fake.email(),
            "address": fake.address(),
            "phone": fake.phone_number(),
            "company": fake.company(),
            "Avg. Salary per Year": random.randint(60000, 120000),
            "job": fake.job()
        }

        conn_duckdb.execute("CREATE TABLE pessoas AS SELECT * FROM (SELECT * FROM UNNEST(?))", [fake_dictionary])
        conn_duckdb.from_dicts(fake_dictionary).create("pessoas")

        MongoConnection.writing_data(conn_duckdb.execute("SELECT * FROM pessoas").fetchall_dict())

        time.sleep(60)