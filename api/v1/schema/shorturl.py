from pydantic import BaseModel

class ShortURL(BaseModel):
    original_url: str
    short_code: str
    
    
    
class ShortURLRequest(ShortURL):
    pass


class ShortURLResponse(ShortURL):
    id: int
    short_code: str

    class Config:
        from_attributes = True
        
        
    


