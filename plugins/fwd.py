import logging
import os
import random
import time
import re

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import Message


from config import Config
from Tools.database import *
from Tools.progress import progress_for_pyrogram
from Tools.screenshot import take_screen_shot
from translation import Translation

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
