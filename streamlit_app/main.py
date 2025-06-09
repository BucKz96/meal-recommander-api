import streamlit as st
import requests

st.set_page_config(page_title="Recommandation de repas", layout="wide")

st.title("🍽️ Meal Recommender")
st.write("Obtiens des suggestions de repas selon les ingrédients que tu as sous la main.")

# Champ d'entrée utilisateur
user_ingredients = st.text_input("Ingrédients disponibles (séparés par des virgules)", "Chicken, Rice, Tomato")

if st.button("Recommander"):
    ingredients_list = [i.strip() for i in user_ingredients.split(",") if i.strip()]
    try:
        response = requests.get("http://localhost:8000/meals/by-ingredients", params={"available_ingredients": ingredients_list})
        response.raise_for_status()
        meals = response.json()

        if not meals:
            st.warning("Aucun plat trouvé avec les ingrédients donnés.")
        else:
            st.success(f"{len(meals)} repas trouvés :")
            for meal in meals:
                st.markdown(f"### {meal['name']}")
                st.write(f"- Ingrédients : {', '.join(meal['ingredients'])}")
                st.write(f"- Calories : {meal['calories']}")
                st.write(f"- Cuisine : {meal['cuisine']}")
                st.write("---")

    except Exception as e:
        st.error(f"Erreur lors de l'appel à l'API : {e}")
