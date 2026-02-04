"""Utilitaires pour l'application Streamlit.

Fonctions d'aide pour la sécurité, le formatage et la validation.
"""

import hashlib
import html
from typing import Any


def safe_html_escape(text: Any) -> str:
    """Échappe le HTML pour éviter les injections XSS.
    
    Args:
        text: Texte à échapper (peut être any type)
        
    Returns:
        Texte échappé safe pour HTML
    """
    if text is None:
        return ""
    return html.escape(str(text))


def generate_image_seed(seed_source: str) -> str:
    """Génère un hash pour les images placeholder.
    
    Args:
        seed_source: Source du seed (nom de recette, etc.)
        
    Returns:
        Hash hexadécimal de 12 caractères
    """
    return hashlib.md5(seed_source.encode("utf-8")).hexdigest()[:12]


def fallback_image_url(seed_source: str, width: int = 400, height: int = 300) -> str:
    """Génère une URL d'image de fallback.
    
    Args:
        seed_source: Source pour le seed (garantit cohérence)
        width: Largeur de l'image
        height: Hauteur de l'image
        
    Returns:
        URL Picsum Photos avec seed déterministe
    """
    seed = generate_image_seed(seed_source)
    return f"https://picsum.photos/seed/{seed}/{width}/{height}"


def sanitize_image_url(url: Any, fallback_seed: str = "default") -> str:
    """Nettoie et valide une URL d'image.
    
    - Convertit HTTP en HTTPS
    - Filtre les domaines problématiques
    - Retourne fallback si invalide
    
    Args:
        url: URL à nettoyer
        fallback_seed: Seed pour l'image de remplacement
        
    Returns:
        URL safe ou fallback
    """
    if not isinstance(url, str):
        return fallback_image_url(fallback_seed)

    url = url.strip()

    # Valeurs invalides connues
    if url.lower() in ("nan", "none", "null", ""):
        return fallback_image_url(fallback_seed)

    # Domaines bloqués (images qui ne chargent pas)
    blocked_domains = ["media-allrecipes.com"]
    if any(domain in url for domain in blocked_domains):
        return fallback_image_url(fallback_seed)

    # Force HTTPS
    if url.startswith("http://"):
        url = url.replace("http://", "https://", 1)

    # Vérifie que c'est bien une URL
    if not url.startswith("https://"):
        return fallback_image_url(fallback_seed)

    return url


def format_ingredients_list(ingredients: Any, max_display: int = 3) -> list[str]:
    """Formate une liste d'ingrédients pour l'affichage.
    
    Args:
        ingredients: Liste d'ingrédients ou string
        max_display: Nombre max à afficher avant "+X more"
        
    Returns:
        Liste formatée pour affichage
    """
    if not ingredients:
        return []

    if isinstance(ingredients, str):
        # Parse string séparée par virgules
        ingredients = [i.strip() for i in ingredients.split(",") if i.strip()]

    if not isinstance(ingredients, list):
        return []

    result = []
    for i, ing in enumerate(ingredients[:max_display]):
        result.append(safe_html_escape(str(ing)))

    # Ajoute le compteur si plus d'ingrédients
    remaining = len(ingredients) - max_display
    if remaining > 0:
        result.append(f"+{remaining} more")

    return result


def truncate_text(text: Any, max_length: int = 100, suffix: str = "...") -> str:
    """Tronque un texte à une longueur maximale.
    
    Args:
        text: Texte à tronquer
        max_length: Longueur maximale
        suffix: Suffixe à ajouter si tronqué
        
    Returns:
        Texte tronqué
    """
    if text is None:
        return ""

    text_str = str(text)
    if len(text_str) <= max_length:
        return text_str

    return text_str[:max_length - len(suffix)] + suffix
