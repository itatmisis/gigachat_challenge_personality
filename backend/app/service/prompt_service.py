import random
import uuid
from dataclasses import dataclass

from repository.redis_repository import RedisRepository
from schemas.prompt import (
    FetchRequest,
    FetchResponse,
    MainPage,
    PromptPatternRequest,
    PromptRequest,
    PromptResponse,
)
from service.image_service import ImageService
from shared.base import logger
from shared.settings import app_settings
from supplier.gigachat_supplier import GigachatSupplier
from supplier.kandinsky_supplier import KandinskySupplier, themes
from supplier.patterns import RANDOM, name_to_pattern
from supplier.photoroom_supplier import PhotoroomSupplier


@dataclass
class PromptService:
    kandinsky_supplier: KandinskySupplier
    gigachat_supplier: GigachatSupplier
    redis_repository: RedisRepository
    photoroom_supplier: PhotoroomSupplier
    image_service: ImageService

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
            theme = random.choice(themes)
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

    def get_images(self, img_id: uuid.UUID, resize: int | None = None) -> bytes | None:
        imgs = self.fetch_images(FetchRequest(ids=[img_id]))
        if not imgs:
            return None

        img = imgs[0].img
        if resize is not None:
            img = self.image_service.resize_base64_img(img, shape=(resize, resize))

        return img

    def generate_for_patterns(self) -> None:
        for pattern in name_to_pattern.values():
            imgs = []
            if pattern.title == "random":
                count = 50
            else:
                count = 30

            logger.info(
                "starting generating images for pattern: {}, count: {}",
                pattern.title,
                count,
            )

            for _ in range(count):
                imgs.append(
                    self.generate_image_from_pattern(
                        PromptPatternRequest(pattern=pattern.title)
                    ).id_
                )

            logger.info("fetching images", pattern.title, count)

            images = self.fetch_images(FetchRequest(ids=imgs))
            for img in images:
                self.redis_repository.put_images_by_pattern(
                    pattern.title, img_id=img.id_
                )

    def get_all(self) -> MainPage:
        images = {}
        count = 0
        max_ = 72
        # patterns = random.choices(list(name_to_pattern.keys()), k=3)
        patterns = ["xmas", "skihorise", "crippy"]

        for pattern in patterns:
            images[pattern] = self.redis_repository.get_images_ids_by_pattern(
                pattern, count=8
            )
            count += len(images[pattern])
            logger.info("images: {}, pattern: {}", count, pattern)

        random_count = max_ - count - 1
        if random_count > 0:
            images[RANDOM] = self.redis_repository.get_images_ids_by_pattern(
                RANDOM, count=random_count
            )
            count += len(images[RANDOM])
            logger.info("images: {}, pattern: {}", count, RANDOM)

        return MainPage(images=images)

    # DEPRECATED
    def get_all_maxed(self, count: int = 24, max_per_pattern: int = 6) -> MainPage:
        images = {}
        keys = set(name_to_pattern.keys())
        keys.discard(RANDOM)
        any_pattern = random.choice(list(keys))

        images[any_pattern] = self.redis_repository.get_images_ids_by_pattern(
            any_pattern, end=max_per_pattern - 1
        )
        logger.info("fetched: {}, count: {}", any_pattern, len(images[any_pattern]))

        images[RANDOM] = self.redis_repository.get_images_ids_by_pattern(
            RANDOM, count - len(images[any_pattern]) - 1
        )
        logger.info("fetched: {}, count: {}", RANDOM, len(images[RANDOM]))

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
