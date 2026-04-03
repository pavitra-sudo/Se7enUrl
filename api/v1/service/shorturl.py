
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from api.v1.model.shorturl import ShortURL
from api.v1.database.db_connector import get_db
from api.v1.schema.shorturl import ShortURLRequest



class ShortURLService:
    
    @staticmethod
    def normalize_url(url: str) -> str:
        if not url.startswith(("http://", "https://")):
            return "https://" + url
        return url  
    
    @staticmethod
    def post_shorturl(r: ShortURLRequest, db: Session ):
        r.short_code = r.short_code.lower()
        r.original_url = ShortURLService.normalize_url(r.original_url)
        url = ShortURL(original_url=r.original_url, short_code=r.short_code)
        db.add(url)
        db.flush()
        db.refresh(url)
        return url
    
    @staticmethod
    def get_shorturl(short_code: str, db: Session):
        query = db.query(ShortURL).filter(ShortURL.short_code == short_code)

        url = query.first()

        if not url:
            raise HTTPException(status_code=404, detail="Short URL not found")

        query.update({
            ShortURL.click_count: ShortURL.click_count + 1
        })

        db.commit()