import base64
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

import requests
import ujson

from shared.settings import app_settings


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
        return data[0]["id"]

    def generate(
        self,
        prompt: str,
        style: str | None = None,
        images: int = 1,
        width: int = 1024,
        height: int = 1024,
    ) -> uuid.UUID:
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {"query": f"{prompt}"},
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

        return uuid.UUID(data["uuid"])

    def wait_generation(
        self, request_id: uuid.UUID, attempts: int = 10, delay: int = 10
    ) -> list[bytes] | None:
        while attempts > 0:
            response = self.session.get(
                self._url + "/key/api/v1/text2image/status/" + str(request_id),
            )
            data = response.json()
            if data["status"] == "DONE":
                return [img.encode() for img in data["images"]]

            attempts -= 1
            time.sleep(delay)

    def generate_and_wait(
        self,
        prompt: str,
        # https://cdn.fusionbrain.ai/static/styles/api
        # KANDINSKY, UHD, ANIME, DEFAULT
        style: str | None = None,
        images: int = 1,
        width: int = 1024,
        height: int = 1024,
    ) -> list[bytes] | None:
        id_ = self.generate(
            prompt=prompt, style=style, images=images, width=width, height=height
        )
        return self.wait_generation(id_)

    def save(self, img: bytes, path: str | Path) -> None:
        with open(path, "wb") as fh:  # noqa: SCS109
            fh.write(base64.decodebytes(img))
