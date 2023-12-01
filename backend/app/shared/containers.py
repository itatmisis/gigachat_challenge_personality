from dataclasses import dataclass

from repository.db_repository import DbRepository
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
    db_repository = DbRepository()
    heath_service = HeathService(db_repository=db_repository)
    kandinsky_supplier = KandinskySupplier()
    gigachat_supplier = GigachatSupplier()
    prompt_service = PromptService(
        gigachat_supplier=gigachat_supplier, kandinsky_supplier=kandinsky_supplier
    )

    return Container(
        heath_service=heath_service,
        kandinsky_supplier=kandinsky_supplier,
        gigachat_supplier=gigachat_supplier,
        prompt_service=prompt_service,
    )
