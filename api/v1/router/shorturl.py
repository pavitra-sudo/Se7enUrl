from fastapi import APIRouter,HTTPException,Depends
from fastapi.responses import RedirectResponse
from api.v1.database.db_connector import get_db
from sqlalchemy.orm import Session
from api.v1.model.shorturl import ShortURL
from api.v1.schema.shorturl import ShortURLRequest, ShortURLResponse
from api.v1.service.shorturl import ShortURLService


router = APIRouter(prefix="/api/v1/shorturl", tags=["ShortURL"])


@router.post("/", response_model=ShortURLResponse, status_code=201,responses={400: {"description": "Bad Request"}})
def create_shorturl(r: ShortURLRequest, db: Session = Depends(get_db)):
    return ShortURLService.post_shorturl(r, db)


@router.get("/{short_code}", response_model=ShortURLResponse)
def get_shorturl(short_code: str, db: Session = Depends(get_db)):
    return ShortURLService.get_shorturl(short_code, db)


