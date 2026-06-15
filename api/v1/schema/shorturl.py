from pydantic import BaseModel

class ShortURL(BaseModel):
    original_url: str
    short_code: str
    
    
    
class ShortURLRequest(BaseModel):
    original_url: str
    short_code: str | None = None

class ShortURLResponse(ShortURL):
    id: int
    short_code: str

    class Config:
        from_attributes = True
        
        
    


