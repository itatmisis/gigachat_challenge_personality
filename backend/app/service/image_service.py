import base64
import io
from dataclasses import dataclass

from PIL import Image


@dataclass
class ImageService:
    def resize_base64_img(self, img: bytes, shape: tuple[int, int]) -> bytes:
        imgdata = base64.b64decode(img)
        newimg = self.resize_img(imgdata, shape=shape)
        img_b64 = base64.b64encode(newimg)

        return img_b64

    def resize_img(self, img: bytes, shape: tuple[int, int]) -> bytes:
        pil_img = Image.open(io.BytesIO(img))
        new_img = pil_img.resize(shape)
        buffer = io.BytesIO()
        new_img.save(buffer, format="PNG")

        return buffer.getvalue()

    def make_grip(self, images_bytes: list[bytes], rows: int, cols: int) -> bytes:
        if len(images_bytes) > rows * cols:
            raise Exception("invalid dimensions")

        images = []
        for img in images_bytes:
            images.append(Image.open(io.BytesIO(img)))

        w, h = images[0].size
        grid = Image.new("RGB", size=(cols * w, rows * h), color=(255, 255, 255))

        for i, img in enumerate(images):
            grid.paste(img, box=(i % cols * w, i // cols * h))

        buffer = io.BytesIO()
        grid.save(buffer, format="PNG")
        return buffer.getvalue()
