from dataclasses import dataclass

from repository.db_repository import DbRepository
from service.heath_service import HeathService
from supplier.kandinsky_supplier import KandinskySupplier


@dataclass
class Container:
    heath_service: HeathService
    kandinsky_supplier: KandinskySupplier


def init_combat_container() -> Container:
    db_repository = DbRepository()
    heath_service = HeathService(db_repository=db_repository)
    kandinsky_supplier = KandinskySupplier()

    return Container(heath_service=heath_service, kandinsky_supplier=kandinsky_supplier)
