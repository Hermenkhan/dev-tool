# app.py  (Streamlit frontend)

import streamlit as st
import requests

API_URL = "http://127.0.0.1:8007"  # FastAPI backend

st.set_page_config(page_title="Function Calling App", page_icon="⚡")

st.title("⚡ Function Calling API Frontend")

st.sidebar.header("Choose an action")

option = st.sidebar.selectbox(
    "Select Endpoint",
    (
        "Weather",
        "News",
        "Movie",
        "Recipe",
        "Distance",
        "Calculator",
        "Agent"
    )
)

if option == "Weather":
    city = st.text_input("Enter city name:")
    if st.button("Get Weather"):
        res = requests.get(f"{API_URL}/weather", params={"city": city})
        st.write(res.json())

elif option == "News":
    topic = st.text_input("Enter topic:")
    if st.button("Get News"):
        res = requests.get(f"{API_URL}/news", params={"topic": topic})
        st.write(res.json())

elif option == "Movie":
    movie = st.text_input("Enter movie name:")
    if st.button("Get Movie Details"):
        res = requests.get(f"{API_URL}/movie", params={"movie_name": movie})
        st.write(res.json())

elif option == "Recipe":
    dish = st.text_input("Enter dish name:")
    if st.button("Get Recipe"):
        res = requests.get(f"{API_URL}/recipe", params={"dish_name": dish})
        st.write(res.json())

elif option == "Distance":
    loc1 = st.text_input("Enter first location:")
    loc2 = st.text_input("Enter second location:")
    if st.button("Calculate Distance"):
        res = requests.get(f"{API_URL}/distance", params={"location1": loc1, "location2": loc2})
        st.write(res.json())

elif option == "Calculator":
    expr = st.text_input("Enter mathematical expression:")
    if st.button("Calculate"):
        res = requests.get(f"{API_URL}/calculate", params={"expression": expr})
        st.write(res.json())

elif option == "Agent":
    prompt = st.text_area("Enter prompt for the agent:")
    if st.button("Ask Agent"):
        res = requests.post(f"{API_URL}/agent", json={"prompt": prompt})
        st.write(res.json())
