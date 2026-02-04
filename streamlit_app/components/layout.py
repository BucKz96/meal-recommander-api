"""Composants de layout et styles CSS responsive.

Design mobile-first avec thème bleu moderne.
"""

import streamlit as st


def render_custom_css() -> None:
    """Injecte les styles CSS personnalisés responsive."""
    st.markdown(
        """
    <style>
        /* ===== VARIABLES THEME BLEU ===== */
        :root {
            --primary: #2563eb;
            --primary-light: #3b82f6;
            --primary-dark: #1d4ed8;
            --accent: #60a5fa;
            --card-bg: #ffffff;
            --card-border: #e0e7ff;
            --soft-bg: #eef2ff;
            --muted: #6b7280;
            --text-dark: #111827;
            --button-text: #ffffff;
            --shadow-sm: 0 1px 2px rgba(37, 99, 235, 0.05);
            --shadow-md: 0 4px 12px rgba(37, 99, 235, 0.1);
            --shadow-lg: 0 10px 30px rgba(37, 99, 235, 0.15);
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 24px;
        }

        /* ===== BASE ===== */
        .stApp {
            background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
            min-height: 100vh;
        }

        /* ===== HERO SECTION ===== */
        .hero {
            position: relative;
            border-radius: var(--radius-xl);
            padding: 32px 20px 40px;
            margin-bottom: 24px;
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%);
            color: #fff;
            text-align: center;
            overflow: hidden;
            box-shadow: var(--shadow-lg);
        }

        .hero::after {
            content: "";
            position: absolute;
            inset: 0;
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
            opacity: 0.3;
        }

        .hero-content {
            position: relative;
            max-width: 600px;
            margin: 0 auto;
            z-index: 1;
        }

        .hero .eyebrow {
            letter-spacing: 0.2em;
            text-transform: uppercase;
            font-size: 0.7rem;
            color: rgba(255,255,255,0.8);
            font-weight: 500;
        }

        .hero h1 {
            font-size: clamp(1.6rem, 4vw, 2.4rem);
            font-weight: 700;
            margin: 0.5rem 0 0.75rem;
            line-height: 1.2;
        }

        .hero p {
            font-size: clamp(0.875rem, 2vw, 1rem);
            margin: 0 auto;
            line-height: 1.5;
            color: rgba(255,255,255,0.9);
            max-width: 90%;
        }

        /* ===== SEARCH SECTION COMPACTE ===== */
        .search-section {
            width: min(420px, 92vw);
            margin: -16px auto 20px;
            padding: 0 12px;
            text-align: center;
            position: relative;
            z-index: 10;
        }

        .search-shell {
            background: var(--card-bg);
            border-radius: var(--radius-lg);
            border: 1px solid var(--card-border);
            padding: 12px 16px;
            box-shadow: var(--shadow-md);
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .search-shell .stTextInput {
            margin-bottom: 0 !important;
        }

        .search-shell .stTextInput > div > div > input {
            font-size: 0.9rem;
            padding: 0.6rem 0.875rem;
            border-radius: var(--radius-md);
            border: 1px solid #d1d5db;
            background: #ffffff;
            color: var(--text-dark);
            box-shadow: none;
            transition: all 0.2s ease;
        }

        .search-shell .stTextInput input::placeholder {
            color: #9ca3af;
            opacity: 1;
            font-size: 0.85rem;
        }

        .search-shell .stTextInput > div > div > input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
            outline: none;
        }

        .search-shell .stButton > button {
            margin: 0;
            font-size: 0.875rem;
            padding: 0.5rem 1.25rem;
            border-radius: var(--radius-md);
            width: auto;
            min-width: 120px;
            background: var(--primary);
            font-weight: 500;
            box-shadow: var(--shadow-sm);
        }

        .search-shell .stButton > button:hover {
            background: var(--primary-dark);
            box-shadow: var(--shadow-md);
        }

        /* ===== BUTTONS ===== */
        .stButton > button {
            background: var(--primary);
            border: none;
            color: var(--button-text);
            font-weight: 500;
            border-radius: var(--radius-md);
            padding: 0.4rem 0.875rem;
            font-size: 0.85rem;
            box-shadow: var(--shadow-sm);
            transition: all 0.15s ease;
        }

        .stButton > button:hover {
            background: var(--primary-dark);
            box-shadow: var(--shadow-md);
            transform: translateY(-1px);
        }

        /* ===== RESULTS HEADER ===== */
        .results-header {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            align-items: center;
            justify-content: space-between;
            padding: 12px 16px;
            border-radius: var(--radius-md);
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            box-shadow: var(--shadow-sm);
            margin-bottom: 16px;
        }

        .count-number {
            font-size: clamp(1.5rem, 3vw, 2rem);
            font-weight: 700;
            color: var(--primary);
            line-height: 1;
        }

        .count-label {
            font-size: 0.8rem;
            color: var(--muted);
            font-weight: 500;
        }

        /* ===== MEAL CARDS ===== */
        .meal-card-wrapper {
            padding: 6px;
        }

        .meal-card {
            background: var(--card-bg);
            border-radius: var(--radius-lg);
            overflow: hidden;
            border: 1px solid var(--card-border);
            box-shadow: var(--shadow-sm);
            transition: all 0.2s ease;
            display: flex;
            flex-direction: column;
            height: 100%;
            position: relative;
        }

        .meal-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
            border-color: var(--primary-light);
        }

        .meal-card--active {
            border-color: var(--primary);
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
        }

        .meal-image-container {
            position: relative;
            height: 140px;
            overflow: hidden;
        }

        .meal-image-container img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }

        .meal-card:hover .meal-image-container img {
            transform: scale(1.03);
        }

        .meal-badge {
            position: absolute;
            top: 8px;
            left: 8px;
            background: rgba(255, 255, 255, 0.95);
            padding: 3px 8px;
            border-radius: 999px;
            font-size: 0.7rem;
            font-weight: 600;
            color: var(--primary-dark);
            border: 1px solid var(--card-border);
            backdrop-filter: blur(4px);
        }

        .meal-content {
            padding: 12px;
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        .meal-title {
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-dark);
            margin-bottom: 4px;
            line-height: 1.3;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .meal-meta {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            color: var(--muted);
            font-size: 0.75rem;
            margin-bottom: 8px;
        }

        .ingredients-list {
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
            margin-bottom: 8px;
        }

        .ingredient-tag {
            background: var(--soft-bg);
            color: var(--primary-dark);
            padding: 2px 8px;
            border-radius: 999px;
            font-size: 0.7rem;
            border: 1px solid var(--card-border);
            white-space: nowrap;
        }

        /* ===== BOUTONS ACTIONS DANS LA CARTE ===== */
        .card-actions {
            position: absolute;
            bottom: 8px;
            right: 8px;
            display: flex;
            gap: 6px;
            z-index: 10;
        }

        .card-actions .stButton {
            width: auto !important;
        }

        .card-actions .stButton > button {
            width: 32px !important;
            height: 32px !important;
            min-width: 32px !important;
            min-height: 32px !important;
            padding: 0 !important;
            border-radius: 50% !important;
            font-size: 1rem !important;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(255, 255, 255, 0.95) !important;
            border: 1px solid var(--card-border) !important;
            color: var(--primary) !important;
            box-shadow: var(--shadow-sm) !important;
            transition: all 0.15s ease !important;
        }

        .card-actions .stButton > button:hover {
            background: var(--primary) !important;
            border-color: var(--primary) !important;
            color: white !important;
            transform: scale(1.05) !important;
            box-shadow: var(--shadow-md) !important;
        }

        .card-actions .stButton:first-child > button {
            background: rgba(255, 255, 255, 0.95) !important;
        }

        .card-actions .stButton:last-child > button {
            background: rgba(255, 255, 255, 0.95) !important;
        }

        /* ===== MESSAGES ===== */
        .warning-message {
            background: linear-gradient(120deg, #eff6ff, #dbeafe);
            border-radius: var(--radius-md);
            padding: 16px;
            border: 1px solid var(--card-border);
            text-align: center;
            color: var(--text-dark);
            margin: 16px 0;
            font-size: 0.9rem;
        }

        /* ===== DETAILS PANEL ===== */
        .details-panel {
            background: var(--card-bg);
            border-radius: var(--radius-lg);
            border: 1px solid var(--card-border);
            padding: 20px;
            box-shadow: var(--shadow-md);
            margin-top: 1rem;
        }

        .details-header {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 16px;
        }

        .details-header .eyebrow {
            letter-spacing: 0.15em;
            text-transform: uppercase;
            font-size: 0.65rem;
            color: var(--muted);
            margin-bottom: 0;
        }

        .details-header h3 {
            margin: 0;
            font-size: clamp(1.1rem, 2.5vw, 1.5rem);
            color: var(--text-dark);
            line-height: 1.3;
            font-weight: 600;
        }

        .details-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-top: 8px;
            color: var(--muted);
        }

        .details-meta span {
            background: var(--soft-bg);
            padding: 3px 10px;
            border-radius: 999px;
            font-size: 0.75rem;
            border: 1px solid var(--card-border);
            color: var(--primary-dark);
        }

        .details-body {
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
        }

        .details-image img {
            width: 100%;
            border-radius: var(--radius-md);
            object-fit: cover;
            border: 1px solid var(--card-border);
            box-shadow: var(--shadow-sm);
        }

        .details-info h4 {
            margin-top: 0;
            margin-bottom: 8px;
            color: var(--text-dark);
            font-size: 0.95rem;
            font-weight: 600;
        }

        .details-info ul {
            padding-left: 16px;
            margin-bottom: 16px;
        }

        .details-info li {
            margin-bottom: 3px;
            color: var(--text-dark);
            font-size: 0.85rem;
        }

        .details-nutrition {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
        }

        .nutrition-item {
            background: var(--soft-bg);
            border-radius: var(--radius-md);
            padding: 8px 10px;
            border: 1px solid var(--card-border);
            text-align: center;
        }

        .nutrition-item span {
            display: block;
            font-size: 0.7rem;
            color: var(--muted);
            margin-bottom: 2px;
        }

        .nutrition-item strong {
            font-size: 0.95rem;
            color: var(--primary-dark);
            font-weight: 600;
        }

        /* ===== FOOTER ===== */
        .footer {
            text-align: center;
            color: var(--muted);
            padding: 1rem 0;
            font-size: 0.8rem;
        }

        /* ===== BREAKPOINTS ===== */
        /* Small devices (480px and up) */
        @media (min-width: 480px) {
            .hero {
                padding: 40px 24px 48px;
            }
            
            .search-section {
                margin-top: -20px;
            }
            
            .meal-card-wrapper {
                padding: 8px;
            }
            
            .details-nutrition {
                grid-template-columns: repeat(4, 1fr);
            }
        }

        /* Medium devices (768px and up) */
        @media (min-width: 768px) {
            .hero {
                padding: 48px 32px 56px;
                margin-bottom: 32px;
            }
            
            .search-section {
                margin-top: -24px;
            }
            
            .search-shell {
                flex-direction: row;
                align-items: center;
                padding: 12px 16px;
            }
            
            .search-shell .stTextInput {
                flex: 1;
            }
            
            .search-shell .stButton > button {
                min-width: 100px;
            }
            
            .results-header {
                padding: 14px 20px;
            }
            
            .meal-image-container {
                height: 160px;
            }
            
            .details-header {
                flex-direction: row;
                justify-content: space-between;
                align-items: center;
            }
            
            .details-body {
                grid-template-columns: 1fr 1fr;
            }
        }

        /* Large devices (1024px and up) */
        @media (min-width: 1024px) {
            .hero {
                padding: 56px 48px 64px;
            }
            
            .hero h1 {
                font-size: 2.5rem;
            }
            
            .meal-image-container {
                height: 180px;
            }
            
            .details-body {
                grid-template-columns: 2fr 3fr;
            }
        }

        /* Extra large devices (1200px and up) */
        @media (min-width: 1200px) {
            .hero-content {
                max-width: 640px;
            }
            
            .meal-title {
                font-size: 1rem;
            }
        }

        /* ===== SIDEBAR STYLING ===== */
        .css-1d391kg, [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%) !important;
        }

        /* ===== INPUT FOCUS STATES ===== */
        input:focus, textarea:focus, select:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
        }

        /* ===== SCROLLBAR ===== */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 3px;
        }

        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 3px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
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
                <h1>Trouvez la recette parfaite</h1>
                <p>Saisissez vos ingrédients et découvrez des recettes adaptées.</p>
            </div>
        </section>
    """,
        unsafe_allow_html=True,
    )


def render_results_header(filtered_count: int, total_count: int, limit: int) -> None:
    """Affiche l'en-tête des résultats."""
    st.markdown(
        f"""
        <div class="results-header">
            <div>
                <div class="count-number">{filtered_count}</div>
                <div class="count-label">recettes trouvées</div>
            </div>
            <div style="color: var(--muted); font-size: 0.8rem;">
                {min(filtered_count, limit)} sur {total_count}
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
            Meal Recommender · Trouvez votre inspiration culinaire
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state() -> None:
    """Affiche le message d'état vide."""
    st.markdown(
        """
        <div class="warning-message">
            <strong>🍽️ Prêt à cuisiner ?</strong><br>
            Entrez quelques ingrédients et lancez la recherche.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_no_results() -> None:
    """Affiche le message quand aucun résultat ne correspond."""
    st.markdown(
        """
        <div class="warning-message">
            <strong>🍽️ Aucune recette trouvée</strong><br>
            Essayez d'autres ingrédients ou moins de filtres.
        </div>
        """,
        unsafe_allow_html=True,
    )
