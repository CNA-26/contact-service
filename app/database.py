import os
import logging
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in environment")

logging.basicConfig(level=logging.INFO)

# Create a connection pool
try:
    db_pool = psycopg2.pool.SimpleConnectionPool(1, 5, dsn=DATABASE_URL)
except Exception as e:
    logging.error(f"Error creating connection pool: {e}")
    raise