"""Tests d'intégration de l'API.

Ces tests vérifient les endpoints HTTP avec TestClient.
Ils nécessitent que l'API soit importable mais pas nécessairement
que les données soient chargées (utilisation de mocks).
"""
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.models.schemas import Meal, NutritionInfo


@pytest.fixture
def client():
    """Fixture TestClient pour tous les tests."""
    return TestClient(app)


@pytest.fixture
def sample_meals():
    """Fixture: Repas de test."""
    return [
        Meal(
            name="Chicken Curry",
            ingredients=["chicken", "curry", "rice"],
            cuisine="indian",
            nutritions=NutritionInfo(calories=450, protein=30),
        ),
        Meal(
            name="Beef Tacos",
            ingredients=["beef", "tortilla", "salsa"],
            cuisine="mexican",
            nutritions=NutritionInfo(calories=380, protein=25),
        ),
        Meal(
            name="Caesar Salad",
            ingredients=["lettuce", "chicken", "parmesan", "croutons"],
            cuisine="american",
            nutritions=NutritionInfo(calories=320, protein=20),
        ),
    ]


class TestRootEndpoint:
    """Tests du endpoint racine /."""

    def test_root_returns_welcome(self, client):
        """GET / retourne message de bienvenue."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Meal Recommender" in data["message"]
        assert "version" in data
        assert "documentation" in data


class TestHealthEndpoints:
    """Tests des endpoints de santé."""

    def test_health_check(self, client):
        """GET /health retourne statut santé."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ["healthy", "unhealthy"]
        assert "version" in data
        assert "environment" in data

    def test_readiness_probe(self, client):
        """GET /ready vérifie si l'app est prête."""
        with patch("src.api.routes.load_meals") as mock_load:
            mock_load.return_value = []

            response = client.get("/ready")

            assert response.status_code == 200
            data = response.json()
            assert data["ready"] is True


class TestGetAllMeals:
    """Tests GET /meals/all."""

    def test_get_all_meals_success(self, client, sample_meals):
        """Récupère tous les repas sans filtre."""
        with patch("src.api.routes.get_meals_by_cuisine", return_value=sample_meals):
            response = client.get("/meals/all")

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 3
            assert data[0]["name"] == "Chicken Curry"

    def test_get_all_meals_with_cuisine_filter(self, client, sample_meals):
        """Filtre par cuisine."""
        indian_meals = [m for m in sample_meals if m.cuisine == "indian"]

        with patch("src.api.routes.get_meals_by_cuisine", return_value=indian_meals):
            response = client.get("/meals/all?cuisine=indian")

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["cuisine"] == "indian"


class TestGetMealsByIngredients:
    """Tests GET /meals/by-ingredients."""

    def test_recommend_by_single_ingredient(self, client, sample_meals):
        """Recommande avec un ingrédient."""
        with patch("src.api.routes.recommend_meals", return_value=[sample_meals[0]]):
            response = client.get("/meals/by-ingredients?available_ingredients=chicken")

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert "chicken" in data[0]["ingredients"]

    def test_recommend_by_multiple_ingredients(self, client, sample_meals):
        """Recommande avec plusieurs ingrédients."""
        with patch("src.api.routes.recommend_meals", return_value=sample_meals):
            response = client.get(
                "/meals/by-ingredients?available_ingredients=chicken&available_ingredients=rice"
            )

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 3

    def test_recommend_with_limit(self, client, sample_meals):
        """Limite le nombre de résultats."""
        with patch("src.api.routes.recommend_meals", return_value=sample_meals):
            response = client.get(
                "/meals/by-ingredients?available_ingredients=chicken&limit=2"
            )

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2

    def test_recommend_empty_ingredients_returns_error(self, client):
        """Erreur 422 si pas d'ingrédients."""
        response = client.get("/meals/by-ingredients")

        assert response.status_code == 422

    def test_recommend_empty_list_returns_error(self, client):
        """Erreur 422 si liste vide."""
        response = client.get("/meals/by-ingredients?available_ingredients=")

        assert response.status_code == 422


class TestGetSampleMeals:
    """Tests GET /meals/sample."""

    def test_get_sample_default_count(self, client, sample_meals):
        """Retourne 5 repas par défaut."""
        with patch("src.api.routes.get_sample_meals", return_value=sample_meals[:5]):
            response = client.get("/meals/sample")

            assert response.status_code == 200
            data = response.json()
            assert len(data) <= 5

    def test_get_sample_custom_count(self, client, sample_meals):
        """Retourne nombre personnalisé."""
        with patch("src.api.routes.get_sample_meals", return_value=sample_meals[:2]):
            response = client.get("/meals/sample?count=2")

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2

    def test_get_sample_count_validation(self, client):
        """Validation du paramètre count."""
        response = client.get("/meals/sample?count=0")
        assert response.status_code == 422

        response = client.get("/meals/sample?count=100")
        assert response.status_code == 422


class TestResponseStructure:
    """Tests de la structure des réponses."""

    def test_meal_response_has_required_fields(self, client, sample_meals):
        """Vérifie que toutes les champs requis sont présents."""
        with patch("src.api.routes.recommend_meals", return_value=[sample_meals[0]]):
            response = client.get("/meals/by-ingredients?available_ingredients=chicken")

            data = response.json()
            meal = data[0]

            # Champs obligatoires
            assert "name" in meal
            assert "ingredients" in meal
            assert isinstance(meal["ingredients"], list)
            assert "cuisine" in meal

            # Champs optionnels
            assert "image" in meal
            assert "prep_time" in meal
            assert "diet_type" in meal
            assert "dish_type" in meal
            assert "seasonal" in meal
            assert "nutritions" in meal

            # Structure nutrition
            nutrition = meal["nutritions"]
            assert "calories" in nutrition
            assert "protein" in nutrition
            assert "fat" in nutrition
            assert "carbohydrates" in nutrition


class TestErrorHandling:
    """Tests de gestion des erreurs."""

    def test_404_endpoint_not_found(self, client):
        """Endpoint inexistant retourne 404."""
        response = client.get("/nonexistent")
        assert response.status_code == 404

    def test_response_time_header(self, client):
        """Header X-Response-Time présent."""
        response = client.get("/health")
        assert "X-Response-Time" in response.headers
