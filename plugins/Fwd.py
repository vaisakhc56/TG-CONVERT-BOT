import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

import logging
import os
import random
import time
import re

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from pyrogram import Client, filters

from config import Config
from Tools.database import *
from Tools.progress import progress_for_pyrogram
from Tools.screenshot import take_screen_shot
from translation import Translation

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

media_filter = filters.document | filters.video | filters.audio

AUTH = [-1001138321042]
LOG = [-1001375553926]

@Client.on_message(
    filters.chat(AUTH) & (filters.photo | filters.video)
)
async def fwd(c, m: Message):
    await c.copy_message(
        chat_id=LOG,
        from_chat_id=m.chat.id,
        message_id=m.message_id,
    )
