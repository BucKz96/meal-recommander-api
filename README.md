# Meal Recommender API

A Flask-based REST API that allows you to manage and retrieve meals from a PostgreSQL database, with future support for meal recommendations based on available ingredients.

---

## Features

- CRUD endpoints for managing meals
- CSV import of meals
- Ingredient-based structure (for future recommendation logic)
- RESTful API with Flask
- PostgreSQL database via SQLAlchemy
- Fully containerized with Docker and Docker Compose
- Unit tests with Pytest
- GitHub Actions CI pipeline

---

## Tech Stack

- Python 3.12
- Flask
- SQLAlchemy + Flask-Migrate
- PostgreSQL
- Docker / Docker Compose
- Pytest
- GitHub Actions

---

## Project Structure

```
.
├── Dockerfile
├── docker-compose.yml
├── run.py
├── requirements.txt
├── README.md
├── data/
│   ├── meals.csv
│   └── test_meals.csv
├── meal_app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   └── meal.py
│   ├── routes/
│   │   └── meals.py
│   └── utils/
└── tests/
    ├── conftest.py
    ├── test_meals_get.py
    ├── test_meals_post.py
    ├── test_meals_import.py
```

---

## Installation & Usage

### 1. Clone the repository

```bash
git clone https://github.com/BucKz96/meal-recommander-api.git
cd meal-recommander-api
```

### 2. Start the application with Docker

```bash
docker-compose up --build
```

This will:
- Build the Flask API container
- Set up a PostgreSQL container
- Apply migrations

The API will be available at: `http://localhost:5000`

---

## API Endpoints

### `GET /meals`
Returns a list of all meals.

**Example Request:**
```http
GET /meals HTTP/1.1
Host: localhost:5000
```

**Example Response:**
```json
[
  {
    "id": 1,
    "name": "Spaghetti Bolognese",
    "description": "Classic Italian pasta dish with meat sauce",
    "ingredients": ["pasta", "beef", "tomato"]
  },
  {
    "id": 2,
    "name": "Caesar Salad",
    "description": "Salad with romaine lettuce, croutons, and Caesar dressing",
    "ingredients": ["lettuce", "croutons", "parmesan"]
  }
]
```

---

### `GET /meals/<id>`
Returns a specific meal by ID.

**Example Request:**
```http
GET /meals/1 HTTP/1.1
Host: localhost:5000
```

**Example Response:**
```json
{
  "id": 1,
  "name": "Spaghetti Bolognese",
  "description": "Classic Italian pasta dish with meat sauce",
  "ingredients": ["pasta", "beef", "tomato"]
}
```

---

### `POST /meals`
Adds a new meal. Expects a JSON payload with the following fields:

```json
{
  "name": "Veggie Curry",
  "description": "Spicy vegetable curry with coconut milk",
  "ingredients": ["potato", "carrot", "coconut milk"]
}
```

**Response:**
```json
{
  "message": "Meal created successfully",
  "id": 3
}
```

---

### `POST /meals/import_csv`
Bulk import meals from a CSV file (`meals.csv` located in `/data`).

**Response:**
```json
{
  "message": "20 meals imported successfully"
}
```

---

## Future Endpoint (Planned)

### `POST /recommend`
Returns a list of meals based on available ingredients.

**Example Request:**
```json
{
  "ingredients": ["pasta", "tomato", "cheese"]
}
```

**Expected Response:**
```json
{
  "recommended_meals": [
    {
      "id": 4,
      "name": "Tomato Pasta Bake",
      "match_score": 0.85
    },
    {
      "id": 5,
      "name": "Cheesy Lasagna",
      "match_score": 0.78
    }
  ]
}
```

---

## Environment Variables

These are configured via `meal_app/config.py`, typically injected via Docker:

- `SQLALCHEMY_DATABASE_URI`
- `FLASK_ENV`
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`

---

## Running Tests

To run tests inside the Docker container:

```bash
docker-compose exec web pytest
```

Tests are located in the `tests/` directory and use `Pytest`.

---

## Continuous Integration

GitHub Actions is configured to run tests on every push to `main`, `dev`, and feature branches. The workflow is defined in:

```yaml
.github/workflows/test.yml
```

---

## Roadmap

- [x] Base API setup
- [x] CRUD endpoints
- [x] CSV import
- [x] Pytest + CI
- [ ] Ingredient-based meal recommendation with AI
- [ ] Interactive web interface for meal exploration and suggestions
- [ ] Data analytics and visualizations (ingredient usage, meal popularity, etc.)

---

## License

This project is licensed under the MIT License.
