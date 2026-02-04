"""Composants de layout et styles CSS."""

import streamlit as st


def render_custom_css() -> None:
    """Injecte les styles CSS personnalisés."""
    st.markdown(
        """
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
            width: min(520px, 92vw);
            margin: -70px auto 32px;
            padding: 0 8px;
            text-align: center;
        }

        .search-shell {
            background: var(--card-bg);
            border-radius: 28px;
            border: 1.5px solid var(--card-border);
            padding: 24px 26px;
            box-shadow: 0 30px 60px rgba(15, 23, 42, 0.16);
        }

        .search-shell .stTextInput > div > div > input {
            font-size: 0.95rem;
            padding: 0.75rem 1rem;
            border-radius: 14px;
            border: 1px solid var(--card-border);
            background: var(--soft-bg);
            color: var(--text-dark);
            box-shadow: inset 0 1px 3px rgba(15, 23, 42, 0.08);
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }

        .search-shell .stTextInput input::placeholder {
            color: rgba(100, 116, 139, 0.9);
            opacity: 1;
        }

        .search-shell .stTextInput > div > div > input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
            outline: none;
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

        .card-shell-marker {
            display: none;
        }

        div[data-testid="stVerticalBlock"]:has(.card-shell-marker) {
            background: var(--card-bg);
            border-radius: 22px;
            border: 1.5px solid var(--card-border);
            box-shadow: 0 16px 28px rgba(15, 23, 42, 0.12);
            padding: 0;
            margin-bottom: 24px;
            overflow: hidden;
            transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
        }

        div[data-testid="stVerticalBlock"]:has(.card-shell-marker[data-active="true"]) {
            border-color: var(--primary);
            box-shadow: 0 30px 50px rgba(37, 99, 235, 0.2);
        }

        div[data-testid="stVerticalBlock"]:has(.card-shell-marker):hover {
            transform: translateY(-4px);
            box-shadow: 0 26px 48px rgba(37, 99, 235, 0.18);
        }

        div[data-testid="stVerticalBlock"]:has(.card-shell-marker) > div {
            padding: 0 !important;
        }

        div[data-testid="stVerticalBlock"]:has(.card-shell-marker) [data-testid="element-container"] {
            padding: 0 20px;
            background: transparent;
        }

        div[data-testid="stVerticalBlock"]:has(.card-shell-marker) [data-testid="element-container"]:first-of-type {
            padding-top: 20px;
        }

        div[data-testid="stVerticalBlock"]:has(.card-shell-marker) [data-testid="element-container"]:last-of-type {
            padding-bottom: 20px;
        }

        .meal-card-wrapper {
            padding: 0;
        }

        .meal-card {
            background: transparent;
            border: none;
            box-shadow: none;
        }

        .meal-image-container {
            position: relative;
            height: 190px;
            overflow: hidden;
        }

        .meal-image-container img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.35s ease;
        }

        .meal-card:hover .meal-image-container img {
            transform: scale(1.05);
        }

        .meal-badge {
            position: absolute;
            top: 14px;
            left: 14px;
            background: rgba(248, 250, 255, 0.95);
            padding: 5px 12px;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-dark);
            border: 1px solid var(--card-border);
        }

        .meal-content {
            padding: 18px 20px 16px;
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        .meal-title {
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--text-dark);
            margin-bottom: 8px;
            line-height: 1.35;
        }

        .meal-meta {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            color: var(--muted);
            font-size: 0.85rem;
            margin-bottom: 10px;
        }

        .ingredients-list {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 10px;
        }

        .ingredient-tag {
            background: var(--soft-bg);
            color: var(--primary);
            padding: 4px 12px;
            border-radius: 999px;
            font-size: 0.78rem;
            border: 1px solid var(--card-border);
        }

        div[data-testid="stVerticalBlock"]:has(.card-shell-marker) [data-testid="stHorizontalBlock"] {
            margin: 16px 20px 20px;
            padding: 8px 12px;
            border-radius: 999px;
            background: var(--soft-bg);
            border: 1px solid var(--card-border);
            box-shadow: inset 0 1px 3px rgba(15, 23, 42, 0.08);
            gap: 12px;
            align-items: center;
        }

        div[data-testid="stVerticalBlock"]:has(.card-shell-marker) [data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            flex: 1;
        }

        div[data-testid="stVerticalBlock"]:has(.card-shell-marker) [data-testid="stHorizontalBlock"] button {
            width: 100%;
            border-radius: 14px;
            font-size: 0.9rem;
            padding: 0.3rem 0;
            border: none;
            background: transparent;
            color: var(--primary);
            box-shadow: none;
            cursor: pointer;
        }

        div[data-testid="stVerticalBlock"]:has(.card-shell-marker) [data-testid="stHorizontalBlock"] button:last-child {
            color: var(--text-dark);
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
            div[data-testid="stVerticalBlock"]:has(.card-shell-marker) [data-testid="stHorizontalBlock"] {
                flex-direction: column;
            }
        }
    </style>
    """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    """Affiche la section hero."""
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


def render_results_header(filtered_count: int, total_count: int, limit: int) -> None:
    """Affiche l'en-tête des résultats.
    
    Args:
        filtered_count: Nombre de résultats filtrés
        total_count: Nombre total de suggestions
        limit: Limite affichée
    """
    st.markdown(
        f"""
        <div class="results-header">
            <div>
                <div class="count-number">{filtered_count}</div>
                <div class="count-label">matching recipes</div>
            </div>
            <div style="color: var(--muted); font-weight:600;">
                Showing up to {limit} of {total_count} suggestions
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Affiche le footer."""
    st.markdown(
        """
        <div class="footer">
            🍽️ Meal Recommender · Curated recipes for every pantry
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state() -> None:
    """Affiche le message d'état vide."""
    st.markdown(
        """
        <div class="warning-message">
            <strong>Let's cook something!</strong><br>
            Enter two or three ingredients and press the search button.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_no_results() -> None:
    """Affiche le message quand aucun résultat ne correspond."""
    st.markdown(
        """
        <div class="warning-message">
            <strong>🍽️ No meals match your filters.</strong><br>
            Try tweaking the cuisine or adding fewer constraints.
        </div>
        """,
        unsafe_allow_html=True,
    )
