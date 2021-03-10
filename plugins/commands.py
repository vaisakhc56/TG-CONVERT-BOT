import os

from config import Config

from translation import Translation

from pyrogram import Client, filters



@Client.on_message(filters.private & filters.command(["start"]))
async def start(c, m):
    await c.send_message(
        chat_id=m.chat.id,
        text=Translation.START.format(m.from_user.first_name, Config.USER_NAME),
        reply_to_message_id=m.message_id
    )


