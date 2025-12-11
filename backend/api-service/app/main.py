# main.py
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import logging

from .database import Base, engine
from .routes.import_google_drive import router as import_router
from .routes.images import router as images_router

# create tables (keep as is)
Base.metadata.create_all(bind=engine)

# basic app
app = FastAPI(title="Image Import API")

# ---- CORS (must be added before routers and other middleware) ----
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://humorous-creation-production-841f.up.railway.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],    # allow OPTIONS & POST etc.
    allow_headers=["*"],
)

# ---- Short-circuit preflight OPTIONS (safe fallback) ----
@app.middleware("http")
async def short_circuit_options(request: Request, call_next):
    if request.method == "OPTIONS":
        # Return empty 200 so preflight succeeds (CORS headers are added by CORSMiddleware)
        return Response(status_code=200)
    return await call_next(request)

# ---- Optional debug logging for OPTIONS (temporary) ----
logger = logging.getLogger("uvicorn.error")
@app.middleware("http")
async def log_options(request: Request, call_next):
    if request.method == "OPTIONS":
        logger.info(f"OPTIONS headers: {dict(request.headers)}")
    return await call_next(request)

# root + routers
@app.get("/")
def root():
    return {"message": "Image Import API is running"}

app.include_router(import_router, prefix="/api/v1")
app.include_router(images_router, prefix="/api/v1")
