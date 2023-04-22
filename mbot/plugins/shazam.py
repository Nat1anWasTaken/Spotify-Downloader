from __future__ import unicode_literals

import datetime
import os
import time

from pyrogram import Client
from pyrogram import filters
from requests import get
from shazamio import Shazam

from mbot.utils.shazam import humanbytes
from mbot.utils.util import run_cmd as runcmd

NOT_SUPPORT = []
ADMINS = 1794941609


def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])


# @sync_to_async
def thumb_down(album_id, img):
    with open(f"/tmp/thumbnails/{album_id}.jpg", "wb") as file:
        file.write(get(img).content)
    return f"/tmp/thumbnails/{album_id}.jpg"


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


async def shazam(file):
    shazam = Shazam()
    try:
        r = await shazam.recognize_song(file)
    except:
        return None, None, None
    if not r:
        return None, None, None
    track = r.get("track")
    nt = track.get("images")
    image = nt.get("coverarthq")
    by = track.get("subtitle")
    title = track.get("title")
    return image, by, title


async def convert_to_audio(vid_path):
    stark_cmd = f"ffmpeg -i {vid_path} -map 0:a friday.mp3"
    await runcmd(stark_cmd)
    final_warner = "friday.mp3"
    if not os.path.exists(final_warner):
        return None
    return final_warner


@Client.on_message(filters.command(["find", "shazam"]))
async def shazam_(client, message):
    stime = time.time()
    msg = await message.reply_text("`Shazaming This Song.")
    if not message.reply_to_message:
        return await msg.edit("`Reply To Song File`")
    if not (message.reply_to_message.audio or message.reply_to_message.voice or message.reply_to_message.video):
        return await msg.edit("`Reply To Audio File.`")
    if message.reply_to_message.video:
        video_file = await message.reply_to_message.download()
        music_file = await convert_to_audio(video_file)
        dur = message.reply_to_message.video.duration
        if not music_file:
            return await msg.edit("`Unable To Convert To Song File. Is This A Valid File?`")
    elif (message.reply_to_message.voice or message.reply_to_message.audio):
        dur = message.reply_to_message.voice.duration if message.reply_to_message.voice else message.reply_to_message.audio.duration
        music_file = await message.reply_to_message.download()
    size_ = humanbytes(os.stat(music_file).st_size)
    dur = datetime.timedelta(seconds=dur)
    thumb, by, title = await shazam(music_file)
    if title is None:
        return await msg.edit("`No Results Found.`")
    etime = time.time()
    t_k = round(etime - stime)
    caption = f"""<b><u>Shazamed Song</b></u>
    
<b>Song Name :</b> <code>{title}</code>
<b>Singer :</b> <code>{by}</code>
<b>Duration :</b> <code>{dur}</code>
<b>Size :</b> <code>{size_}</code>
<b>Time Taken :</b> <code>{t_k} Seconds</code>

<b><u>Shazamed By @Spotify_downloa_bot</b></u>
    """
    if thumb:
        await msg.delete()
        await message.reply_to_message.reply_photo(thumb, caption=caption, quote=True)
    else:
        await msg.edit(caption)
    os.remove(music_file)
    if thumb:
        os.remove(thumb)
