from langchain_tavily import TavilySearch
from config import TAVILY_API_KEY
from langchain.tools import tool
from geopy.distance import geodesic
import requests
from config import OPENWEATHER_API_KEY
from config import EXCHANGE_API_KEY
from itinerary_chain import build_itinerary_chain
import re

tavily = TavilySearch(
    api_key=TAVILY_API_KEY,
    max_results=5,
    topic="general",
)

@tool
def get_web_search_tool(query: str):
    """Perform a web search for the given query and return the results."""

    response = tavily.invoke(query)
    results = response.get("results", [])
    content = ""

    for result in results:
        content += result.get("content", "")

    return content

def extract_cities(query: str):
    words = query.split()

    cities = []
    current = []

    for w in words:
        if w and w[0].isalpha() and w[0].isupper():
            current.append(w)
        else:
            if current:
                cities.append(" ".join(current))
                current = []

    if current:
        cities.append(" ".join(current))

    if len(cities) < 2:
        return None, None

    return cities[0], cities[1]

@tool
def travel_distance(query: str):
    """
    Calculates the distance of two cities OR two GPS coordinates.
    Automatically converts city names to coordinates when needed. Also supports conversion after knowing the name of two places.
    """
    try:
        # Otherwise, treat it as city names
        city1, city2 = extract_cities(query)

        def get_coords(city):
            url = f"https://nominatim.openstreetmap.org/search?format=json&q={city}"
            r = requests.get(url, headers={"User-Agent": "TravelAgent"}).json()
            if not r:
                return None
            return float(r[0]["lat"]), float(r[0]["lon"])

        c1 = get_coords(city1)
        c2 = get_coords(city2)

        if not c1 or not c2:
            return "Could not determine coordinates for one or both cities."

        km = geodesic(c1, c2).km
        return f"Distance from {city1} to {city2}: {km:.2f} km"

    except Exception as e:
        return f"Error calculating distance: {e}"

@tool
def get_weather(city: str):
    """
    Returns real-time weather for a city using OpenWeather API. 
    """
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        r = requests.get(url).json()

        if "main" not in r:
            return "Weather not found. Check city name."

        temp = r["main"]["temp"]
        desc = r["weather"][0]["description"]
        humidity = r["main"]["humidity"]

        return f"Weather in {city}: {temp}°C, {desc}, Humidity {humidity}%"
    except Exception as e:
        return f"Weather tool error: {e}"

@tool
def get_hotel_recommendations(city):
    """
    Get hotels and restuarants for the given city
    The tool will automatically detect the city and price (if provided),
    and search for hotel recommendations accordingly. Also fetches restaurants based on distance and weather.
    """
    query = f"Hotels & Restaurants in {city}"
    return get_web_search_tool.invoke(query)

@tool
def convert_currency(data: str):
    """
    Converts currency.
    Input format: '100 USD to INR'
    """
    try:
        amount, base, _, target = data.split()
        amount = float(amount)

        url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/{base.upper()}"
        r = requests.get(url).json()

        rate = r["conversion_rates"].get(target.upper())
        if not rate:
            return "Invalid currency code."

        return f"{amount} {base} = {amount * rate:.2f} {target}"
    except Exception as e:
        return f"Currency tool error: {e}"

@tool
def create_itinerary(input_text: str):
    """
    Create a detailed travel itinerary.
    User input format example:
    'Plan a 3 day trip to Goa'
    'Make a 2-day itinerary for Mumbai'

    The tool auto-detects city & days, fetches attractions and weather,
    then uses the itinerary chain to generate a final itinerary.
    """



    # Extract days
    day_match = re.search(r"(\d+)\s*day", input_text.lower())
    days = day_match.group(1) if day_match else "3"

    # Extract city → last word approach
    words = input_text.split()
    city = words[-1]

    # Build itinerary chain
    chain = build_itinerary_chain()
    result = chain.invoke({
        "city": city,
        "days": days
    })

    return result