from langchain.tools import tool
from dotenv import load_dotenv
import os
import requests
from .rag import rag_search

load_dotenv()

API_KEY=os.getenv("STOCK_API_KEY")

@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol 
    using Alpha Vantage Global Quote API.
    """
    url = (
        "https://www.alphavantage.co/query"
        f"?function=GLOBAL_QUOTE"
        f"&symbol={symbol}"
        f"&apikey={API_KEY}"
    )

    response = requests.get(url)
    return response.json()


#creating list of tools
tools=[get_stock_price,rag_search]

