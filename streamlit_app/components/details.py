"""Composant pour l'affichage du panneau de détails d'un repas."""


import streamlit as st

from streamlit_app.favorites import favorite_button
from streamlit_app.utils import safe_html_escape, sanitize_image_url


def render_details_panel() -> None:
    """Affiche le panneau de détails du repas sélectionné."""
    meal = st.session_state.get("selected_meal")
    if not meal:
        return

    meal_name = str(meal.get("name", "Recipe"))
    if not st.session_state.get("selected_meal_name"):
        st.session_state["selected_meal_name"] = meal_name

    meal_name_safe = safe_html_escape(meal_name)
    cuisine = safe_html_escape(meal.get("cuisine") or "International")
    dish_type = safe_html_escape(meal.get("dish_type"))
    category_value = safe_html_escape(meal.get("category"))
    diet_type = safe_html_escape(meal.get("diet_type") or "Unspecified")
    prep_time = safe_html_escape(meal.get("prep_time") or "N/A")

    ingredients = meal.get("ingredients") or []
    if not isinstance(ingredients, list):
        ingredients = []

    image_url = sanitize_image_url(meal.get("image"), meal_name)
    nutritions = meal.get("nutritions") or {}

    # Construction des items nutritionnels
    nutrition_items: list[str] = []
    nutrition_schema = [
        ("Calories", "calories", "kcal"),
        ("Protéines", "protein", "g"),
        ("Glucides", "carbohydrates", "g"),
        ("Lipides", "fat", "g"),
    ]
    for label, key, unit in nutrition_schema:
        value = nutritions.get(key)
        if value in (None, ""):
            value = 0
        nutrition_items.append(
            f"<div class='nutrition-item'><span>{label}</span><strong>{value} {unit}</strong></div>"
        )

    ingredient_list = (
        "".join(f"<li>{safe_html_escape(ing)}</li>" for ing in ingredients)
        or "<li>Aucun ingrédient listé</li>"
    )

    # Badges de métadonnées
    badge_meta = [cuisine]
    if category_value:
        badge_meta.append(category_value)
    if dish_type:
        badge_meta.append(dish_type)
    if diet_type:
        badge_meta.append(diet_type)

    meta_html = "".join(f"<span>{item}</span>" for item in badge_meta)

    detail_html = f"""
    <div class="details-panel">
        <div class="details-header">
            <div>
                <p class="eyebrow">Recette sélectionnée</p>
                <h3>{meal_name_safe}</h3>
                <div class="details-meta">{meta_html}</div>
            </div>
            <div class="details-meta">
                <span>{prep_time}</span>
            </div>
        </div>
        <div class="details-body">
            <div class="details-image">
                <img src="{image_url}" alt="{meal_name_safe}" />
            </div>
            <div class="details-info">
                <h4>Ingrédients</h4>
                <ul>{ingredient_list}</ul>
                <h4>Valeurs nutritionnelles</h4>
                <div class="details-nutrition">{ "".join(nutrition_items) }</div>
            </div>
        </div>
    </div>
    """

    st.markdown(detail_html, unsafe_allow_html=True)

    # Boutons d'action
    button_cols = st.columns([2, 1])
    with button_cols[0]:
        favorite_button(meal, key_suffix="details", show_label=True)
    with button_cols[1]:
        if st.button("Masquer les détails", use_container_width=True):
            st.session_state["selected_meal"] = None
            st.session_state["selected_meal_name"] = None
