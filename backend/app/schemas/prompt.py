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


class PromptRequest(CamelizedBaseModel):
    prompts: list[str] = [
        "Anime sticker girl with fazbear in left hand and green flag in right hand"
    ]
    # https://cdn.fusionbrain.ai/static/styles/api
    # KANDINSKY, UHD, ANIME, DEFAULT
    style: str | None = None
    width: int = 1024
    height: int = 1024
    negative_prompt: str | None = _default_negative_prompt
    sticker: bool = True

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "prompt": [
                        "Anime sticker girl with fazbear in left hand and green flag in right hand"
                    ],
                    "style": "ANIME",
                    "images": 1,
                    "width": 1024,
                    "height": 1024,
                    "negative_prompt": negative_prompt,
                    "sticker": True,
                }
            ]
        },
    )


class FetchRequest(CamelizedBaseModel):
    ids: list[uuid.UUID] = [uuid.UUID("34418e36-46b9-4ec5-93bf-fd40c0a6a50a")]
    attempts: int = 3
    delay: int = 2

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "ids": ["34418e36-46b9-4ec5-93bf-fd40c0a6a50a"],
                    "attempts": 3,
                    "delay": 2,
                }
            ]
        },
    )


class FetchResponse(CamelizedBaseModel):
    id_: uuid.UUID = Field(..., alias="id")
    img: bytes
