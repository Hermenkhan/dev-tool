import requests

API_KEY = "e9c6d47717ab4738b733f4a8e15f9375"
BASE_URL = "https://newsapi.org/v2/everything"


def get_latest_news(topic: str, raw: bool = False):
    """
    Fetch latest news articles on a topic.
    """
    url = f"{BASE_URL}?q={topic}&apiKey={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or not data.get("articles"):
            return f"No news found for {topic}"

        articles = data["articles"]

        if raw:
            return articles

        result = f"Latest news on {topic}:\n"
        for a in articles[:5]:
            result += f"- {a['title']}: {a['url']}\n"
        return result
    except Exception as e:
        return f"Error fetching news: {e}"
