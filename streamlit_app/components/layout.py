"""Layout et styles CSS."""

import streamlit as st


def render_custom_css() -> None:
    """Injecte les styles CSS."""
    st.markdown("""
    <style>
        /* Reset boutons Streamlit - couleur bleue forcée */
        .stButton > button {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35) !important;
        }

        /* Hero */
        .hero {
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%);
            padding: 40px 24px;
            border-radius: 20px;
            margin-bottom: 24px;
            text-align: center;
            color: white;
        }

        .hero h1 {
            font-size: 2rem;
            font-weight: 700;
            margin: 8px 0 12px;
        }

        .hero p {
            opacity: 0.9;
            font-size: 1rem;
        }

        /* Search bar - centree et compacte */
        [data-testid="stForm"] {
            max-width: 480px !important;
            margin: -16px auto 32px !important;
            background: white;
            padding: 20px 24px;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border: 1px solid #e2e8f0;
        }

        [data-testid="stForm"] .stTextInput input {
            font-size: 1.1rem !important;
            padding: 14px 16px !important;
            border-radius: 12px !important;
            border: 2px solid #e2e8f0 !important;
            min-height: 52px !important;
        }

        [data-testid="stForm"] .stTextInput input:focus {
            border-color: #2563eb !important;
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1) !important;
        }

        [data-testid="stForm"] .stButton > button {
            border-radius: 999px !important;
            padding: 12px 32px !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            margin-top: 12px !important;
        }

        /* Cartes repas */
        .meal-card {
            background: white;
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid #e2e8f0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            transition: all 0.2s ease;
        }

        .meal-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        }

        .meal-card--active {
            border-color: #2563eb;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2);
        }

        /* Boutons d'action dans les cartes */
        .card-actions {
            display: flex;
            gap: 8px;
            padding: 0 12px 12px;
            justify-content: flex-end;
        }

        .card-actions button {
            width: 36px !important;
            height: 36px !important;
            border-radius: 50% !important;
            padding: 0 !important;
            font-size: 1.1rem !important;
            background: white !important;
            border: 1px solid #e2e8f0 !important;
            color: #2563eb !important;
        }

        .card-actions button:hover {
            background: #2563eb !important;
            color: white !important;
        }

        /* Modal/Dialog overlay */
        [data-testid="stDialog"] {
            max-width: 700px !important;
        }
    </style>
    """, unsafe_allow_html=True)


def render_hero() -> None:
    """Hero section."""
    # Style inline compact pour eviter ligne trop longue
    sub_style = "font-size:0.75rem;opacity:0.8;letter-spacing:0.2em;text-transform:uppercase;"
    st.markdown(f"""
    <div class="hero">
        <div style="{sub_style}">Meal Recommender</div>
        <h1>Trouvez la recette parfaite</h1>
        <p>Saisissez vos ingredients et decouvrez des recettes adaptees.</p>
    </div>
    """, unsafe_allow_html=True)


def render_search_form() -> tuple[str, bool]:
    """Formulaire de recherche simple et fonctionnel."""
    with st.form("search_form", clear_on_submit=False):
        st.text_input(
            "",
            key="ingredients_input",
            placeholder="Ex: poulet, riz, tomate...",
            label_visibility="collapsed",
        )
        # Centrer le bouton
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("🔍 Rechercher", use_container_width=True)

    return st.session_state.get("ingredients_input", ""), submitted
