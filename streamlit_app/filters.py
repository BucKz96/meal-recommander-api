"""Filtres."""

from typing import Any

import streamlit as st


def render_filters(meals: list[dict[str, Any]]) -> tuple[str, str, int]:
    """Filtres sidebar."""
    with st.sidebar.expander("Filtres", expanded=True):
        name = st.text_input("🔎 Nom", key="f_name")

        cuisines = sorted({str(m.get("cuisine")) for m in meals if m.get("cuisine")})
        cuisine = st.selectbox("🌍 Cuisine", ["Toutes", *cuisines], key="f_cuisine")

        limit = st.slider("Max", 6, 60, 24, 6, key="f_limit")

    return name.strip().lower(), cuisine, limit


def filter_meals(meals: list[dict[str, Any]], name: str, cuisine: str, limit: int) -> list[dict[str, Any]]:
    """Filtre les repas."""
    result = []
    for m in meals:
        if name and name not in str(m.get("name", "")).lower():
            continue
        if cuisine != "Toutes" and m.get("cuisine") != cuisine:
            continue
        result.append(m)
    return result[:limit]
