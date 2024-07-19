# Flask Web App Tutorial

## Setup & Installation

Make sure you have the latest version of Python installed.

## Database Migration
```bash
alembic revision --autogenerate -m "INSERT COMMENT HERE"
alembic upgrade head
```

# View Components of Database
```bash
sqlite3 instance/database.db
.tables
SELECT * FROM Marble;
```

```bash
git clone <repo-url>
```

```bash
pip install -r requirements.txt
```

## Running The App

```bash
python main.py
```

## Viewing The App

Go to `http://127.0.0.1:5000`
