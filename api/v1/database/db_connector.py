from api.v1.database.database import SessionLocal
from fastapi import Request
from sqlalchemy.orm import Session



def get_db(request: Request):
    db: Session = SessionLocal()
    try:

        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()