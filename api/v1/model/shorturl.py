from sqlalchemy import Column, Integer, String
from api.v1.database.database import ShortURLBase

class ShortURL(ShortURLBase):
    __tablename__ = "shorturls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, nullable=False)
    click_count = Column(Integer, default=0)
    
    
    