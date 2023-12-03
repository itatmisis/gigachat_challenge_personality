import base64
import io
import uuid
from dataclasses import dataclass

import telebot
from repository.redis_repository import RedisRepository
from service.image_service import ImageService
from shared.base import logger
from shared.settings import app_settings
from telebot.apihelper import ApiTelegramException
from telebot.types import InputFile, InputSticker, Message


@dataclass
class TgSupplier:
    redis_repository: RedisRepository
    image_service: ImageService

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
        images = []
        for id_ in ids:
            img_b64 = self.redis_repository.get_image(id_)
            if img_b64 is None:
                logger.warning("image not found: {}", img_b64)
                return

            file_bytes = self.image_service.resize_img(
                base64.b64decode(img_b64), shape=(512, 512)
            )
            file_bytes = self.image_service.add_corners(im_bytes=file_bytes, rad=50)

            images.append(file_bytes)
            stickers.append(InputSticker(io.BytesIO(file_bytes), emoji_list=["😳"]))

        logger.info("uploading stickers: {}", ids)

        id_ = str(sticker_id)[:8]
        name = f"stickers_{id_}_by_{self.me.username}"

        try:
            ok = self.bot.create_new_sticker_set(
                user_id,
                name=name,
                title=id_,
                stickers=stickers,
                sticker_format="static",
            )
        except ApiTelegramException as exc:
            logger.warning(f"unknown error occurred: {exc}")
        else:
            if not ok:
                raise Exception("Not ok(((")

        sticker_set = self.bot.get_sticker_set(name)

        self.bot.send_sticker(user_id, sticker=sticker_set.stickers[0].file_id)
        self.bot.send_message(
            user_id, text="Твои стикеры для использования в телеграме!"
        )

        rows, cols = 3, 4
        batch_step = rows * cols
        for batch_idx in range(len(images) // batch_step + 1):
            batch = images[batch_idx * batch_step : (batch_idx + 1) * batch_step]
            if not batch:
                continue

            grid = self.image_service.make_grip(
                images_bytes=batch,
                rows=rows,
                cols=cols,
            )
            input_file = InputFile(io.BytesIO(grid))
            input_file.file_name = "stickers.png"
            self.bot.send_document(
                user_id,
                document=input_file,
                caption="Стикеры, готовые к печати",
            )

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
            message, text="Начинаю генерацию твоих стикеров, это займет меньше минуты!"
        )
        self.create_stickers(message.from_user.id, set_id, images)

    def start_bot(self) -> None:
        self.bot.register_message_handler(self.message_handler)

        while True:
            try:
                self.bot.polling(non_stop=True)
            except Exception:
                logger.exception("restarting bot, because of error")
