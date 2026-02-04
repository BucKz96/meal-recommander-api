"""Application Meal Recommender - Version simplifiée."""

from typing import Any

import requests
import streamlit as st

from streamlit_app.api_client import API_FETCH_LIMIT, fetch_meals
from streamlit_app.components.cards import render_meal_cards
from streamlit_app.components.layout import render_custom_css, render_hero, render_search_form
from streamlit_app.favorites import display_favorites
from streamlit_app.filters import filter_meals, render_filters
from streamlit_app.history import add_to_history, display_history_sidebar


def init_state() -> None:
    """Initialise le state."""
    defaults: dict[str, Any] = {
        "last_ingredients": (),
        "last_results": [],
        "selected_meal": None,
        "selected_meal_name": None,
        "ingredients_input": "",
        "trigger_history_submit": False,
    }
    for key, val in defaults.items():
        st.session_state.setdefault(key, val)


def main() -> None:
    """Point d'entrée."""
    st.set_page_config(page_title="Meal Recommender", page_icon="🍽️", layout="wide")

    init_state()
    render_custom_css()

    # Sidebar
    st.sidebar.markdown("## Menu")
    nav = st.sidebar.radio("", ["Rechercher", "Favoris"], label_visibility="collapsed")
    display_history_sidebar()

    # Page Favoris
    if nav == "Favoris":
        st.markdown("## ⭐ Mes Favoris")
        display_favorites()
        return

    # Page Recherche
    render_hero()

    # Formulaire
    ingredients_input, submitted = render_search_form()

    # Déclenchement
    history_trigger = st.session_state.pop("trigger_history_submit", False)
    should_fetch = submitted or history_trigger

    meals: list[dict[str, Any]] = []

    if should_fetch:
        ingredients = tuple(i.strip() for i in ingredients_input.split(",") if i.strip())

        if not ingredients:
            st.warning("Ajoutez au moins un ingrédient.")
            meals = st.session_state.get("last_results", [])
        else:
            try:
                with st.spinner("Recherche en cours..."):
                    meals = fetch_meals(ingredients, limit=API_FETCH_LIMIT)

                st.session_state["last_ingredients"] = ingredients
                st.session_state["last_results"] = meals
                add_to_history(list(ingredients), len(meals))

            except requests.RequestException as e:
                st.error(f"Erreur API: {e}")
                meals = st.session_state.get("last_results", [])
    else:
        meals = st.session_state.get("last_results", [])

    # Résultats
    if not meals:
        st.info("👆 Entrez des ingrédients et cliquez sur Rechercher")
        return

    # Filtres
    name_query, cuisine, limit = render_filters(meals)
    filtered = filter_meals(meals, name_query, cuisine, limit)

    # Header résultats
    header_style = "display:flex;justify-content:space-between;align-items:center;padding:12px 16px;background:white;border-radius:12px;border:1px solid #e2e8f0;margin-bottom:16px;"  # noqa: E501
    st.markdown(f"""
    <div style="{header_style}">
        <div>
            <span style="font-size:1.8rem;font-weight:700;color:#2563eb;">{len(filtered)}</span>
            <span style="color:#64748b;font-size:0.9rem;margin-left:4px;">recettes</span>
        </div>
        <div style="color:#64748b;font-size:0.85rem;">
            {min(len(filtered), limit)} sur {len(meals)}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Affichage cartes
    render_meal_cards(filtered)


if __name__ == "__main__":
    main()
