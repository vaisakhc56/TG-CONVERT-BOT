import logging
import os
import time

from Tools.progress import progress_for_pyrogram
from translation import Translation

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def upload_video(
    c, m, send, media_location, thumb_image_path, duration, width, height
):
    await send.edit(Translation.UPLOAD_START)
    c_time = time.time()
    if m.video:
        await c.send_video(
            chat_id=m.chat.id,
            video=media_location,
            #            caption=f"{cp} | @MoviesBdarija",
            caption=m.caption,
            duration=duration,
            width=width,
            height=height,
            supports_streaming=True,
            thumb=thumb_image_path,
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
