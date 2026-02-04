"""Configuration centralisée de l'application.

Ce module utilise Pydantic Settings pour gérer toute la configuration
via des variables d'environnement ou un fichier .env
"""
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration de l'application.

    Les valeurs peuvent être définies via:
    1. Variables d'environnement (priorité haute)
    2. Fichier .env (priorité moyenne)
    3. Valeurs par défaut ci-dessous (priorité basse)

    Exemple:
        export APP_ENV=production
        export API_RATE_LIMIT_PER_MINUTE=200
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignore les variables non définies ici
    )

    # 📱 Application
    app_name: str = "Meal Recommender API"
    app_version: str = "2.0.0"
    app_description: str = "API intelligente de recommandation de repas par ingrédients"

    # 🌍 Environnement
    app_env: Literal["development", "staging", "production"] = "development"
    debug: bool = False

    # 🌐 Serveur API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = False  # True uniquement en dev

    # 🛡️ Sécurité & Rate Limiting
    api_rate_limit_per_minute: int = 100
    cors_origins: list[str] = ["*"]  # En production: ["https://monsite.com"]

    # 📊 Données
    data_dir: Path = Path(__file__).parent.parent.parent / "data"
    data_source: Literal["mealdb", "csv"] = "mealdb"
    csv_url: str = (
        "https://huggingface.co/spaces/BucKz96/csv_app/resolve/main/recipes_clean.csv"
    )
    mealdb_api_base: str = "https://www.themealdb.com/api/json/v1/1"
    mealdb_letters: str = "abcdefghijklmnopqrstuvwxyz"
    cache_ttl_seconds: int = 3600  # 1 heure

    # 📝 Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    log_format: Literal["json", "text"] = "json" if app_env == "production" else "text"

    @property
    def is_development(self) -> bool:
        """Vérifie si on est en environnement de développement."""
        return self.app_env == "development"

    @property
    def is_production(self) -> bool:
        """Vérifie si on est en production."""
        return self.app_env == "production"

    @property
    def csv_path(self) -> Path:
        """Chemin vers le fichier CSV local."""
        if self.data_source == "mealdb":
            return self.data_dir / "recipes_mealdb.csv"
        return self.data_dir / "recipes_clean.csv"


@lru_cache
def get_settings() -> Settings:
    """Retourne les paramètres (singleton pattern avec cache).

    Le décorateur @lru_cache garantit que la configuration
    est chargée une seule fois, même si cette fonction est
    appelée plusieurs fois.

    Returns:
        Settings: Instance unique des paramètres
    """
    return Settings()
