from fastapi import FastAPI
from .routers import router

app = FastAPI(title="NASA Mega API Backend", version="1.0")

app.include_router(router)
