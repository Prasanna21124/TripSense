from langchain_core.prompts import PromptTemplate
from llm import get_llm

def build_itinerary_chain():

    prompt = PromptTemplate(
        input_variables=["city", "days"],
        template="""
Create a detailed {days}-day travel itinerary for {city}.

Rules:
- Morning, Afternoon, Evening for each day
- Include recommended food, local transport, and tips
- If weather is bad, suggest indoor activities
- Keep it simple, helpful, realistic

Now generate itinerary. Don't give any extra explanations, note or suggestions just the itinerary itself.
        """
    )

    llm = get_llm()
    chain = prompt | llm 
    return chain
