import base64
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

import requests
import ujson

from schemas.prompt import FetchRequest, PromptRequest
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

    def generate(self, req: PromptRequest) -> list[uuid.UUID]:
        idxs = []
        for _ in range(req.images):
            idxs.append(
                self._send_generate_request(
                    prompt=req.prompt,
                    style=req.style,
                    width=req.width,
                    height=req.height,
                    negative_prompt=req.negative_prompt,
                )
            )

        return idxs

    def _send_generate_request(
        self,
        prompt: str,
        style: str | None,
        width: int,
        height: int,
        negative_prompt: str | None,
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
        self, request_id: uuid.UUID, attempts: int = 3, delay: float = 2
    ) -> bytes | None:
        while attempts > 0:
            logger.info(
                "status: kandinsky image generation getting result, request_id: {}",
                request_id,
            )
            response = self.session.get(
                self._url + "/key/api/v1/text2image/status/" + str(request_id)
            )
            data = response.json()
            if data["status"] == "DONE":
                return data["images"][0].encode()

            attempts -= 1
            time.sleep(delay)
        logger.warning("status: unable to get image, requist_id: {}", request_id)

    def generate_and_wait(self, req: PromptRequest) -> list[bytes] | None:
        idxs = self.generate(req)

        images_bytes = []
        for idx in idxs:
            images_bytes.append(self.wait_generation(idx))

        return images_bytes

    def fetch(self, req: FetchRequest) -> list[bytes]:
        imgs = []
        for id_ in req.ids:
            img = self.wait_generation(id_, attempts=req.attempts, delay=req.delay)
            if img:
                imgs.append(img)

        return imgs

    def save(self, img: bytes, path: str | Path) -> None:
        with open(path, "wb") as fh:  # noqa: SCS109
            fh.write(base64.decodebytes(img))
