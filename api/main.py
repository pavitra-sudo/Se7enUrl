from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.v1.router.shorturl import router as shorturl_router
from api.v1.database.database import engine, ShortURLBase
# Import models to ensure they are registered with the Base
from api.v1.model.shorturl import ShortURL

# Create database tables automatically
ShortURLBase.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(shorturl_router)

# Mount frontend static files to serve it together with the backend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
