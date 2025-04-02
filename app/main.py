from fastapi import FastAPI
from app.routes import contacts

app = FastAPI()

app.include_router(contacts.router, prefix="/api")
