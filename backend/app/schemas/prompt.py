import uuid

from pydantic import ConfigDict, Field

from schemas.base import CamelizedBaseModel


class Attributes(CamelizedBaseModel):
    style: str | None = None
    mood: str | None = None
    color_style: str | None = None
    draw_style: str | None = None


class PromptRequest(CamelizedBaseModel):
    prompt: str = "Синий лебедь и медведь"

    # https://cdn.fusionbrain.ai/static/styles/api
    # KANDINSKY, UHD, ANIME, DEFAULT
    populate_prompt: bool = True
    attributes: Attributes = Attributes()

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"examples": [{"prompt": "Аниме девочка и медведь"}]},
    )


class PromptPatternRequest(CamelizedBaseModel):
    pattern: str = "random"

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"examples": [{"pattern": "random"}]},
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
