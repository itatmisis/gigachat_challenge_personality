import enum
import uuid

from fastapi import APIRouter

from presentation.dependencies import container
from presentation.web.schemas import HealthResponse, HealthStatuses
from schemas.prompt import FetchRequest, PromptRequest
from shared.base import logger

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


@router.post("/images/generate", response_model=list[uuid.UUID])
def generate_image(req: PromptRequest) -> list[uuid.UUID]:
    return container.prompt_service.generate_image(req)


@router.post("/images/wait", response_model=list[bytes])
def images_wait(req: FetchRequest) -> list[bytes]:
    return container.prompt_service.fetch_images(req)
