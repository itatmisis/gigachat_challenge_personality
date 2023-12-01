from dataclasses import dataclass

from shared.base import logger


class CheckFailed(Exception):
    ...


@dataclass
class HeathService:
    async def check(self) -> None:
        try:
            ...
        except Exception as exc:
            raise CheckFailed("Check failed for db_repository") from exc
        else:
            logger.info("db_repository check passed")
