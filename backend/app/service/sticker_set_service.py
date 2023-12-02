import uuid
from dataclasses import dataclass

from repository.redis_repository import RedisRepository


@dataclass
class StickerSetService:
    redis_repository: RedisRepository

    def put_set(self, images: list[str]) -> uuid.UUID:
        id_ = uuid.uuid4()
        self.redis_repository.put_set(id_, images)

        return id_
