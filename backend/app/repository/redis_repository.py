import uuid
from dataclasses import dataclass

import redis

from shared.settings import app_settings


@dataclass
class RedisRepository:
    def __post_init__(self) -> None:
        self.r = redis.Redis(host=app_settings.redis_host, port=app_settings.redis_port)

    def get_image(self, id_: uuid.UUID) -> bytes | None:
        return self.r.get(str(id_))

    def set_image(self, id_: uuid.UUID, img: bytes) -> None:
        self.r.set(str(id_), value=img)
