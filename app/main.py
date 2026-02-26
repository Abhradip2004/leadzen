from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.routes.whatsapp import router as whatsapp_router
from app.routes.test import router as test_router

app = FastAPI()

app.include_router(whatsapp_router)
app.include_router(test_router)