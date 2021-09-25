"""
VideoPlayerBot, Telegram Video Chat Bot
Copyright (c) 2021  Asm Safone <https://github.com/AsmSafone>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import os
import sys
import asyncio
from config import Config
from helpers.log import LOGGER
from pyrogram import Client, filters
from helpers.utils import delete, update, is_admin
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaDocument


HOME_TEXT = "👋🏻 **Salut\Buna [{}](tg://user?id={})**, \n\nEu sunt @OTRmoviebot ! \nPot face stream video, Radio, YouTube & la fisiere de pe Telegram audio / video direct in grup pe voice chat. Hai sa ne bucuram impreuna de acest bot pe @filme4kpetelegram 😉! \n\n**Made With ❤️ By @OTRofficial ❌ LupiiDinHaita !** 🐺"
HELP_TEXT = """
🏷️ --**Cum sa setezi BOT'ul**-- :

\u2022 Porneste un voice chat pe grup!
\u2022 Adauga @OTRmoviebot in grupul tau!
\u2022 Foloseste /play [nume video] sau foloseste /play ca raspuns la un fisier video trimis sau link de YouTube.

💡 --**Comenzi**--:

\u2022 `/start` - verifica statusul bot'ului
\u2022 `/help` - arata mesajul de ajutor
\u2022 `/current` - arata video/streamul curent
\u2022 `/playlist` - arata playlistul

💡 --**Comenzi ADMIN ONLY**--:

\u2022 `/seek` - deruleaza video
\u2022 `/skip` - da skip la video
\u2022 `/stream` - porneste stream video
\u2022 `/pause` - pune pauza la video
\u2022 `/resume` - scoate videoul de pe pauza
\u2022 `/mute` - pune botul pe mute in vc
\u2022 `/unmute` - scoate botul de pe mute in vc
\u2022 `/leave` - scoate botul de pe vc
\u2022 `/shuffle` - amesteca playlistul
\u2022 `/volume` - ajusteaza volumul (0-200)
\u2022 `/replay` - da play de la inceput
\u2022 `/clrlist` - sterge playlistul curent
\u2022 `/restart` - update & restart the bot
\u2022 `/setvar` - seteaza/schimba configul heroku
\u2022 `/getlogs` - trimite ffmpeg & bot logs

© **Powered By** : 
**@OTRofficial | @LupiiDinHaita** 🔥
"""

admin_filter=filters.create(is_admin) 

@Client.on_message(filters.command(["start", f"start@{Config.BOT_USERNAME}"]))
async def start(client, message):
    buttons = [
            [
                InlineKeyboardButton("CAUTA INLINE", switch_inline_query_current_chat=""),
            ],
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/OTRportal"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/OTRofficial"),
            ],
            [
                InlineKeyboardButton("H.A.I.T.A.🐺🎭😍⚔❤", url="https://t.me/LupiiDinHaita"),
                InlineKeyboardButton("Grupuri Romanesti", url="https://t.me/GrupuriRomanesti"),
            ],
            [
                InlineKeyboardButton("❔ CUM SE FOLOSESTE ❔", callback_data="help"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    m=await message.reply_photo(photo=Config.THUMB_LINK, caption=HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)
    await delete(m)


@Client.on_message(filters.command(["help", f"help@{Config.BOT_USERNAME}"]))
async def show_help(client, message):
    buttons = [
            [
                InlineKeyboardButton("SEARCH VIDEOS", switch_inline_query_current_chat=""),
            ],
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/OTRportal"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/OTRofficial"),
            ],
            [
                InlineKeyboardButton("H.A.I.T.A.🐺🎭😍⚔❤", url="https://t.me/LupiiDinHaita"),
                InlineKeyboardButton("Grupuri Romanesti", url="https://t.me/GrupuriRomanesti"),
            ],
            [
                InlineKeyboardButton("INAPOI", callback_data="home"),
                InlineKeyboardButton("INCHIDE MENIU", callback_data="close"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    if Config.msg.get('help') is not None:
        try:
            await Config.msg['help'].delete()
        except:
            pass
    Config.msg['help'] = await message.reply_photo(photo=Config.THUMB_LINK, caption=HELP_TEXT, reply_markup=reply_markup)
    await delete(message)


@Client.on_message(filters.command(["restart", "update", f"restart@{Config.BOT_USERNAME}", f"update@{Config.BOT_USERNAME}"]) & admin_filter)
async def update_handler(client, message):
    k=await message.reply_text("🔄 **Verific ...**")
    await asyncio.sleep(3)
    if Config.HEROKU_APP:
        await k.edit("🔄 **Nu am detectat Heroku, \nRestarting App To Update!**")
    else:
        await k.edit("🔄 **Ma restartez, Te rog sa astepti...**")
    await update()
    try:
        await k.edit("✅ **Restart reusit! \nJoin @OTRportal and @GrupuriRomanesti For Update!**")
        await k.reply_to_message.delete()
    except:
        pass


@Client.on_message(filters.command(["getlogs", f"getlogs@{Config.BOT_USERNAME}"]) & admin_filter)
async def get_logs(client, message):
    logs=[]
    if os.path.exists("ffmpeg.txt"):
        logs.append(InputMediaDocument("ffmpeg.txt", caption="FFMPEG Logs"))
    if os.path.exists("ffmpeg.txt"):
        logs.append(InputMediaDocument("botlog.txt", caption="Video Player Logs"))
    if logs:
        try:
            await message.reply_media_group(logs)
            await delete(message)
        except:
            m=await message.reply_text("❌ **A aparut o ERROARE !**")
            await delete(m)
            pass
        logs.clear()
    else:
        m=await message.reply_text("❌ **Nu am gasit loguri !**")
        await delete(m)


@Client.on_message(filters.command(["setvar", f"setvar@{Config.BOT_USERNAME}"]) & admin_filter)
async def set_heroku_var(client, message):
    if not Config.HEROKU_APP:
        buttons = [[InlineKeyboardButton('HEROKU_API_KEY', url='https://dashboard.heroku.com/account/applications/authorizations/new')]]
        k=await message.reply_text(
            text="❗ **No Heroku App Found !** \n__Please Note That, This Command Needs The Following Heroku Vars To Be Set :__ \n\n1. `HEROKU_API_KEY` : Your heroku account api key.\n2. `HEROKU_APP_NAME` : Your heroku app name. \n\n**For More Ask In @SafoTheBot !!**", 
            reply_markup=InlineKeyboardMarkup(buttons))
        await delete(k)
        return     
    if " " in message.text:
        cmd, env = message.text.split(" ", 1)
        if  not "=" in env:
            k=await message.reply_text("❗ **You Should Specify The Value For Variable!** \n\nFor Example: \n`/setvar CHAT_ID=-1001313215676`")
            await delete(k)
            return
        var, value = env.split("=", 2)
        config = Config.HEROKU_APP.config()
        if not value:
            m=await message.reply_text(f"❗ **No Value Specified, So Deleting `{var}` Variable !**")
            await asyncio.sleep(2)
            if var in config:
                del config[var]
                await m.edit(f"🗑 **Sucessfully Deleted `{var}` !**")
                config[var] = None
            else:
                await m.edit(f"🤷‍♂️ **Variable Named `{var}` Not Found, Nothing Was Changed !**")
            return
        if var in config:
            m=await message.reply_text(f"⚠️ **Variable Already Found, So Edited Value To `{value}` !**")
        else:
            m=await message.reply_text(f"⚠️ **Variable Not Found, So Setting As New Var !**")
        await asyncio.sleep(2)
        await m.edit(f"✅ **Succesfully Set Variable `{var}` With Value `{value}`, Now Restarting To Apply Changes !**")
        config[var] = str(value)
        await delete(m)
    else:
        k=await message.reply_text("❗ **You Haven't Provided Any Variable, You Should Follow The Correct Format !** \n\nFor Example: \n• `/setvar CHAT_ID=-1001313215676` to change or set CHAT_ID var. \n• `/setvar REPLY_MESSAGE=` to delete REPLY_MESSAGE var.")
        await delete(k)
