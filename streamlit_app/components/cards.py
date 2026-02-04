"""Composants pour l'affichage des cartes de repas."""

from typing import Any

import streamlit as st

from streamlit_app.favorites import favorite_button_icon
from streamlit_app.utils import fallback_image_url, safe_html_escape, sanitize_image_url

RESULTS_PER_ROW = 3


def render_meal_cards(meals: list[dict[str, Any]]) -> None:
    """Affiche les cartes de repas dans une grille responsive."""
    if not meals:
        st.markdown(
            """
            <div class="warning-message">
                <strong>Aucune recette trouvée.</strong><br>
                Essayez d'autres ingrédients ou filtres.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    rows = (len(meals) + RESULTS_PER_ROW - 1) // RESULTS_PER_ROW
    for row in range(rows):
        columns = st.columns(RESULTS_PER_ROW, gap="small")
        for idx in range(RESULTS_PER_ROW):
            meal_index = row * RESULTS_PER_ROW + idx
            if meal_index >= len(meals):
                continue
            meal = meals[meal_index]
            with columns[idx]:
                render_meal_card(meal, key_suffix=f"{row}_{idx}")


def render_meal_card(meal: dict[str, Any], key_suffix: str) -> None:
    """Affiche une carte de repas avec boutons intégrés dans le footer."""
    meal_name = meal.get("name", "Recipe")
    meal_name_safe = safe_html_escape(meal_name)
    cuisine = meal.get("cuisine", "International")
    category = meal.get("dish_type") or ""
    ingredients = meal.get("ingredients") or []
    if not isinstance(ingredients, list):
        ingredients = []

    image_url = sanitize_image_url(meal.get("image"), meal_name)
    fallback = fallback_image_url(f"{meal_name}-fallback")
    safe_fallback = fallback.replace("'", "\\'")

    selected_name = st.session_state.get("selected_meal_name")
    card_classes = "meal-card"
    if selected_name and selected_name == meal_name:
        card_classes += " meal-card--active"

    # Tags ingrédients
    ingredients_html = ""
    if ingredients:
        tags = [
            f'<span class="ingredient-tag">{safe_html_escape(ingredient)}</span>'
            for ingredient in ingredients[:2]
        ]
        if len(ingredients) > 2:
            tags.append(f'<span class="ingredient-tag">+{len(ingredients) - 2}</span>')
        ingredients_html = '<div class="ingredients-list">' + "".join(tags) + "</div>"

    # Meta info
    meta_parts = []
    if category:
        meta_parts.append(safe_html_escape(category))
    if ingredients:
        meta_parts.append(f"{len(ingredients)} ingr.")
    meta_html = '<div class="meal-meta">' + " · ".join(meta_parts) + "</div>" if meta_parts else ""

    # Structure HTML complète de la carte
    card_html = f"""
    <div class="meal-card-wrapper">
        <div class="{card_classes}">
            <div class="meal-image-container">
                <img src="{image_url}" alt="{meal_name_safe}" onerror="this.onerror=null;this.src='{safe_fallback}';"/>
                <div class="meal-badge">{safe_html_escape(cuisine)}</div>
            </div>
            <div class="meal-content">
                <div class="meal-title">{meal_name_safe}</div>
                {meta_html}
                {ingredients_html}
            </div>
        </div>
    </div>
    """.strip()

    # Affichage de la carte
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Boutons dans une ligne compacte sous la carte mais visuellement attachés
    # Utilisation de colonnes pour alignement
    btn_cols = st.columns([1, 1, 3])  # 2 colonnes pour boutons, 1 pour espace
    
    with btn_cols[0]:
        # Bouton favoris (étoile)
        favorite_button_icon(meal, key_suffix=f"fav_{key_suffix}")
    
    with btn_cols[1]:
        # Bouton détails (+)
        if st.button(
            "+",
            key=f"det_{key_suffix}_{meal_name}",
            help="Voir détails",
            use_container_width=True,
        ):
            st.session_state["selected_meal"] = meal
            st.session_state["selected_meal_name"] = meal_name
            st.rerun()
