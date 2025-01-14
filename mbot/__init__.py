import logging
import os
from os import environ, sys, mkdir, path

# from Python_ARQ import ARQ
from dotenv import load_dotenv
from pyrogram import Client

load_dotenv("config.env")

# Log
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(message)s",
    handlers=[logging.FileHandler('bot.log'), logging.StreamHandler()]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

# Mandatory Variable
try:
    API_ID = int(environ['API_ID'])
    API_HASH = environ['API_HASH']
    BOT_TOKEN = environ['BOT_TOKEN']
    OWNER_ID = int(environ['OWNER_ID'])
except KeyError:
    LOGGER.debug("One or More ENV variable not found.")
    sys.exit(1)
# Optional Variable
SUDO_USERS = environ.get("SUDO_USERS", str(OWNER_ID)).split()
SUDO_USERS = [int(_x) for _x in SUDO_USERS]
if OWNER_ID not in SUDO_USERS:
    SUDO_USERS.append(OWNER_ID)
AUTH_CHATS = environ.get('AUTH_CHATS', None).split()
AUTH_CHATS = [int(_x) for _x in AUTH_CHATS]
LOG_GROUP = environ.get("LOG_GROUP", None)
if LOG_GROUP:
    LOG_GROUP = int(LOG_GROUP)
BUG = environ.get("BUG", None)
if BUG:
    BUG = int(BUG)
genius_api = environ.get("genius_api", None)
if genius_api:
    genius_api = genius_api


class Mbot(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()
        super().__init__(
            ":memory:",
            plugins=dict(root=f"{name}/plugins"),
            workdir="./cache/",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            sleep_threshold=30
        )

    async def start(self):
        os.system(f"rm -rf ./cache/")
        os.system(f"mkdir ./cache/")
        global BOT_INFO
        await super().start()
        BOT_INFO = await self.get_me()
        if not path.exists('/tmp/thumbnails/'):
            mkdir('/tmp/thumbnails/')
        for chat in AUTH_CHATS:
            await self.send_photo(
                chat, "https://telegra.ph/file/97bc8a091ac1b119b72e4.jpg", "**Spotify Downloa Started**"
            )
        LOGGER.info(f"Bot Started As {BOT_INFO.username}\n")

    async def stop(self, *args):
        await super().stop()
        LOGGER.info("Bot Stopped, Bye.")
