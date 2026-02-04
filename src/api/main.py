"""Point d'entrée principal de l'application FastAPI.

Configure et lance l'API avec:
- Documentation auto (Swagger/ReDoc)
- Middlewares (CORS, rate limiting, logging)
- Routes organisées
- Configuration centralisée
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from src.api.middleware import setup_middlewares
from src.api.routes import dataset_router, health_router
from src.core.config import Settings, get_settings
from src.core.logging import configure_logging, get_logger
from src.services.cache import cache
from src.services.recommender import load_meals

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Gestion du cycle de vie de l'application.

    Exécuté au démarrage et à l'arrêt de l'app.

    Startup:
    - Configure logging
    - Précharge les données (warm cache)

    Shutdown:
    - Cleanup ressources
    """
    # Startup
    settings = get_settings()
    configure_logging(settings)

    logger.info(
        "Demarrage API",
        name=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
    )

    # Précharge les données (warm cache)
    try:
        logger.info("Prechargement des donnees...")
        meals = load_meals()
        logger.info(f"{len(meals)} repas charges en memoire")
    except Exception as e:
        logger.error(f"Erreur prechargement: {e}")
        # Continue quand même, les données se chargeront à la 1ère requête

    yield  # App running

    # Shutdown
    logger.info("Arret API, cleanup...")
    cache.clear()
    logger.info("Cleanup termine")


def create_application(settings: Settings | None = None) -> FastAPI:
    """Factory pour créer l'app FastAPI configurée.

    Args:
        settings: Configuration (auto-chargée si None)

    Returns:
        Instance FastAPI prête
    """
    if settings is None:
        settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=settings.app_description,
        docs_url="/docs" if not settings.is_production else None,  # Cache Swagger en prod
        redoc_url="/redoc" if not settings.is_production else None,
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # Configure middlewares
    setup_middlewares(app)

    # Enregistre les routes
    app.include_router(dataset_router)
    app.include_router(health_router)

    # Route racine
    @app.get("/", tags=["Racine"])
    async def root() -> dict[str, str]:
        """Message de bienvenue avec liens utiles."""
        return {
            "message": f"Bienvenue sur {settings.app_name}",
            "version": settings.app_version,
            "documentation": "/docs",
            "health": "/health",
        }

    return app


# Instance globale (pour uvicorn)
app = create_application()


def custom_openapi() -> dict[str, Any] | None:
    """Customisation du schéma OpenAPI."""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Ajoute des infos supplémentaires
    openapi_schema["info"]["x-logo"] = {
        "url": "https://cdn-icons-png.flaticon.com/512/1830/1830839.png"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi  # type: ignore[assignment]


def main() -> None:
    """Entrypoint console script pour démarrer l'API avec Uvicorn."""
    import uvicorn

    settings = get_settings()

    uvicorn.run(
        "src.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
