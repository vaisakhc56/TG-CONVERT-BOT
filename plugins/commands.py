import logging

from pyrogram import Client, Filters, InlineKeyboardButton, InlineKeyboardMarkup

from config import Config
from translation import Translation

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


my_father = "https://t.me/{}".format(Config.USER_NAME[1:])
support = "https://telegram.dog/Ns_Bot_supporters"


@Client.on_message(Filters.command(["start"]))
async def start(c, m):

    await c.send_message(
        chat_id=m.chat.id,
        text=Translation.START.format(m.from_user.first_name, Config.USER_NAME),
        reply_to_message_id=m.message_id,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("My Father 👨‍💻", url=my_father),
                    InlineKeyboardButton("📌Support channel", url=support),
                ]
            ]
        ),
    )
    logger.info(f"{m.from_user.first_name} used start command")
