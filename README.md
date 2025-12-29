# FastAPI CRUD API

A lightweight FastAPI project demonstrating a protected CRUD API with filtering, pagination, and SQLite persistence. Every endpoint is secured by an API key provided via the `X-API-Key` header. The project includes logging to console and file, plus basic pytest coverage using `httpx` against the ASGI app.

## Features
- FastAPI app with automatic Swagger UI at `/docs` and Redoc at `/redoc`.
- CRUD operations for `Item` resources with pagination, price filters, and name search.
- SQLite database via SQLAlchemy ORM.
- API-key security using the `X-API-Key` header (defaults to `change-me`).
- Logging to console and `logs/app.log`.
- Pytest-based integration tests using an in-process ASGI client.

## Requirements
- Python 3.9+
- Dependencies listed in `requirements.txt`.

## Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Create a `.env` file if you want to override defaults:
```
API_KEY=change-me
DATABASE_URL=sqlite:///./items.db
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

## Running the app
```bash
uvicorn main:app --reload
```

The API documentation will be available at `http://127.0.0.1:8000/docs`.

## Entity schema
`Item` fields:
- `id` (int, primary key)
- `name` (string, required)
- `description` (string, optional)
- `price` (float, non-negative)
- `created_at` (datetime)
- `in_stock` (boolean)

## Curl examples
> Replace `CHANGE_ME_KEY` with your API key (default `change-me`).

### Create an item
```bash
curl -X POST "http://127.0.0.1:8000/items" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: CHANGE_ME_KEY" \
  -d '{"name": "Keyboard", "description": "Mechanical", "price": 99.99, "in_stock": true}'
```

### List items with pagination and filters
```bash
# Simple list
curl "http://127.0.0.1:8000/items?limit=5&offset=0" -H "X-API-Key: CHANGE_ME_KEY"

# Filter by minimum price
curl "http://127.0.0.1:8000/items?min_price=50" -H "X-API-Key: CHANGE_ME_KEY"

# Filter by maximum price
curl "http://127.0.0.1:8000/items?max_price=150" -H "X-API-Key: CHANGE_ME_KEY"

# Search by name
curl "http://127.0.0.1:8000/items?q=board" -H "X-API-Key: CHANGE_ME_KEY"
```

### Get item by ID
```bash
curl "http://127.0.0.1:8000/items/1" -H "X-API-Key: CHANGE_ME_KEY"
```

### Update an item
```bash
curl -X PUT "http://127.0.0.1:8000/items/1" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: CHANGE_ME_KEY" \
  -d '{"price": 120.00, "in_stock": false}'
```

### Delete an item
```bash
curl -X DELETE "http://127.0.0.1:8000/items/1" -H "X-API-Key: CHANGE_ME_KEY"
```

## Running tests
```bash
pytest
```

Tests spin up the FastAPI app in-process via `httpx`, create an item, and assert it appears in the list endpoint.
