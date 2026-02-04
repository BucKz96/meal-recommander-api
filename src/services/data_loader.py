"""Chargement et parsing des données de recettes.

Ce module gère:
- Téléchargement automatique depuis HuggingFace
- Parsing sécurisé (sans ast.literal_eval risqué)
- Retry avec backoff exponentiel
- Validation des données
"""
import re
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from src.core.config import get_settings
from src.core.exceptions import DataLoadError
from src.core.logging import get_logger

logger = get_logger(__name__)


def safe_parse_list(value: str | list[Any] | None) -> list[str]:
    """Parse une liste d'ingrédients de manière sécurisée.

    AVANT (risqué):
        >>> ast.literal_eval("[1, 2, 3]")  # Exécute du code Python!

    APRÈS (sécurisé):
        >>> safe_parse_list("flour, sugar, eggs")
        ['flour', 'sugar', 'eggs']

    Args:
        value: String, liste, ou None

    Returns:
        Liste d'ingrédients nettoyés
    """
    if value is None:
        return []

    if isinstance(value, list):
        return [str(item).strip().lower() for item in value if item]

    if isinstance(value, str):
        # Séparateurs: virgule, point-virgule, caret (^)
        ingredients = re.split(r"[,;\^]", value)
        return [ing.strip().lower() for ing in ingredients if ing.strip()]

    # Fallback pour tout autre type (int, float, etc.)
    return []  # type: ignore[unreachable]


def safe_parse_nutrition(value: str | dict[str, Any] | None) -> dict[str, float]:
    """Parse les informations nutritionnelles.

    Gère:
    - Dictionnaires Python
    - Chaînes JSON-like
    - Valeurs manquantes
    - Conversion safe en float

    Args:
        value: Dict, string, ou None

    Returns:
        Dict avec calories, protein, fat, etc.
    """
    if value is None:
        return {}

    nutrition_dict: dict[str, Any] = {}

    # Si c'est déjà un dict
    if isinstance(value, dict):
        nutrition_dict = value
    elif isinstance(value, str):
        # Parsing manuel safe (sans eval)
        try:
            # Remplace les quotes simples par doubles pour JSON-like
            cleaned_str = value.replace("'", '"')
            # Extrait les paires clé: valeur
            pattern = r'"(\w+)":\s*\{?\s*"amount":\s*([\d.]+)'
            matches = re.findall(pattern, cleaned_str)
            nutrition_dict = {k: float(v) for k, v in matches}
        except Exception:
            logger.warning(f"Impossible de parser nutrition: {value[:100]}...")
            return {}

    # Nettoie et extrait les valeurs importantes
    cleaned_nutrition: dict[str, float] = {}
    for key in ["calories", "protein", "fat", "carbohydrates", "sugars", "fiber"]:
        try:
            val = nutrition_dict.get(key, 0)
            if isinstance(val, (int, float)):
                cleaned_nutrition[key] = round(float(val), 2)
            elif isinstance(val, dict) and "amount" in val:
                cleaned_nutrition[key] = round(float(val["amount"]), 2)
            else:
                cleaned_nutrition[key] = 0.0
        except (ValueError, TypeError):
            cleaned_nutrition[key] = 0.0

    return cleaned_nutrition


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True,
)
def download_csv(url: str, target_path: Path) -> None:
    """Télécharge le CSV avec retry automatique.

    Args:
        url: URL de téléchargement
        target_path: Chemin local de destination

    Raises:
        DataLoadError: Si le téléchargement échoue après 3 tentatives
    """
    logger.info(f"Téléchargement dataset depuis {url}")

    try:
        response = requests.get(url, timeout=30, stream=True)
        response.raise_for_status()

        # Écriture par chunks (pour gros fichiers)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with target_path.open("wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        logger.info(f"Dataset téléchargé: {target_path.stat().st_size / 1024:.1f} KB")

    except requests.exceptions.RequestException as e:
        raise DataLoadError(
            source=url,
            reason=f"Erreur HTTP: {e}",
        ) from e


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=8),
    reraise=True,
)
def fetch_mealdb_by_letter(letter: str) -> list[dict[str, Any]]:
    """Récupère les recettes TheMealDB pour une lettre donnée."""
    settings = get_settings()
    url = f"{settings.mealdb_api_base}/search.php?f={letter}"
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    payload = response.json()
    return payload.get("meals") or []


def build_mealdb_csv(target_path: Path) -> None:
    """Construit un CSV local depuis TheMealDB (avec images)."""
    settings = get_settings()
    letters = settings.mealdb_letters
    meals_by_id: dict[str, dict[str, Any]] = {}

    logger.info("Chargement des données TheMealDB...")
    for letter in letters:
        try:
            meals = fetch_mealdb_by_letter(letter)
        except Exception as e:
            logger.warning(f"Échec fetch TheMealDB pour '{letter}': {e}")
            continue
        for meal in meals:
            meal_id = str(meal.get("idMeal", "")).strip()
            if meal_id:
                meals_by_id[meal_id] = meal

    rows: list[dict[str, Any]] = []
    for meal in meals_by_id.values():
        ingredients: list[str] = []
        for i in range(1, 21):
            ing = meal.get(f"strIngredient{i}")
            if ing and str(ing).strip():
                ingredients.append(str(ing).strip().lower())

        area = str(meal.get("strArea") or "").strip().lower()
        raw_tags = str(meal.get("strTags") or "").strip()
        tags_list = []
        if area:
            tags_list.append(area)
        if raw_tags:
            tags_list.extend([t.strip().lower() for t in raw_tags.split(",") if t.strip()])
        tags_value = ";".join(tags_list)

        rows.append(
            {
                "name": meal.get("strMeal") or "Unnamed Recipe",
                "ingredients": ", ".join(ingredients),
                "nutritions": "{}",
                "tags": tags_value,
                "image_url": meal.get("strMealThumb") or "",
                "prep_time": "",
                "diet_type": "",
                "dish_type": meal.get("strCategory") or "",
                "seasonal": "",
                "category": meal.get("strCategory") or "",
            }
        )

    if not rows:
        raise DataLoadError(source="TheMealDB", reason="Aucune recette récupérée")

    df = pd.DataFrame(rows)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(target_path, index=False, encoding="utf-8")
    logger.info(f"Dataset TheMealDB généré: {len(df)} recettes")


def load_recipes_df(force_refresh: bool = False) -> pd.DataFrame:
    """Charge le DataFrame des recettes (avec cache fichier).

    Args:
        force_refresh: Force le re-téléchargement

    Returns:
        DataFrame pandas des recettes

    Raises:
        DataLoadError: Si le chargement échoue
    """
    settings = get_settings()
    csv_path = settings.csv_path

    # Source TheMealDB
    if settings.data_source == "mealdb":
        if force_refresh or not csv_path.exists():
            build_mealdb_csv(csv_path)
    else:
        # Source CSV distante
        if force_refresh or not csv_path.exists():
            logger.info("Dataset non trouvé localement, téléchargement...")
            download_csv(settings.csv_url, csv_path)

    try:
        # Lecture avec gestion d'encodage
        df = pd.read_csv(csv_path, encoding="utf-8")
        logger.info(f"Dataset chargé: {len(df)} recettes")
        return df

    except pd.errors.EmptyDataError as e:
        raise DataLoadError(
            source=str(csv_path),
            reason="Fichier CSV vide",
        ) from e
    except Exception as e:
        raise DataLoadError(
            source=str(csv_path),
            reason=f"Erreur parsing CSV: {e}",
        ) from e
