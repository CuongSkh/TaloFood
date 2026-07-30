from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import ALLOWED_ORIGINS, IMAGE_DIR
from app.routers.products import router as products_router

IMAGE_DIR.mkdir(parents=True, exist_ok=True)
app = FastAPI(title="TaloFood API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=ALLOWED_ORIGINS, allow_credentials=True,
                   allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], allow_headers=["*"])
app.mount("/images", StaticFiles(directory=IMAGE_DIR), name="images")
app.include_router(products_router)

@app.get("/", tags=["System"])
def root():
    return {"message": "TaloFood API is running"}

@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}
