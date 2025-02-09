from dataclasses import dataclass

from repository.redis_repository import RedisRepository
from service.heath_service import HeathService
from service.image_service import ImageService
from service.prompt_service import PromptService
from service.sticker_set_service import StickerSetService
from supplier.gigachat_supplier import GigachatSupplier
from supplier.kandinsky_supplier import KandinskySupplier
from supplier.photoroom_supplier import PhotoroomSupplier
from supplier.tg_supplier import TgSupplier


@dataclass
class Container:
    heath_service: HeathService
    kandinsky_supplier: KandinskySupplier
    gigachat_supplier: GigachatSupplier
    prompt_service: PromptService
    sticker_set_service: StickerSetService
    tg_supplier: TgSupplier


def init_combat_container() -> Container:
    heath_service = HeathService()
    kandinsky_supplier = KandinskySupplier()
    redis_repository = RedisRepository()
    gigachat_supplier = GigachatSupplier()
    photoroom_supplier = PhotoroomSupplier()
    image_service = ImageService()
    prompt_service = PromptService(
        gigachat_supplier=gigachat_supplier,
        kandinsky_supplier=kandinsky_supplier,
        redis_repository=redis_repository,
        image_service=image_service,
        photoroom_supplier=photoroom_supplier,
    )
    tg_supplier = TgSupplier(
        redis_repository=redis_repository, image_service=image_service
    )
    sticker_set_service = StickerSetService(
        redis_repository=redis_repository, tg_supplier=tg_supplier
    )

    return Container(
        heath_service=heath_service,
        kandinsky_supplier=kandinsky_supplier,
        gigachat_supplier=gigachat_supplier,
        prompt_service=prompt_service,
        sticker_set_service=sticker_set_service,
        tg_supplier=tg_supplier,
    )
