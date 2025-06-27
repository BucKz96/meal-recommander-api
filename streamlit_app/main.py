import streamlit as st
import requests
import os
import ast

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Meal Recommender",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- CSS global ---
st.markdown("""
    <style>
    html, body, .main, [data-testid="stAppViewContainer"], [data-testid="stVerticalBlock"] {
        background-color: #fdfaf4 !important;
        color: #000000 !important;
        font-family: 'Segoe UI', sans-serif;
    }

    input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #3AA17E !important;
        border-radius: 6px !important;
        padding: 0.5rem;
    }

    button {
        background-color: #3AA17E !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        transition: background-color 0.3s ease, box-shadow 0.3s ease;
    }
    button:hover {
        background-color: #2e8b6d !important;
        box-shadow: 0 0 10px rgba(58, 161, 126, 0.4);
    }

    .card {
        background-color: #ffffff;
        border: 1px solid #3AA17E;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        height: 100%;
        transition: all 0.3s ease-in-out;
    }

    .meal-count {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2e8b6d;
        margin: 1rem 0 1.5rem;
        text-align: center;
    }

    summary {
        cursor: pointer;
        text-align: center;
        font-weight: 600;
        color: #3AA17E;
        padding: 0.5rem;
        border-top: 1px solid #3AA17E;
        list-style: none;
    }

    .details-wrapper {
        background-color: #f0fdf7;
        border-radius: 8px;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Bannière ---
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
            🍲 Meal Recommender
        </h1>
    </div>
""", unsafe_allow_html=True)

st.subheader("Find the best meals based on the ingredients you already have!")
st.markdown("Simply enter a list of available ingredients, and we’ll suggest delicious recipes you can make.")

user_ingredients = st.text_input("🍇 Ingredients you have (comma-separated)", "Chicken, Rice, Tomato")

def display_or_unspecified(value):
    if value in [None, "", 0, "0", "0.0"]:
        return "Not specified"
    return str(value)

if st.button("🍎 Find meals"):
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
            st.markdown(f"""
                <div class="meal-count">
                    🍽️ {len(meals)} delicious meal(s) available
                </div>
            """, unsafe_allow_html=True)

            cols_per_row = 3
            for i in range(0, len(meals), cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    if i + j < len(meals):
                        meal = meals[i + j]
                        with cols[j]:
                            image_url = meal.get("image", "https://via.placeholder.com/200")
                            prep_time = display_or_unspecified(meal.get("prep_time"))

                            ingredients = meal.get("ingredients", [])
                            nutrition = meal.get("nutritions", {})
                            if isinstance(nutrition, str):
                                try:
                                    nutrition = ast.literal_eval(nutrition)
                                except:
                                    nutrition = {}

                            nutrition_table = ""
                            if nutrition:
                                nutrition_table = "<table><tbody>" + "".join(
                                    f"<tr><td><strong>{k.capitalize()}</strong></td><td>{v:.2f}</td></tr>"
                                    for k, v in nutrition.items()
                                ) + "</tbody></table>"

                            card_html = f'''
                            <div class="card">
                              <div style="text-align: center; font-weight: bold; font-size: 1.5rem; margin-bottom: 0.5rem;">
                                {meal.get("name", "Unnamed Meal")}
                              </div>
                              <div style="text-align: center;">
                                <img src="{image_url}" width="200" height="150"
                                     style="object-fit: cover; border-radius: 8px;" />
                                <div style="margin-top: 0.5rem;">
                                  ⏱️ <strong>Time:</strong> {prep_time}
                                </div>
                              </div>
                              <details class="details-wrapper">
                                <summary>🔹 View recipe details</summary>
                                <div style="padding-top: 1rem;">
                                    <p>🍲 <strong>Dish type:</strong> {display_or_unspecified(meal.get('dish_type'))}</p>
                                    <p>🦪 <strong>Diet type:</strong> {display_or_unspecified(meal.get('diet_type'))}</p>
                                    <p><strong>Ingredients:</strong><br>{', '.join(ingredients) if ingredients else 'Not specified'}</p>
                                    <p><strong>Nutrition (per serving):</strong><br>{nutrition_table if nutrition_table else 'Nutrition information not available.'}</p>
                                </div>
                              </details>
                            </div>
                            '''
                            st.markdown(card_html, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error while contacting API: {e}")
