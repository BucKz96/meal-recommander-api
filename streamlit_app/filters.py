"""Gestion des filtres."""

from typing import Any

import streamlit as st


def render_filters(meals: list[dict[str, Any]]) -> tuple[str, str, int]:
    """Affiche les filtres dans la sidebar."""
    with st.sidebar.expander("Filtres", expanded=True):
        name_query = st.text_input("🔎 Rechercher", key="filter_name")

        cuisine_values = [
            str(cuisine)
            for cuisine in (m.get("cuisine") for m in meals)
            if isinstance(cuisine, str) and cuisine
        ]
        cuisine_options = sorted(set(cuisine_values))

        cuisine = st.selectbox(
            "🌍 Cuisine",
            ["Toutes", *cuisine_options],
            key="filter_cuisine",
        )

        limit = st.slider("Max", 6, 60, 24, step=6, key="filter_limit")

    return name_query.strip().lower(), cuisine, limit


def filter_meals(
    meals: list[dict[str, Any]],
    name_query: str,
    cuisine: str,
    limit: int,
) -> list[dict[str, Any]]:
    """Filtre les repas."""
    filtered = []

    for meal in meals:
        name = str(meal.get("name", ""))
        if name_query and name_query not in name.lower():
            continue
        if cuisine != "Toutes" and meal.get("cuisine") != cuisine:
            continue
        filtered.append(meal)

    return filtered[:limit]


def ensure_state_defaults() -> None:
    """Initialise le session_state."""
    st.session_state.setdefault("last_ingredients", ())
    st.session_state.setdefault("last_results", [])
    st.session_state.setdefault("selected_meal", None)
    st.session_state.setdefault("selected_meal_name", None)
    st.session_state.setdefault("ingredients_input", "")
    st.session_state.setdefault("trigger_history_submit", False)
    st.session_state.setdefault("filter_limit", 24)
