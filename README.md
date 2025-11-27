# TripSense – AI Travel & Itinerary Planner

TripSense is an AI-powered travel assistant that helps users:

- Plan multi-day itineraries
- Check live weather for destinations
- Find hotels and restaurants
- Calculate distances between cities
- Convert currencies for international trips

Built with **LangChain**, **Gemini**, **Streamlit**, and custom tools, TripSense acts like a smart travel buddy you can chat with.

---

## Features

### AI Travel Agent
- Uses **Gemini 2.5 Flash** via `langchain-google-genai`
- Follows a **system prompt** designed for:
  - Structured itineraries (Day 1 / Day 2 / Day 3…)
  - Practical travel suggestions
  - Clear, human-like answers (no visible chain-of-thought)
  
### Custom Tools (LangChain @tool)

TripSense uses several tools to solve real-world travel tasks:

- `get_web_search_tool`  
  Uses **Tavily Search** API to fetch:
  - attractions
  - points of interest
  - general travel info

- `get_weather`  
  Uses **OpenWeather API** to fetch:
  - current weather
  - temperature
  - description, humidity

- `get_hotel_recommendations`  
  Combines Tavily search and custom prompts to suggest:
  - hotels
  - restaurants
  - places to stay

- `travel_distance`  
  Uses **Nominatim (OpenStreetMap)** + **geopy** to:
  - convert city names → coordinates
  - compute distance between two cities 

- `convert_currency`  
  Uses an exchange-rate API to:
  - convert amounts from one currency to other
  - validate currency codes

- `create_itinerary`  
  Uses a custom **itinerary chain** (`itinerary_chain.py`) to:
  - generate multi-day itineraries based on:
    - city
    - number of days
    - user preferences

---

## Tech Stack

- **Frontend**: Streamlit (`st.chat_message`, `st.chat_input`)
- **LLM Orchestration**: LangChain
- **Model**: `gemini-2.5-flash` via `langchain-google-genai`
- **Web Search**: Tavily API
- **Weather**: OpenWeather API
- **Currency**: Exchange rate API
- **Geocoding & Distance**: Nominatim + geopy
- **Memory**: Simple JSON-based chat history (`chat_history.json`)
- **Extras**:
  - Typewriter-style response animation
  - Download last response as `.txt`
  - Custom logo

---

## UI / UX (Streamlit)

- Clean chat-style interface
- User and assistant bubbles
- Sidebar:
  - App title & navigation header
  - "Clear History" button
  - About information
- Main area:
  - Past conversation loaded
  - New chat input at the bottom
  - Typewriter effect for assistant replies
  - Download button to save last response

---

## Project Structure

```bash
TripSense/
├── app.py                # Streamlit main app
├── agent.py              # LangChain agent + tool wiring
├── tools.py              # All custom tools (@tool)
├── itinerary_chain.py    # Itinerary Prompt + LLM Chain
├── llm.py                # LLM configuration (Gemini)
├── history_manager.py    # JSON-based chat history storage
├── config.py             # API keys & config variables (not committed)
├── requirements.txt      # Python dependencies
├── logo.png              # App logo used in UI
└── README.md             # Project documentation
