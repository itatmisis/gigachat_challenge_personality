import base64
import io
import random
import uuid
from dataclasses import dataclass

from PIL import Image
from repository.redis_repository import RedisRepository
from schemas.prompt import (
    FetchRequest,
    FetchResponse,
    MainPage,
    PromptPatternRequest,
    PromptRequest,
    PromptResponse,
)
from shared.base import logger
from shared.settings import app_settings
from supplier.gigachat_supplier import GigachatSupplier
from supplier.kandinsky_supplier import KandinskySupplier, _themes
from supplier.patterns import name_to_pattern
from supplier.photoroom_supplier import PhotoroomSupplier


@dataclass
class PromptService:
    kandinsky_supplier: KandinskySupplier
    gigachat_supplier: GigachatSupplier
    redis_repository: RedisRepository
    photoroom_supplier: PhotoroomSupplier

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

    def generate_image_from_pattern(self, req: PromptPatternRequest) -> PromptResponse:
        pattern = name_to_pattern[req.pattern]

        if not pattern.themes:
            theme = random.choice(_themes)
        else:
            theme = random.choice(pattern.themes)

        prompt = random.choice(self.generate_prompt(theme))

        return self.kandinsky_supplier.generate_from_pattern(prompt, pattern)

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
        if app_settings.remove_bg:
            for idx, img in enumerate(fetched_imgs):
                fetched_imgs[idx].img = self.photoroom_supplier.remove_bg(img.img)

        for fetched_img in fetched_imgs:
            imgs.append(fetched_img)
            self.redis_repository.set_image(id_=fetched_img.id_, img=fetched_img.img)

        return imgs

    def resize_base64_img(self, img: bytes, shape: tuple[int, int]) -> bytes:
        buffer = io.BytesIO()
        imgdata = base64.b64decode(img)
        img = Image.open(io.BytesIO(imgdata))
        new_img = img.resize(shape)
        new_img.save(buffer, format="PNG")
        img_b64 = base64.b64encode(buffer.getvalue())

        return img_b64

    def get_images(self, img_id: uuid.UUID, resize: int | None = None) -> bytes | None:
        imgs = self.fetch_images(FetchRequest(ids=[img_id]))
        if not imgs:
            return None

        img = imgs[0].img
        if resize is not None:
            img = self.resize_base64_img(img, shape=(resize, resize))

        return img

    def generate_for_patterns(self) -> None:
        for pattern in name_to_pattern.values():
            imgs = []
            if pattern.title == "random":
                count = 8
            else:
                count = 4

            for _ in range(count):
                imgs.append(
                    self.generate_image_from_pattern(
                        PromptPatternRequest(pattern=pattern.title)
                    ).id_
                )

            images = self.fetch_images(FetchRequest(ids=imgs))
            for img in images:
                self.redis_repository.put_images_by_pattern(
                    pattern.title, img_id=img.id_
                )

    def get_all(self) -> MainPage:
        max_images = 24
        map_images_per_pattern = len(name_to_pattern.keys()) // max_images + 1
        images = {}
        for pattern in name_to_pattern.values():
            images[pattern.title] = self.redis_repository.get_images_by_pattern(
                pattern.title
            )[:map_images_per_pattern]
            for im in images[pattern.title]:
                im.img = self.resize_base64_img(im.img, shape=(256, 256))

        return MainPage(images=images)

    def gen_all_images_md(self) -> None:
        images = self.redis_repository.get_image_all_ids()
        cols = 6
        template = """### All generated images\n\n"""

        col = "| "
        for _ in range(cols):
            col += "... | "
        col += "\n"
        template += col

        col = "| "
        for _ in range(cols):
            col += "--- | "
        template += col
        col += "\n"

        col = ""

        for idx, image in enumerate(images):
            if idx % cols == 0:
                col += "\n"
                template += col
                col = "| "

            col += f"![{image}]({app_settings.base_path}/images/{image}?reshape=512) | "

        col += "\n"
        template += col
        col = "| "

        with open("../../images/README.md", "w") as f:  # noqa: SCS109
            f.write(template)
