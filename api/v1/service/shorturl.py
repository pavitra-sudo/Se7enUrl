
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from api.v1.model.shorturl import ShortURL
from api.v1.database.db_connector import get_db
from api.v1.schema.shorturl import ShortURLRequest

from api.v1.cache.redis import redis_client



class ShortURLService:
    
    @staticmethod
    def normalize_url(url: str) -> str:
        if not url.startswith(("http://", "https://")):
            return "https://" + url
        return url  
    
    @staticmethod
    def post_shorturl(r: ShortURLRequest, db: Session ):
        import string
        import random
        
        if not r.short_code:
            # Generate a random 7-character string
            r.short_code = "".join(random.choices(string.ascii_letters + string.digits, k=7))
            
        r.short_code = r.short_code.lower()
        r.original_url = ShortURLService.normalize_url(r.original_url)
        url = ShortURL(original_url=r.original_url, short_code=r.short_code)
        db.add(url)
        from sqlalchemy.exc import IntegrityError
        try:
            db.flush()
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Short code already exists. Please choose a different one.")
        db.refresh(url)
        return url
    
   

    @staticmethod
    def get_shorturl(short_code: str, db: Session):
        
        key = f"url:{short_code}"
        
        # 1. Try cache
        cached_url = redis_client.get(key)
        if cached_url:
            # increment count (still DB for now)
            db.query(ShortURL).filter(
                ShortURL.short_code == short_code
            ).update({
                ShortURL.click_count: ShortURL.click_count + 1
            })
            db.commit()
            print(f"Cache hit: {key}")

            return RedirectResponse(cached_url, status_code=307) #type: ignore

        # 2. Fallback to DB
        url = db.query(ShortURL).filter(
            ShortURL.short_code == short_code
        ).first()

        if not url:
            raise HTTPException(status_code=404, detail="Short URL not found")

        # 3. Cache it
        redis_client.set(key, url.original_url, ex=3600)  #type: ignore
        print(f"URL cached: {key}") 

        # 4. Increment count
        db.query(ShortURL).filter(
            ShortURL.short_code == short_code
        ).update({
            ShortURL.click_count: ShortURL.click_count + 1
        })
        db.commit()

        return RedirectResponse(str(url.original_url), status_code=307)