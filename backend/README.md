# Disease Prediction API - Backend

FastAPI backend for the Symptom-Based Disease Prediction Application.

## Prerequisites

- Python 3.11 or higher
- PostgreSQL database
- uv (Python package manager)

## Installation

### 1. Install uv (if not already installed)

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install Dependencies

```bash
cd backend
uv sync
```

This will create a virtual environment and install all dependencies from `pyproject.toml`.

### 3. Setup Database

Make sure PostgreSQL is running and create the database:

```sql
CREATE DATABASE disease_prediction;
CREATE USER disease_user WITH PASSWORD 'disease_password';
GRANT ALL PRIVILEGES ON DATABASE disease_prediction TO disease_user;
```

### 4. Configure Environment

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env` with your database credentials.

### 5. Run Database Migrations

```bash
uv run alembic upgrade head
```

### 6. Train ML Model

Before running the API, train the ML model:

```bash
python ml/scripts/download_data.py
python ml/scripts/preprocess_data.py
python ml/scripts/train_model.py
```

## Running the Application

### Development Mode

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once the server is running, visit:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── api/              # API routes
│   ├── core/             # Core configuration
│   ├── db/               # Database setup
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   └── ml/               # ML integration
├── tests/                # Test files
├── alembic/              # Database migrations
└── pyproject.toml        # Project dependencies
```

## Testing

```bash
uv run pytest
```

## Common Commands

**Add a new dependency:**
```bash
uv add package-name
```

**Add a dev dependency:**
```bash
uv add --dev package-name
```

**Update dependencies:**
```bash
uv sync
```

**Run scripts:**
```bash
uv run python script.py
```

