# DataMatrix Auth Backend

FastAPI backend for desktop app login, session tokens, login event logging, and Telegram notifications.

## Features

- username/password login
- PostgreSQL-ready SQLAlchemy models
- 7-day access token support
- 3-day offline grace value returned to the client
- login event logging
- Telegram notification on successful login
- Render deployment scaffold

## Local setup

1. Create a virtual environment
2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env`
4. Fill in:
- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `ADMIN_API_KEY`

5. Run:

```powershell
uvicorn app.main:app --reload
```

Convenience scripts:

- [create_env.bat](C:/Users/ops03.ru/Documents/New%20project/datamatrix-auth-backend/create_env.bat)
- [run_backend.bat](C:/Users/ops03.ru/Documents/New%20project/datamatrix-auth-backend/run_backend.bat)
- [seed_user.bat](C:/Users/ops03.ru/Documents/New%20project/datamatrix-auth-backend/seed_user.bat)

## Key endpoints

- `GET /health`
- `POST /login`
- `POST /validate-token`
- `POST /admin/create-user`

## Create the first user

Local CLI helper:

```powershell
python create_user.py your_username your_password "Full Name"
```

Or via API:

```powershell
Invoke-RestMethod -Method Post -Uri "https://your-render-service.onrender.com/admin/create-user" `
  -Headers @{ "x-api-key" = "YOUR_ADMIN_API_KEY" } `
  -ContentType "application/json" `
  -Body '{"username":"user1","password":"temp123","full_name":"User One"}'
```

## Render notes

- Set the same values from `.env` as Render environment variables
- Point `DATABASE_URL` to your Render Postgres connection string
- Keep `JWT_SECRET_KEY`, Telegram token, and database credentials private
- Required Render env vars:
  - `DATABASE_URL`
  - `JWT_SECRET_KEY`
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_CHAT_ID`
  - `ADMIN_API_KEY`

## First deployment checklist

1. Push this folder to your GitHub repo
2. Create a Render web service from that repo
3. Add the required env vars in Render
4. Deploy
5. Create your first user with the local CLI or the protected API
6. Put the Render service URL into the desktop app `Auth server` setting
