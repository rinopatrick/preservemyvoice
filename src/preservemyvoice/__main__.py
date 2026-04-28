from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .api import router as api_router
from .config import settings
from .logging import setup_logging

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes (must come before static mount)
app.include_router(api_router)

# Mount static files (for frontend) - LAST so API routes take priority
static_dir = "./frontend/dist"
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


@app.get("/")
async def root():
    """Serve the main page."""
    return FileResponse(f"{static_dir}/index.html")


@app.get("/api")
async def api_root():
    """API root info."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
    }


def main() -> None:
    """Entry point for the application."""
    import uvicorn

    uvicorn.run(
        "preservemyvoice.__main__:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info",
    )


if __name__ == "__main__":
    main()
