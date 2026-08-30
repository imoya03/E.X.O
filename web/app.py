from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from web import websocket_server, rest_api

app = FastAPI(title="EXO API")

app.include_router(rest_api.router)
app.include_router(websocket_server.router)

app.mount("/", StaticFiles(directory="web/static", html=True), name="static")