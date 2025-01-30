import os 
from openai import OpenAI
from dotenv import load_dotenv

# client = OpenAI(
#     api_key = os.getenv("DEEPSEEK_API_KEY"),
#     base_url = "https://api.deepseek.com"   
# )



load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com"

INITIAL_TASKS = """
- Work: 4 hours (high priority)
- Study: 2 hours (high priority)
- Exercise: 1 hour (medium priority)
- Leisure: 1 hour (low priority)
"""

INITIAL_CONSTRAINTS = """
- Start time: 9:00 AM
- End time: 9:00 PM
- Recurring events:
  - Lunch: 12:00 PM for 1 hour
  - Dinner: 6:00 PM for 1 hour
"""