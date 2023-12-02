import io
import uuid
from dataclasses import dataclass

import requests

import telebot
from shared.base import logger
from shared.settings import app_settings
from telebot.types import InputSticker


@dataclass
class TgSupplier:
    def __post_init__(self) -> None:
        self.bot = telebot.TeleBot(app_settings.tg_bot_token, parse_mode=None)

    def create_stickers(self, user_id: int, ids: list[uuid.UUID]) -> None:
        # stickers = [
        #     "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"
        # ]
        stickers = []
        for id_ in ids:
            res = requests.get(
                f"{app_settings.base_path}/images/{str(id_)}?resize=512", timeout=3
            )
            file_bytes = io.BytesIO(res.content)
            stickers.append(InputSticker(file_bytes, emoji_list=["👉"]))

        logger.info("uploading stickers: {}", ids)

        ok = self.bot.create_new_sticker_set(
            user_id,
            "stickers_by_ai_generated_stickers_bot",
            "stickers",
            stickers=stickers,
            sticker_format="static",
        )
        print(ok)
