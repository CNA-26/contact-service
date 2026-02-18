from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import logging

# Configure logging level
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow requests
    allow_methods=["*"],      # Allow all HTTP methods
    allow_headers=["*"],      # Allow all headers
)

# Define the expected structure of the request body
class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

# Endpoint for submitting a contact message
@app.post("/api/contact")
async def contact(data: ContactRequest):
    # prevent empty fields
    if (
        not data.name.strip()
        or not data.subject.strip()
        or not data.message.strip()
    ):
        # Return error if validation fails
        raise HTTPException(status_code=400, detail="Invalid input")

    # Log the contact message
    logging.info(
        f"New contact message | "
        f"Name: {data.name} | "
        f"Email: {data.email} | "
        f"Subject: {data.subject} | "
        f"Message: {data.message}"
    )

    # Return success response to frontend
    return {"success": True}

@app.get("/health")
def health():
    return {"status": "ok"}