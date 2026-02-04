# Fonctionnalités détaillées

## Algorithme de recommandation

Le moteur de recommandation utilise un scoring basé sur le nombre d'ingrédients correspondants :

1. **Normalisation** - Tous les ingrédients sont convertis en minuscules et trimés
2. **Matching partiel** - "chicken" match avec "chicken breast", "chicken thigh", etc.
3. **Scoring** - Chaque recette reçoit un score = nombre d'ingrédients trouvés
4. **Tri** - Résultats triés par score décroissant
5. **Filtrage** - Seules les recettes avec au moins 1 match sont retournées

Exemple : recherche `["chicken", "rice", "tomato"]`
- "Chicken Rice Tomato" → score 3 (premier)
- "Chicken Rice" → score 2 (deuxième)
- "Chicken Curry" → score 1 (troisième)

## Système de cache

Cache mémoire TTL (Time To Live) implémenté avec threading.Lock pour thread-safety :

- **Cache key** : `all_meals` pour le dataset complet
- **TTL** : Configurable via `CACHE_TTL_SECONDS` (défaut: 3600s)
- **Stats** : Exposées via endpoint `/health`
- **Warmup** : Préchargement au démarrage de l'API

```python
# Exemple d'utilisation
cache.set("key", value, ttl_seconds=3600)
value = cache.get("key")  # None si expiré
cache.clear()  # Invalidation manuelle
```

## Rate Limiting

Protection contre l'abus via SlowAPI :

- **Stratégie** : Limitation par IP (get_remote_address)
- **Limite** : Configurable via `API_RATE_LIMIT_PER_MINUTE` (défaut: 100/min)
- **Réponse** : HTTP 429 avec retry-after header

## Observabilité

### Logging structuré

Utilisation de structlog pour des logs JSON en production et lisibles en développement :

```json
{
  "timestamp": "2024-01-15T10:30:45",
  "level": "info",
  "event": "Requête HTTP",
  "method": "GET",
  "path": "/meals/by-ingredients",
  "status_code": 200,
  "duration_ms": 45.2
}
```

### Health checks

Deux endpoints pour le monitoring :

- **GET /health** - Vérification générale (cache, config)
- **GET /ready** - Readiness pour Kubernetes (données chargées)

## Frontend Streamlit

### Architecture

- **Session State** - Gestion d'état entre reruns
- **Caching** - `@st.cache_data` pour les appels API (TTL 5min)
- **Components** - Modularisation thème, favoris, historique

### Thème dynamique

Variables CSS exposées via `:root` :

```css
:root {
  --primary: #1d4ed8;
  --accent: #38bdf8;
  --card-bg: #ffffff;
  --card-border: #dbeafe;
  --text-dark: #0f172a;
  --muted: #64748b;
}
```

Toggle clair/sombre avec persistance session.

### Favoris

Stockage session_state avec détection de doublons :

```python
# Toggle favori
if is_favorite(meal_name):
    remove_from_favorites(meal_name)
else:
    add_to_favorites(meal)
```

### Historique

Dernières recherches conservées (max 10) avec horodatage :

```python
entry = {
    "ingredients": ["chicken", "rice"],
    "results_count": 24,
    "timestamp": "14:30:25",
    "date": "2024-01-15"
}
```

Cliquer sur une entrée recharge la recherche instantanément.

## Sécurité

### Input validation

- **Pydantic** - Validation automatique des schémas
- **Min/Max** - Contraintes sur les listes d'ingrédients (1-50) et limit (1-500)
- **HTML escaping** - Protection XSS côté Streamlit

### CORS

Configuration via `CORS_ORIGINS` :

```python
# Développement
["*"]

# Production
["https://monsite.com", "https://app.monsite.com"]
```

## Docker

### Multi-stage build

```dockerfile
# Stage 1: Builder
FROM python:3.12-slim AS builder
RUN pip install .

# Stage 2: Production (sans build deps)
FROM python:3.12-slim AS production
COPY --from=builder /opt/venv /opt/venv
USER appuser  # Non-root
```

### Health checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s \
    CMD python -c "urllib.request.urlopen('http://localhost:8000/health')"
```

## CI/CD

Pipeline GitHub Actions :

1. **Lint** - Ruff + format check
2. **Type check** - MyPy strict
3. **Test** - Pytest avec coverage
4. **Docker build** - Images API + Streamlit

Matrix Python 3.11 et 3.12.
