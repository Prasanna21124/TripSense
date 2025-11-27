from langchain_google_genai import ChatGoogleGenerativeAI
from config import GEMINI_API_KEY

def get_llm():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        api_key=GEMINI_API_KEY
    )
    return llm