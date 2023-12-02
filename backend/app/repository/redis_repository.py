import uuid
from dataclasses import dataclass

import redis
import ujson

from schemas.prompt import FetchResponse
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

    def _make_themes_key(self, theme: str) -> str:
        return f"theme::{str(theme)}"

    def get_theme(self, theme: str) -> list[str] | None:
        result = self.r.get(self._make_themes_key(theme))
        if result is None:
            return None

        return ujson.loads(result.decode())

    def put_theme(self, theme: str, descriptions: list[str]) -> None:
        encoded = ujson.dumps(descriptions)
        self.r.set(self._make_themes_key(theme), encoded)

    def _make_pattern_key(self, pattern: str) -> str:
        return f"pattern::{pattern}"

    def get_images_by_patter(self, theme: str) -> list[FetchResponse]:
        list_ = self.r.lrange(self._make_pattern_key(theme), 0, -1)
        imgs = []
        for item in list_:
            id_ = uuid.UUID(item.decode())
            img = self.get_image(id_)
            if img is not None:
                imgs.append(FetchResponse(id=id_, img=img))

        return imgs

    def put_images_by_pattern(self, pattern: str, img_id: uuid.UUID) -> None:
        self.r.rpush(self._make_pattern_key(pattern), str(img_id))