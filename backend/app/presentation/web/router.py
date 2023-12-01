import enum

from fastapi import APIRouter

from presentation.dependencies import container
from presentation.web.schemas import HealthResponse, HealthStatuses
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
