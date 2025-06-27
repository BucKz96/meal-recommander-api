import streamlit as st
import requests
import os
import ast

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Meal Recommender", layout="wide")

# --- Bannière avec overlay ---
st.markdown("""
    <div style="position: relative; text-align: center;">
        <img src="https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=1600&q=80"
             style="width: 100%; height: 250px; object-fit: cover; border-radius: 8px; margin-bottom: 1rem;" />
        <h1 style="
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-size: 3em;
            background-color: rgba(0,0,0,0.5);
            padding: 0.3em 1em;
            border-radius: 10px;
        ">
            🍽️ Meal Recommender
        </h1>
    </div>
""", unsafe_allow_html=True)

st.subheader("Find the best meals based on the ingredients you already have!")
st.markdown("Simply enter a list of available ingredients, and we’ll suggest delicious recipes you can make.")

# --- Entrée utilisateur ---
user_ingredients = st.text_input("🛒 Ingredients you have (comma-separated)", "Chicken, Rice, Tomato")

def display_or_unspecified(value):
    if value in [None, "", 0, "0", "0.0"]:
        return "Not specified"
    return str(value)

# --- Requête et affichage ---
if st.button("🔍 Find meals"):
    ingredients_list = [i.strip() for i in user_ingredients.split(",") if i.strip()]
    try:
        response = requests.get(
            f"{API_URL}/meals/by-ingredients",
            params={"available_ingredients": ingredients_list}
        )
        response.raise_for_status()
        meals = response.json()

        if not meals:
            st.warning("⚠️ No meals found for the given ingredients.")
        else:
            st.success(f"✅ {len(meals)} meal(s) found:")

            cols_per_row = 3
            for i in range(0, len(meals), cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    if i + j < len(meals):
                        meal = meals[i + j]
                        with cols[j]:
                            # Nom centré
                            name = meal.get('name', 'Unnamed meal')
                            st.markdown(f"""
                                <div style='
                                    height: 48px;
                                    text-align: center;
                                    font-size: 1.1em;
                                    font-weight: 600;
                                    overflow: hidden;
                                    text-overflow: ellipsis;
                                    display: -webkit-box;
                                    -webkit-line-clamp: 2;
                                    -webkit-box-orient: vertical;
                                    line-height: 1.2em;
                                '>{name}</div>
                            """, unsafe_allow_html=True)

                            # Image centrée, taille fixe
                            image_url = meal.get("image", "https://via.placeholder.com/200")
                            time = display_or_unspecified(meal.get('prep_time'))
                            st.markdown(
                                f"<div style='text-align: center;'>"
                                f"<img src='{image_url}' width='200' height='150' style='object-fit: cover; border-radius: 8px;'/>"
                                f"<br>"
                                f"<br>"
                                f"<p> ⏱️Time: {time} </p>" 
                                f"</div>",
                                unsafe_allow_html=True
                            )

                            # Temps de préparation
                            #st.markdown(f"⏱️ **Time:** {display_or_unspecified(meal.get('prep_time'))} min")

                            # Détail complet
                            with st.expander("📋 View recipe details"):
                                st.markdown(f"🍽️ **Dish type:** {display_or_unspecified(meal.get('dish_type'))}")
                                st.markdown(f"🥗 **Diet type:** {display_or_unspecified(meal.get('diet_type'))}")

                                ingredients = meal.get("ingredients", [])
                                st.markdown("**Ingredients:**")
                                st.markdown(", ".join(ingredients) if ingredients else "Not specified")

                                nutrition = meal.get("nutritions", {})
                                if isinstance(nutrition, str):
                                    try:
                                        nutrition = ast.literal_eval(nutrition)
                                    except:
                                        nutrition = {}

                                if nutrition:
                                    st.markdown("**Nutrition (per serving):**")
                                    st.table({k.capitalize(): f"{v:.2f}" for k, v in nutrition.items()}.items())
                                else:
                                    st.markdown("Nutrition information not available.")

                            st.markdown("---")

    except Exception as e:
        st.error(f"❌ Error while contacting API: {e}")
