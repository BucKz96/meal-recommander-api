"""Tests unitaires des services.

Ces tests vérifient la logique métier en isolation,
sans dépendances externes (API, CSV, etc.)
"""

from src.models.schemas import Meal, NutritionInfo
from src.services.cache import CacheManager, cache
from src.services.data_loader import safe_parse_list, safe_parse_nutrition
from src.services.recommender import (
    clean_image_url,
    extract_cuisine_from_tags,
    parse_prep_time,
    recommend_meals,
)


class TestSafeParseList:
    """Tests du parsing d'ingrédients."""

    def test_parse_list_from_string_comma(self):
        """Parse une chaîne avec virgules."""
        result = safe_parse_list("flour, sugar, eggs")
        assert result == ["flour", "sugar", "eggs"]

    def test_parse_list_from_string_semicolon(self):
        """Parse une chaîne avec point-virgules."""
        result = safe_parse_list("flour;sugar;eggs")
        assert result == ["flour", "sugar", "eggs"]

    def test_parse_list_from_list(self):
        """Conserve une liste existante."""
        result = safe_parse_list(["flour", "sugar"])
        assert result == ["flour", "sugar"]

    def test_parse_list_empty(self):
        """Retourne liste vide pour None."""
        assert safe_parse_list(None) == []
        assert safe_parse_list("") == []


class TestSafeParseNutrition:
    """Tests du parsing nutritionnel."""

    def test_parse_from_dict(self):
        """Parse un dictionnaire."""
        data = {
            "calories": 100.5,
            "protein": 10.2,
            "fat": 5.0,
        }
        result = safe_parse_nutrition(data)
        assert result["calories"] == 100.5
        assert result["protein"] == 10.2
        assert result["fat"] == 5.0

    def test_parse_from_string(self):
        """Parse une chaîne JSON-like."""
        data = '{"calories": {"amount": 200}, "protein": {"amount": 15}}'
        result = safe_parse_nutrition(data)
        assert result["calories"] == 200.0

    def test_parse_missing_values(self):
        """Retourne 0.0 pour valeurs manquantes."""
        result = safe_parse_nutrition({})
        assert result["calories"] == 0.0
        assert result["protein"] == 0.0


class TestCacheManager:
    """Tests du système de cache."""

    def test_singleton_pattern(self):
        """Vérifie que c'est bien un singleton."""
        cache1 = CacheManager()
        cache2 = CacheManager()
        assert cache1 is cache2

    def test_cache_set_get(self):
        """Stocke et récupère une valeur."""
        cache.clear()
        cache.set("test_key", "test_value", ttl_seconds=60)
        result = cache.get("test_key")
        assert result == "test_value"

    def test_cache_expiration(self):
        """Vérifie l'expiration TTL."""
        cache.clear()
        cache.set("expire_key", "value", ttl_seconds=0)  # Expire immédiatement
        result = cache.get("expire_key")
        assert result is None

    def test_cache_stats(self):
        """Statistiques du cache."""
        cache.clear()
        cache.set("key1", "value1", 60)
        cache.set("key2", "value2", 60)
        stats = cache.get_stats()
        assert stats["active_entries"] == 2


class TestRecommenderHelpers:
    """Tests des fonctions utilitaires du recommender."""

    def test_extract_cuisine(self):
        """Extrait la cuisine depuis les tags."""
        assert extract_cuisine_from_tags("italian;pasta;quick") == "italian"
        assert extract_cuisine_from_tags(None) == "unknown"
        assert extract_cuisine_from_tags("") == "unknown"

    def test_clean_image_url(self):
        """Nettoie les URLs d'images."""
        assert clean_image_url("http://example.com/img.jpg") == "https://example.com/img.jpg"
        assert clean_image_url("https://example.com/img.jpg") == "https://example.com/img.jpg"
        assert "placeholder" in clean_image_url(None)

    def test_parse_prep_time(self):
        """Parse le temps de préparation."""
        assert parse_prep_time("30-minutes-or-less") == "30 minutes or less"
        assert parse_prep_time(None) == ""


class TestRecommendMeals:
    """Tests de l'algorithme de recommandation."""

    def test_recommend_single_ingredient(self):
        """Recommande avec un seul ingrédient."""
        # Création de repas de test
        meal1 = Meal(
            name="Chicken Rice",
            ingredients=["chicken", "rice"],
            cuisine="asian",
            nutritions=NutritionInfo(),
        )
        meal2 = Meal(
            name="Beef Stew",
            ingredients=["beef", "carrots"],
            cuisine="french",
            nutritions=NutritionInfo(),
        )

        # Test avec mock des données
        import unittest.mock
        with unittest.mock.patch("src.services.recommender.load_meals", return_value=[meal1, meal2]):
            results = recommend_meals(["chicken"])

        assert len(results) == 1
        assert results[0].name == "Chicken Rice"

    def test_recommend_multiple_ingredients(self):
        """Classement par nombre d'ingrédients matchés."""
        meal1 = Meal(
            name="Chicken Rice",
            ingredients=["chicken", "rice"],
            cuisine="asian",
            nutritions=NutritionInfo(),
        )
        meal2 = Meal(
            name="Chicken Rice Tomato",
            ingredients=["chicken", "rice", "tomato"],
            cuisine="asian",
            nutritions=NutritionInfo(),
        )

        import unittest.mock
        with unittest.mock.patch("src.services.recommender.load_meals", return_value=[meal1, meal2]):
            results = recommend_meals(["chicken", "rice", "tomato"])

        # meal2 doit être premier (3 matchs > 2 matchs)
        assert results[0].name == "Chicken Rice Tomato"
        assert results[1].name == "Chicken Rice"

    def test_recommend_empty_ingredients(self):
        """Retourne liste vide si pas d'ingrédients."""
        results = recommend_meals([])
        assert results == []

    def test_recommend_no_matches(self):
        """Retourne liste vide si aucun match."""
        meal = Meal(
            name="Chicken Rice",
            ingredients=["chicken", "rice"],
            cuisine="asian",
            nutritions=NutritionInfo(),
        )

        import unittest.mock
        with unittest.mock.patch("src.services.recommender.load_meals", return_value=[meal]):
            results = recommend_meals(["chocolate"])

        assert results == []
