"""Client API pour communiquer avec le backend FastAPI.

Gère les appels HTTP avec cache et gestion d'erreurs.
"""

import os
from typing import Any, cast

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")
API_FETCH_LIMIT = 60


@st.cache_data(ttl=300, show_spinner=False)
def fetch_meals(ingredients: tuple[str, ...], limit: int | None = None) -> list[dict[str, Any]]:
    """Récupère les repas depuis l'API avec cache.

    Args:
        ingredients: Tuple d'ingrédients pour la recherche
        limit: Nombre maximum de résultats

    Returns:
        Liste des repas trouvés

    Raises:
        requests.RequestException: Si l'API est inaccessible
    """
    if ingredients:
        params: list[tuple[str, str]] = [("available_ingredients", ing) for ing in ingredients]
        url = f"{API_URL}/meals/by-ingredients"
    else:
        params = []
        url = f"{API_URL}/meals/all"

    if limit is not None:
        params.append(("limit", str(limit)))

    response = requests.get(url, params=params or None, timeout=15)
    response.raise_for_status()
    return cast(list[dict[str, Any]], response.json())


def check_api_health() -> dict[str, Any] | None:
    """Vérifie que l'API est accessible.

    Returns:
        Données du health check ou None si indisponible
    """
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        response.raise_for_status()
        return cast(dict[str, Any], response.json())
    except requests.RequestException:
        return None
