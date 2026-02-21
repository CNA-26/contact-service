# Contact Service

## Beskrivning
Backend för kontaktformuläret. Tar emot namn, e-post, ämne och meddelande och sparar dem i en PostgreSQL-databas.

Base URL: http://contact-service-rasanjim-traskelr-contact-service.2.rahtiapp.fi/

---

## Funktioner
- Ta emot kontaktformulär (`name`, `email`, `subject`, `message`)  
- Validerar input (inga tomma fält, giltig e-postadress)  
- Sparar meddelanden i PostgreSQL  
- Loggar alla inkommande meddelanden  
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
  }'
```