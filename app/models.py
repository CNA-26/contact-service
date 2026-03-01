from pydantic import BaseModel, EmailStr
from typing import Literal

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str
    ticket_type: Literal["support", "billing", "bug", "general"]

class UpdateStatus(BaseModel):
    status: Literal["open", "in_progress", "resolved", "closed"]