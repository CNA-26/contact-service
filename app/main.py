from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import tickets

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include ticket routes with /api prefix
app.include_router(tickets.router, prefix="/api")

# Root endpoint with custom welcome message
@app.get("/")
def root():
    return {"message": "Contact/Ticket Service API is running!"}

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}