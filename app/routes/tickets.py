from fastapi import APIRouter, HTTPException, Query
from database import db_pool
from models import ContactRequest, UpdateStatus
import logging
from typing import Optional

router = APIRouter()


# Create a new ticket

@router.post("/contact")
async def create_ticket(data: ContactRequest):
    # Basic input validation
    if not data.name.strip() or not data.subject.strip() or not data.message.strip():
        raise HTTPException(status_code=400, detail="Invalid input")

    conn = None
    try:
        conn = db_pool.getconn()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO contact_messages
                (name, email, subject, message, ticket_type, priority)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    data.name.strip(),
                    data.email,
                    data.subject.strip(),
                    data.message.strip(),
                    data.ticket_type,
                    data.priority
                )
            )
        conn.commit()
        logging.info(f"New Ticket | {data.ticket_type} | {data.email} | Priority: {data.priority}")
    finally:
        if conn:
            db_pool.putconn(conn)

    return {"success": True}



# Get tickets with optional filtering and pagination

@router.get("/tickets")
def get_tickets(
    status: Optional[str] = Query(None, description="Filter by status"),
    ticket_type: Optional[str] = Query(None, description="Filter by ticket_type"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1)
):
    offset = (page - 1) * limit
    conn = None
    try:
        conn = db_pool.getconn()
        with conn.cursor() as cursor:
            query = """
                SELECT id, name, email, subject, message, ticket_type, status, priority, created_at
                FROM contact_messages
                WHERE 1=1
            """
            params = []

            if status:
                query += " AND status = %s"
                params.append(status)
            if ticket_type:
                query += " AND ticket_type = %s"
                params.append(ticket_type)

            # Add pagination
            query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])

            cursor.execute(query, params)
            rows = cursor.fetchall()

            tickets = []
            for row in rows:
                tickets.append({
                    "id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "subject": row[3],
                    "message": row[4],
                    "ticket_type": row[5],
                    "status": row[6],
                    "priority": row[7],
                    "created_at": row[8].isoformat() if row[8] else None
                })
        return {"tickets": tickets, "page": page, "limit": limit}
    finally:
        if conn:
            db_pool.putconn(conn)



# Update ticket status

@router.patch("/tickets/{ticket_id}")
def update_ticket_status(ticket_id: int, data: UpdateStatus):
    conn = None
    try:
        conn = db_pool.getconn()
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE contact_messages SET status = %s WHERE id = %s",
                (data.status, ticket_id)
            )
            # Check if ticket exists
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Ticket not found")
        conn.commit()
        return {"success": True, "ticket_id": ticket_id, "new_status": data.status}
    finally:
        if conn:
            db_pool.putconn(conn)


# Delete a ticket

@router.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int):
    conn = None
    try:
        conn = db_pool.getconn()
        with conn.cursor() as cursor:
            # Delete ticket from database
            cursor.execute(
                "DELETE FROM contact_messages WHERE id = %s",
                (ticket_id,)
            )
            # Check if ticket exists
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Ticket not found")
        conn.commit()
        return {"success": True, "ticket_id": ticket_id}
    finally:
        if conn:
            db_pool.putconn(conn)