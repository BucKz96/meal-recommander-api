import streamlit as st
import requests

st.set_page_config(page_title="Recommandation de repas", layout="wide")

st.title("🍽️ Meal Recommender")
st.write("Obtiens des suggestions de repas personnalisés selon tes critères nutritionnels.")

# Input utilisateur
calories_max = st.number_input("Calories max", min_value=0, step=50, value=700)
min_proteins = st.number_input("Protéines min (g)", min_value=0, step=5, value=20)
vegetarian = st.checkbox("Végétarien seulement")

# Bouton de recommandation
if st.button("Recommander un repas"):
    params = {
        "max_calories": calories_max,
        "min_protein": min_proteins,
        "vegetarian": vegetarian
    }
    try:
        response = requests.get("http://localhost:8000/meals", params=params)
        response.raise_for_status()
        meals = response.json()

        if not meals:
            st.warning("Aucune suggestion ne correspond à tes critères.")
        else:
            st.success(f"{len(meals)} repas trouvés :")
            for meal in meals:
                st.markdown(f"### {meal['name']}")
                st.write(f"- Calories : {meal['calories']}")
                st.write(f"- Protéines : {meal['proteins']}g")
                st.write(f"- Végétarien : {'Oui' if meal.get('vegetarian') else 'Non'}")
                st.write("---")
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
