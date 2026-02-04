"""Routes API FastAPI.

Définit tous les endpoints REST de l'application.
Organisation claire avec tags pour la documentation Swagger.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse

from src.core.config import Settings, get_settings
from src.core.exceptions import AppError
from src.core.logging import get_logger
from src.models.schemas import HealthCheck, Meal
from src.services.cache import cache
from src.services.recommender import (
    get_meals_by_cuisine,
    get_sample_meals,
    load_meals,
    recommend_meals,
)

logger = get_logger(__name__)

# Router avec préfixe et tags
dataset_router = APIRouter(prefix="/meals", tags=["Repas"])
health_router = APIRouter(tags=["Santé"])


@dataset_router.get(
    "/by-ingredients",
    response_model=list[Meal],
    summary="Recommander repas par ingrédients",
    description="""
    Recommande des recettes basées sur les ingrédients disponibles.

    Algorithme:
    - Match partiel des ingrédients (ex: "chicken" match "chicken breast")
    - Score par nombre d'ingrédients correspondants
    - Tri par pertinence décroissante
    """,
    response_description="Liste des repas triés par pertinence",
)
async def get_meals_by_ingredients(
    available_ingredients: list[str] = Query(
        ...,
        description="Liste d'ingrédients (ex: chicken,rice,tomato)",
        min_length=1,
        examples=["chicken"],
    ),
    limit: int | None = Query(
        default=100,
        ge=1,
        le=500,
        description="Nombre max de résultats",
    ),
) -> list[Meal]:
    """Endpoint principal pour les recommandations.

    Args:
        available_ingredients: Liste d'ingrédients (depuis query params)
        limit: Limite de résultats

    Returns:
        Liste de repas

    Raises:
        HTTPException: Si aucun ingrédient fourni
    """
    logger.info(
        "Requête recommandations",
        ingredients=available_ingredients,
        limit=limit,
    )

    try:
        # Validation: nettoie et filtre les ingrédients vides
        cleaned_ingredients = [ing.strip() for ing in available_ingredients if ing and ing.strip()]

        if not cleaned_ingredients:
            raise HTTPException(
                status_code=422,
                detail="Au moins un ingrédient non-vide requis",
            )

        # Utilise les ingrédients nettoyés
        available_ingredients = cleaned_ingredients

        # Recommandations
        meals = recommend_meals(available_ingredients)

        # Limite les résultats
        limited_meals = meals[:limit] if limit else meals

        logger.info(
            "Recommandations générées",
            count=len(limited_meals),
            total_available=len(meals),
        )

        return limited_meals

    except HTTPException:
        # Laisse passer les HTTPException (gérées par FastAPI)
        raise
    except AppError as e:
        logger.error("Erreur métier", error=e.message)
        raise HTTPException(status_code=e.status_code, detail=e.message) from e
    except Exception as e:
        logger.exception("Erreur inattendue")
        raise HTTPException(status_code=500, detail=str(e)) from e


@dataset_router.get(
    "/all",
    response_model=list[Meal],
    summary="Lister tous les repas",
    description="Retourne tous les repas, avec option de filtrage par cuisine.",
)
async def get_all_meals(
    cuisine: str | None = Query(
        None,
        description="Filtrer par type de cuisine (ex: italian, indian)",
    ),
) -> list[Meal]:
    """Liste tous les repas, filtrable par cuisine."""
    logger.info("Requête liste repas", cuisine=cuisine)

    try:
        meals = get_meals_by_cuisine(cuisine)
        return meals
    except Exception as e:
        logger.exception("Erreur liste repas")
        raise HTTPException(status_code=500, detail=str(e)) from e


@dataset_router.get(
    "/sample",
    response_model=list[Meal],
    summary="Exemple de repas",
    description="Retourne un échantillon de repas pour démo/debug.",
)
async def get_sample(count: int = Query(default=5, ge=1, le=20)) -> list[Meal]:
    """Retourne un échantillon de repas."""
    logger.info("Requête échantillon", count=count)
    return get_sample_meals(count)


@health_router.get(
    "/health",
    response_model=HealthCheck,
    summary="Vérifier santé API",
    description="Endpoint pour monitoring (Kubernetes, Render, etc.)",
)
async def health_check(settings: Settings = Depends(get_settings)) -> HealthCheck:
    """Health check pour monitoring.

    Vérifie:
    - API répond
    - Cache accessible
    - Configuration chargée
    """
    try:
        # Test cache
        cache_stats = cache.get_stats()

        return HealthCheck(
            status="healthy",
            version=settings.app_version,
            environment=settings.app_env,
            cache_stats=cache_stats,
        )
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        return HealthCheck(
            status="unhealthy",
            version=settings.app_version,
            environment=settings.app_env,
            cache_stats=None,
        )


@health_router.get("/ready", summary="Readiness probe")
async def readiness_probe() -> JSONResponse:
    """Readiness probe pour Kubernetes.

    Vérifie que l'app est prête à recevoir du trafic.
    """
    try:
        # Vérifie que les données sont chargées
        meals = load_meals()
        return JSONResponse(
            content={"ready": True, "meals_loaded": len(meals)},
            status_code=200,
        )
    except Exception as e:
        return JSONResponse(
            content={"ready": False, "error": str(e)},
            status_code=503,
        )
