from fastapi import FastAPI
from .routes import router

app=FastAPI(tittle="langgraph")
app.include_router(router)