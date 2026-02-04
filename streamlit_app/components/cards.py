"""Cartes de repas avec modal."""

from typing import Any

import streamlit as st

from streamlit_app.favorites import favorite_button_icon
from streamlit_app.utils import fallback_image_url, safe_html_escape, sanitize_image_url

RESULTS_PER_ROW = 3


def render_meal_cards(meals: list[dict[str, Any]]) -> None:
    """Affiche les cartes en grille."""
    if not meals:
        st.info("Aucune recette trouvée. Essayez d'autres ingrédients.")
        return

    rows = (len(meals) + RESULTS_PER_ROW - 1) // RESULTS_PER_ROW
    for row in range(rows):
        cols = st.columns(RESULTS_PER_ROW, gap="small")
        for idx in range(RESULTS_PER_ROW):
            meal_idx = row * RESULTS_PER_ROW + idx
            if meal_idx >= len(meals):
                continue
            with cols[idx]:
                render_meal_card(meals[meal_idx], f"{row}_{idx}")


@st.dialog("Détails de la recette", width="large")
def show_meal_details(meal: dict[str, Any]) -> None:
    """Affiche les détails dans une modal."""
    meal_name = meal.get("name", "Recette")
    cuisine = meal.get("cuisine", "International")
    image_url = sanitize_image_url(meal.get("image"), meal_name)
    ingredients = meal.get("ingredients") or []
    nutritions = meal.get("nutritions") or {}

    # Image
    st.image(image_url, use_container_width=True)

    # Titre et badges
    st.subheader(meal_name)

    cols = st.columns(3)
    with cols[0]:
        st.metric("Cuisine", cuisine.title())
    with cols[1]:
        st.metric("Ingrédients", len(ingredients))
    with cols[2]:
        calories = nutritions.get("calories", "N/A")
        cal_display = f"{calories} kcal" if isinstance(calories, (int, float)) else calories
        st.metric("Calories", cal_display)

    st.divider()

    # Ingrédients
    st.markdown("**Ingrédients:**")
    if ingredients:
        st.write(", ".join(ingredients))
    else:
        st.write("Non spécifié")

    # Nutrition
    st.markdown("**Valeurs nutritionnelles:**")
    nutri_cols = st.columns(4)
    with nutri_cols[0]:
        st.metric("Protéines", f"{nutritions.get('protein', 0)}g")
    with nutri_cols[1]:
        st.metric("Glucides", f"{nutritions.get('carbohydrates', 0)}g")
    with nutri_cols[2]:
        st.metric("Lipides", f"{nutritions.get('fat', 0)}g")
    with nutri_cols[3]:
        st.metric("Fibres", f"{nutritions.get('fiber', 0)}g")

    st.divider()

    # Bouton favoris dans la modal
    if st.button("⭐ Ajouter aux favoris", use_container_width=True):
        from streamlit_app.favorites import add_to_favorites
        add_to_favorites(meal)
        st.rerun()


def render_meal_card(meal: dict[str, Any], key_suffix: str) -> None:
    """Affiche une carte avec boutons intégrés."""
    meal_name = meal.get("name", "Recette")
    cuisine = meal.get("cuisine", "International")
    category = meal.get("dish_type") or ""
    ingredients = meal.get("ingredients") or []
    if not isinstance(ingredients, list):
        ingredients = []

    image_url = sanitize_image_url(meal.get("image"), meal_name)
    fallback = fallback_image_url(meal_name)

    # NOTE: selected_meal_name pourrait être utilisé pour highlight

    # Tags
    tags_html = ""
    if ingredients:
        tag_style = "background:#eef2ff;color:#1d4ed8;padding:2px 8px;border-radius:999px;font-size:0.7rem;margin-right:4px;"  # noqa: E501
        more_style = "background:#f1f5f9;color:#64748b;padding:2px 8px;border-radius:999px;font-size:0.7rem;"  # noqa: E501
        tags = [f'<span style="{tag_style}">{safe_html_escape(i)}</span>' for i in ingredients[:2]]
        if len(ingredients) > 2:
            tags.append(f'<span style="{more_style}">+{len(ingredients)-2}</span>')
        tags_html = "".join(tags)

    # HTML de la carte
    card_style = "background:white;border-radius:16px;overflow:hidden;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.06);margin-bottom:8px;"  # noqa: E501
    img_container = "position:relative;height:140px;overflow:hidden;"
    img_style = "width:100%;height:100%;object-fit:cover;"
    cuisine_style = "position:absolute;top:8px;left:8px;background:rgba(255,255,255,0.95);padding:4px 10px;border-radius:999px;font-size:0.7rem;font-weight:600;color:#1e40af;"  # noqa: E501
    title_style = "font-weight:600;color:#1e293b;margin-bottom:4px;font-size:0.95rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;"  # noqa: E501

    st.markdown(f"""
    <div style="{card_style}">
        <div style="{img_container}">
            <img src="{image_url}" style="{img_style}" onerror="this.src='{fallback}'"/>
            <span style="{cuisine_style}">{safe_html_escape(cuisine)}</span>
        </div>
        <div style="padding:12px;">
            <div style="{title_style}">{safe_html_escape(meal_name)}</div>
            <div style="font-size:0.8rem;color:#64748b;margin-bottom:8px;">
                {safe_html_escape(category)} · {len(ingredients)} ingr.
            </div>
            <div>{tags_html}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Boutons d'action (en dehors du HTML pour fonctionnalité)
    btn_cols = st.columns([1, 1, 3])
    with btn_cols[0]:
        favorite_button_icon(meal, key_suffix)
    with btn_cols[1]:
        if st.button("+", key=f"plus_{key_suffix}_{meal_name}", help="Voir détails"):
            show_meal_details(meal)
