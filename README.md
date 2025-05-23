<!-- Trigger CI: TEMP -->

# HIPAA-AI-Assistant Backend

A FastAPI-based backend for HIPAA-compliant user management with email verification and TOTP-based MFA.

---

## Environment Variables

### Database
- `DATABASE_URL` — SQLAlchemy database URL (e.g., `postgresql+psycopg2://hipaa_user:your_password_here@db:5432/hipaa_ai`)

### Email Verification
- `SMTP_HOST` — your SMTP server host (e.g. `smtp.sendgrid.net`)
- `SMTP_PORT` — your SMTP port (e.g. `587`)
- `SMTP_USER` — SMTP username
- `SMTP_PASSWORD` — SMTP password
- `EMAIL_FROM` — “from” address for verification emails
- `EMAIL_VERIFY_TOKEN_EXPIRE_SECONDS` — how long the email-verification link is valid (in seconds; default `3600`)

### Multi-Factor Authentication (MFA)
- `MFA_ISSUER` — the issuer name shown in the user’s Authenticator app (default `hipaa-ai-assistant`)

---

## ⚙️ Makefile Commands

| Command         | Description                                 |
|-----------------|---------------------------------------------|
| `make build`    | Build Docker images                         |
| `make dev`      | Run app with hot-reload (local dev)         |
| `make shell`    | Open a bash shell in the backend container  |
| `make test`     | Run all tests via pytest                    |
| `make lint`     | Format code with `black` and check with `flake8` |
| `make check`    | Run Bandit security scan                    |
| `make migrate`  | Apply Alembic DB migrations                 |
| `make down`     | Stop and remove Docker containers/volumes   |

---

## Quick-Start Auth Flow (dev)

1. **Register**

   ```bash
   curl -X POST http://127.0.0.1:8000/auth/register \
     -H 'Content-Type: application/x-www-form-urlencoded' \
     -d 'username=<USER>&password=<PASS>'
   ```

---

## 🛡️ Managing `.env.example`

To keep `.env.example` accurate:

- Always update it when you add a new environment variable to `.env`
- Never include actual secrets — leave values blank or use dummy placeholders
- Keep it in sync with your FastAPI config or `getenv()` usage

### Recommended workflow:

```bash
# After adding new variables to .env:
code .env.example
# Manually copy keys with blank or safe values
```

<!-- CI trigger - safe to remove -->
<!-- test ruleset trigger -->
<!-- final ruleset test -->
