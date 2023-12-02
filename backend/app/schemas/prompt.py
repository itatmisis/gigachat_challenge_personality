import uuid

from pydantic import ConfigDict, Field

from schemas.base import CamelizedBaseModel

_default_negative_prompt = (
    "lowres, text, error, cropped, worst quality, low quality, "
    "jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, extra fingers, "
    "mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, "
    "dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, "
    "gross proportions, malformed limbs, missing arms, missing legs, extra arms, "
    "extra legs, fused fingers, too many fingers, long neck, username, watermark, signature"
)


class Attributes(CamelizedBaseModel):
    style: str | None = None
    mood: str | None = None
    color_style: str | None = None
    draw_style: str | None = None


class PromptRequest(CamelizedBaseModel):
    prompt: str = (
        "Anime sticker girl with fazbear in left hand and green flag in right hand"
    )

    # https://cdn.fusionbrain.ai/static/styles/api
    # KANDINSKY, UHD, ANIME, DEFAULT
    width: int = 1024
    height: int = 1024
    negative_prompt: str | None = _default_negative_prompt
    populate_prompt: bool = True
    attributes: Attributes = Attributes()
    count: int = 10

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "prompt": "Аниме девочка и медведь",
                    "style": "ANIME",
                    "width": 1024,
                    "height": 1024,
                    "negative_prompt": negative_prompt,
                    "sticker": True,
                }
            ]
        },
    )


class PromptResponse(CamelizedBaseModel):
    id_: uuid.UUID = Field(..., alias="id")
    prompt: str
    attributes: Attributes


class FetchRequest(CamelizedBaseModel):
    ids: list[uuid.UUID] = [uuid.UUID("34418e36-46b9-4ec5-93bf-fd40c0a6a50a")]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "ids": ["34418e36-46b9-4ec5-93bf-fd40c0a6a50a"],
                }
            ]
        },
    )


class FetchResponse(CamelizedBaseModel):
    id_: uuid.UUID = Field(..., alias="id")
    img: bytes
