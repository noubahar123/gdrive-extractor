# main.py
import logging
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import your DB and routers (adjust these import paths to your project layout)
from .database import Base, engine
from .routes.import_google_drive import router as import_router
from .routes.images import router as images_router

# Create DB tables (if you want to keep this here)
Base.metadata.create_all(bind=engine)

# App
app = FastAPI(title="Image Import API")

# -------------------------
# CORS configuration (exact origins, no trailing slash)
# -------------------------
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://humorous-creation-production-841f.up.railway.app",  # your frontend origin
    # add other allowed origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # allow OPTIONS, POST, GET, etc.
    allow_headers=["*"],
)

# -------------------------
# Short-circuit preflight OPTIONS (safe fallback)
# This prevents other middleware/dependencies/validators from running for OPTIONS.
# CORSMiddleware will attach Access-Control-Allow-* headers for the response.
# -------------------------
@app.middleware("http")
async def short_circuit_options(request: Request, call_next):
    if request.method == "OPTIONS":
        # Return an empty 200 response for preflight
        return Response(status_code=200)
    return await call_next(request)

# -------------------------
# Debug logging middleware (temporary, remove in production)
# -------------------------
logger = logging.getLogger("uvicorn.error")

@app.middleware("http")
async def log_options(request: Request, call_next):
    if request.method == "OPTIONS":
        logger.info(f"OPTIONS request to {request.url.path} headers: {dict(request.headers)}")
    try:
        return await call_next(request)
    except Exception as exc:
        # Log exceptions and re-raise so normal error handlers apply
        logger.exception("Unhandled exception during request")
        raise

# -------------------------
# (Optional) Explicit OPTIONS route for the single endpoint
# If you prefer an explicit route instead of relying on the middleware,
# you can keep this. It's safe and fast.
# -------------------------
@app.options("/api/v1/import/google-drive")
async def import_google_drive_options():
    # Return 200; CORSMiddleware will add CORS headers to this response.
    return Response(status_code=200)

# -------------------------
# Root and routers
# -------------------------
@app.get("/", response_class=JSONResponse)
def root():
    return {"message": "Image Import API is running"}

# include your routers after CORS & middlewares
app.include_router(import_router, prefix="/api/v1")
app.include_router(images_router, prefix="/api/v1")
