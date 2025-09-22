




from fastapi import FastAPI, Query
from pydantic import BaseModel
import requests
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from dotenv import load_dotenv
import os
from math import radians, sin, cos, sqrt, atan2
from fastapi import HTTPException

load_dotenv()  # load .env if running locally

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=GOOGLE_API_KEY)


app = FastAPI()

# ---------- TOOLS ----------

@tool
def calculator(expression: str) -> float:
    """Evaluate a mathematical expression and return the result."""
    try:
        result = eval(expression, {"__builtins__": {}})
        return float(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"

@tool
def get_weather(city: str) -> str:
    """Fetches the current weather for a given city."""
    api_key = os.getenv("OPENWEATHER_API_KEY") or "049048adef5f0ac4aa3012b93db79b78"
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        city_name = data["name"]
        temp = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        return (
            f"Weather in {city_name}:\n"
            f"Temperature: {temp}°C\n"
            f"Condition: {weather_description.capitalize()}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        )
    except requests.exceptions.HTTPError:
        return "City not found. Please check the city name."
    except Exception as e:
        return f"An error occurred: {e}"

@tool
def get_latest_news(topic: str) -> str:
    """Fetches the latest news for a given topic."""
    api_key = os.getenv("NEWS_API_KEY") or "e9c6d47717ab4738b733f4a8e15f9375"
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data.get('articles'):
            articles = data['articles']
            result = f"Here are the latest news articles related to {topic}:\n"
            for article in articles[:5]:
                title = article['title']
                link = article['url']
                result += f"- {title}: {link}\n"
            return result
        else:
            return f"Error: Could not fetch news for {topic}. Reason: {data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"Error: Unable to fetch news. Details: {str(e)}"

@tool
def get_movie_details(movie_name: str) -> str:
    """Fetches detailed information about a movie using its name."""
    api_key = os.getenv("OMDB_API_KEY") or "31f29fd0"
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "True":
            title = data.get("Title", "N/A")
            year = data.get("Year", "N/A")
            genre = data.get("Genre", "N/A")
            director = data.get("Director", "N/A")
            plot = data.get("Plot", "N/A")
            imdb_rating = data.get("imdbRating", "N/A")

            return (
                f"Movie Details:\n"
                f"- Title: {title}\n"
                f"- Year: {year}\n"
                f"- Genre: {genre}\n"
                f"- Director: {director}\n"
                f"- Plot: {plot}\n"
                f"- IMDb Rating: {imdb_rating}/10"
            )
        else:
            return f"Movie not found: {movie_name}"
    except Exception as e:
        return f"Error fetching movie details: {str(e)}"

@tool
def get_recipe(dish_name: str) -> str:
    """Fetches a recipe for a given dish name using the Spoonacular API."""
    api_key = os.getenv("SPOON_API_KEY") or "716e3a77f3e841669be0a6974ff05b9b"

    try:
        url = f"https://api.spoonacular.com/recipes/complexSearch?query={dish_name}&apiKey={api_key}&number=1"
        response = requests.get(url)
        data = response.json()

        if data.get('results'):
            recipe_id = data['results'][0]['id']
            recipe_title = data['results'][0]['title']

            details_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={api_key}"
            details_response = requests.get(details_url)
            details_data = details_response.json()

            ingredients = details_data.get('extendedIngredients', [])
            instructions = details_data.get('instructions', 'No instructions available.')

            recipe_text = f"Recipe for {recipe_title}:\n\nIngredients:\n"
            for ingredient in ingredients:
                recipe_text += f"- {ingredient['original']}\n"

            recipe_text += f"\nInstructions:\n{instructions}"
            return recipe_text
        else:
            return f"Error: Could not find a recipe for {dish_name}."
    except Exception as e:
        return f"Error: Unable to fetch recipe. Details: {str(e)}"



@tool
def get_distance(location1: str, location2: str) -> str:
    """
    Calculates the distance between two locations using the OpenCage Geocoder API.
    """

    api_key = "52420d959f5749cfbd67a5258d590195"  # Replace with your OpenCage API key

    # Geocode the origin location
    url1 = f"https://api.opencagedata.com/geocode/v1/json?q={location1}&key={api_key}"
    response1 = requests.get(url1)

    # Geocode the destination location
    url2 = f"https://api.opencagedata.com/geocode/v1/json?q={location2}&key={api_key}"
    response2 = requests.get(url2)

    # Check if both responses are successful
    if response1.status_code == 200 and response2.status_code == 200:
        data1 = response1.json()
        data2 = response2.json()

        # Make sure both have at least one result
        if not data1.get('results') or not data2.get('results'):
            return f"Error: One or both locations not found. Check if both locations are valid.\nTool used: get_distance"

        try:
            # Extract latitude and longitude for both locations
            lat1 = data1['results'][0]['geometry']['lat']
            lon1 = data1['results'][0]['geometry']['lng']
            lat2 = data2['results'][0]['geometry']['lat']
            lon2 = data2['results'][0]['geometry']['lng']
        except (IndexError, KeyError):
            return f"Error: Could not parse coordinates from API response.\nTool used: get_distance"

        # Calculate the distance using the Haversine formula
        from math import radians, sin, cos, sqrt, atan2

        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # Radius of the Earth in kilometers
        radius = 6371.0

        # Calculate the distance
        distance = radius * c

        return f"Tool used: get_distance\n get_distance tool is used to find The distance between {location1} and {location2} is {distance:.2f} km."

    else:
        return f"Error: Could not calculate the distance. Check if both locations are valid.\nTool used: get_distance"




# ------------- LANGCHAIN AGENT -------------
tools = [calculator, get_weather, get_latest_news, get_movie_details, get_recipe, get_distance]

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=GOOGLE_API_KEY)

agent = initialize_agent(tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION)

# ---------- FASTAPI ROUTES ----------
@app.get("/")
def root():
    return {"message": "Welcome to Function Calling API"}

@app.get("/calculate")
def calculate(expression: str = Query(...)):
    return {"result": calculator(expression)}

@app.get("/weather")
def weather(city: str = Query(...)):
    return {"result": get_weather(city)}

@app.get("/news")
def news(topic: str = Query(...)):
    return {"result": get_latest_news(topic)}

@app.get("/movie")
def movie(movie_name: str = Query(...)):
    return {"result": get_movie_details(movie_name)}

@app.get("/recipe")
def recipe(dish_name: str = Query(...)):
    return {"result": get_recipe(dish_name)}


@app.get("/distance")
def distance(
    location1: str = Query(..., description="First location (e.g., New York)"),
    location2: str = Query(..., description="Second location (e.g., Los Angeles)")
):
    """
    FastAPI endpoint to calculate the distance between two locations.
    Works with LangChain @tool-decorated get_distance.
    """
    try:
        # Pass input as a single dict
        tool_input = {"location1": location1, "location2": location2}
        result = get_distance.run(tool_input)
        return {"result": result}
    except Exception as e:
        return {"error": f"Failed to compute distance: {str(e)}"}



# General agent endpoint
class AgentInput(BaseModel):
    prompt: str

@app.post("/agent")
def run_agent(input: AgentInput):
    response = agent.invoke(input.prompt)
    return {"output": response["output"]}
