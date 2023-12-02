import uuid

from pydantic import ConfigDict, Field

from schemas.base import CamelizedBaseModel


class SetResponse(CamelizedBaseModel):
    id_: uuid.UUID = Field(..., alias="id")
    link: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": "34418e36-46b9-4ec5-93bf-fd40c0a6a50a",
                    "link": "https://t.me/ai_generated_stickers_bot?start=34418e36-46b9-4ec5-93bf-fd40c0a6a50a",
                }
            ]
        },
    )
