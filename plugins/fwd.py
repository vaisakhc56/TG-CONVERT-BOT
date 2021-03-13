import logging

from pyrogram import Client, filters
from pyrogram.types import Message



logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# Download the media

AUTH = [-1001138321042]
LOG = [-1001375553926]


@Client.on_message(filters.group & filters.video)
async def fwd(c, m: Message):
    await m.forward(
        chat_id=LOG)
