# Memory - Meal Recommender API

> Fichier de contexte pour les sessions futures. Dernière mise à jour : 2026-02-04

---

## 🏗️ Architecture du Projet

### Backend (FastAPI)
```
src/
├── api/           # Routes FastAPI
├── core/          # Config, logging
├── models/        # Modèles Pydantic
└── services/      # Logique métier (recommandation, cache)
```

### Frontend (Streamlit)
```
streamlit_app/
├── components/
│   ├── cards.py      # Cartes recettes + MODAL détails
│   └── layout.py     # CSS + barre recherche + hero
├── api_client.py     # Appels API avec @st.cache_data
├── favorites.py      # Gestion favoris + import/export JSON
├── filters.py        # Filtres sidebar (cuisine, limite)
├── history.py        # Historique recherches sidebar
├── main.py           # Point d'entrée application
└── utils.py          # Utilitaires (images, HTML escape)
```

---

## ✅ Derniers Changements Majeurs (2026-02-04)

### UI Streamlit Refactorée
1. **Barre de recherche** :
   - Centrée avec max-width: 480px
   - Input agrandi (font-size: 1.1rem)
   - Bouton centré sous l'input
   - Suppression du div blanc parasite

2. **Cartes de recettes** :
   - HTML/CSS pour l'affichage (image, titre, tags ingrédients)
   - Boutons d'action EN DEHORS du HTML (contrainte Streamlit) :
     - `☆/⭐` : Favoris (toggle)
     - `+` : Ouvre modal détails
   - Style bleu #2563eb cohérent

3. **Modal détails** :
   - Utilise `st.dialog()` (Streamlit 1.44+)
   - Affiche : image grande, métriques, ingrédients complets, nutrition
   - Bouton "⭐ Ajouter aux favoris" intégré

### Code nettoyé
- ❌ Supprimé : `theme.py` (thème intégré dans layout.py)
- ❌ Supprimé : `details.py` (remplacé par modal dans cards.py)

---

## 📊 État Actuel

| Aspect | Status |
|--------|--------|
| Tests | 35/35 passent ✅ |
| Ruff | 0 erreur ✅ |
| MyPy | 1 warning (stubs requests - acceptable) |
| Coverage | >80% |

### Couleurs du thème
- Primary : `#2563eb` (bleu)
- Gradient : `#2563eb` → `#1d4ed8`
- Hover : `#1d4ed8` → `#1e40af`

---

## 🔧 Points Techniques Importants

### Contraintes Streamlit
- Les boutons dans `st.markdown()` ne fonctionnent PAS
- Solution : HTML pour le visuel + `st.button()` en dehors pour l'interactivité
- `st.dialog()` nécessite Streamlit >= 1.44

### Cache
- Backend : `lru_cache` sur les services
- Frontend : `@st.cache_data(ttl=300)` sur `fetch_meals()`

### API Backend
- URL : `http://localhost:8000` (défaut)
- Endpoints utilisés :
  - `GET /meals/by-ingredients?available_ingredients=X&available_ingredients=Y`
  - `GET /meals/all`
  - `GET /health`

---

## 📝 Pour la Prochaine Session

### Si bug sur la recherche
- Vérifier que `ingredients_input` est bien récupéré via `st.session_state`
- Le formulaire utilise `clear_on_submit=False`

### Si problème de style
- Les styles sont dans `render_custom_css()` dans `layout.py`
- Utiliser `!important` pour surcharger Streamlit

### Si besoin d'ajouter une fonctionnalité
- Favoris : voir `favorites.py` (JSON en session_state)
- Filtres : voir `filters.py` (sidebar expander)
- Nouveau composant : créer dans `components/`

---

## 🔗 Liens Utiles

- Repo : `https://github.com/BucKz96/meal-recommander-api`
- Dernier commit : `0c9eb37` - "Refactor: UI Streamlit avec modals et barre de recherche centree"
