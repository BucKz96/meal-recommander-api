"""Composants de layout et styles CSS responsive.

Design mobile-first avec breakpoints:
- xs: < 480px (mobile)
- sm: 480px - 767px (large mobile)
- md: 768px - 1023px (tablet)
- lg: 1024px - 1199px (desktop)
- xl: >= 1200px (large desktop)
"""

import streamlit as st


def render_custom_css() -> None:
    """Injecte les styles CSS personnalisés responsive."""
    st.markdown(
        """
    <style>
        /* ===== VARIABLES CSS ===== */
        :root {
            --primary: #1d4ed8;
            --primary-light: #60a5fa;
            --accent: #38bdf8;
            --card-bg: #ffffff;
            --card-border: #dbeafe;
            --soft-bg: #eff6ff;
            --muted: #64748b;
            --text-dark: #0f172a;
            --button-text: #ffffff;
            --shadow-sm: 0 4px 6px rgba(15, 23, 42, 0.05);
            --shadow-md: 0 10px 20px rgba(15, 23, 42, 0.1);
            --shadow-lg: 0 20px 40px rgba(15, 23, 42, 0.15);
            --radius-sm: 12px;
            --radius-md: 20px;
            --radius-lg: 28px;
            --radius-xl: 36px;
        }

        /* ===== BASE ===== */
        .stApp {
            background: var(--app-background, radial-gradient(circle at top, #f8fbff 0%, #ecf2ff 55%, #e2e8f0 100%));
            min-height: 100vh;
        }

        /* ===== HERO SECTION ===== */
        .hero {
            position: relative;
            border-radius: var(--radius-xl);
            padding: 40px 20px 50px;
            margin-bottom: 40px;
            background: url("https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=1600&q=80")
                center/cover no-repeat;
            color: #fff;
            text-align: center;
            overflow: hidden;
            box-shadow: var(--shadow-lg);
        }

        .hero::after {
            content: "";
            position: absolute;
            inset: 0;
            background: radial-gradient(circle at top, rgba(15, 23, 42, 0.6), rgba(15, 23, 42, 0.2));
        }

        .hero-content {
            position: relative;
            max-width: 640px;
            margin: 0 auto;
            z-index: 1;
        }

        .hero .eyebrow {
            letter-spacing: 0.3em;
            text-transform: uppercase;
            font-size: 0.75rem;
            color: rgba(255,255,255,0.85);
        }

        .hero h1 {
            font-size: clamp(1.8rem, 5vw, 3.2rem);
            font-weight: 800;
            margin: 0.5rem 0 1rem;
            line-height: 1.2;
        }

        .hero p {
            font-size: clamp(0.9rem, 2.5vw, 1.1rem);
            margin: 0 auto;
            line-height: 1.5;
            color: rgba(255,255,255,0.9);
            max-width: 90%;
        }

        /* ===== SEARCH SECTION ===== */
        .search-section {
            width: min(480px, 94vw);
            margin: -30px auto 24px;
            padding: 0 12px;
            text-align: center;
            position: relative;
            z-index: 10;
        }

        .search-shell {
            background: var(--card-bg);
            border-radius: var(--radius-lg);
            border: 1.5px solid var(--card-border);
            padding: 20px;
            box-shadow: var(--shadow-lg);
        }

        .search-shell .stTextInput > div > div > input {
            font-size: 0.95rem;
            padding: 0.75rem 1rem;
            border-radius: var(--radius-md);
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
            margin: 0.75rem auto 0;
            font-size: 0.95rem;
            padding: 0.6rem 0;
            border-radius: 999px;
            width: 100%;
            max-width: 200px;
        }

        /* ===== BUTTONS ===== */
        .stButton > button {
            background: linear-gradient(120deg, var(--primary), var(--accent));
            border: none;
            color: var(--button-text, #fff);
            font-weight: 600;
            border-radius: 999px;
            padding: 0.5rem 1.2rem;
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.25);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 28px rgba(37, 99, 235, 0.35);
        }

        .stButton > button:active {
            transform: translateY(0);
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
            background: var(--card-bg);
            border: 1.5px solid var(--card-border);
            box-shadow: var(--shadow-md);
            margin-bottom: 20px;
        }

        .count-number {
            font-size: clamp(1.8rem, 4vw, 2.4rem);
            font-weight: 800;
            color: var(--primary);
            line-height: 1;
        }

        .count-label {
            font-size: 0.85rem;
            color: var(--muted);
            font-weight: 500;
        }

        /* ===== MEAL CARDS ===== */
        .meal-card-wrapper {
            padding: 8px;
        }

        .meal-card {
            background: var(--card-bg);
            border-radius: var(--radius-lg);
            overflow: hidden;
            border: 1.5px solid var(--card-border);
            box-shadow: var(--shadow-md);
            transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
            display: flex;
            flex-direction: column;
            height: 100%;
        }

        .meal-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
            border-color: var(--primary-light);
        }

        .meal-card--active {
            border-color: var(--primary);
            box-shadow: 0 20px 40px rgba(37, 99, 235, 0.2);
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
            transition: transform 0.35s ease;
        }

        .meal-card:hover .meal-image-container img {
            transform: scale(1.05);
        }

        .meal-badge {
            position: absolute;
            top: 12px;
            left: 12px;
            background: rgba(248, 250, 255, 0.95);
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--text-dark);
            border: 1px solid var(--card-border);
            backdrop-filter: blur(4px);
        }

        .meal-content {
            padding: 16px;
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        .meal-title {
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-dark);
            margin-bottom: 6px;
            line-height: 1.3;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .meal-meta {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            color: var(--muted);
            font-size: 0.8rem;
            margin-bottom: 10px;
        }

        .ingredients-list {
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
            margin-bottom: 12px;
        }

        .ingredient-tag {
            background: var(--soft-bg);
            color: var(--primary);
            padding: 3px 10px;
            border-radius: 999px;
            font-size: 0.7rem;
            border: 1px solid var(--card-border);
            white-space: nowrap;
        }

        .card-actions {
            padding: 12px 16px 16px;
            display: flex;
            gap: 8px;
            background: var(--card-bg);
            border-top: 1px solid var(--card-border);
            margin-top: auto;
        }

        .card-actions .stButton {
            flex: 1;
        }

        .card-actions .stButton > button {
            height: 32px;
            border-radius: 999px;
            font-size: 0.85rem;
            padding: 0;
            width: 100%;
        }

        .card-actions .stButton:first-child > button {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            color: var(--primary);
            box-shadow: none;
        }

        .card-actions .stButton:last-child > button {
            background: var(--primary);
            color: var(--button-text, #fff);
            border: none;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        }

        /* ===== MESSAGES ===== */
        .warning-message {
            background: linear-gradient(120deg, #eff6ff, #dbeafe);
            border-radius: var(--radius-md);
            padding: 20px;
            border: 1px solid var(--card-border);
            text-align: center;
            color: var(--text-dark);
            margin: 20px 0;
        }

        /* ===== DETAILS PANEL ===== */
        .details-panel {
            background: var(--card-bg);
            border-radius: var(--radius-lg);
            border: 1.5px solid var(--card-border);
            padding: 24px;
            box-shadow: var(--shadow-lg);
            margin-top: 1rem;
        }

        .details-header {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 20px;
        }

        .details-header .eyebrow {
            letter-spacing: 0.2em;
            text-transform: uppercase;
            font-size: 0.7rem;
            color: var(--muted);
            margin-bottom: 2px;
        }

        .details-header h3 {
            margin: 0;
            font-size: clamp(1.2rem, 3vw, 1.8rem);
            color: var(--text-dark);
            line-height: 1.3;
        }

        .details-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            color: var(--muted);
        }

        .details-meta span {
            background: var(--soft-bg);
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 0.8rem;
            border: 1px solid var(--card-border);
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
            border: 1px solid var(--card-border);
            box-shadow: var(--shadow-md);
        }

        .details-info h4 {
            margin-top: 0;
            margin-bottom: 10px;
            color: var(--text-dark);
            font-size: 1rem;
        }

        .details-info ul {
            padding-left: 18px;
            margin-bottom: 20px;
        }

        .details-info li {
            margin-bottom: 4px;
            color: var(--text-dark);
            font-size: 0.9rem;
        }

        .details-nutrition {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }

        .nutrition-item {
            background: var(--soft-bg);
            border-radius: var(--radius-md);
            padding: 10px 12px;
            border: 1px solid var(--card-border);
            text-align: center;
        }

        .nutrition-item span {
            display: block;
            font-size: 0.75rem;
            color: var(--muted);
            margin-bottom: 4px;
        }

        .nutrition-item strong {
            font-size: 1rem;
            color: var(--text-dark);
        }

        /* ===== FOOTER ===== */
        .footer {
            text-align: center;
            color: var(--muted);
            padding: 1.5rem 0;
            font-size: 0.85rem;
        }

        /* ===== BREAKPOINTS ===== */
        /* Small devices (480px and up) */
        @media (min-width: 480px) {
            .hero {
                padding: 50px 30px 60px;
            }
            
            .search-section {
                margin-top: -40px;
            }
            
            .meal-card-wrapper {
                padding: 12px;
            }
            
            .details-nutrition {
                grid-template-columns: repeat(4, 1fr);
            }
        }

        /* Medium devices (768px and up) */
        @media (min-width: 768px) {
            .hero {
                padding: 60px 40px 70px;
                margin-bottom: 50px;
            }
            
            .search-section {
                margin-top: -50px;
            }
            
            .search-shell {
                padding: 24px;
            }
            
            .results-header {
                padding: 20px 24px;
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

        /* Large devices (1024px and up) */
        @media (min-width: 1024px) {
            .hero {
                padding: 70px 60px 80px;
            }
            
            .hero h1 {
                font-size: 3rem;
            }
            
            .meal-image-container {
                height: 200px;
            }
            
            .details-body {
                grid-template-columns: 2fr 3fr;
            }
        }

        /* Extra large devices (1200px and up) */
        @media (min-width: 1200px) {
            .hero-content {
                max-width: 720px;
            }
            
            .meal-title {
                font-size: 1.1rem;
            }
        }

        /* Dark mode adjustments */
        @media (prefers-color-scheme: dark) {
            .meal-badge {
                background: rgba(30, 41, 59, 0.95);
                color: #f8fafc;
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
                <p>Indique les ingrédients disponibles et découvre instantanément des recettes adaptées.</p>
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
                <div class="count-label">recettes trouvées</div>
            </div>
            <div style="color: var(--muted); font-size: 0.85rem;">
                Affichage: {min(filtered_count, limit)} sur {total_count}
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
