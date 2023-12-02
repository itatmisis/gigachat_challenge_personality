import base64
import enum
import uuid

from fastapi import APIRouter, HTTPException, Response, status

from presentation.dependencies import container
from presentation.web.schemas import HealthResponse, HealthStatuses
from schemas.prompt import FetchRequest, FetchResponse, PromptRequest, PromptResponse
from shared.base import logger
from supplier.kandinsky_supplier import _attr_names

router = APIRouter(prefix="")


class Tags(str, enum.Enum):
    SERVICE = "service"


@router.get(
    "/health",
    response_model=HealthResponse,
    response_model_exclude_none=True,
    tags=[Tags.SERVICE],
)
async def check_server_health() -> HealthResponse:
    """
    Check service health
    """
    try:
        await container.heath_service.check()
    except Exception as exc:
        logger.exception("Exception while checking health")
        return HealthResponse(
            status=HealthStatuses.ERR, error=f"{exc.__class__.__name__}: {str(exc)}"
        )

    return HealthResponse(status=HealthStatuses.OK)


@router.post("/images/generate", response_model=PromptResponse)
def generate_image(req: PromptRequest) -> PromptResponse:
    return container.prompt_service.generate_image(req)


@router.post("/images/wait", response_model=list[FetchResponse])
def images_wait(req: FetchRequest) -> list[FetchResponse]:
    return container.prompt_service.fetch_images(req)


@router.get("/images/{image_id}")
def get_image(image_id: uuid.UUID) -> Response:
    img = container.prompt_service.get_images(image_id)
    if img is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )

    base64_bytes = base64.b64decode(img)

    return Response(content=base64_bytes, media_type="image/png")


@router.get("/images/attributes", response_model=dict[str, list[str]])
def get_attributes() -> dict[str, list[str]]:
    return _attr_names


@router.post("/sets", response_model=uuid.UUID)
def create_image_set(images: list[str]) -> uuid.UUID:
    id_ = container.sticker_set_service.put_set(images=images)
    return id_
