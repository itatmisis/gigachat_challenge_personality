import random
import uuid
from dataclasses import dataclass

from repository.redis_repository import RedisRepository
from schemas.prompt import FetchRequest, FetchResponse, PromptRequest, PromptResponse
from shared.base import logger
from supplier.gigachat_supplier import GigachatSupplier
from supplier.kandinsky_supplier import KandinskySupplier


@dataclass
class PromptService:
    kandinsky_supplier: KandinskySupplier
    gigachat_supplier: GigachatSupplier
    redis_repository: RedisRepository

    def parse_bot_response(self, res: str) -> list[str]:
        res = res[res.find("1. ") :]
        ideas = [
            x.split(". ")[-1] if x.split(". ")[0].isnumeric() else ""
            for x in res.split("\n")
        ]

        while "" in ideas:
            ideas.remove("")
        return ideas

    def generate_prompt(self, theme: str) -> list[str]:
        themes = self.redis_repository.get_theme(theme=theme)
        if themes is not None:
            return themes

        translated = self.gigachat_supplier.translate_to_english(prompt=theme)
        sticker_ideas = self.parse_bot_response(
            self.gigachat_supplier.single_message(
                f"Come up with 10 ideas for a drawing on the theme of {translated}"
            )
        )
        logger.info("detailed description generated: {}", sticker_ideas)

        self.redis_repository.put_theme(theme=theme, descriptions=sticker_ideas)

        return sticker_ideas

    def generate_image(self, req: PromptRequest) -> PromptResponse:
        prompt = random.choice(self.generate_prompt(req.prompt))

        req.prompt = prompt
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

    def get_images(self, img_id: uuid.UUID) -> bytes | None:
        imgs = self.fetch_images(FetchRequest(ids=[img_id]))
        if not imgs:
            return None

        return imgs[0].img
