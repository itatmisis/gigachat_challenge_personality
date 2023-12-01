from dataclasses import dataclass

from shared.base import logger


class CheckFailed(Exception):
    ...


@dataclass
class HeathService:
    async def check(self) -> None:
        try:
            1 + 1
        except Exception as exc:
            raise CheckFailed("Check failed for ...") from exc
        else:
            logger.info("... check passed")
