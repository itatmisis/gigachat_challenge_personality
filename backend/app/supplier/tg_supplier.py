from dataclasses import dataclass

import telebot
from shared.settings import app_settings


@dataclass
class TgSupplier:
    def __post_init__(self) -> None:
        self.bot = telebot.TeleBot(app_settings.tg_bot_token, parse_mode=None)

    def create_stickers(self, user_id: int) -> None:
        self.bot.create_new_sticker_set(user_id, "stickers", "stickers")
