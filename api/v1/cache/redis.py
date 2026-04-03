import redis
from api.v1.config.redis_config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db = 0,
    decode_responses=True
)



