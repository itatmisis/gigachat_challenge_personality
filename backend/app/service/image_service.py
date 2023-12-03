import base64
import io
from dataclasses import dataclass

from PIL import Image, ImageDraw
from PIL.Image import Image as ImageType


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

        return self.to_bytes(new_img)

    def make_grip(self, images_bytes: list[bytes], rows: int, cols: int) -> bytes:
        if len(images_bytes) > rows * cols:
            raise Exception("invalid dimensions")

        images = []
        for img in images_bytes:
            images.append(self.from_bytes(img))

        w, h = images[0].size
        grid = Image.new("RGB", size=(cols * w, rows * h), color=(255, 255, 255))

        for i, img in enumerate(images):
            grid.paste(img, box=(i % cols * w, i // cols * h))

        return self.to_bytes(grid)

    def from_bytes(self, img: bytes) -> ImageType:
        return Image.open(io.BytesIO(img))

    def to_bytes(self, img: ImageType) -> bytes:
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")

        return buffer.getvalue()

    def add_corners(self, im_bytes: bytes, rad: int) -> bytes:
        im = self.from_bytes(im_bytes)

        circle = Image.new("L", (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
        alpha = Image.new("L", im.size, 255)
        w, h = im.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        im.putalpha(alpha)
        return self.to_bytes(im)
