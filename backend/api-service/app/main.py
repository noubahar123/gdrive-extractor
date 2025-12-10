from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routes.import_google_drive import router as import_router
from .routes.images import router as images_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Image Import API")

# 👇 CORS config
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # or ["*"] during dev
    allow_credentials=True,
    allow_methods=["*"],          # important: allow OPTIONS & POST
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Image Import API is running"}


# Routers
app.include_router(import_router, prefix="/api/v1")
app.include_router(images_router, prefix="/api/v1")
