import pandas as pd
import plotly.express as px
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# ---------------- WEATHER ----------------
def weather_chart(weather_data: dict):
    """
    Create a temperature + humidity + wind chart from weather API response.
    """
    try:
        df = pd.DataFrame({
            "Metric": ["Temperature (°C)", "Humidity (%)", "Wind Speed (m/s)"],
            "Value": [
                weather_data.get("main", {}).get("temp", 0),
                weather_data.get("main", {}).get("humidity", 0),
                weather_data.get("wind", {}).get("speed", 0),
            ]
        })

        fig = px.bar(
            df,
            x="Metric",
            y="Value",
            color="Metric",
            title=f"Weather Overview: {weather_data.get('name', 'Unknown')}",
            text="Value"
        )
        fig.update_traces(textposition="outside")
        return fig
    except Exception as e:
        st.error(f"Error creating weather chart: {e}")
        return None


# ---------------- MOVIES ----------------
def movie_chart(movie_data: dict):
    """
    Create a bar chart for IMDb rating.
    """
    try:
        rating = float(movie_data.get("imdbRating", 0))

        fig = px.bar(
            x=[movie_data.get("Title", "Movie")],
            y=[rating],
            title=f"IMDb Rating for {movie_data.get('Title', 'Movie')}",
            labels={"x": "Movie", "y": "Rating"}
        )
        fig.update_yaxes(range=[0, 10])
        return fig
    except Exception as e:
        st.error(f"Error creating movie chart: {e}")
        return None


# ---------------- NEWS ----------------
def news_wordcloud(articles: list):
    """
    Generate a word cloud from a list of news article titles.

    Args:
        articles (list): List of dicts with 'title' field.

    Returns:
        matplotlib Figure
    """
    try:
        text = " ".join([a.get("title", "") for a in articles])
        wc = WordCloud(width=800, height=400, background_color="white").generate(text)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        return fig
    except Exception as e:
        st.error(f"Error creating word cloud: {e}")
        return None


# ---------------- RECIPES ----------------
def recipe_nutrition_pie(recipe_data: dict):
    """
    Create a pie chart of nutrition data from Spoonacular API.

    Args:
        recipe_data (dict): Recipe info with 'nutrition' field containing nutrients.

    Returns:
        plotly Figure
    """
    try:
        nutrients = recipe_data.get("nutrition", {}).get("nutrients", [])
        if not nutrients:
            st.warning("No nutrition data available for this recipe.")
            return None

        df = pd.DataFrame(nutrients)
        # Only keep top nutrients (Calories, Fat, Protein, Carbs, etc.)
        df = df[df["name"].isin(["Calories", "Fat", "Protein", "Carbohydrates"])]

        fig = px.pie(
            df,
            names="name",
            values="amount",
            title=f"Nutrition Breakdown: {recipe_data.get('title', 'Recipe')}"
        )
        return fig
    except Exception as e:
        st.error(f"Error creating nutrition chart: {e}")
        return None
