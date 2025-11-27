from llm import get_llm
from tools import get_web_search_tool, travel_distance, get_hotel_recommendations, get_weather, convert_currency, create_itinerary
from prompt import SYSTEM_PROMPT
from langchain.agents import create_agent

def build_agent():
    tools = [get_web_search_tool, get_weather, get_hotel_recommendations, travel_distance, convert_currency, create_itinerary]
    llm = get_llm()
    llm_with_tools = llm.bind_tools(tools)
    agent = create_agent(
        tools=tools,
        model=llm_with_tools,
        system_prompt=SYSTEM_PROMPT
    )
    return agent