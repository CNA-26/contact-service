from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import logging
import psycopg2
from psycopg2 import pool
from contextlib import closing
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in environment")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create a simple connection pool (min 1, max 5 connections)
try:
    db_pool = psycopg2.pool.SimpleConnectionPool(
        1, 5, dsn=DATABASE_URL
    )
except Exception as e:
    logging.error(f"Error creating connection pool: {e}")
    raise

app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for contact requests
class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

# Endpoint for submitting contact messages
@app.post("/api/contact")
async def contact(data: ContactRequest):
    # Validate input
    if not data.name.strip() or not data.subject.strip() or not data.message.strip():
        raise HTTPException(status_code=400, detail="Invalid input")

    # Log the message
    logging.info(
        f"New contact message | Name: {data.name} | Email: {data.email} | "
        f"Subject: {data.subject} | Message: {data.message}"
    )

    # Insert into database using connection pool and context manager
    try:
        conn = db_pool.getconn()
        with closing(conn):
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO contact_messages (name, email, subject, message)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (data.name.strip(), data.email, data.subject.strip(), data.message.strip())
                )
            conn.commit()
    except Exception as e:
        logging.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        if conn:
            db_pool.putconn(conn)

    return {"success": True}

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}