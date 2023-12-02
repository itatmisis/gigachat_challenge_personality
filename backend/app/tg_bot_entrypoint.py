from presentation.dependencies import container
from shared.base import logger

if __name__ == "__main__":
    logger.info("starting tg bot: {}", container.tg_supplier.me.username)

    container.tg_supplier.start_bot()
