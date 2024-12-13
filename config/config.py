# config.py
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("POSTGRESQL_HOST")
DB_PORT = os.environ.get("POSTGRESQL_PORT")
DB_NAME = os.environ.get("POSTGRESQL_DBNAME")
DB_USER = os.environ.get("POSTGRESQL_USER")
DB_PASS = os.environ.get("POSTGRESQL_PASSWORD")

SECRET = os.environ.get("POSTGRESQL_PASSWORD")

redis_url = os.environ.get("REDIS_URL")

