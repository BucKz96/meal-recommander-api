"""Exceptions personnalisées de l'application.

Pourquoi des exceptions custom ?
- Messages d'erreur cohérents pour l'API
- Séparation des erreurs métier vs techniques
- Facilite le debugging avec des contextes riches
"""

from typing import Any


class AppError(Exception):
    """Exception de base pour toute l'application.

    Attributes:
        message: Message d'erreur lisible
        status_code: Code HTTP associé (pour l'API)
        error_code: Code d'erreur interne unique
        details: Informations supplémentaires (debug)
    """

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "INTERNAL_ERROR",
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details: dict[str, Any] = details or {}


class DataNotFoundError(AppError):
    """Levée quand une donnée n'est pas trouvée.

    Exemple: Recette inexistante, fichier CSV manquant
    """

    def __init__(self, resource: str, identifier: str | None = None):
        message = f"{resource} non trouvé"
        if identifier:
            message += f" (identifiant: {identifier})"

        super().__init__(
            message=message,
            status_code=404,
            error_code="DATA_NOT_FOUND",
            details={"resource": resource, "identifier": identifier},
        )


class ValidationError(AppError):
    """Levée quand les données utilisateur sont invalides.

    Exemple: Liste d'ingrédients vide, format incorrect
    """

    def __init__(self, field: str, reason: str, details: dict[str, Any] | None = None):
        super().__init__(
            message=f"Champ '{field}' invalide: {reason}",
            status_code=422,
            error_code="VALIDATION_ERROR",
            details={"field": field, "reason": reason, **(details or {})},
        )


class DataLoadError(AppError):
    """Levée quand le chargement des données échoue.

    Exemple: CSV corrompu, URL inaccessible, parsing error
    """

    def __init__(self, source: str, reason: str):
        super().__init__(
            message=f"Échec du chargement des données depuis {source}: {reason}",
            status_code=503,
            error_code="DATA_LOAD_ERROR",
            details={"source": source, "reason": reason},
        )
