from pyrogram.types.messages_and_media import message
from config import OWNER_ID
from pyrogram import filters
from pyrogram.errors import BadRequest
from Bot import app
import Bot.sql.blacklist_sql as sql
from Bot.utils import get_arg


@app.on_message(filters.user(OWNER_ID) & filters.command("blacklist"))
async def blacklist(client, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user["id"]
    else:
        arg = get_arg(message)
        if len(arg) != 1:
            await message.reply(
                "Bunun üçün istifadəçi kimliyi və ya istifadəçi mesajına cavab vermək lazımdır!"
            )
            return ""
        if arg.startswith("@"):
            try:
                user = await app.get_users(arg)
                user_id = user.id
            except BadRequest as ex:
                await message.reply("Etibarlı bir istifadəçi deyil")
                print(ex)
                return ""
        else:
            user_id = int(arg)
        sql.add_user_to_bl(int(user_id))
        await message.reply(f"[Qara Siyahı](tg://user?id={user_id})")


@app.on_message(filters.user(OWNER_ID) & filters.command("unblacklist"))
async def unblacklist(client, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user["id"]
    else:
        arg = get_arg(message)
        if len(arg) != 1:
            await message.reply(
                "Bunun üçün istifadəçi kimliyi və ya istifadəçi mesajına cavab vermək lazımdır!"
            )
            return ""
        if arg.startswith("@"):
            try:
                user = await app.get_users(arg)
                user_id = user.id
            except BadRequest:
                await message.reply("Etibarlı bir istifadəçi deyil!")
                return ""
        else:
            user_id = int(arg)
        sql.rem_user_from_bl(int(user_id))
        await message.reply(f"[Siyahıdan Kənar](tg://user?id={user_id})")
