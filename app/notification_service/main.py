from fastapi.applications import FastAPI
from notification_service.routers import (telegram, ws)

app = FastAPI()

app.include_router(telegram.router)
app.include_router(ws.router)
