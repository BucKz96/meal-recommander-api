"""Gestion des favoris avec import/export JSON."""

import json
from typing import Any

import streamlit as st

FAVORIS_KEY = "meal_recommender_favorites"


def get_favorites() -> list[dict[str, Any]]:
    """Récupère les favoris depuis le session state."""
    if FAVORIS_KEY not in st.session_state:
        st.session_state[FAVORIS_KEY] = []
    return st.session_state[FAVORIS_KEY]


def add_to_favorites(meal: dict[str, Any]) -> None:
    """Ajoute une recette aux favoris."""
    favorites = get_favorites()

    if not any(f.get("name") == meal.get("name") for f in favorites):
        favorites.append(meal)
        st.session_state[FAVORIS_KEY] = favorites
        st.toast(f"⭐ {meal.get('name', 'Recette')} ajoutée aux favoris !", icon="⭐")
    else:
        st.toast("Déjà dans vos favoris", icon="ℹ️")


def remove_from_favorites(meal_name: str | None) -> None:
    """Retire une recette des favoris."""
    favorites = get_favorites()
    favorites = [f for f in favorites if f.get("name") != meal_name]
    st.session_state[FAVORIS_KEY] = favorites
    st.toast(f"Retiré des favoris", icon="🗑️")


def is_favorite(meal_name: str) -> bool:
    """Vérifie si une recette est dans les favoris."""
    favorites = get_favorites()
    return any(f.get("name") == meal_name for f in favorites)


def clear_favorites() -> None:
    """Vide tous les favoris."""
    st.session_state[FAVORIS_KEY] = []


def export_favorites_json() -> str:
    """Exporte les favoris en JSON."""
    favorites = get_favorites()
    return json.dumps(favorites, indent=2, ensure_ascii=False)


def import_favorites_json(json_str: str) -> tuple[bool, str]:
    """Importe des favoris depuis JSON."""
    try:
        data = json.loads(json_str)
        if not isinstance(data, list):
            return False, "Le JSON doit être une liste"

        for item in data:
            if not isinstance(item, dict) or "name" not in item:
                return False, "Format invalide"

        existing = get_favorites()
        existing_names = {f.get("name") for f in existing}

        added = 0
        for item in data:
            if item.get("name") not in existing_names:
                existing.append(item)
                added += 1

        st.session_state[FAVORIS_KEY] = existing
        return True, f"{added} recette(s) importée(s)"

    except json.JSONDecodeError as e:
        return False, f"JSON invalide: {e}"


def display_favorites() -> None:
    """Affiche la page des favoris."""
    favorites = get_favorites()

    with st.expander("📁 Importer / Exporter"):
        col1, col2 = st.columns(2)

        with col1:
            st.caption("Exporter")
            if favorites:
                json_data = export_favorites_json()
                st.download_button(
                    "⬇️ JSON",
                    data=json_data,
                    file_name="favorites.json",
                    mime="application/json",
                )
            else:
                st.button("⬇️ JSON", disabled=True)

        with col2:
            st.caption("Importer")
            uploaded = st.file_uploader("Choisir", type=["json"], label_visibility="collapsed")
            if uploaded is not None:
                content = uploaded.read().decode("utf-8")
                success, msg = import_favorites_json(content)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    st.markdown("---")

    if not favorites:
        st.info("Vous n'avez pas encore de favoris.")
        return

    st.write(f"**{len(favorites)}** recette(s)")

    if st.button("🗑️ Tout supprimer", type="secondary"):
        clear_favorites()
        st.rerun()

    st.markdown("---")

    for meal in favorites:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.write(f"**{meal.get('name', 'Sans nom')}**")

            with col2:
                if st.button("👁️", key=f"view_{meal.get('name')}"):
                    st.session_state.selected_meal = meal
                    st.session_state.selected_meal_name = meal.get("name")
                    st.rerun()

            with col3:
                if st.button("🗑️", key=f"del_{meal.get('name')}"):
                    remove_from_favorites(meal.get("name"))
                    st.rerun()


def favorite_button_icon(meal: dict[str, Any], key_suffix: str) -> None:
    """Bouton favoris minimal avec icône étoile."""
    meal_name = meal.get("name", "")
    is_fav = is_favorite(meal_name)

    icon = "⭐" if is_fav else "☆"
    help_text = "Retirer" if is_fav else "Ajouter"

    if st.button(
        icon,
        key=f"fav_{key_suffix}_{meal_name}",
        help=help_text,
    ):
        if is_fav:
            remove_from_favorites(meal_name)
        else:
            add_to_favorites(meal)
        st.rerun()


def favorite_button(
    meal: dict[str, Any],
    key_suffix: str = "card",
    *,
    show_label: bool = False,
) -> None:
    """Bouton favoris standard."""
    meal_name = meal.get("name", "")
    is_fav = is_favorite(meal_name)

    icon = "⭐" if is_fav else "☆"
    label = "Retirer" if is_fav else "Favori"
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
