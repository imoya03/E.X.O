"""
Development server launcher.
Runs uvicorn with --reload limited to actual source folders,
avoiding reload loops from .venv/site-packages changes.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "web.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["web", "data", "config", "core", "physical"],
    )