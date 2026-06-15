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

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from api.v1.database.db_connector import get_db
from api.v1.service.shorturl import ShortURLService

@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    # Ignore static files so they fall through to StaticFiles mount (though FastAPI matches routes first)
    if short_code in ["style.css", "app.js", "favicon.ico", "index.html"]:
        raise HTTPException(status_code=404)
        
    try:
        return ShortURLService.get_shorturl(short_code, db)
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Short URL not found")
        raise e

# Mount frontend static files to serve it together with the backend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
