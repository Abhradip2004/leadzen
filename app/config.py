import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set")