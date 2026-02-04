"""Application Streamlit Meal Recommender.

Point d'entrée principal qui orchestre les composants.
"""

from typing import Any

import requests
import streamlit as st

from streamlit_app.api_client import API_FETCH_LIMIT, fetch_meals
from streamlit_app.components.cards import render_meal_cards
from streamlit_app.components.details import render_details_panel
from streamlit_app.components.layout import (
    render_custom_css,
    render_empty_state,
    render_footer,
    render_hero,
    render_results_header,
)
from streamlit_app.favorites import display_favorites
from streamlit_app.filters import (
    ensure_state_defaults,
    filter_meals,
    render_filters,
    render_search_form,
)
from streamlit_app.history import add_to_history, display_history_sidebar
from streamlit_app.theme import apply_theme, theme_toggle


def main() -> None:
    """Point d'entrée principal de l'application."""
    # Configuration de la page
    st.set_page_config(
        page_title="Meal Recommender",
        page_icon="🍽️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Initialisation
    ensure_state_defaults()
    apply_theme(st.session_state.get("theme", "light"))
    render_custom_css()

    # Sidebar navigation
    st.sidebar.markdown("## Navigation")
    nav_choice = st.sidebar.radio(
        "Navigation",
        ["Discover", "Favorites"],
        label_visibility="collapsed",
    )
    
    with st.sidebar:
        theme_toggle()
    
    display_history_sidebar()

    # Page Favorites
    if nav_choice == "Favorites":
        st.markdown("## ⭐ Favorites")
        display_favorites()
        render_details_panel()
        return

    # Page Discover (main)
    render_hero()
    
    # Formulaire de recherche
    ingredients_input, submitted = render_search_form()

    # Gestion de l'historique
    history_triggered = st.session_state.pop("trigger_history_submit", False)
    should_fetch = submitted or history_triggered

    # Récupération des données
    meals: list[dict[str, Any]] = []
    
    if should_fetch:
        ingredients = tuple(i.strip() for i in ingredients_input.split(",") if i.strip())

        if not ingredients:
            st.warning("Ajoute au moins un ingrédient avant de lancer la recherche.")
            meals = st.session_state.get("last_results", [])
        else:
            try:
                with st.spinner("Searching for recipes..."):
                    meals = fetch_meals(ingredients, limit=API_FETCH_LIMIT)
                
                # Mise à jour du state
                st.session_state["last_ingredients"] = ingredients
                st.session_state["last_results"] = meals
                st.session_state["selected_meal"] = None
                st.session_state["selected_meal_name"] = None
                
                # Ajout à l'historique
                add_to_history(list(ingredients), len(meals))
                
            except requests.RequestException as exc:
                st.error(f"Unable to reach the API: {exc}")
                meals = st.session_state.get("last_results", [])
    else:
        meals = st.session_state.get("last_results", [])

    # Affichage des résultats
    if not meals:
        render_empty_state()
        render_details_panel()
        return

    # Filtres
    name_query, cuisine, limit = render_filters(meals)
    filtered_meals = filter_meals(meals, name_query, cuisine, limit)

    # En-tête des résultats
    render_results_header(len(filtered_meals), len(meals), limit)

    # Cartes de repas
    render_meal_cards(filtered_meals)
    
    # Détails du repas sélectionné
    render_details_panel()

    # Footer
    render_footer()


if __name__ == "__main__":
    main()
