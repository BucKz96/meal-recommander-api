"""Middlewares FastAPI.

Configure:
- Rate limiting (SlowAPI)
- Gestion d'erreurs centralisée
- CORS
- Logging des requêtes
"""
import time
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.config import get_settings
from src.core.logging import get_logger

logger = get_logger(__name__)


def setup_middlewares(app: FastAPI) -> None:
    """Configure tous les middlewares de l'application.

    Ordre d'exécution (important):
    1. CORS (tout en premier)
    2. Rate Limiting
    3. Logging des requêtes
    4. Gestion erreurs

    Args:
        app: Instance FastAPI
    """
    settings = get_settings()

    # 1. CORS - Autorise les requêtes cross-origin
    # En production, remplacer ["*"] par les domains autorisés
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info("CORS middleware configuré", origins=settings.cors_origins)

    # 2. Rate Limiting - Protège contre l'abus
    # Utilise SlowAPI (wrapper autour de limits)
    limiter = Limiter(
        key_func=get_remote_address,  # Limite par IP
        default_limits=[f"{settings.api_rate_limit_per_minute} per minute"],
    )
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]
    logger.info(
        "Rate limiting activé",
        limit=f"{settings.api_rate_limit_per_minute}/minute",
    )

    # 3. Logging middleware - Log chaque requête
    app.add_middleware(LoggingMiddleware)

    # 4. Error handling middleware - Catch-all
    app.add_middleware(ErrorHandlingMiddleware)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Log toutes les requêtes HTTP avec timing.

    Format:
        [2024-01-15 10:30:45] GET /meals/by-ingredients 200 45ms
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        start_time = time.time()

        # Exécute la requête
        response = await call_next(request)

        # Calcule le temps
        duration_ms = (time.time() - start_time) * 1000

        # Log structuré
        logger.info(
            "Requête HTTP",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
            client_ip=request.client.host if request.client else None,
        )

        # Header de timing (pour debug)
        response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"

        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware de gestion d'erreurs global.

    Capture toutes les exceptions non gérées et retourne
    une réponse JSON propre.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        try:
            return await call_next(request)

        except HTTPException:
            # Laisse passer les HTTPException (422, 404, etc. gérées par FastAPI)
            raise

        except Exception as e:
            # Log l'erreur complète (vraies erreurs 500)
            logger.exception(
                "Erreur non gérée",
                path=request.url.path,
                method=request.method,
                error_type=type(e).__name__,
            )

            # Retourne une réponse propre
            from fastapi.responses import JSONResponse

            return JSONResponse(
                status_code=500,
                content={
                    "error": "Erreur interne du serveur",
                    "error_code": "INTERNAL_ERROR",
                    "message": str(e) if get_settings().is_development else "Contactez l'administrateur",
                },
            )
