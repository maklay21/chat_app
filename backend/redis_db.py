from typing import Dict, ClassVar
import redis

from config.settings import settings


REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT
REDIS_PASSWORD = settings.REDIS_PASSWORD

if settings.ENVIRONMENT == 'production':
    REDIS_DB = 0
else:
    REDIS_DB = 1


class StrictRedisPools:

    _redis_pools: ClassVar[Dict[int, redis.ConnectionPool]] = {}

    def __init__(self) -> None:
        self.REDIS_HOST = REDIS_HOST
        self.REDIS_PORT = REDIS_PORT
        self.REDIS_PASSWORD= REDIS_PASSWORD
        
    def get_pool(self, db_number: int) -> redis.ConnectionPool:
        if db_number not in self._redis_pools:
            self._redis_pools[db_number] = redis.ConnectionPool(
                host=self.REDIS_HOST,
                port=self.REDIS_PORT,
                #password=self.REDIS_PASSWORD,
                db=db_number,
                decode_responses=True
            )
        return self._redis_pools[db_number]

    def get_connection(self, db_number: int) -> redis.Redis:
        return redis.Redis(
            connection_pool=self.get_pool(db_number)
        )

redis_pools = StrictRedisPools()
redis_client = redis_pools.get_connection(db_number=REDIS_DB)
