import uuid
from dataclasses import dataclass

from schemas.prompt import FetchRequest, PromptRequest
from supplier.gigachat_supplier import GigachatSupplier
from supplier.kandinsky_supplier import KandinskySupplier


@dataclass
class PromptService:
    kandinsky_supplier: KandinskySupplier
    gigachat_supplier: GigachatSupplier

    def generate_image(self, req: PromptRequest) -> list[uuid.UUID]:
        return self.kandinsky_supplier.generate(req)

    def fetch_images(self, req: FetchRequest) -> list[bytes]:
        return self.kandinsky_supplier.fetch(req)
