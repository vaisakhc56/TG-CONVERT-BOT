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


@Client.on_message(filters.private & filters.video)
async def download(c, m):
    if m.caption is not None:
        try:
            txt = m.caption
            cp = re.sub("@\\S+", "", txt)
        except BaseException:
            pass
    if m.caption is None:
        cp = m.video.file_name

    send = await c.send_message(
        chat_id=m.chat.id,
        text=Translation.DOWNLOAD_START,
        reply_to_message_id=m.message_id,
    )
#    logger.info(f"Downloading strated by {m.from_user.first_name}")

    download_location = Config.DOWNLOAD_LOCATION + "/"
    c_time = time.time()
    media_location = await c.download_media(
        message=m.video,
        file_name=download_location,
        progress=progress_for_pyrogram,
        progress_args=("Download Status:", send, c_time),
    )
    if media_location is not None:
        await send.edit(Translation.DOWNLOAD_COMPLETE)
#        logger.info(f"{media_location} was downloaded successfully")

        width = 0
        height = 0
        duration = 0
        metadata = extractMetadata(createParser(media_location))
        if metadata.has("duration"):
            duration = metadata.get("duration").seconds
        thumb_image_path = Config.DOWNLOAD_LOCATION + \
            "/" + str(m.from_user.id) + ".jpg"

        if not os.path.exists(thumb_image_path):
            mes = await thumb(m.from_user.id)
            if mes is not None:
                try:
                    mes = await c.get_messages(m.chat.id, mes.msg_id)
                    await mes.download(file_name=thumb_image_path)
                    thumb_image_path = thumb_image_path
                except BaseException:
                    pass
            if mes is None:
                thumb_image_path = await take_screen_shot(
                    media_location,
                    os.path.dirname(media_location),
                    random.randint(0, duration - 1),
                )
            logger.info(thumb_image_path)

            metadata = extractMetadata(createParser(thumb_image_path))
            if metadata.has("width"):
                width = metadata.get("width")
            if metadata.has("height"):
                height = metadata.get("height")

            Image.open(thumb_image_path).convert("RGB").save(thumb_image_path)
            img = Image.open(thumb_image_path)

            img.resize((90, height))
            img.save(thumb_image_path, "JPEG")

        await send.edit(Translation.UPLOAD_START)
    c_time = time.time()
    await c.send_video(
        chat_id=m.chat.id,
        video=media_location,
        caption=f"{cp} | @MoviesBdarija",
        duration=duration,
        width=width,
        height=height,
        supports_streaming=True,
        #        thumb=thumb_image_path,
        thumb="mov.jpg",
        reply_to_message_id=m.message_id,
        progress=progress_for_pyrogram,
        progress_args=("Upload Status:", send, c_time),
    )

    try:
        os.remove(media_location)
    except BaseException:
        pass
    await send.edit(Translation.UPLOAD_COMPLETE)
    logger.info(f"{m.from_user.first_name}'s Task completed")
