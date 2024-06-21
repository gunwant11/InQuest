import redis
from app.config import settings

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

def get_redis_client():
    return redis_client