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

from asyncio import sleep
from config import Config
from pyrogram import Client
from helpers.log import LOGGER
from pyrogram.errors import MessageNotModified
from plugins.private import HOME_TEXT, HELP_TEXT
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from helpers.utils import get_admins, get_buttons, get_playlist_str, mute, pause, restart_playout, resume, seek_file, shuffle_playlist, skip, unmute

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    admins = await get_admins(Config.CHAT_ID)
    if query.from_user.id not in admins and query.data != "help":
        await query.answer(
            "Nu ai permisiune! 🤣",
            show_alert=True
            )
        return
    if query.data.lower() == "shuffle":
        if not Config.playlist:
            await query.answer("⛔️ Lista de redare goală !", show_alert=True)
            return
        await shuffle_playlist()
        await query.answer("🔁 Amestec !", show_alert=True)
        await sleep(1)
        try:
            await query.edit_message_reply_markup(reply_markup=await get_buttons())
        except MessageNotModified:
            pass

    elif query.data.lower() == "pause":
        if Config.PAUSE:
            await query.answer("⏸ Am pus deja pauza la video !", show_alert=True)
        else:
            await pause()
            await query.answer("⏸ Am pus pauza !", show_alert=True)
            await sleep(1)
        try:
            await query.edit_message_reply_markup(reply_markup=await get_buttons())
        except MessageNotModified:
            pass
    
    elif query.data.lower() == "resume":   
        if not Config.PAUSE:
            await query.answer("▶️ Deja Redau !", show_alert=True)
        else:
            await resume()
            await query.answer("▶️ Redau din nou !", show_alert=True)
            await sleep(1)
        try:
            await query.edit_message_reply_markup(reply_markup=await get_buttons())
        except MessageNotModified:
            pass

    elif query.data.lower() == "skip":   
        if not Config.playlist:
            await query.answer("⛔️ Lista de redare goală !", show_alert=True)
        else:
            await skip()
            await query.answer("⏩ Am dat skip !", show_alert=True)
            await sleep(1)
        if Config.playlist:
            title=f"▶️ <b>{Config.playlist[0][1]}</b>"
        elif Config.STREAM_LINK:
            title=f"▶️ <b>Streaming [Stream Link]({Config.DATA['FILE_DATA']['file']}) !</b>"
        else:
            title=f"▶️ <b>Streaming [Startup Stream]({Config.STREAM_URL}) !</b>"
        try:
            await query.message.edit_message_text(f"{title}",
                reply_markup=await get_buttons()
            )
        except MessageNotModified:
            pass

    elif query.data.lower() == "replay":
        if not Config.playlist:
            await query.answer("⛔️ Lista de redare goală !", show_alert=True)
        else:
            await restart_playout()
            await query.answer("🔂 Redau video de la inceput !", show_alert=True)
            await sleep(1)
        try:
            await query.edit_message_reply_markup(reply_markup=await get_buttons())
        except MessageNotModified:
            pass

    elif query.data.lower() == "mute":
        if Config.MUTED:
            await unmute()
            await query.answer("🔉 Am iesit de pe mute !", show_alert=True)
        else:
            await mute()
            await query.answer("🔇 Acum sunt pe MUTE !", show_alert=True)
        await sleep(1)
        try:
            await query.edit_message_reply_markup(reply_markup=await get_buttons())
        except MessageNotModified:
            pass

    elif query.data.lower() == "seek":
        if not Config.CALL_STATUS:
            return await query.answer("⛔️ Lista de redare goală !", show_alert=True)
        if not (Config.playlist or Config.STREAM_LINK):
            return await query.answer("⚠️ Streamul de pornire nu poate fi căutat !", show_alert=True)
        data=Config.DATA.get('FILE_DATA')
        if not data.get('dur', 0) or \
            data.get('dur') == 0:
            return await query.answer("⚠️ Acest stream nu poate fi căutat !", show_alert=True)
        k, reply = await seek_file(10)
        if k == False:
            return await query.answer(reply, show_alert=True)
        try:
            await query.edit_message_reply_markup(reply_markup=await get_buttons())
        except MessageNotModified:
            pass

    elif query.data.lower() == "rewind":
        if not Config.CALL_STATUS:
            return await query.answer("⛔️ Lista de redare goală !", show_alert=True)
        if not (Config.playlist or Config.STREAM_LINK):
            return await query.answer("⚠️ Streamul de pornire nu poate fi căutat !", show_alert=True)
        data=Config.DATA.get('FILE_DATA')
        if not data.get('dur', 0) or \
            data.get('dur') == 0:
            return await query.answer("⚠️ Acest stream nu poate fi căutat !", show_alert=True)
        k, reply = await seek_file(-10)
        if k == False:
            return await query.answer(reply, show_alert=True)
        try:
            await query.edit_message_reply_markup(reply_markup=await get_buttons())
        except MessageNotModified:
            pass

    elif query.data.lower() == "help":
        buttons = [
            [
                InlineKeyboardButton("Cauta pe YouTube", switch_inline_query_current_chat=""),
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
        try:
            await query.edit_message_text(
                HELP_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data.lower() == "home":
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
                InlineKeyboardButton("❔ CUM SE FOLOSESTE ❔", callback_data="help"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                HOME_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data.lower() == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            pass

    await query.answer()

