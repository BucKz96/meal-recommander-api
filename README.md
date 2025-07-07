# 🥘 Meal Recommender API

Recommandez facilement des plats en fonction des ingrédients que vous avez à disposition. Ce projet utilise **FastAPI** pour fournir une API performante et **Streamlit** pour une interface utilisateur interactive.

🔗 Démo en ligne : https://meal-recommander-streamlit.onrender.com


---

## 🚀 Stack technique

- [FastAPI](https://fastapi.tiangolo.com/) – API asynchrone, typée, documentée automatiquement
- [Streamlit](https://streamlit.io/) – UI simple et rapide pour tester les fonctionnalités
- [Pydantic](https://docs.pydantic.dev/) – Modèles de données robustes
- [pytest](https://docs.pytest.org/) – Tests unitaires
- [pandas](https://pandas.pydata.org/) – Manipulation de CSV

---

## 📁 Structure du projet

L'organisation suit une architecture claire :
- `app/` : contient l'API FastAPI, les modèles, la logique métier et les données.
- `streamlit_app/` : l'interface utilisateur avec Streamlit.
- `tests/` : les tests unitaires pour l'API.
- `requirements.txt` : les dépendances Python.

--- 

## ⚙️ Installation

### 1. Cloner le repo
```bash
git clone https://github.com/BucKz96/meal-recommander-api.git
cd meal-recommander-api
```

### 2. Créer un environnement virtuel
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

---

## 🧪 Lancer les services

### API FastAPI
```bash
uvicorn app.main:app --reload
```
→ Accès Swagger UI : http://localhost:8000/docs

### Interface utilisateur Streamlit
```bash
streamlit run streamlit_app/main.py
```

---

## ✅ Tester l'API

```bash
pytest
```

---

## 📌 Exemple d'appel API

```
GET /meals/by-ingredients?available_ingredients=chicken&available_ingredients=rice
```

Retourne :
```json
[
  {
    "name": "Chicken Curry",
    "ingredients": ["chicken", "curry sauce", "rice"],
    "calories": 400,
    "cuisine": "Indian"
  }
]
```

---

## 💡 Améliorations prévues

- Matching partiel (scoring par ingrédients)
- Filtrage par régime (végétarien, sans gluten, etc.)
- Déploiement sur Streamlit Cloud et Render
- Ajout de tests avancés (erreurs, cas limites)

---

## 👨‍💻 Auteur

**Maxime L.** – [https://github.com/BucKz96](https://github.com/BucKz96)

Projet développé comme vitrine pro d’un moteur de recommandation simple, rapide et extensible️.
