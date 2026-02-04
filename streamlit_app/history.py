"""Historique des recherches avec gestion de session.

L'historique est conservé pendant la session Streamlit
et peut être effacé manuellement.
"""

from typing import Any

import streamlit as st

HISTORY_KEY = "meal_recommender_history"
MAX_HISTORY = 10


def add_to_history(ingredients: list[str], results_count: int) -> None:
    """Ajoute une recherche à l'historique.
    
    Args:
        ingredients: Liste des ingrédients recherchés
        results_count: Nombre de résultats trouvés
    """
    if HISTORY_KEY not in st.session_state:
        st.session_state[HISTORY_KEY] = []

    history = st.session_state[HISTORY_KEY]

    # Crée l'entrée
    from datetime import datetime
    entry = {
        "ingredients": ingredients.copy(),
        "results_count": results_count,
        "timestamp": datetime.now().strftime("%H:%M"),
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


def get_history() -> list[dict[str, Any]]:
    """Récupère l'historique."""
    return st.session_state.get(HISTORY_KEY, [])


def clear_history() -> None:
    """Vide l'historique."""
    st.session_state[HISTORY_KEY] = []


def display_history_sidebar() -> None:
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
                f"🍳 {ingredients_str} ({entry['results_count']})",
                key=f"hist_{entry['timestamp']}_{id(entry)}",
                use_container_width=True,
            ):
                st.session_state["ingredients_input"] = ", ".join(entry["ingredients"])
                st.session_state["trigger_history_submit"] = True
                st.rerun()

        with col2:
            st.caption(entry["timestamp"])

    if len(history) > 5 and st.sidebar.button("🗑️ Vider", key="clear_hist"):
        clear_history()
        st.rerun()
