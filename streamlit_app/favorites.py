"""Gestion des favoris avec local storage.

Permet de sauvegarder des recettes préférées localement.
"""

from typing import List, Dict, Any

import streamlit as st

FAVORIS_KEY = "meal_recommender_favorites"


def get_favorites() -> List[Dict[str, Any]]:
    """Récupère les favoris depuis le session state."""
    if FAVORIS_KEY not in st.session_state:
        st.session_state[FAVORIS_KEY] = []
    return st.session_state[FAVORIS_KEY]


def add_to_favorites(meal: Dict[str, Any]):
    """Ajoute une recette aux favoris."""
    favorites = get_favorites()

    # Évite les doublons
    if not any(f.get("name") == meal.get("name") for f in favorites):
        favorites.append(meal)
        st.session_state[FAVORIS_KEY] = favorites
        st.success(f"⭐ {meal.get('name', 'Recette')} ajoutée aux favoris !")
    else:
        st.info("Cette recette est déjà dans vos favoris.")


def remove_from_favorites(meal_name: str | None):
    """Retire une recette des favoris."""
    favorites = get_favorites()
    favorites = [f for f in favorites if f.get("name") != meal_name]
    st.session_state[FAVORIS_KEY] = favorites
    st.success(f"❌ {meal_name} retiré des favoris.")


def is_favorite(meal_name: str) -> bool:
    """Vérifie si une recette est dans les favoris."""
    favorites = get_favorites()
    return any(f.get("name") == meal_name for f in favorites)


def display_favorites():
    """Affiche la page des favoris."""
    st.subheader("⭐ Mes Favoris")

    favorites = get_favorites()

    if not favorites:
        st.info("Vous n'avez pas encore de favoris. Ajoutez des recettes !")
        return

    st.write(f"{len(favorites)} recette(s) sauvegardée(s)")

    for meal in favorites:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.write(f"**{meal.get('name', 'Sans nom')}**")

            with col2:
                if st.button("👁️ Voir", key=f"view_{meal.get('name')}"):
                    st.session_state.selected_meal = meal
                    st.session_state.selected_meal_name = meal.get("name")
                    st.rerun()

            with col3:
                if st.button("🗑️", key=f"del_{meal.get('name')}"):
                    remove_from_favorites(meal.get("name"))
                    st.rerun()


def favorite_button(
    meal: Dict[str, Any],
    key_suffix: str = "card",
    *,
    show_label: bool = False,
):
    """Bouton favoris avec indicateur clair."""

    meal_name = meal.get("name", "")
    is_fav = is_favorite(meal_name)

    icon = "⭐" if is_fav else "☆"
    label = "Retirer des favoris" if is_fav else "Ajouter aux favoris"
    button_text = f"{icon} {label}" if show_label else icon

    if st.button(
        button_text,
        key=f"fav_btn_{key_suffix}_{meal_name}",
        help=label,
        use_container_width=True,
    ):
        if is_fav:
            remove_from_favorites(meal_name)
        else:
            add_to_favorites(meal)
        st.rerun()
