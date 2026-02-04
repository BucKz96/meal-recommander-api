"""Configuration de thème pour Streamlit.

Usage dans main.py:
    from theme import apply_theme
    apply_theme("dark")  # ou "light"
"""

import streamlit as st

THEMES = {
    "light": {
        "text": "#0f172a",
        "primary": "#1d4ed8",
        "primary_light": "#60a5fa",
        "accent": "#38bdf8",
        "card_bg": "#ffffff",
        "card_border": "#dbeafe",
        "soft_bg": "#eff6ff",
        "muted": "#64748b",
        "app_background": "radial-gradient(circle at top, #f8fbff 0%, #ecf2ff 55%, #e2e8f0 100%)",
        "button_text": "#ffffff",
    },
    "dark": {
        "text": "#f8fafc",
        "primary": "#93c5fd",
        "primary_light": "#bfdbfe",
        "accent": "#5eead4",
        "card_bg": "#111827",
        "card_border": "#1f2937",
        "soft_bg": "#1e293b",
        "muted": "#94a3b8",
        "app_background": "radial-gradient(circle at top, #0b1120 0%, #020617 65%, #00040d 100%)",
        "button_text": "#0f172a",
    },
}


def apply_theme(theme_name: str = "light"):
    """Applique le thème choisi en exposant des variables CSS globales."""

    theme = THEMES.get(theme_name, THEMES["light"])

    css = f"""
    <style>
    :root {{
        --primary: {theme["primary"]};
        --primary-light: {theme["primary_light"]};
        --accent: {theme["accent"]};
        --card-bg: {theme["card_bg"]};
        --card-border: {theme["card_border"]};
        --soft-bg: {theme["soft_bg"]};
        --muted: {theme["muted"]};
        --text-dark: {theme["text"]};
        --app-background: {theme["app_background"]};
        --button-text: {theme["button_text"]};
    }}

    body, .stApp {{
        color: {theme["text"]} !important;
    }}
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)
    st.session_state.theme = theme_name


def theme_toggle(label: str = "🌓"):
    """Simple toggle button that flips the saved theme."""
    current = st.session_state.get("theme", "light")
    new_theme = "dark" if current == "light" else "light"

    if st.button(label, help="Changer de thème"):
        st.session_state.theme = new_theme
        st.rerun()
