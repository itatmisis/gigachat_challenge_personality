from dataclasses import dataclass

from repository.redis_repository import RedisRepository
from schemas.prompt import FetchRequest, FetchResponse, PromptRequest, PromptResponse
from supplier.gigachat_supplier import GigachatSupplier
from supplier.kandinsky_supplier import KandinskySupplier


@dataclass
class PromptService:
    kandinsky_supplier: KandinskySupplier
    gigachat_supplier: GigachatSupplier
    redis_repository: RedisRepository

    def generate_image(self, req: PromptRequest) -> PromptResponse:
        return self.kandinsky_supplier.generate(req)

    def fetch_images(self, req: FetchRequest) -> list[FetchResponse]:
        imgs = []
        not_found_ids = []
        for id_ in req.ids:
            img = self.redis_repository.get_image(id_)

            if img is None:
                not_found_ids.append(id_)
            else:
                imgs.append(FetchResponse(img=img, id=id_))

        if len(not_found_ids) == 0:
            return imgs

        req.ids = not_found_ids
        fetched_imgs = self.kandinsky_supplier.fetch(req)

        for fetched_img in fetched_imgs:
            imgs.append(fetched_img)
            self.redis_repository.set_image(id_=fetched_img.id_, img=fetched_img.img)

        return imgs
