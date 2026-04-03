
from datetime import datetime

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
        r.short_code = r.short_code.lower()
        r.original_url = ShortURLService.normalize_url(r.original_url)
        url = ShortURL(original_url=r.original_url, short_code=r.short_code)
        db.add(url)
        db.flush()
        db.refresh(url)
        return url
    
   

    @staticmethod
    def get_shorturl(short_code: str, db: Session):
        starttime = datetime.now()
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
            print(f"Time taken: {(datetime.now() - starttime).total_seconds()} seconds")
            

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
        print(f"Time taken: {(datetime.now() - starttime).total_seconds()} seconds")
        return RedirectResponse(str(url.original_url), status_code=307)