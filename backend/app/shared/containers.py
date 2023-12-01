from dataclasses import dataclass

from repository.redis_repository import RedisRepository
from service.heath_service import HeathService
from service.prompt_service import PromptService
from supplier.gigachat_supplier import GigachatSupplier
from supplier.kandinsky_supplier import KandinskySupplier


@dataclass
class Container:
    heath_service: HeathService
    kandinsky_supplier: KandinskySupplier
    gigachat_supplier: GigachatSupplier
    prompt_service: PromptService


def init_combat_container() -> Container:
    heath_service = HeathService()
    kandinsky_supplier = KandinskySupplier()
    redis_repository = RedisRepository()
    gigachat_supplier = GigachatSupplier()
    prompt_service = PromptService(
        gigachat_supplier=gigachat_supplier,
        kandinsky_supplier=kandinsky_supplier,
        redis_repository=redis_repository,
    )

    return Container(
        heath_service=heath_service,
        kandinsky_supplier=kandinsky_supplier,
        gigachat_supplier=gigachat_supplier,
        prompt_service=prompt_service,
    )
