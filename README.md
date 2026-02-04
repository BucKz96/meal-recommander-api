# Meal Recommender API

Meal Recommender API is a FastAPI service and Streamlit client that match available ingredients with curated recipes. The project was built as a personal showcase and is engineered like a production service: strict typing, exhaustive automated tests, Docker images, and a modern user interface with client-side favorites and search history.

---

## Highlights

- Incremental fuzzy matching on ingredients with deterministic scoring and nutrition metadata for every recipe
- Preloading pipeline backed by HuggingFace and TheMealDB, cached in memory with TTL control and rate limiting at the edge
- Streamlit interface with theme toggle, debounced search form, favorites, and searchable filters (cuisine, name, cap on results)
- Observability baked in: health/readiness probes, structured logging via structlog, and cache statistics exposed though the API
- Reproducible toolchain powered by `pyproject.toml`, Ruff, MyPy, pytest, and multi-stage Docker images for the API and Streamlit front-end

---

## Architecture Overview

```mermaid
graph TB
    subgraph Client
        ST[Streamlit UI]
    end

    subgraph API Layer
        F[FastAPI]
        MW[Middlewares\n(CORS, Rate Limiting, Logging)]
        RT[Routes\n/meals • /health • /ready]
    end

    subgraph Core
        CFG[Pydantic Settings]
        LOG[Structlog]
        CACHE[In-memory Cache]
    end

    subgraph Services
        DL[Data Loader\nHuggingFace/TheMealDB]
        REC[Recommender]
    end

    subgraph Data
        CSV[(recipes_clean.csv)]
    end

    ST -->|REST| F --> MW --> RT --> REC
    REC --> CACHE
    REC --> DL --> CSV
```

---

## Getting Started

### Requirements

- Python 3.11+
- Docker (optional) for local orchestration
- Make is recommended for the provided shortcuts

### Local environment

```bash
git clone https://github.com/BucKz96/meal-recommander-api.git
cd meal-recommander-api

python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# Run FastAPI
make run-api

# Run Streamlit client in another terminal
make run-streamlit
```

Configure the service by duplicating `.env.example`:

```bash
cp .env.example .env
# Adjust dataset source, cache TTL, or rate limit before starting
```

### Docker Compose

```bash
docker-compose up --build

# API:       http://localhost:8000
# Streamlit: http://localhost:8501
# Swagger:   http://localhost:8000/docs
```

Both images are built with multi-stage Dockerfiles (see `docker/api` and `docker/streamlit`) and run as non-root users.

---

## API Overview

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET | `/` | Welcome payload with service metadata |
| GET | `/meals/by-ingredients` | Main recommender endpoint with optional `limit` |
| GET | `/meals/all` | Raw dataset explorer, filterable by cuisine |
| GET | `/meals/sample` | Sample payload for demos/tests |
| GET | `/health` | Health probe exposing cache stats |
| GET | `/ready` | Readiness probe used by Render/Kubernetes |

Example request:

```bash
curl "http://localhost:8000/meals/by-ingredients?available_ingredients=chicken&available_ingredients=rice&limit=10"
```

```json
[
  {
    "name": "Chicken Fried Rice",
    "ingredients": ["chicken", "rice", "eggs", "soy sauce"],
    "cuisine": "asian",
    "nutritions": {
      "calories": 450.5,
      "protein": 32.1,
      "fat": 12.3,
      "carbohydrates": 58.2
    },
    "prep_time": "30 minutes or less"
  }
]
```

Swagger UI and ReDoc are automatically available (`/docs` and `/redoc`).

---

## Streamlit Client

The Streamlit app mirrors the API capabilities and adds client-side niceties:

- Debounced ingredients form with cached responses and API error handling
- Filters for free-text search, cuisine, and maximum number of cards
- Details panel with nutrition badge, responsive layout, and inline animations
- Favorites persisted in session state and a searchable history sidebar so repeated queries are one click away
- Theme toggle wired to CSS variables used across the UI for a consistent light/dark experience

Launch it locally with `make run-streamlit` or through Docker Compose. The default UI intentionally waits for the first submission to avoid preloading thousands of recipes on load.

---

## Quality Gates

```bash
# Linters and typing
make lint            # Ruff + MyPy

# Formatting
make format

# Tests
make test            # Pytest (unit + integration)
make test-cov        # Pytest with coverage + HTML report
```

Tests rely on fixtures and extensive mocking to avoid network calls. Coverage stays above 80%, and cache/stateless services are validated through dedicated unit tests.

---

## Tech Stack

| Area | Tools |
| ---- | ----- |
| API | FastAPI, Pydantic v2, Structlog, SlowAPI |
| Data | Pandas, Requests, Tenacity (retry/backoff) |
| Front-end | Streamlit, Plotly for charts, custom CSS |
| Tooling | Pytest, Ruff, MyPy, Make, Docker, GitHub Actions |

---

## Roadmap

- Short term: JWT authentication, persistent favorites, and pagination
- Mid term: PostgreSQL storage and scheduled data refresh jobs
- Long term: Collaborative filtering model and weekly meal plans directly in the UI

---

## Project Layout

```
meal-recommander-api/
├── src/
│   ├── api/          # FastAPI entrypoint, routes, middlewares
│   ├── core/         # Config, logging, custom exceptions
│   ├── models/       # Pydantic schemas
│   └── services/     # Cache, data loader, recommender
├── streamlit_app/    # Streamlit UI modules (main, favorites, history, theme)
├── tests/            # Unit + integration suites
├── docker/           # API and Streamlit Dockerfiles
├── data/             # Cached CSV datasets
├── pyproject.toml    # Dependencies + tooling config
└── Makefile          # Developer shortcuts
```

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Maintainer

**Maxime L.** – [@BucKz96](https://github.com/BucKz96)
