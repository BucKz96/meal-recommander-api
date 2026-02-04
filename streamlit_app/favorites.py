"""Gestion des favoris."""

import json
from typing import Any, cast

import streamlit as st

FAVORIS_KEY = "meal_recommender_favorites"


def get_favorites() -> list[dict[str, Any]]:
    """Récupère les favoris."""
    if FAVORIS_KEY not in st.session_state:
        st.session_state[FAVORIS_KEY] = []
    return cast(list[dict[str, Any]], st.session_state[FAVORIS_KEY])


def add_to_favorites(meal: dict[str, Any]) -> None:
    """Ajoute aux favoris."""
    favorites = get_favorites()
    if not any(f.get("name") == meal.get("name") for f in favorites):
        favorites.append(meal)
        st.session_state[FAVORIS_KEY] = favorites
        st.toast("⭐ Ajouté aux favoris !")


def remove_from_favorites(meal_name: str) -> None:
    """Retire des favoris."""
    favorites = get_favorites()
    st.session_state[FAVORIS_KEY] = [f for f in favorites if f.get("name") != meal_name]
    st.rerun()


def is_favorite(meal_name: str) -> bool:
    """Vérifie si favori."""
    return any(f.get("name") == meal_name for f in get_favorites())


def display_favorites() -> None:
    """Affiche les favoris."""
    favorites = get_favorites()

    if not favorites:
        st.info("Aucun favori. Ajoutez des recettes depuis la recherche.")
        return

    # Export/Import
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "⬇️ Exporter",
            data=json.dumps(favorites, indent=2, ensure_ascii=False),
            file_name="favorites.json",
            mime="application/json",
        )
    with col2:
        uploaded = st.file_uploader("⬆️ Importer", type=["json"])
        if uploaded:
            try:
                data = json.loads(uploaded.read().decode("utf-8"))
                if isinstance(data, list):
                    existing = {f.get("name") for f in get_favorites()}
                    added = [d for d in data if d.get("name") not in existing]
                    get_favorites().extend(added)
                    st.success(f"{len(added)} recette(s) importée(s)")
                    st.rerun()
            except Exception as e:
                st.error(f"Erreur: {e}")

    st.divider()

    # Liste
    for meal in favorites:
        with st.container():
            c1, c2 = st.columns([4, 1])
            with c1:
                st.write(f"**{meal.get('name', 'Sans nom')}**")
            with c2:
                meal_name = meal.get("name", "")
                if st.button("🗑️", key=f"del_{meal_name}"):
                    remove_from_favorites(str(meal_name))


def favorite_button_icon(meal: dict[str, Any], key_suffix: str) -> None:
    """Bouton favoris avec icône."""
    meal_name = meal.get("name", "")
    is_fav = is_favorite(meal_name)
    icon = "⭐" if is_fav else "☆"

    if st.button(icon, key=f"fav_{key_suffix}_{meal_name}", help="Favori"):
        if is_fav:
            remove_from_favorites(meal_name)
        else:
            add_to_favorites(meal)
