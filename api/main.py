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

from fastapi.responses import FileResponse, RedirectResponse

app.mount("/static", StaticFiles(directory="frontend", html=False), name="static")

@app.get("/")
def read_index():
    return FileResponse("frontend/index.html")

@app.get("/{short_code}", response_class=RedirectResponse, status_code=307)
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    try:
        # Service already returns RedirectResponse
        return ShortURLService.get_shorturl(short_code, db)
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Short URL not found")
        raise e
