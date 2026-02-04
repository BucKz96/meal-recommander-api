"""Composants de layout et styles CSS responsive.

Design mobile-first avec thème bleu moderne.
"""

import streamlit as st


def render_custom_css() -> None:
    """Injecte les styles CSS personnalisés avec priorité élevée."""
    st.markdown(
        """
    <style>
        /* ===== RESET STREAMLIT BUTTONS ===== */
        /* Force la couleur sur tous les boutons */
        button[kind="secondary"],
        button[kind="primary"],
        .stButton > button {
            background-color: #2563eb !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
        }
        
        .stButton > button:hover {
            background-color: #1d4ed8 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
        }

        /* Boutons secondaires (outline) */
        button[kind="secondary"] {
            background-color: white !important;
            color: #2563eb !important;
            border: 1px solid #e0e7ff !important;
        }
        
        button[kind="secondary"]:hover {
            background-color: #eef2ff !important;
            border-color: #2563eb !important;
        }

        /* ===== VARIABLES THEME BLEU ===== */
        :root {
            --primary: #2563eb;
            --primary-light: #3b82f6;
            --primary-dark: #1d4ed8;
            --accent: #60a5fa;
            --card-bg: #ffffff;
            --card-border: #e2e8f0;
            --soft-bg: #f8fafc;
            --muted: #64748b;
            --text-dark: #1e293b;
            --button-text: #ffffff;
            --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07);
            --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 24px;
        }

        /* ===== BASE ===== */
        .stApp {
            background: #f8fafc;
        }

        /* ===== HERO SECTION ===== */
        .hero {
            position: relative;
            border-radius: var(--radius-xl);
            padding: 40px 24px 48px;
            margin-bottom: 32px;
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%);
            color: #fff;
            text-align: center;
            box-shadow: var(--shadow-lg);
        }

        .hero::before {
            content: "";
            position: absolute;
            inset: 0;
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
            opacity: 0.4;
            border-radius: var(--radius-xl);
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
            color: rgba(255,255,255,0.85);
            font-weight: 600;
        }

        .hero h1 {
            font-size: clamp(1.8rem, 4vw, 2.5rem);
            font-weight: 700;
            margin: 0.5rem 0 0.75rem;
            line-height: 1.2;
        }

        .hero p {
            font-size: clamp(0.9rem, 2vw, 1rem);
            margin: 0 auto;
            line-height: 1.5;
            color: rgba(255,255,255,0.9);
            max-width: 90%;
        }

        /* ===== SEARCH BAR CENTRÉE ET COMPACTE ===== */
        .search-container {
            max-width: 500px;
            margin: -20px auto 32px;
            padding: 0 16px;
            position: relative;
            z-index: 10;
        }

        .search-box {
            background: white;
            border-radius: var(--radius-lg);
            border: 1px solid #e2e8f0;
            padding: 20px 24px;
            box-shadow: var(--shadow-md);
        }

        /* Input plus gros */
        .search-box .stTextInput > div > div > input {
            font-size: 1.1rem !important;
            padding: 14px 18px !important;
            border-radius: var(--radius-md) !important;
            border: 2px solid #e2e8f0 !important;
            background: white !important;
            color: #1e293b !important;
            min-height: 52px !important;
            transition: all 0.2s ease !important;
        }

        .search-box .stTextInput > div > div > input:focus {
            border-color: #2563eb !important;
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1) !important;
            outline: none !important;
        }

        .search-box .stTextInput input::placeholder {
            color: #94a3b8 !important;
            font-size: 1rem !important;
        }

        /* Bouton recherche centré et taille moyenne */
        .search-button-container {
            display: flex;
            justify-content: center;
            margin-top: 16px;
        }

        .search-box .stButton > button {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            color: white !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            padding: 12px 32px !important;
            border-radius: 9999px !important;
            border: none !important;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
            min-width: 160px !important;
        }

        .search-box .stButton > button:hover {
            background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.45) !important;
            transform: translateY(-2px) !important;
        }

        /* ===== RESULTS HEADER ===== */
        .results-header {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            align-items: center;
            justify-content: space-between;
            padding: 16px 20px;
            border-radius: var(--radius-md);
            background: white;
            border: 1px solid #e2e8f0;
            box-shadow: var(--shadow-sm);
            margin-bottom: 20px;
        }

        .count-number {
            font-size: clamp(1.8rem, 3vw, 2.2rem);
            font-weight: 700;
            color: #2563eb;
            line-height: 1;
        }

        .count-label {
            font-size: 0.85rem;
            color: #64748b;
            font-weight: 500;
        }

        /* ===== MEAL CARDS ===== */
        .meal-card-wrapper {
            padding: 6px;
            margin-bottom: 8px;
        }

        .meal-card {
            background: white;
            border-radius: var(--radius-lg);
            overflow: hidden;
            border: 1px solid #e2e8f0;
            box-shadow: var(--shadow-sm);
            transition: all 0.25s ease;
            display: flex;
            flex-direction: column;
            height: 100%;
        }

        .meal-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
            border-color: #bfdbfe;
        }

        .meal-card--active {
            border-color: #2563eb;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
        }

        .meal-image-container {
            position: relative;
            height: 160px;
            overflow: hidden;
        }

        .meal-image-container img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.4s ease;
        }

        .meal-card:hover .meal-image-container img {
            transform: scale(1.05);
        }

        .meal-badge {
            position: absolute;
            top: 10px;
            left: 10px;
            background: rgba(255, 255, 255, 0.95);
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 0.7rem;
            font-weight: 600;
            color: #1e40af;
            border: 1px solid #e0e7ff;
            backdrop-filter: blur(4px);
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }

        .meal-content {
            padding: 14px;
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        .meal-title {
            font-size: 0.95rem;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 4px;
            line-height: 1.35;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .meal-meta {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            color: #64748b;
            font-size: 0.8rem;
            margin-bottom: 8px;
        }

        .ingredients-list {
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
            margin-bottom: 8px;
        }

        .ingredient-tag {
            background: #eef2ff;
            color: #1d4ed8;
            padding: 2px 8px;
            border-radius: 999px;
            font-size: 0.7rem;
            font-weight: 500;
            border: 1px solid #dbeafe;
        }

        /* ===== CARD ACTIONS (BOUTONS DANS LA CARTE) ===== */
        /* Container pour les boutons - visuellement dans la carte */
        .meal-card-actions {
            display: flex;
            gap: 8px;
            padding: 0 14px 14px;
            justify-content: flex-end;
            margin-top: auto;
        }

        /* Style spécifique pour les boutons d'action des cartes */
        div[data-testid="stHorizontalBlock"]:has(button[key^="fav_"]),
        div[data-testid="stHorizontalBlock"]:has(button[key^="det_"]) {
            gap: 8px !important;
        }

        /* Boutons icônes dans les cartes */
        button[key^="fav_"],
        button[key^="det_"] {
            width: 36px !important;
            height: 36px !important;
            min-width: 36px !important;
            min-height: 36px !important;
            padding: 0 !important;
            border-radius: 50% !important;
            font-size: 1.1rem !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            background: white !important;
            border: 1px solid #e2e8f0 !important;
            color: #2563eb !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        }

        button[key^="fav_"]:hover,
        button[key^="det_"]:hover {
            background: #2563eb !important;
            border-color: #2563eb !important;
            color: white !important;
            transform: scale(1.05) !important;
        }

        /* ===== MESSAGES ===== */
        .warning-message {
            background: linear-gradient(120deg, #eff6ff, #dbeafe);
            border-radius: var(--radius-md);
            padding: 20px;
            border: 1px solid #bfdbfe;
            text-align: center;
            color: #1e293b;
            margin: 20px 0;
            font-size: 0.95rem;
        }

        /* ===== DETAILS PANEL ===== */
        .details-panel {
            background: white;
            border-radius: var(--radius-lg);
            border: 1px solid #e2e8f0;
            padding: 24px;
            box-shadow: var(--shadow-md);
            margin-top: 1rem;
        }

        .details-header {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 20px;
        }

        .details-header .eyebrow {
            letter-spacing: 0.15em;
            text-transform: uppercase;
            font-size: 0.7rem;
            color: #64748b;
        }

        .details-header h3 {
            margin: 0;
            font-size: clamp(1.2rem, 2.5vw, 1.6rem);
            color: #1e293b;
            line-height: 1.3;
            font-weight: 600;
        }

        .details-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .details-meta span {
            background: #f1f5f9;
            padding: 4px 12px;
            border-radius: 999px;
            font-size: 0.8rem;
            color: #475569;
            border: 1px solid #e2e8f0;
        }

        .details-body {
            display: grid;
            grid-template-columns: 1fr;
            gap: 24px;
        }

        .details-image img {
            width: 100%;
            border-radius: var(--radius-md);
            object-fit: cover;
            border: 1px solid #e2e8f0;
            box-shadow: var(--shadow-sm);
        }

        .details-info h4 {
            margin-top: 0;
            margin-bottom: 10px;
            color: #1e293b;
            font-size: 1rem;
            font-weight: 600;
        }

        .details-info ul {
            padding-left: 18px;
            margin-bottom: 20px;
        }

        .details-info li {
            margin-bottom: 4px;
            color: #475569;
            font-size: 0.9rem;
        }

        .details-nutrition {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }

        .nutrition-item {
            background: #f8fafc;
            border-radius: var(--radius-md);
            padding: 12px;
            border: 1px solid #e2e8f0;
            text-align: center;
        }

        .nutrition-item span {
            display: block;
            font-size: 0.75rem;
            color: #64748b;
            margin-bottom: 4px;
        }

        .nutrition-item strong {
            font-size: 1.1rem;
            color: #2563eb;
            font-weight: 700;
        }

        /* ===== FOOTER ===== */
        .footer {
            text-align: center;
            color: #64748b;
            padding: 1.5rem 0;
            font-size: 0.85rem;
        }

        /* ===== BREAKPOINTS ===== */
        @media (min-width: 768px) {
            .hero {
                padding: 48px 32px 56px;
                margin-bottom: 40px;
            }
            
            .search-container {
                margin-top: -24px;
            }
            
            .meal-image-container {
                height: 180px;
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

        @media (min-width: 1024px) {
            .hero {
                padding: 56px 48px 64px;
            }
            
            .hero h1 {
                font-size: 2.5rem;
            }
            
            .details-body {
                grid-template-columns: 2fr 3fr;
            }
        }

        /* ===== SCROLLBAR ===== */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )


def render_search_form():
    """Affiche le formulaire de recherche centré et compact."""
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    st.markdown('<div class="search-box">', unsafe_allow_html=True)
    
    # Input plus gros
    ingredients_input = st.text_input(
        "Ingrédients",
        key="ingredients_input",
        placeholder="Ex: poulet, riz, tomate...",
        label_visibility="collapsed",
    )
    
    # Bouton centré sous l'input
    st.markdown('<div class="search-button-container">', unsafe_allow_html=True)
    submitted = st.button("🔍 Rechercher", key="search_btn", use_container_width=False)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    return ingredients_input, submitted


def render_hero() -> None:
    """Affiche la section hero."""
    st.markdown(
        """
        <div class="hero">
            <div class="hero-content">
                <p class="eyebrow">Meal Recommender</p>
                <h1>Trouvez la recette parfaite</h1>
                <p>Saisissez vos ingrédients et découvrez des recettes adaptées.</p>
            </div>
        </div>
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
            <div style="color: #64748b; font-size: 0.85rem;">
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
