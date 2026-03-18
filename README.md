# Python Frameworks

FastAPI CRUD application for managing products. The project provides both server-rendered HTML pages and JSON API endpoints, using SQLite for storage.

## Stack

- FastAPI
- SQLAlchemy
- Jinja2
- SQLite
- Uvicorn

## Product Fields

Each product contains:

- `name`
- `price`
- `quantity`
- `category`

## Run With `uv`

This project uses `uv` only.

1. Install dependencies:

```bash
uv sync
```

2. Start the development server:

```bash
uv run uvicorn app.main:app --reload
```

3. Open the app:

- HTML interface: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`

## API Endpoints

- `GET /api/products`
- `GET /api/products/{product_id}`
- `POST /api/products`
- `PUT /api/products/{product_id}`
- `DELETE /api/products/{product_id}`

## Notes

- The SQLite database file `app.db` is created automatically on first run.
- Tables are created automatically when the application starts.
