"""Logging structuré avec structlog.

Pourquoi structlog ?
- Logs JSON en production (parsable par ELK, Datadog, etc.)
- Logs texte lisibles en développement
- Correlation IDs pour tracer les requêtes
- Performance optimisée (lazy evaluation)
"""
import logging
import sys
from typing import Any

import structlog
from structlog.types import EventDict

from src.core.config import Settings, get_settings


def add_app_info(
    _logger: logging.Logger,
    _method_name: str,
    event_dict: EventDict,
) -> EventDict:
    """Ajoute des informations sur l'application aux logs.

    Args:
        _logger: Logger structlog
        _method_name: Nom de la méthode appelée
        event_dict: Dictionnaire de l'événement log

    Returns:
        EventDict enrichi avec app_name et version
    """
    settings = get_settings()
    event_dict["app_name"] = settings.app_name
    event_dict["app_version"] = settings.app_version
    return event_dict


def configure_logging(settings: Settings | None = None) -> None:
    """Configure le logging structuré pour toute l'application.

    Cette fonction configure:
    1. Le logging standard Python (compatibilité)
    2. structlog pour le formatage structuré
    3. Les processors (filtres et enrichissements)

    Args:
        settings: Configuration (auto-chargée si None)

    Exemple:
        >>> configure_logging()
        >>> logger = structlog.get_logger()
        >>> logger.info("Hello", user_id=123)
        {"event": "Hello", "user_id": 123, "timestamp": "..."}
    """
    if settings is None:
        settings = get_settings()

    # Configuration du niveau de log
    log_level = getattr(logging, settings.log_level)

    # Processors communs (tous les environnements)
    shared_processors: list[Any] = [
        # Ajoute le niveau de log (INFO, DEBUG, etc.)
        structlog.stdlib.add_log_level,
        # Ajoute un timestamp ISO 8601
        structlog.processors.TimeStamper(fmt="iso"),
        # Ajoute des infos sur l'app (notre fonction custom)
        add_app_info,
        # Formate les exceptions Python proprement
        structlog.processors.format_exc_info,
    ]

    # Rendu final selon l'environnement
    renderer: structlog.processors.JSONRenderer | structlog.dev.ConsoleRenderer
    if settings.is_production:
        # JSON pour parsing automatique en production
        renderer = structlog.processors.JSONRenderer()
    else:
        # Texte coloré et lisible en développement
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    # Configuration structlog
    structlog.configure(
        processors=[*shared_processors, renderer],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configuration logging standard (pour les libs externes)
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )


def get_logger(name: str | None = None) -> Any:
    """Retourne un logger structuré configuré.

    Args:
        name: Nom du logger (généralement __name__)

    Returns:
        Logger structuré prêt à l'emploi

    Exemple:
        >>> logger = get_logger(__name__)
        >>> logger.info("Requête reçue", method="GET", path="/meals")
    """
    return structlog.get_logger(name)
