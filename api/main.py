from fastapi import FastAPI
from api.v1.router.shorturl import router as shorturl_router


app = FastAPI()

# Include routers
app.include_router(shorturl_router)


