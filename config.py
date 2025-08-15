import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Get this value from my.telegram.org/apps
API_ID = int(getenv("API_ID" ,"23212132"))
API_HASH = getenv("API_HASH" ,"1c17efa86bdef8f806ed70e81b473c20")

# Get your token from @BotFather on Telegram.
BOT_TOKEN = getenv("BOT_TOKEN" , "8463253997:AAEUAKGWXKCnx-6TXllnmZmc60cgptPl0vg")

# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://ryumasgod:ryumasgod@cluster0.ojfkovp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 60))

# Chat id of a group for logging bot's activities
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", "-1002800777153"))

# Get this value from @MissRose_Bot on Telegram by /id
OWNER_ID = int(getenv("OWNER_ID", "8429156335"))

## Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

API_URL = getenv("API_URL", 'https://tgmusic.fallenapi.fun') #youtube song url
VIDEO_API_URL = getenv("VIDEO_API_URL", 'https://api.video.thequickearn.xyz')
API_KEY = getenv("API_KEY", "3dba2c_Rvau9IFTFQjgSRaZsvCgNWb0iWeHBN57") # youtube song api key, generate free key or buy paid plan from panel.thequickearn.xyz

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "t.me/meisred",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "master")
GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)  # Fill this variable if your upstream repository is private

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/SHADOWSHQ")
SUPPORT_GROUP = getenv("SUPPORT_GROUP", "https://t.me/SHADOWBOTSHQ")

# Set this to True if you want the assistant to automatically leave chats after an interval
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))

# make your bots privacy from telegra.ph and put your url here 
PRIVACY_LINK = getenv("PRIVACY_LINK", "https://telegra.ph/Privacy-Policy-for-AviaxMusic-08-14")


# Get this credentials from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "1c21247d714244ddbb09925dac565aed")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "709e1a2969664491b58200860623ef19")


# Maximum limit for fetching playlist's track from youtube, spotify, apple links.
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))


# Telegram audio and video file size limit (in bytes)
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 2145386496))
# Checkout https://www.gbmb.org/mb-to-bytes for converting mb to bytes


# Get your pyrogram v2 session from Replit
STRING1 = getenv("STRING_SESSION", "BQGvJ_0Adt6lmVaTljo96G9YV0xaOi0O26V2utMXtqO1d9cySnNMh1KCQh2oqT2rxMwDjTj274JF5QDUOF1wO21nH52TvrOuqDvnuZbiOsKM7o4XeTS5CLmwJFAP0IKDvAvEgCnfVGLBGuaOJEijZNaP4nhFvtMP_sMLYjLATOsJHZLEkdz4PkJyfQZCMTV6MSR1D7BFnythV1VTBRA7qIjqYenmEZzGVHXGy4DaetN-BbDwJZmf2QIIZx90Q2-zvFl_z7-2srBWXcOYYDT5pZ1UkwtX71c1hChhmuFJHhLejZz0PWoTUyVr35GRto9J5QU4D0xGvdTaw8qi7m7qe5Gk4IZkjQAAAAHdw02OAA")
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)


BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}


START_IMG_URL = getenv(
    "START_IMG_URL", "https://files.catbox.moe/39jls1.jpeg"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://files.catbox.moe/39jls1.jpeg"
)
PLAYLIST_IMG_URL = "https://files.catbox.moe/39jls1.jpeg"
STATS_IMG_URL = "https://files.catbox.moe/39jls1.jpeg"
TELEGRAM_AUDIO_URL = "https://files.catbox.moe/39jls1.jpeg"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/39jls1.jpeg"
STREAM_IMG_URL = "https://files.catbox.moe/39jls1.jpeg"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/39jls1.jpeg"
YOUTUBE_IMG_URL = "https://files.catbox.moe/39jls1.jpeg"
SPOTIFY_ARTIST_IMG_URL = "https://files.catbox.moe/39jls1.jpeg"
SPOTIFY_ALBUM_IMG_URL = "https://files.catbox.moe/39jls1.jpeg"
SPOTIFY_PLAYLIST_IMG_URL = "https://files.catbox.moe/39jls1.jpeg"


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))


if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_GROUP:
    if not re.match("(?:http|https)://", SUPPORT_GROUP):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_GROUP url is wrong. Please ensure that it starts with https://"
        )








