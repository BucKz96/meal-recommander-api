"""Historique des recherches de l'utilisateur.

Garde en mémoire les dernières recherches pour un accès rapide.
"""

from typing import List, Dict, Any
from datetime import datetime

import streamlit as st

HISTORY_KEY = "meal_recommender_history"
MAX_HISTORY = 10


def add_to_history(ingredients: List[str], results_count: int):
    """Ajoute une recherche à l'historique."""
    if HISTORY_KEY not in st.session_state:
        st.session_state[HISTORY_KEY] = []

    history = st.session_state[HISTORY_KEY]

    # Crée l'entrée
    entry = {
        "ingredients": ingredients,
        "results_count": results_count,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "date": datetime.now().strftime("%Y-%m-%d"),
    }

    # Évite les doublons consécutifs
    if history and history[0]["ingredients"] == ingredients:
        return

    # Ajoute en début de liste
    history.insert(0, entry)

    # Limite la taille
    if len(history) > MAX_HISTORY:
        history = history[:MAX_HISTORY]

    st.session_state[HISTORY_KEY] = history


def get_history() -> List[Dict[str, Any]]:
    """Récupère l'historique."""
    return st.session_state.get(HISTORY_KEY, [])


def clear_history():
    """Vide l'historique."""
    st.session_state[HISTORY_KEY] = []


def display_history_sidebar():
    """Affiche l'historique dans la sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("🕐 Historique")

    history = get_history()

    if not history:
        st.sidebar.caption("Aucune recherche récente")
        return

    for entry in history[:5]:  # Affiche les 5 dernières
        ingredients_str = ", ".join(entry["ingredients"][:3])
        if len(entry["ingredients"]) > 3:
            ingredients_str += f" +{len(entry['ingredients']) - 3}"

        col1, col2 = st.sidebar.columns([4, 1])
        with col1:
            if st.button(
                f"🍳 {ingredients_str} ({entry['results_count']} résultats)",
                key=f"hist_{entry['timestamp']}",
                use_container_width=True,
            ):
                st.session_state["ingredients_input"] = ", ".join(entry["ingredients"])
                st.session_state["trigger_history_submit"] = True
                st.rerun()

        with col2:
            st.caption(entry["timestamp"])

    if len(history) > 5 and st.sidebar.button("🗑️ Vider l'historique"):
        clear_history()
        st.rerun()
