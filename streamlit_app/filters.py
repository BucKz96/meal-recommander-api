"""Gestion des filtres et du formulaire de recherche."""

from typing import Any

import streamlit as st

DEFAULT_INGREDIENTS = "poulet, riz, tomate"


def render_search_form() -> tuple[str, bool]:
    """Affiche le formulaire de recherche compact.
    
    Returns:
        Tuple (ingredients_input, submitted)
    """
    with st.form("search_form", clear_on_submit=False):
        st.markdown('<div class="search-section">', unsafe_allow_html=True)
        st.markdown('<div class="search-shell">', unsafe_allow_html=True)

        cols = st.columns([5, 2])
        with cols[0]:
            ingredients_input = st.text_input(
                "Ingredients",
                key="ingredients_input",
                placeholder="Ex: poulet, riz, tomate...",
                label_visibility="collapsed",
            )
        with cols[1]:
            submitted = st.form_submit_button("🔍 Rechercher", use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    return ingredients_input, submitted


def render_filters(meals: list[dict[str, Any]]) -> tuple[str, str, int]:
    """Affiche les filtres dans la sidebar.
    
    Args:
        meals: Liste des repas pour extraire les options
        
    Returns:
        Tuple (name_query, cuisine, limit)
    """
    with st.sidebar.expander("Filtres essentiels", expanded=True):
        st.caption("Affinez rapidement les suggestions affichées ci-dessous.")

        name_query = st.text_input("🔎 Rechercher dans les résultats", key="filter_name")

        # Extraction des cuisines uniques
        cuisine_values: list[str] = [
            str(cuisine)
            for cuisine in (m.get("cuisine") for m in meals)
            if isinstance(cuisine, str) and cuisine
        ]
        cuisine_options: list[str] = sorted(set(cuisine_values))

        cuisine = st.selectbox(
            "🌍 Cuisine",
            ["Toutes"] + cuisine_options,
            key="filter_cuisine",
        )

        limit = st.slider("Nombre maximum", 6, 60, 24, step=6, key="filter_limit")

    return name_query.strip().lower(), cuisine, limit


def filter_meals(
    meals: list[dict[str, Any]],
    name_query: str,
    cuisine: str,
    limit: int,
) -> list[dict[str, Any]]:
    """Filtre les repas selon les critères.
    
    Args:
        meals: Liste complète des repas
        name_query: Recherche textuelle sur le nom
        cuisine: Filtre de cuisine (ou "Toutes")
        limit: Nombre maximum de résultats
        
    Returns:
        Liste filtrée et limitée
    """
    filtered: list[dict[str, Any]] = []

    for meal in meals:
        name = str(meal.get("name", ""))
        if name_query and name_query not in name.lower():
            continue
        if cuisine != "Toutes" and meal.get("cuisine") != cuisine:
            continue
        filtered.append(meal)

    return filtered[:limit]


def ensure_state_defaults() -> None:
    """Initialise les valeurs par défaut du session_state."""
    st.session_state.setdefault("last_ingredients", tuple())
    st.session_state.setdefault("last_results", [])
    st.session_state.setdefault("selected_meal", None)
    st.session_state.setdefault("selected_meal_name", None)
    st.session_state.setdefault("ingredients_input", DEFAULT_INGREDIENTS)
    st.session_state.setdefault("trigger_history_submit", False)
    st.session_state.setdefault("filter_limit", 24)
