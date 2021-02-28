from config import OWNER_ID
from pyrogram import filters
from Bot import app
from Bot.utils import get_arg
from Bot.sql.chat_sql import load_chats_list, remove_chat_from_db
from io import BytesIO

# broadcast
@app.on_message(filters.user(OWNER_ID) & filters.command("msg"))
async def msg(client, message):
    to_send = get_arg(message)
    chats = load_chats_list()
    success = 0
    failed = 0
    for chat in chats:
        try:
            await app.send_message(int(chat), to_send)
            success += 1
        except:
            failed += 1
            remove_chat_from_db(str(chat))
            pass
    await message.reply(
        f"{success} Söhbətə Mesaj Göndərildi\n{failed} Söhbət uğursuz oldu!"
    )


@app.on_message(filters.user(OWNER_ID) & filters.command("list"))
async def list(client, message):
    chats = []
    all_chats = load_chats_list()
    for i in all_chats:
        if str(i).startswith("-"):
            chats.append(i)
    chatfile = "Çatların siyahısı.\n0. Söhbət nömrəsi | Üzvlət | Çhat link\n"
    P = 1
    for chat in chats:
        try:
            link = await app.export_chat_invite_link(int(chat))
        except:
            link = "Null"
        try:
            members = await app.get_chat_members_count(int(chat))
        except:
            members = "Null"
        try:
            chatfile += "{}. {} | {} | {}\n".format(P, chat, members, link)
            P = P + 1
        except:
            pass
    with BytesIO(str.encode(chatfile)) as output:
        output.name = "chatlist.txt"
        await message.reply_document(document=output, disable_notification=True)
