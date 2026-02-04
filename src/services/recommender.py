"""Service de recommandation de repas.

Coeur métier de l'application:
- Algorithme de matching par ingrédients
- Scoring par pertinence
- Cache pour performance
"""

import pandas as pd

from src.core.logging import get_logger
from src.models.schemas import Meal, NutritionInfo
from src.services.cache import cache
from src.services.data_loader import load_recipes_df, safe_parse_list, safe_parse_nutrition

logger = get_logger(__name__)

# Constantes
CACHE_KEY_MEALS = "all_meals"
DEFAULT_IMAGE = "https://via.placeholder.com/200?text=No+Image"


def extract_cuisine_from_tags(tags: str | None) -> str:
    """Extrait la cuisine principale depuis les tags.

    Exemple:
        >>> extract_cuisine_from_tags("italian;pasta;quick")
        'italian'
    """
    if not tags or not isinstance(tags, str):
        return "unknown"

    parts = [p.strip().lower() for p in tags.split(";") if p.strip()]
    return parts[0] if parts else "unknown"


def clean_image_url(url: str | None) -> str:
    """Nettoie et valide l'URL d'image.

    - Force HTTPS
    - Fallback vers placeholder
    """
    if not url or not isinstance(url, str):
        return DEFAULT_IMAGE

    url = url.strip()
    if url.startswith("http://"):
        url = url.replace("http://", "https://", 1)

    return url if url.startswith("https://") else DEFAULT_IMAGE


def parse_prep_time(prep_time: str | None) -> str:
    """Nettoie le format du temps de préparation.

    Exemple:
        >>> parse_prep_time("30-minutes-or-less")
        '30 minutes or less'
    """
    if not prep_time or not isinstance(prep_time, str):
        return ""

    return prep_time.replace("-", " ")


def _row_to_meal(row: pd.Series) -> Meal:
    """Convertit une ligne DataFrame en objet Meal.

    Args:
        row: Ligne pandas du DataFrame

    Returns:
        Objet Meal validé
    """
    # Récupération sécurisée des colonnes
    name = str(row.get("name", "Unnamed Recipe"))
    if not name or name == "nan":
        name = "Unnamed Recipe"

    ingredients = safe_parse_list(row.get("ingredients"))
    nutrition = safe_parse_nutrition(row.get("nutritions"))
    cuisine = extract_cuisine_from_tags(row.get("tags"))
    image = clean_image_url(row.get("image_url"))
    prep_time = parse_prep_time(row.get("prep_time"))

    # Champs optionnels (peuvent être None)
    diet_type = str(row.get("diet_type")) if pd.notna(row.get("diet_type")) else None
    dish_type = str(row.get("dish_type")) if pd.notna(row.get("dish_type")) else None
    seasonal = str(row.get("seasonal")) if pd.notna(row.get("seasonal")) else None

    return Meal(
        name=name,
        ingredients=ingredients,
        cuisine=cuisine,
        image=image,
        prep_time=prep_time,
        diet_type=diet_type,
        dish_type=dish_type,
        seasonal=seasonal,
        nutritions=NutritionInfo(**nutrition),
    )


def load_meals(use_cache: bool = True) -> list[Meal]:
    """Charge toutes les recettes (avec cache mémoire).

    C'est la fonction CLÉ pour la performance:
    - Premier appel: charge depuis CSV (~1-2s)
    - Appels suivants: cache mémoire instantané

    Args:
        use_cache: Utiliser le cache (True recommandé)

    Returns:
        Liste de tous les repas
    """
    # 1. Essaie le cache mémoire d'abord
    if use_cache:
        cached = cache.get(CACHE_KEY_MEALS)
        if cached is not None:
            logger.debug(f"Cache mémoire hit: {len(cached)} repas")
            return cached  # type: ignore[no-any-return]

    # 2. Charge depuis CSV
    logger.info("Chargement repas depuis CSV...")
    df = load_recipes_df()

    # 3. Conversion en objets Meal
    meals = []
    for _, row in df.iterrows():
        try:
            meal = _row_to_meal(row)
            meals.append(meal)
        except Exception as e:
            logger.warning(f"Erreur conversion ligne: {e}")
            continue

    # 4. Stocke dans le cache
    if use_cache:
        from src.core.config import get_settings
        settings = get_settings()
        cache.set(CACHE_KEY_MEALS, meals, settings.cache_ttl_seconds)
        logger.info(f"Cache mis à jour: {len(meals)} repas")

    return meals


def recommend_meals(available_ingredients: list[str]) -> list[Meal]:
    """Recommande des repas basés sur les ingrédients disponibles.

    Algorithme:
    1. Normalise les ingrédients utilisateur (lowercase, trim)
    2. Pour chaque repas, compte les ingrédients correspondants
    3. Score = nombre d'ingrédients matchés
    4. Trie par score décroissant
    5. Retourne tous les repas avec au moins 1 match

    Args:
        available_ingredients: Liste d'ingrédients (ex: ["chicken", "rice"])

    Returns:
        Liste triée des repas les plus pertinents

    Exemple:
        >>> meals = recommend_meals(["chicken", "rice", "tomato"])
        >>> # Repas avec chicken+rice+tomato en premier
    """
    logger.info(f"Recherche repas avec: {available_ingredients}")

    # Normalisation (minuscules, sans espaces)
    available = {ing.strip().lower() for ing in available_ingredients if ing.strip()}

    if not available:
        logger.warning("Liste d'ingrédients vide")
        return []

    # Charge tous les repas (avec cache)
    all_meals = load_meals()

    # Scoring
    scored_meals: list[tuple[int, Meal]] = []

    for meal in all_meals:
        matched = 0
        for meal_ing in meal.ingredients:
            meal_ing_lower = meal_ing.lower()
            # Match partiel: l'ingrédient utilisateur doit être DANS l'ingrédient repas
            # Ex: "chicken" match "chicken breast", "chicken thigh", etc.
            if any(user_ing in meal_ing_lower for user_ing in available):
                matched += 1

        if matched > 0:
            scored_meals.append((matched, meal))

    # Tri par score décroissant
    scored_meals.sort(key=lambda x: x[0], reverse=True)

    results = [meal for _, meal in scored_meals]
    logger.info(f"Trouvé {len(results)} repas pertinents")

    return results


def get_meals_by_cuisine(cuisine: str | None = None) -> list[Meal]:
    """Filtre les repas par type de cuisine.

    Args:
        cuisine: Type de cuisine (ex: "italian", "indian")

    Returns:
        Liste filtrée ou tous les repas si cuisine=None
    """
    meals = load_meals()

    if cuisine:
        cuisine_lower = cuisine.strip().lower()
        meals = [m for m in meals if m.cuisine and m.cuisine.lower() == cuisine_lower]
        logger.info(f"Filtre cuisine '{cuisine}': {len(meals)} repas")

    return meals


def get_sample_meals(count: int = 5) -> list[Meal]:
    """Retourne un échantillon de repas (pour debug/demo).

    Args:
        count: Nombre de repas à retourner

    Returns:
        Liste de repas
    """
    meals = load_meals()
    return meals[:count]
