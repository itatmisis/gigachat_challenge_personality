import base64
import io
from dataclasses import dataclass

import requests

from shared.base import logger
from shared.settings import app_settings


@dataclass
class PhotoroomSupplier:
    def __post_init__(self) -> None:
        self.session = requests.Session()
        self.session.headers = {"x-api-key": app_settings.photoroom_api_key}
        self._url = "https://sdk.photoroom.com/v1/segment"

    def remove_bg(self, img: bytes) -> bytes:
        base64_bytes = base64.b64decode(img)
        logger.info("removing background")
        res = self.session.post(
            url=self._url,
            files={"image_file": io.BytesIO(base64_bytes)},
        )

        res.raise_for_status()

        return base64.b64encode(res.content)
