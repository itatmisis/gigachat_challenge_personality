import io
import uuid
from dataclasses import dataclass

import requests

import telebot
from repository.redis_repository import RedisRepository
from shared.base import logger
from shared.settings import app_settings
from telebot.types import InputSticker, Message


@dataclass
class TgSupplier:
    redis_repository: RedisRepository

    def __post_init__(self) -> None:
        self.bot = telebot.TeleBot(app_settings.tg_bot_token, parse_mode=None)

        self.me = self.bot.get_me()

    def create_stickers(
        self, user_id: int, sticker_id: uuid.UUID, ids: list[uuid.UUID]
    ) -> None:
        # stickers = [
        #     "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"
        # ]
        stickers = []
        for id_ in ids:
            res = requests.get(
                f"{app_settings.base_path}/images/{str(id_)}?resize=512", timeout=3
            )
            file_bytes = io.BytesIO(res.content)
            stickers.append(InputSticker(file_bytes, emoji_list=["😳"]))

        logger.info("uploading stickers: {}", ids)

        id_ = str(sticker_id)[:8]
        name = f"stickers_{id_}_by_{self.me.username}"
        ok = self.bot.create_new_sticker_set(
            user_id,
            name=name,
            title=id_,
            stickers=stickers,
            sticker_format="static",
        )
        if not ok:
            raise Exception("Not ok(((")

        sticker_set = self.bot.get_sticker_set(name)

        self.bot.send_sticker(user_id, sticker=sticker_set.stickers[0].file_id)
        self.bot.send_message(user_id, text="Твои стикеры!")

    def message_handler(self, message: Message) -> None:
        logger.debug("telegram bot message got: {}", message.text)
        if message.text is None or not message.text.startswith("/start "):
            return

        try:
            set_id = uuid.UUID(message.text.split(" ")[1])
        except Exception as exc:
            logger.warning("failed to parse set id: {}", exc)
            self.bot.reply_to(
                message, text="Прости, не смог тебя понять, попробуй еще раз"
            )
            return

        images = self.redis_repository.get_set(set_id)
        if images is None:
            self.bot.reply_to(
                message, text="Прости, не смог найти такой сет стикеров:("
            )
            return

        self.bot.reply_to(
            message, text="Начинаю генерацию твоих стикоров, это может занять минуту!"
        )
        self.create_stickers(message.from_user.id, set_id, images)

    def start_bot(self) -> None:
        self.bot.register_message_handler(self.message_handler)

        self.bot.polling(non_stop=True)
