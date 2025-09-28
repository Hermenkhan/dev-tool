import streamlit as st
import pandas as pd

# Import tools
from tools.weather import get_weather
from tools.movies import get_movie_details
from tools.distance import get_distance
from tools.news import get_latest_news
from tools.recipes import get_recipe
from tools.calculator import calculator

# Import charts
from utils.charts import (
    weather_chart,
    movie_chart,
    news_wordcloud,
    recipe_nutrition_pie,
)

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Smart Assistant Dashboard", layout="wide")
st.sidebar.title("Smart Assistant Dashboard")
menu = st.sidebar.radio(
    "Choose a Tool",
    ["Weather", "Movies", "Distance", "News", "Recipes", "Calculator"],
)


# ---------------- WEATHER ----------------
if menu == "Weather":
    city = st.text_input("Enter city name", "London")
    if st.button("Get Weather"):
        data = get_weather(city, raw=True)  # raw=True -> return JSON dict
        if isinstance(data, dict):
            st.json(data)
            fig = weather_chart(data)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(data)


# ---------------- MOVIES ----------------
elif menu == "Movies":
    movie_name = st.text_input("Enter movie name", "Inception")
    if st.button("Get Movie Details"):
        data = get_movie_details(movie_name, raw=True)
        if isinstance(data, dict):
            st.json(data)
            fig = movie_chart(data)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(data)


# ---------------- DISTANCE ----------------
elif menu == "Distance":
    col1, col2 = st.columns(2)
    with col1:
        loc1 = st.text_input("Enter first location", "New York")
    with col2:
        loc2 = st.text_input("Enter second location", "Los Angeles")

    if st.button("Calculate Distance"):
        dist, coords = get_distance(loc1, loc2, raw=True)
        if dist:
            st.success(dist)

            # Map integration
            if coords:
                df = pd.DataFrame(coords, columns=["lat", "lon"])
                st.map(df)
        else:
            st.error("Could not calculate distance")


# ---------------- NEWS ----------------
elif menu == "News":
    topic = st.text_input("Enter a topic", "Technology")
    if st.button("Get News"):
        articles = get_latest_news(topic, raw=True)
        if isinstance(articles, list):
            for a in articles[:5]:
                st.write(f"- [{a['title']}]({a['url']})")

            fig = news_wordcloud(articles)
            if fig:
                st.pyplot(fig)
        else:
            st.error(articles)


# ---------------- RECIPES ----------------
elif menu == "Recipes":
    dish = st.text_input("Enter dish name", "Pasta")
    if st.button("Get Recipe"):
        recipe = get_recipe(dish, raw=True)
        if isinstance(recipe, dict):
            st.subheader(recipe.get("title", "Recipe"))
            st.write(recipe.get("instructions", "No instructions available."))

            fig = recipe_nutrition_pie(recipe)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(recipe)


# ---------------- CALCULATOR ----------------
elif menu == "Calculator":
    expr = st.text_input("Enter a mathematical expression", "2 + 3 * 4")
    if st.button("Calculate"):
        result = calculator(expr)
        if result is not None:
            st.success(f"Result: {result}")
            if "calc_history" not in st.session_state:
                st.session_state.calc_history = []
            st.session_state.calc_history.append(result)

            # Show history chart
            st.line_chart(st.session_state.calc_history)
        else:
            st.error("Invalid expression")
