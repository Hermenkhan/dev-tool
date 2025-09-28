import requests

API_KEY = "716e3a77f3e841669be0a6974ff05b9b"
SEARCH_URL = "https://api.spoonacular.com/recipes/complexSearch"
DETAIL_URL = "https://api.spoonacular.com/recipes/{id}/information"


def get_recipe(dish_name: str, raw: bool = False):
    """
    Fetch recipe + nutrition details for a dish.
    """
    try:
        search_url = f"{SEARCH_URL}?query={dish_name}&apiKey={API_KEY}&number=1&addRecipeNutrition=true"
        resp = requests.get(search_url)
        data = resp.json()

        if not data.get("results"):
            return f"No recipe found for {dish_name}"

        recipe = data["results"][0]

        if raw:
            return recipe

        ingredients = recipe.get("nutrition", {}).get("ingredients", [])
        inst = recipe.get("instructions", "No instructions available.")

        out = f"Recipe for {recipe['title']}:\n\nIngredients:\n"
        for ing in ingredients[:10]:
            out += f"- {ing['name']}: {ing['amount']} {ing['unit']}\n"
        out += f"\nInstructions:\n{inst}"

        return out
    except Exception as e:
        return f"Error fetching recipe: {e}"
