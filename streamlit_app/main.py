"""Streamlit UI for the Meal Recommender platform.

This version focuses on a smoother UX:
- Theming, favorites and history modules are wired in
- API calls are cached and triggered through a debounced form
- Details open inside a modal with a consistent button inside each card
- CSS clean-up for a modern but lighter layout
"""

from __future__ import annotations

import hashlib
import html
import os
from typing import Any

import requests
import streamlit as st

from favorites import display_favorites, favorite_button
from history import add_to_history, display_history_sidebar
from theme import apply_theme, theme_toggle

API_URL = os.getenv("API_URL", "http://localhost:8000")
RESULTS_PER_ROW = 3
API_FETCH_LIMIT = 60
DEFAULT_INGREDIENTS = "Chicken, Rice, Tomato"


def fallback_image_url(seed_source: str) -> str:
    digest = hashlib.md5(seed_source.encode("utf-8")).hexdigest()[:12]
    return f"https://picsum.photos/seed/{digest}/400/300"


CUSTOM_CSS = """
<style>
    .stApp {
        background: var(--app-background, radial-gradient(circle at top, #f8fbff 0%, #ecf2ff 55%, #e2e8f0 100%));
        min-height: 100vh;
    }

    .hero {
        position: relative;
        border-radius: 36px;
        padding: 70px 30px 80px;
        margin-bottom: 56px;
        background: url("https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=1600&q=80")
            center/cover no-repeat;
        color: #fff;
        text-align: center;
        overflow: hidden;
        box-shadow: 0 30px 60px rgba(15, 23, 42, 0.25);
    }

    .hero::after {
        content: "";
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at top, rgba(15, 23, 42, 0.55), rgba(15, 23, 42, 0.15));
    }

    .hero-content {
        position: relative;
        max-width: 640px;
        margin: 0 auto;
    }

    .hero .eyebrow {
        letter-spacing: 0.4em;
        text-transform: uppercase;
        font-size: 0.85rem;
        color: rgba(255,255,255,0.8);
    }

    .hero h1 {
        font-size: clamp(2.8rem, 4.5vw, 3.6rem);
        font-weight: 800;
        margin: 0.35rem 0 0.75rem;
    }

    .hero p {
        font-size: 1.1rem;
        margin: 0 auto;
        line-height: 1.6;
        color: rgba(255,255,255,0.9);
    }

    .search-section {
        max-width: 360px;
        margin: -60px auto 24px;
        text-align: center;
    }

    .search-shell {
        background: var(--card-bg);
        border-radius: 24px;
        border: 1.5px solid var(--card-border);
        padding: 20px 22px;
        box-shadow: 0 30px 60px rgba(15, 23, 42, 0.12);
    }

    .search-shell .stTextInput > div > div > input {
        font-size: 0.95rem;
        padding: 0.75rem 1rem;
        border-radius: 14px;
        border: 1px solid var(--card-border);
    }

    .search-shell .stButton > button {
        margin: 1rem auto 0;
        font-size: 0.95rem;
        padding: 0.75rem 0;
        border-radius: 999px;
        width: 100%;
        max-width: 220px;
    }

    .stButton > button {
        background: linear-gradient(120deg, var(--primary), var(--accent));
        border: none;
        color: var(--button-text, #fff);
        font-weight: 600;
        border-radius: 999px;
        padding: 0.6rem 1.4rem;
        box-shadow: 0 12px 24px rgba(37, 99, 235, 0.25);
    }

    .results-header {
        display: flex;
        flex-wrap: wrap;
        gap: 16px;
        align-items: center;
        justify-content: space-between;
        padding: 24px;
        border-radius: 20px;
        background: var(--card-bg);
        border: 1.5px solid var(--card-border);
        box-shadow: 0 20px 45px rgba(15, 23, 42, 0.08);
        margin-bottom: 24px;
    }

    .count-number {
        font-size: clamp(2rem, 4vw, 2.8rem);
        font-weight: 800;
        color: var(--primary);
    }

    .meal-card-wrapper {
        padding: 16px;
        display: flex;
        height: 100%;
    }

    .meal-card {
        background: var(--card-bg);
        border-radius: 24px;
        overflow: hidden;
        border: 1.5px solid var(--card-border);
        box-shadow: 0 16px 35px rgba(15, 23, 42, 0.12);
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        display: flex;
        flex-direction: column;
        position: relative;
        width: 100%;
    }

    .meal-card--active {
        border-color: var(--primary);
        box-shadow: 0 32px 60px rgba(37, 99, 235, 0.25);
    }

    .meal-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 30px 60px rgba(37, 99, 235, 0.2);
    }

    .meal-image-container {
        position: relative;
        height: 200px;
        overflow: hidden;
    }

    .meal-image-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.4s ease;
    }

    .meal-card:hover .meal-image-container img {
        transform: scale(1.08);
    }

    .meal-badge {
        position: absolute;
        top: 16px;
        left: 16px;
        background: rgba(248, 250, 255, 0.95);
        padding: 6px 14px;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--text-dark);
        border: 1px solid var(--card-border);
    }

    .meal-content {
        padding: 20px 22px 0;
        flex: 1;
        display: flex;
        flex-direction: column;
    }

    .meal-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--text-dark);
        margin-bottom: 10px;
        line-height: 1.3;
        min-height: 52px;
    }

    .meal-meta {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        color: var(--muted);
        font-size: 0.9rem;
        margin-bottom: 12px;
    }

    .ingredients-list {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 12px;
    }

    .ingredient-tag {
        background: var(--soft-bg);
        color: var(--primary);
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.8rem;
        border: 1px solid var(--card-border);
    }

    .card-actions {
        margin-top: 12px;
        padding: 12px 18px 18px;
        display: flex;
        gap: 10px;
        background: var(--card-bg);
        border-top: 1px solid var(--card-border);
    }

    .card-actions .stButton {
        flex: 1;
    }

    .card-actions .stButton > button {
        height: 34px;
        border-radius: 24px;
        font-size: 0.95rem;
        padding: 0;
    }

    .card-actions .stButton:first-child > button {
        background: #fff;
        border: 1px solid var(--card-border);
        color: var(--primary);
        box-shadow: none;
    }

    .card-actions .stButton:last-child > button {
        background: var(--primary);
        color: var(--button-text, #fff);
        border: none;
        box-shadow: 0 6px 14px rgba(37, 99, 235, 0.25);
    }

    .warning-message {
        background: linear-gradient(120deg, #eff6ff, #dbeafe);
        border-radius: 20px;
        padding: 24px;
        border: 1px solid var(--card-border);
        text-align: center;
        color: var(--text-dark);
    }

    .details-panel {
        background: var(--card-bg);
        border-radius: 28px;
        border: 1.5px solid var(--card-border);
        padding: 32px;
        box-shadow: 0 30px 60px rgba(15, 23, 42, 0.15);
        margin-top: 1rem;
    }

    .details-header {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        align-items: center;
        margin-bottom: 24px;
    }

    .details-header .eyebrow {
        letter-spacing: 0.2em;
        text-transform: uppercase;
        font-size: 0.75rem;
        color: var(--muted);
        margin-bottom: 4px;
    }

    .details-header h3 {
        margin: 0;
        font-size: clamp(1.4rem, 2.5vw, 2rem);
        color: var(--text-dark);
    }

    .details-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 10px;
        color: var(--muted);
    }

    .details-meta span {
        background: var(--soft-bg);
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 0.85rem;
        border: 1px solid var(--card-border);
    }

    .details-body {
        display: grid;
        grid-template-columns: 2fr 3fr;
        gap: 32px;
        align-items: start;
    }

    .details-image img {
        width: 100%;
        border-radius: 20px;
        object-fit: cover;
        border: 1px solid var(--card-border);
        box-shadow: 0 16px 40px rgba(15, 23, 42, 0.12);
    }

    .details-info h4 {
        margin-top: 0;
        margin-bottom: 12px;
        color: var(--text-dark);
    }

    .details-info ul {
        padding-left: 20px;
        margin-bottom: 24px;
    }

    .details-info li {
        margin-bottom: 6px;
        color: var(--text-dark);
    }

    .details-nutrition {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 12px;
    }

    .nutrition-item {
        background: var(--soft-bg);
        border-radius: 16px;
        padding: 12px 14px;
        border: 1px solid var(--card-border);
        text-align: center;
    }

    .nutrition-item span {
        display: block;
        font-size: 0.8rem;
        color: var(--muted);
        margin-bottom: 6px;
    }

    .nutrition-item strong {
        font-size: 1.1rem;
        color: var(--text-dark);
    }

    .footer {
        text-align: center;
        color: var(--muted);
        padding: 2rem 0;
    }

    @media (max-width: 1200px) {
        .hero {
            padding: 40px 24px;
        }
        .meal-card-wrapper {
            padding: 10px;
        }
        .details-body {
            grid-template-columns: 1fr;
        }
    }

    @media (max-width: 768px) {
        .results-header {
            flex-direction: column;
            align-items: flex-start;
        }
        .hero {
            text-align: center;
        }
        .meal-title {
            min-height: auto;
        }
        .card-actions {
            flex-direction: column;
        }
    }
</style>
"""


@st.cache_data(ttl=300, show_spinner=False)
def fetch_meals(ingredients: tuple[str, ...], limit: int | None = None) -> list[dict[str, Any]]:
    """Query the API once and cache the payload."""

    if ingredients:
        params: list[tuple[str, str]] = [("available_ingredients", ing) for ing in ingredients]
        url = f"{API_URL}/meals/by-ingredients"
    else:
        params = []
        url = f"{API_URL}/meals/all"

    if limit is not None:
        params.append(("limit", str(limit)))

    response = requests.get(url, params=params or None, timeout=15)
    response.raise_for_status()
    return response.json()


def render_filters(meals: list[dict[str, Any]]) -> tuple[str, str, int]:
    """Sidebar filters for name, cuisine and result limit."""

    with st.sidebar.expander("Filtres essentiels", expanded=True):
        st.caption("Affinez rapidement les suggestions affichées ci-dessous.")
        name_query = st.text_input("🔎 Rechercher dans les résultats", key="filter_name")

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
    filtered: list[dict[str, Any]] = []
    for meal in meals:
        name = str(meal.get("name", ""))
        if name_query and name_query not in name.lower():
            continue
        if cuisine != "Toutes" and meal.get("cuisine") != cuisine:
            continue
        filtered.append(meal)

    return filtered[:limit]


def render_meal_cards(meals: list[dict[str, Any]]) -> None:
    """Display recipe cards in a responsive grid."""

    if not meals:
        st.markdown(
            """
            <div class="warning-message">
                <strong>🍽️ No meals match your filters.</strong><br>
                Try tweaking the cuisine or adding fewer constraints.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    rows = (len(meals) + RESULTS_PER_ROW - 1) // RESULTS_PER_ROW
    for row in range(rows):
        columns = st.columns(RESULTS_PER_ROW, gap="medium")
        for idx in range(RESULTS_PER_ROW):
            meal_index = row * RESULTS_PER_ROW + idx
            if meal_index >= len(meals):
                continue
            meal = meals[meal_index]
            with columns[idx]:
                render_meal_card(meal, key_suffix=f"{row}_{idx}")


def render_meal_card(meal: dict[str, Any], key_suffix: str) -> None:
    meal_name = meal.get("name", "Recipe")
    meal_name_safe = html.escape(str(meal_name))
    cuisine = meal.get("cuisine", "International")
    category = meal.get("dish_type") or ""
    ingredients = meal.get("ingredients") or []
    if not isinstance(ingredients, list):
        ingredients = []

    image_url = sanitize_image(meal.get("image"), fallback_image_url(meal_name))
    fallback = fallback_image_url(f"{meal_name}-fallback")

    selected_name = st.session_state.get("selected_meal_name")
    card_classes = "meal-card"
    if selected_name and selected_name == meal_name:
        card_classes += " meal-card--active"

    card_html_start = [
        '<div class="meal-card-wrapper">',
        f'<div class="{card_classes}">',
        '<div class="meal-image-container">',
        f'<img src="{image_url}" alt="{meal_name_safe}" onerror="this.onerror=null;this.src=\'{fallback}\';"/>',
        f'<div class="meal-badge">{html.escape(str(cuisine))}</div>',
        "</div>",
        '<div class="meal-content">',
        f'<div class="meal-title">{meal_name_safe}</div>',
    ]

    meta_parts = []
    if category:
        meta_parts.append(html.escape(str(category)))
    if ingredients:
        meta_parts.append(f"{len(ingredients)} ingredients")
    if meta_parts:
        card_html_start.append('<div class="meal-meta">' + " · ".join(meta_parts) + "</div>")

    if ingredients:
        card_html_start.append('<div class="ingredients-list">')
        for ingredient in ingredients[:3]:
            card_html_start.append(
                f'<span class="ingredient-tag">{html.escape(str(ingredient))}</span>'
            )
        if len(ingredients) > 3:
            card_html_start.append(
                f'<span class="ingredient-tag">+{len(ingredients) - 3} more</span>'
            )
        card_html_start.append("</div>")

    card_html_start.append("</div>")  # close meal-content
    card_head = card_html_start + ['<div class="card-actions">']
    card_tail = "</div></div></div>"

    with st.container():
        st.markdown("\n".join(card_head), unsafe_allow_html=True)
        btn_cols = st.columns([6, 4])
        with btn_cols[0]:
            favorite_button(meal, key_suffix=f"card_{key_suffix}")
        with btn_cols[1]:
            if st.button(
                "+",
                key=f"expand_{key_suffix}_{meal_name}",
                use_container_width=True,
                help="Voir les détails",
            ):
                st.session_state["selected_meal"] = meal
                st.session_state["selected_meal_name"] = meal_name
        st.markdown(card_tail, unsafe_allow_html=True)


def sanitize_image(image_value: Any, fallback: str) -> str:
    if not isinstance(image_value, str) or image_value.lower() == "nan":
        return fallback
    url = image_value.strip()
    if "media-allrecipes.com" in url:
        return fallback
    if url.startswith("http://"):
        url = url.replace("http://", "https://", 1)
    return url or fallback


def render_details_panel() -> None:
    meal = st.session_state.get("selected_meal")
    if not meal:
        return

    meal_name = str(meal.get("name", "Recipe"))
    if not st.session_state.get("selected_meal_name"):
        st.session_state["selected_meal_name"] = meal_name
    meal_name_safe = html.escape(meal_name)
    cuisine = html.escape(str(meal.get("cuisine") or "International"))
    dish_type = html.escape(str(meal.get("dish_type") or ""))
    diet_type = html.escape(str(meal.get("diet_type") or "Unspecified"))
    prep_time = html.escape(str(meal.get("prep_time") or "N/A"))
    ingredients = meal.get("ingredients") or []
    if not isinstance(ingredients, list):
        ingredients = []

    image_url = sanitize_image(meal.get("image"), fallback_image_url(meal_name))
    nutritions = meal.get("nutritions") or {}
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
        "".join(f"<li>{html.escape(str(ing))}</li>" for ing in ingredients)
        or "<li>Aucun ingrédient listé</li>"
    )

    badge_meta = [cuisine]
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
                <div class="details-nutrition">{"".join(nutrition_items)}</div>
            </div>
        </div>
    </div>
    """

    st.markdown(detail_html, unsafe_allow_html=True)

    button_cols = st.columns([2, 1])
    with button_cols[0]:
        favorite_button(meal, key_suffix="details")
    with button_cols[1]:
        if st.button("Masquer les détails", use_container_width=True):
            st.session_state["selected_meal"] = None
            st.session_state["selected_meal_name"] = None


def ensure_state_defaults() -> None:
    st.session_state.setdefault("last_ingredients", tuple())
    st.session_state.setdefault("last_results", [])
    st.session_state.setdefault("selected_meal", None)
    st.session_state.setdefault("selected_meal_name", None)
    st.session_state.setdefault("ingredients_input", DEFAULT_INGREDIENTS)
    st.session_state.setdefault("trigger_history_submit", False)
    st.session_state.setdefault("filter_limit", 24)


def main() -> None:
    st.set_page_config(
        page_title="Meal Recommender",
        page_icon="🍽️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    ensure_state_defaults()
    apply_theme(st.session_state.get("theme", "light"))
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    st.sidebar.markdown("## Navigation")
    nav_choice = st.sidebar.radio(
        "Navigation",
        ["Discover", "Favorites"],
        label_visibility="collapsed",
    )
    with st.sidebar:
        theme_toggle()
    display_history_sidebar()

    if nav_choice == "Favorites":
        st.markdown("## ⭐ Favorites")
        display_favorites()
        render_details_panel()
        return

    st.markdown(
        """
        <section class="hero">
            <div class="hero-content">
                <p class="eyebrow">Meal Recommender</p>
                <h1>Compose ton menu en quelques secondes</h1>
                <p>Indique les ingrédients disponibles et découvre instantanément des recettes adaptées à ta cuisine.</p>
            </div>
        </section>
    """,
        unsafe_allow_html=True,
    )

    with st.form("search_form", clear_on_submit=False):
        st.markdown('<div class="search-section">', unsafe_allow_html=True)
        st.markdown('<div class="search-shell">', unsafe_allow_html=True)
        ingredients_input = st.text_input(
            "Ingredients",
            key="ingredients_input",
            placeholder=f"Ex: {DEFAULT_INGREDIENTS}",
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("🔍 Find recipes", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    history_triggered = st.session_state.pop("trigger_history_submit", False)
    should_fetch = submitted or history_triggered

    if should_fetch:
        ingredients = tuple(i.strip() for i in ingredients_input.split(",") if i.strip())

        if not ingredients:
            st.warning("Ajoute au moins un ingrédient avant de lancer la recherche.")
            meals = st.session_state.get("last_results", [])
        else:
            try:
                with st.spinner("Searching for recipes..."):
                    meals = fetch_meals(ingredients, limit=API_FETCH_LIMIT)
                st.session_state["last_ingredients"] = ingredients
                st.session_state["last_results"] = meals
                st.session_state["selected_meal"] = None
                st.session_state["selected_meal_name"] = None
                add_to_history(list(ingredients), len(meals))
            except requests.RequestException as exc:
                st.error(f"Unable to reach the API: {exc}")
                meals = st.session_state.get("last_results", [])
            else:
                meals = st.session_state["last_results"]
    else:
        meals = st.session_state["last_results"]

    if not meals:
        st.markdown(
            """
            <div class="warning-message">
                <strong>Let's cook something!</strong><br>
                Enter two or three ingredients and press the search button.
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_details_panel()
        return

    name_query, cuisine, limit = render_filters(meals)
    filtered_meals = filter_meals(meals, name_query, cuisine, limit)

    st.markdown(
        f"""
        <div class="results-header">
            <div>
                <div class="count-number">{len(filtered_meals)}</div>
                <div class="count-label">matching recipes</div>
            </div>
            <div style="color: var(--muted); font-weight:600;">
                Showing up to {limit} of {len(meals)} suggestions
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_meal_cards(filtered_meals)
    render_details_panel()

    st.markdown(
        """
        <div class="footer">
            🍽️ Meal Recommender · Curated recipes for every pantry
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
