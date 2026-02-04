"""Gestionnaire de cache pour l'application.

Pourquoi un cache manager ?
- Évite de recharger le CSV à chaque requête (performance x1000)
- Pattern Singleton : une seule instance partagée
- Cache avec TTL (Time To Live) pour données fraîches
- Thread-safe pour production
"""
import threading
import time
from typing import Any, Generic, TypeVar

from src.core.logging import get_logger

T = TypeVar("T")
logger = get_logger(__name__)


class CacheEntry(Generic[T]):
    """Entrée de cache avec TTL.

    Attributes:
        value: Valeur stockée
        timestamp: Moment de création (epoch)
        ttl_seconds: Durée de vie en secondes
    """

    def __init__(self, value: T, ttl_seconds: int):
        self.value = value
        self.timestamp = time.time()
        self.ttl_seconds = ttl_seconds

    @property
    def is_expired(self) -> bool:
        """Vérifie si l'entrée a expiré."""
        return (time.time() - self.timestamp) > self.ttl_seconds


class CacheManager:
    """Gestionnaire de cache thread-safe (Pattern Singleton).

    Ce pattern garantit qu'une seule instance existe dans toute l'app.
    Le cache est partagé entre toutes les requêtes.

    Usage:
        >>> cache = CacheManager()
        >>> cache.set("meals", data, ttl=3600)
        >>> meals = cache.get("meals")

    Thread-safety:
        - Lock sur chaque opération
        - Accès concurrent sans corruption
    """

    _instance: "CacheManager | None" = None
    _lock: threading.Lock = threading.Lock()
    _cache: dict[str, CacheEntry[Any]]
    _cache_lock: threading.RLock

    def __new__(cls) -> "CacheManager":
        """Crée ou retourne l'instance unique (Singleton)."""
        if cls._instance is None:
            with cls._lock:
                # Double-check locking (pattern thread-safe)
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._cache = {}
                    cls._instance._cache_lock = threading.RLock()
                    logger.debug("CacheManager initialisé")
        return cls._instance

    def get(self, key: str) -> Any | None:
        """Récupère une valeur du cache.

        Args:
            key: Clé de l'entrée

        Returns:
            La valeur si présente et non expirée, None sinon
        """
        with self._cache_lock:
            entry = self._cache.get(key)

            if entry is None:
                return None

            if entry.is_expired:
                # Auto-cleanup des entrées expirées
                del self._cache[key]
                logger.debug(f"Cache expiré pour '{key}'")
                return None

            logger.debug(f"Cache hit pour '{key}'")
            return entry.value

    def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        """Stocke une valeur dans le cache.

        Args:
            key: Clé unique
            value: Valeur à stocker
            ttl_seconds: Durée de vie (0 = illimité, déconseillé)
        """
        with self._cache_lock:
            self._cache[key] = CacheEntry(value, ttl_seconds)
            logger.debug(f"Cache set pour '{key}' (TTL: {ttl_seconds}s)")

    def delete(self, key: str) -> bool:
        """Supprime une entrée du cache.

        Returns:
            True si supprimé, False si inexistant
        """
        with self._cache_lock:
            if key in self._cache:
                del self._cache[key]
                logger.debug(f"Cache supprimé pour '{key}'")
                return True
            return False

    def clear(self) -> None:
        """Vide complètement le cache (utile pour tests)."""
        with self._cache_lock:
            self._cache.clear()
            logger.info("Cache complètement vidé")

    def get_stats(self) -> dict[str, int]:
        """Retourne des statistiques sur le cache.

        Returns:
            Dict avec nombre d'entrées et entrées actives
        """
        with self._cache_lock:
            total = len(self._cache)
            active = sum(1 for entry in self._cache.values() if not entry.is_expired)
            expired = total - active

            return {
                "total_entries": total,
                "active_entries": active,
                "expired_entries": expired,
            }


# Instance globale pour import facile
cache = CacheManager()
