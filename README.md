# Contact/Ticket Service

## Beskrivning
Backend för ett kontakt- och ärendehanteringssystem. Tar emot kontaktförfrågningar, kategoriserar dem som ärenden och lagrar dem i en PostgreSQL-databas.

Base URL: http://contact-service-rasanjim-traskelr-contact-service.2.rahtiapp.fi/

---

## Funktioner
- Ta emot ärenden via kontaktformulär (`name`, `email`, `subject`, `message`, `ticket_type`)  
- Validerar input (inga tomma fält, giltig e-postadress)  
- Sparar ärenden i PostgreSQL  
- Loggar alla inkommande ärenden  
- Lista ärenden med filtrering (`status`, `ticket_type`)  
- Stöd för paginering (`page`, `limit`)  
- Uppdatera ärendestatus (`open`, `in_progress`, `resolved`, `closed`)  
- Ta bort ärenden
- Hälsokontroll via `/health`  
- Stöder CORS för frontend

---

## Körning lokalt

### Installera beroenden:  
```powershell
pip install fastapi uvicorn psycopg2-binary python-dotenv "pydantic[email]"
```

### Sätt `DATABASE_URL` i .env
```python
# Exempel
DATABASE_URL="postgres://username:password@host:port/dbname?sslmode=require"
```

### Starta backend
```powershell
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testa API

#### Hälsokontroll
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -Method GET
```

#### Skicka ett testmeddelande
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/contact" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{
    "name": "Alice",
    "email": "alice@example.com",
    "subject": "Test",
    "message": "Hej från lokalt test!"
    "ticket_type": "general"
  }'
```