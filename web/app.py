from contextlib import asynccontextmanager
import asyncio

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config import settings
from web import websocket_server, rest_api
from core.orchestrator import Orchestrator

orchestrator_task = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global orchestrator_task
    if settings.ENABLE_ORCHESTRATOR:
        orchestrator = Orchestrator()
        orchestrator_task = asyncio.create_task(orchestrator.run())
        print("[App] Orchestrator started.")

    yield

    if orchestrator_task:
        orchestrator_task.cancel()
        print("[App] Orchestrator stopped.")


app = FastAPI(title="EXO API", lifespan=lifespan)

app.include_router(rest_api.router)
app.include_router(websocket_server.router)

from fastapi.responses import Response
from starlette.staticfiles import StaticFiles as StarletteStaticFiles


class NoCacheStaticFiles(StarletteStaticFiles):
    """During development, prevent the browser from caching static files
    (HTML/JS/JSON) so edits are reflected immediately without hard-refresh."""

    def file_response(self, *args, **kwargs) -> Response:
        response = super().file_response(*args, **kwargs)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return response


app.mount("/", NoCacheStaticFiles(directory="web/static", html=True), name="static")