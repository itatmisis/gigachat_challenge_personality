import base64
import random
import time
import uuid
from dataclasses import dataclass

import requests
import ujson

from schemas.prompt import (
    Attributes,
    FetchRequest,
    FetchResponse,
    PromptRequest,
    PromptResponse,
)
from shared.base import logger
from shared.settings import app_settings
from supplier.patterns import Pattern

_default_negative_prompt = (
    "lowres, text, error, cropped, worst quality, low quality, "
    "jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, extra fingers, "
    "mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, "
    "dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, "
    "gross proportions, malformed limbs, missing arms, missing legs, extra arms, "
    "extra legs, fused fingers, too many fingers, long neck, username, watermark, signature"
)
themes = [
    "nature",
    "city",
    "car",
    "girl",
    "food",
    "science",
    "retrowave",
    "waporwave",
    "future",
    "cute animal",
    "architecture",
    "russia",
    "robots",
    "birds",
    "corgies",
    "energy",
    "anime",
]
_moods = [
    "Enthusiastic",
    "Content",
    "Exhilarated",
    "Festive",
    "Playful",
    "Adorable",
    "Excited",
    "Lovely",
    "Cute",
    "Happy",
    "Hopeful",
    "Delighted",
    "Blissful",
    "Cheerful",
    "Ecstatic",
    "Joyful",
    "Energetic",
]
_color_styles = [
    "Glossy",
    "Bold Colors",
    "Monochrome",
    "Flashy Colors",
    "Intense Colors",
    "Primary Color",
    "Cool Colors",
    "Vibrant Color",
    "Soft Color",
    "Sparkly Colors",
    "Textured",
    "Tertiary Color",
    "Holographic",
    "Earthy",
    "Muted Color",
    "Secondary Color",
    "Bright Colors",
    "Warm Colors",
    "Satin Colors",
    "Electric Colors",
    "Dark",
    "Saturated Colors",
    "Pastel",
    "Neon",
    "Matte",
]
_draw_styles = [
    "art toy style",
    "Minimal",
    "Algorithmic art",
    "Naive Art Style",
    "Geometric",
    "light art style",
    "Disney Pixar",
    "Pixel Art",
    "kinetic art style",
    "Pokemon Card",
    "Pencil Drawn",
    "Hand-Drawn",
    "Kawaii",
    "Art brut style",
    "Photorealism",
    "Anime",
    "Rough Charcoal",
    "Vintage",
    "Concept Art",
    "Gothic",
    "Graffiti",
    "Street Art",
    "Folk Art",
    "Sketch",
    "Yugioh Design",
    "mural art style",
    "outsider art style",
    "Deviant Art",
    "Cartoon",
    "Digital Art",
    "Disney",
    "Chibi",
    "Retro",
    "Artstation",
    "Pop Art",
]
_sticker_ending = "Contour, Vector, Fully White Background, Detailed, Sticker"
_styles = ["KANDINSKY", "UHD", "ANIME", "DEFAULT"]

_attr_names: dict[str, list[str]] = {
    "draw_style": _draw_styles,
    "mood": _moods,
    "color_style": _color_styles,
    "style": _styles,
}


@dataclass
class KandinskySupplier:
    def __post_init__(self) -> None:
        self._url = "https://api-key.fusionbrain.ai"
        self._auth_headers = {
            "X-Key": f"Key {app_settings.kandinsky_api_key}",
            "X-Secret": f"Secret {app_settings.kandinsky_api_secret}",
        }

        self.session = requests.Session()
        self.session.headers = self._auth_headers
        self._model = self.get_model()

    def get_model(self) -> str:
        response = self.session.get(self._url + "/key/api/v1/models")
        data = response.json()
        model = data[0]["id"]
        logger.info("status: kandinsky model got, model: {}", model)
        return model

    @staticmethod
    def get_random_attribute(attr_name: str) -> str:
        return random.choice(_attr_names[attr_name])

    def populate_prompt_from_pattern(
        self, prompt: str, pattern: Pattern
    ) -> tuple[str, Attributes]:
        if pattern.moods:
            mood = random.choice(pattern.moods)
        else:
            mood = self.get_random_attribute("mood")

        if pattern.draw_styles:
            draw_style = random.choice(pattern.draw_styles)
        else:
            draw_style = self.get_random_attribute("draw_style")

        if pattern.styles:
            style = random.choice(pattern.styles)
        else:
            style = self.get_random_attribute("style")

        if pattern.color_styles:
            color_style = random.choice(pattern.color_styles)
        else:
            color_style = self.get_random_attribute("color_style")

        return (
            f"{prompt}, {mood}, {color_style}, {draw_style}, {_sticker_ending}",
            Attributes(
                style=style,
                mood=mood,
                color_style=color_style,
                draw_style=draw_style,
            ),
        )

    def populate_prompt(self, req: PromptRequest) -> tuple[str, Attributes]:
        if not req.populate_prompt:
            return req.prompt, req.attributes

        color_style = req.attributes.color_style
        if color_style is None:
            color_style = self.get_random_attribute("color_style")

        mood = req.attributes.mood
        if mood is None:
            mood = self.get_random_attribute("mood")

        draw_style = req.attributes.draw_style
        if draw_style is None:
            draw_style = self.get_random_attribute("draw_style")

        style = req.attributes.style
        if style is None:
            style = self.get_random_attribute("style")

        return (
            f"{req.prompt}, {mood}, {color_style}, {draw_style}, {_sticker_ending}",
            Attributes(
                style=style,
                mood=mood,
                color_style=color_style,
                draw_style=draw_style,
            ),
        )

    def generate(self, req: PromptRequest) -> PromptResponse:
        populated_prompt, attributes = self.populate_prompt(req)

        id_ = self._send_generate_request(
            prompt=populated_prompt,
            style=req.attributes.style,
            width=1024,
            height=1024,
            negative_prompt=_default_negative_prompt,
        )

        return PromptResponse(prompt=populated_prompt, id=id_, attributes=attributes)

    def generate_from_pattern(self, prompt: str, pattern: Pattern) -> PromptResponse:
        populated_prompt, attributes = self.populate_prompt_from_pattern(
            prompt, pattern
        )

        id_ = self._send_generate_request(
            prompt=populated_prompt,
            style=attributes.style,
            width=1024,
            height=1024,
            negative_prompt=_default_negative_prompt,
        )

        return PromptResponse(prompt=populated_prompt, id=id_, attributes=attributes)

    def _send_generate_request(
        self,
        prompt: str,
        style: str | None,
        width: int,
        height: int,
        negative_prompt: str | None = None,
    ) -> uuid.UUID:
        params = {
            "type": "GENERATE",
            "numImages": 1,
            "width": width,
            "height": height,
            "generateParams": {"query": prompt},
            "negativePromptUnclip": negative_prompt,
            "style": style,
        }

        data = {
            "model_id": (None, self._model),
            "params": (None, ujson.dumps(params), "application/json"),
        }

        res = self.session.post(
            url=f"{self._url}/key/api/v1/text2image/run",
            files=data,
        )
        res.raise_for_status()

        data = res.json()

        id_ = uuid.UUID(data["uuid"])
        logger.info(
            "status: kandinsky image generation requested, prompt: {}, id: {}",
            prompt,
            id_,
        )

        return id_

    def wait_generation(
        self, request_id: uuid.UUID, attempts: int = 5, delay: float = 3
    ) -> bytes | None:
        logger.info(
            "status: kandinsky image generation getting result, request_id: {}",
            request_id,
        )
        while attempts > 0:
            response = self.session.get(
                self._url + "/key/api/v1/text2image/status/" + str(request_id)
            )
            data = response.json()
            if data["status"] == "DONE":
                if data["censored"]:
                    logger.warning(
                        "status: image for censored, request_id: {}", request_id
                    )
                    return None
                return data["images"][0].encode()

            attempts -= 1
            time.sleep(delay)
        logger.warning("status: unable to get image, request_id: {}", request_id)

    def generate_and_safe(self, req: PromptRequest, count: int = 5) -> None:
        gen_results = []
        for _ in range(count):
            gen_results.append(self.generate(req))

        images = []
        for gen_result in gen_results:
            img = self.wait_generation(gen_result.id_)
            if img is not None:
                images.append((img, gen_result.prompt))

        for img, prompt in images:
            with open(  # noqa: SCS109
                f"data/tests/{prompt.replace(' ', '-').lower().replace(',', '')}-{str(uuid.uuid4())[:8]}.png",
                "wb",
            ) as fh:
                fh.write(base64.decodebytes(img))

    def fetch(self, req: FetchRequest) -> list[FetchResponse]:
        imgs = []
        for id_ in req.ids:
            img = self.wait_generation(id_, attempts=5, delay=3)
            if img:
                imgs.append(FetchResponse(img=img, id=id_))

        return imgs

    def mutate_attr(
        self, req1: PromptRequest, req2: PromptRequest, attr_name: str
    ) -> str:
        rand = random.random()
        if rand < 0.1:
            return self.get_random_attribute(attr_name=attr_name)
        if rand < 0.55:
            return getattr(req1.attributes, attr_name)
        return getattr(req2.attributes, attr_name)

    def mutate(self, req1: PromptRequest, req2: PromptRequest) -> PromptRequest:
        color_style = self.mutate_attr(req1, req2, "color_style")
        draw_style = self.mutate_attr(req1, req2, "draw_style")
        mood = self.mutate_attr(req1, req2, "mood")
        style = self.mutate_attr(req1, req2, "style")
        attributes = Attributes(
            style=style, mood=mood, draw_style=draw_style, color_style=color_style
        )

        return PromptRequest(
            prompt=req1.prompt,
            height=req1.height,
            width=req1.width,
            negative_prompt=req1.negative_prompt,
            attributes=attributes,
        )
