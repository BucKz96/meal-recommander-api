"""Modèles de données Pydantic v2.

Les schemas définissent:
- La structure des données API (entrée/sortie)
- La validation automatique
- La documentation OpenAPI
- La sérialisation JSON

Pourquoi Pydantic v2 ?
- Validation 5-10x plus rapide que v1
- Meilleure gestion d'erreurs
- Support Python 3.8+
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class NutritionInfo(BaseModel):
    """Informations nutritionnelles d'un repas.

    Toutes les valeurs sont en grammes ou kcal par portion.
    """
    model_config = ConfigDict(extra="ignore")

    calories: float = Field(default=0.0, ge=0, description="Calories en kcal")
    protein: float = Field(default=0.0, ge=0, description="Protéines en grammes")
    fat: float = Field(default=0.0, ge=0, description="Lipides en grammes")
    carbohydrates: float = Field(default=0.0, ge=0, description="Glucides en grammes")
    sugars: float = Field(default=0.0, ge=0, description="Sucres en grammes")
    fiber: float = Field(default=0.0, ge=0, description="Fibres en grammes")


class Meal(BaseModel):
    """Modèle complet d'une recette/repas.

    Ce modèle est utilisé pour:
    - Réponses API (GET /meals)
    - Validation des données CSV
    - Affichage dans Streamlit
    """
    model_config = ConfigDict(
        extra="ignore",  # Ignore champs inconnus (compatibilité)
        json_schema_extra={
            "example": {
                "name": "Chicken Curry",
                "ingredients": ["chicken", "curry powder", "rice", "coconut milk"],
                "cuisine": "indian",
                "image": "https://example.com/chicken-curry.jpg",
                "prep_time": "30 minutes or less",
                "diet_type": "high-protein",
                "dish_type": "main-dish",
                "seasonal": None,
                "nutritions": {
                    "calories": 450.0,
                    "protein": 35.0,
                    "fat": 12.0,
                    "carbohydrates": 55.0,
                    "sugars": 3.0,
                    "fiber": 2.0,
                },
            }
        },
    )

    # Champs obligatoires
    name: str = Field(..., min_length=1, description="Nom de la recette")
    ingredients: list[str] = Field(
        ...,
        min_length=1,
        description="Liste des ingrédients nécessaires"
    )

    # Champs optionnels
    cuisine: str | None = Field(
        None,
        description="Type de cuisine (ex: italian, indian)"
    )
    image: str | None = Field(
        None,
        description="URL de l'image du plat"
    )
    prep_time: str | None = Field(
        None,
        description="Temps de préparation (format texte)"
    )
    diet_type: str | None = Field(
        None,
        description="Régime alimentaire (ex: vegetarian, low-carb)"
    )
    dish_type: str | None = Field(
        None,
        description="Type de plat (ex: main-dish, dessert)"
    )
    seasonal: str | None = Field(
        None,
        description="Saisonnalité (ex: summer, winter)"
    )

    # Nutrition (dictionnaire ou objet NutritionInfo)
    nutritions: NutritionInfo = Field(
        default_factory=NutritionInfo,
        description="Valeurs nutritionnelles"
    )

    @field_validator("ingredients", mode="before")
    @classmethod
    def validate_ingredients(cls, v: Any) -> list[str]:
        """S'assure que les ingrédients sont une liste de strings.

        Accepte:
        - List[str]: ["flour", "sugar"]
        - str avec séparateurs: "flour, sugar"
        """
        if isinstance(v, str):
            return [ing.strip() for ing in v.split(",") if ing.strip()]
        if isinstance(v, list):
            return [str(ing).strip() for ing in v if ing]
        return []

    @field_validator("nutritions", mode="before")
    @classmethod
    def validate_nutritions(cls, v: Any) -> NutritionInfo:
        """Convetit les nutritions en objet NutritionInfo.

        Accepte:
        - Dict: {"calories": 100, "protein": 10}
        - NutritionInfo object
        - None (retourne valeurs par défaut)
        """
        if v is None:
            return NutritionInfo()
        if isinstance(v, dict):
            return NutritionInfo(**v)
        if isinstance(v, NutritionInfo):
            return v
        return NutritionInfo()


class MealRecommendationRequest(BaseModel):
    """Requête pour obtenir des recommandations.

    Utilisé par POST /recommendations ou validation GET params.
    """
    ingredients: list[str] = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Ingrédients disponibles (1-50 max)",
    )
    max_results: int | None = Field(
        default=100,
        ge=1,
        le=500,
        description="Nombre max de résultats (1-500)",
    )

    @field_validator("ingredients")
    @classmethod
    def validate_non_empty_ingredients(cls, v: list[str]) -> list[str]:
        """Vérifie qu'au moins un ingrédient est non-vide."""
        cleaned = [ing.strip() for ing in v if ing.strip()]
        if not cleaned:
            raise ValueError("Au moins un ingrédient non-vide requis")
        return cleaned


class HealthCheck(BaseModel):
    """Réponse du health check.

    Utilisé par GET /health pour monitoring.
    """
    status: str = Field(..., description="État général: healthy/unhealthy")
    version: str = Field(..., description="Version de l'API")
    environment: str = Field(..., description="Environnement: dev/staging/prod")
    cache_stats: dict[str, Any] | None = Field(
        None,
        description="Statistiques du cache"
    )
