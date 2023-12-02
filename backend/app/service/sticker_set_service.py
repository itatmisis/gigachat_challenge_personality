import uuid
from dataclasses import dataclass

from repository.redis_repository import RedisRepository
from schemas.set import SetResponse
from supplier.tg_supplier import TgSupplier


@dataclass
class StickerSetService:
    redis_repository: RedisRepository
    tg_supplier: TgSupplier

    def put_set(self, images: list[str]) -> SetResponse:
        id_ = uuid.uuid4()
        self.redis_repository.put_set(id_, images)

        link = f"https://t.me/{self.tg_supplier.me.username}?start={id_}"
        return SetResponse(id=id_, link=link)
