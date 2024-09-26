# Don't remove This Line From Here. Tg: @im_piro | @PiroHackz
import asyncio
import base64
import logging
import os
import random
import re
import string 
import time
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, TUT_VID, IS_VERIFY, VERIFY_EXPIRE, SHORTLINK_API, SHORTLINK_URL, PREMIUM_BUTTON, PREMIUM_BUTTON2
from helper_func import subscribed, encode, decode, get_messages, get_shortlink, get_verify_status, update_verify_status, get_exp_time
from database.database import *
from database.db_premium import *

# Enable logging
logging.basicConfig(level=logging.INFO)

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    logging.info(f"Received /start command from user ID: {id}")

    if not await present_user(id):
        try:
            await add_user(id)
        except Exception as e:
            logging.error(f"Error adding user: {e}")
            return

    text = message.text
    is_premium = await is_premium_user(id)
    verify_status = await get_verify_status(id)
    logging.info(f"Is premium: {is_premium}")

    await update_verify_status(id, is_verified=False)

    if "verify_" in message.text:
        _, token = message.text.split("_", 1)
        if verify_status['verify_token'] != token:
            return await message.reply("Your token is invalid or expired ⌛. Try again by clicking /start")

        await update_verify_status(id, is_verified=True, verified_time=time.time())
    
    if verify_status["link"] == "":
        reply_markup = PREMIUM_BUTTON

    await message.reply(f"Your token successfully verified and valid for: {get_exp_time(VERIFY_EXPIRE)} ⏳", reply_markup=PREMIUM_BUTTON, protect_content=False, quote=True)

    if not is_premium:
        await message.reply("Buy premium to access this content\nTo Buy Contact @rohit_1888", reply_markup=PREMIUM_BUTTON2)
        return
    
    try:
        base64_string = text.split(" ", 1)[1]
    except IndexError:
        return

    string = await decode(base64_string)
    argument = string.split("-")

    if len(argument) == 3:
        try:
            start = int(int(argument[1]) / abs(client.db_channel.id))
            end = int(int(argument[2]) / abs(client.db_channel.id))
        except:
            return
        
        ids = range(start, end + 1) if start <= end else []
    
    elif len(argument) == 2:
        try:
            ids = [int(int(argument[1]) / abs(client.db_channel.id))]
        except:
            return

    temp_msg = await message.reply("Please wait...")
    try:
        messages = await get_messages(client, ids)
    except:
        await message.reply_text("Something went wrong..!")
        return

    await temp_msg.delete()
    snt_msgs = []

    for msg in messages:
        original_caption = msg.caption.html if msg.caption else ""
        caption = f"{original_caption}\n\n{CUSTOM_CAPTION}" if CUSTOM_CAPTION else original_caption
        reply_markup = msg.reply_markup if not DISABLE_CHANNEL_BUTTON else None

        try:
            snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
            await asyncio.sleep(0.5)
            snt_msgs.append(snt_msg)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
            snt_msgs.append(snt_msg)
        except:
            pass

    if string.startswith("get"):
        if not is_premium and not verify_status['is_verified']:
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            await update_verify_status(id, verify_token=token, link="")
            link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, f'https://telegram.dog/{client.username}?start=verify_{token}')
            btn = [
                [InlineKeyboardButton("Click here", url=link), InlineKeyboardButton('How to use the bot', url=TUT_VID)],
                [InlineKeyboardButton('BUY PREMIUM', callback_data='buy_prem')]
            ]
            await message.reply(f"Your Ads token is expired or invalid. Please verify to access the files.\n\nToken Timeout: {get_exp_time(VERIFY_EXPIRE)}\n\nWhat is the token?\n\nThis is an ads token. If you pass 1 ad, you can use the bot for 24 Hours after passing the ad.", reply_markup=InlineKeyboardMarkup(btn), protect_content=False, quote=True)
            return

        try:
            base64_string = text.split(" ", 1)[1]
        except IndexError:
            return
        
        string = await decode(base64_string)
        argument = string.split("-")

        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            
            ids = range(start, end + 1) if start <= end else []
        
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        
        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong..!")
            return

        await temp_msg.delete()
        snt_msgs = []
        
        for msg in messages:
            original_caption = msg.caption.html if msg.caption else ""
            caption = f"{original_caption}\n\n{CUSTOM_CAPTION}" if CUSTOM_CAPTION else original_caption
            reply_markup = msg.reply_markup if not DISABLE_CHANNEL_BUTTON else None

            try:
                snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                await asyncio.sleep(0.5)
                snt_msgs.append(snt_msg)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                snt_msgs.append(snt_msg)
            except:
                pass

    else:
        try:
            reply_markup = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("😊 About Me", callback_data="about"), InlineKeyboardButton("🔒 Close", callback_data="close")],
                    [InlineKeyboardButton('BUY PREMIUM', callback_data='buy_prem')]
                ]
            )
            await message.reply_text(
                text=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=None if not message.from_user.username else '@' + message.from_user.username,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                quote=True
            )
        except Exception as e:
            logging.error(f"Error sending start message: {e}")

#=====================================================================================##

WAIT_MSG = """<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a reply to any telegram message without any spaces.</code>"""

#=====================================================================================##

# Don't remove This Line From Here. Tg: @im_piro | @PiroHackz
    
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink),
            InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink2),
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text='Try Again',
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: