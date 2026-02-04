"""Historique des recherches."""

from datetime import datetime

import streamlit as st

HISTORY_KEY = "meal_history"
MAX_HISTORY = 10


def add_to_history(ingredients: list[str], count: int) -> None:
    """Ajoute à l'historique."""
    if HISTORY_KEY not in st.session_state:
        st.session_state[HISTORY_KEY] = []

    entry = {
        "ingredients": ingredients,
        "count": count,
        "time": datetime.now().strftime("%H:%M"),
    }

    # Évite doublons
    if st.session_state[HISTORY_KEY] and \
       st.session_state[HISTORY_KEY][0]["ingredients"] == ingredients:
        return

    st.session_state[HISTORY_KEY].insert(0, entry)
    st.session_state[HISTORY_KEY] = st.session_state[HISTORY_KEY][:MAX_HISTORY]


def display_history_sidebar() -> None:
    """Affiche l'historique dans la sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("🕐 Historique")

    history = st.session_state.get(HISTORY_KEY, [])
    if not history:
        st.sidebar.caption("Aucune recherche")
        return

    for h in history[:5]:
        ings = ", ".join(h["ingredients"][:3])
        if len(h["ingredients"]) > 3:
            ings += f" +{len(h['ingredients']) - 3}"

        if st.sidebar.button(f"🍳 {ings} ({h['count']})", key=f"hist_{h['time']}"):
            st.session_state["ingredients_input"] = ", ".join(h["ingredients"])
            st.session_state["trigger_history_submit"] = True
            st.rerun()
