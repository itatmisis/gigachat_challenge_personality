import uuid
from dataclasses import dataclass

import redis
import ujson

from shared.settings import app_settings


@dataclass
class RedisRepository:
    def __post_init__(self) -> None:
        self.r = redis.Redis(host=app_settings.redis_host, port=app_settings.redis_port)

    def _make_img_key(self, id_: uuid.UUID) -> str:
        return f"image::{str(id_)}"

    def get_image(self, id_: uuid.UUID) -> bytes | None:
        return self.r.get(self._make_img_key(id_))

    def set_image(self, id_: uuid.UUID, img: bytes) -> None:
        self.r.set(self._make_img_key(id_), value=img)

    def _make_sticker_set_key(self, id_: uuid.UUID) -> str:
        return f"set::{str(id_)}"

    def get_set(self, id_: uuid.UUID) -> list[str] | None:
        result = self.r.get(self._make_sticker_set_key(id_))
        if result is None:
            return None

        return ujson.loads(result.decode())

    def put_set(self, id_: uuid.UUID, set_: list[str]) -> None:
        encoded = ujson.dumps(set_)
        self.r.set(self._make_sticker_set_key(id_), encoded)
