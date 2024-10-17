#(©)Codexbotz

from aiohttp import web
from plugins import web_server

from pyrogram import Client
from pyromod import listen
from pyromod.listen import ListenerTypes
from pyrogram.enums import ParseMode
import sys
from datetime import datetime

from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, CHANNEL_ID, PORT, FORCESUB_CHANNEL2
from dotenv import load_dotenv
from database.db_premium import remove_expired_users
from collections import defaultdict

class Bot(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listeners = defaultdict(list)

    # Rest of your bot methods...

from apscheduler.schedulers.asyncio import AsyncIOScheduler
scheduler = AsyncIOScheduler()
scheduler.add_job(remove_expired_users, "interval", seconds=3600)
scheduler.start()

load_dotenv(".env")

class Bot(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listeners = defaultdict(list)

    async def start(self):
        await super().start()
        print("Bot started!")

    async def stop(self, *args):
        await super().stop(*args)
        print("Bot stopped!")

# Initialize your bot
app = Bot("my_bot", api_id=APP_ID, api_hash=API_HASH, bot_token=TG_BOT_TOKEN)

        if FORCE_SUB_CHANNEL:
            try:
                link = await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the FORCE_SUB_CHANNEL value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL}")
                self.LOGGER(__name__).info("\nBot Stopped. @im_piro for support")
                sys.exit()
        if FORCESUB_CHANNEL2:
            try:
                link = (await self.get_chat(FORCESUB_CHANNEL2)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCESUB_CHANNEL2)
                    link = (await self.get_chat(FORCESUB_CHANNEL2)).invite_link
                self.invitelink2 = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the FORCESUB_CHANNEL2 value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCESUB_CHANNEL2}")
                self.LOGGER(__name__).info("\nBot Stopped. Dm https://t.me/im_piro for support")
                sys.exit()
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Make Sure bot is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}")
            self.LOGGER(__name__).info("\nBot Stopped. @rohit_1888 for support")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Bot Running..! Made by @rohit_1888")

        self.username = usr_bot_me.username
        #web-response
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped. Made By @rohit_1888")
