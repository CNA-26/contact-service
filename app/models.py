from pydantic import BaseModel, EmailStr
from typing import Literal, Optional

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str
    ticket_type: Literal["support", "billing", "bug", "general"]
    priority: Optional[Literal["low", "normal", "high"]] = "normal"

class UpdateStatus(BaseModel):
    status: Literal["open", "in_progress", "resolved", "closed"]