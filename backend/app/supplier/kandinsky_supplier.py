import base64
import random
import time
import uuid
from dataclasses import dataclass

import requests
import ujson

from schemas.prompt import FetchRequest, FetchResponse, PromptRequest, PromptResponse
from shared.base import logger
from shared.settings import app_settings

_default_negative_prompt = (
    "lowres, text, error, cropped, worst quality, low quality, "
    "jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, extra fingers, "
    "mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, "
    "dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, "
    "gross proportions, malformed limbs, missing arms, missing legs, extra arms, "
    "extra legs, fused fingers, too many fingers, long neck, username, watermark, signature"
)
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

    def populate_prompt(self, req: PromptRequest) -> None:
        if not req.populate_prompt:
            return

        color_style = req.color_style
        if color_style is None:
            color_style = random.choice(_color_styles)

        mood = req.mood
        if mood is None:
            mood = random.choice(_moods)

        draw_style = req.draw_style
        if draw_style is None:
            draw_style = random.choice(_draw_styles)

        req.prompt = (
            f"{req.prompt}, {mood}, {color_style}, {draw_style}, {_sticker_ending}"
        )

    def generate(self, req: PromptRequest) -> PromptResponse:
        self.populate_prompt(req)
        id_ = self._send_generate_request(
            prompt=req.prompt,
            style=req.style,
            width=req.width,
            height=req.height,
            negative_prompt=req.negative_prompt,
        )

        return PromptResponse(prompt=req.prompt, id=id_)

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
        idxs = []
        for _ in range(count):
            idxs.append(self.generate(req))

        images = []
        for idx, req_id in enumerate(idxs):
            img = self.wait_generation(req_id)
            if img is not None:
                images.append((img, req.prompts[idx]))

        for img, prompt in images:
            with open(  # noqa: SCS109
                f"data/tests/{prompt.replace(' ', '-').lower().replace(',', '')}-{str(uuid.uuid4())[:8]}.png",
                "wb",
            ) as fh:
                fh.write(base64.decodebytes(img))

    def fetch(self, req: FetchRequest) -> list[FetchResponse]:
        imgs = []
        for id_ in req.ids:
            img = self.wait_generation(id_, attempts=req.attempts, delay=req.delay)
            if img:
                imgs.append(FetchResponse(img=img, id=id_))

        return imgs

    def mutate(self, req1: PromptRequest, req2: PromptRequest) -> PromptRequest:
        ...
