import requests

API_KEY = "31f29fd0"
BASE_URL = "http://www.omdbapi.com/"


def get_movie_details(movie_name: str, raw: bool = False):
    """
    Fetch movie details from OMDB.
    """
    url = f"{BASE_URL}?t={movie_name}&apikey={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("Response") != "True":
            return f"Movie not found: {movie_name}"

        if raw:
            return data

        return (
            f"Title: {data.get('Title')}\n"
            f"Year: {data.get('Year')}\n"
            f"Genre: {data.get('Genre')}\n"
            f"Director: {data.get('Director')}\n"
            f"Plot: {data.get('Plot')}\n"
            f"IMDb Rating: {data.get('imdbRating')}/10"
        )
    except Exception as e:
        return f"Error fetching movie details: {e}"
