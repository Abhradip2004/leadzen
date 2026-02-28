from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.routes.whatsapp import router as whatsapp_router
from app.routes.test import router as test_router

from app.routes.admin import router as admin_router

app = FastAPI()

app.include_router(whatsapp_router)
app.include_router(test_router)

app.include_router(admin_router)