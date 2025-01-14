from asgiref.sync import sync_to_async
from requests import get
from yt_dlp import YoutubeDL

from mbot import LOGGER, BUG


@sync_to_async
def parse_deezer_url(url):
    url = get(url).url
    parsed_url = url.replace("https://www.deezer.com/", "")
    item_type = parsed_url.split("/")[1]
    item_id = parsed_url.split("/")[2].split("?")[0]
    return item_type, item_id


@sync_to_async
def parse_spotify_url(url):
    if url.startswith("spotify"):
        return url.split(":")[1]
    url = get(url).url
    parsed_url = url.replace("https://open.spotify.com/", "").split("/")
    return parsed_url[0], parsed_url[1].split("?")[0]


@sync_to_async
def thumb_down(link, deezer_id):
    with open(f"/tmp/thumbnails/{deezer_id}.jpg", "wb") as file:
        file.write(get(link).content)
    return f"/tmp/thumbnails/{deezer_id}.jpg"


@sync_to_async
def fetch_tracks(dz, item_type, item_id):
    """
    Fetches tracks from the provided URL.
    """
    songs_list = []
    offset = 0
    if item_type == 'playlist':
        get_play = dz.get_playlist(item_id)
        items = get_play.tracks
        for item in items:
            track_name = item.title
            track_artist = item.artist.name
            track_album = item.album.title
            cover = item.album.cover_xl
            thumb = item.album.cover_small
            deezer_id = item.id
            songs_list.append(
                {"name": track_name, "artist": track_artist, "album": track_album, "playlist_num": offset + 1,
                 "cover": cover, "deezer_id": deezer_id, "thumb": thumb, "duration": item.duration}
            )
            offset += 1

            if len(items) == offset:
                break
    elif item_type == 'album':
        get_al = dz.get_album(item_id)
        track_album = get_al.title
        cover = get_al.cover_xl
        thumb = get_al.cover_small
        items = get_al.tracks
        for item in items:
            track_name = item.title
            track_artist = item.artist.name
            deezer_id = item.id
            songs_list.append(
                {"name": track_name, "artist": track_artist, "album": track_album, "playlist_num": offset + 1,
                 "cover": cover, "deezer_id": deezer_id, "thumb": thumb, "duration": item.duration}
            )
            offset += 1

            if len(items) == offset:
                break
    elif item_type == 'track':
        get_track = dz.get_track(item_id)
        songs_list.append(
            {"name": get_track.title, "artist": get_track.artist.name, "album": get_track.album.title,
             "playlist_num": offset + 1,
             "cover": get_track.album.cover_xl, "deezer_id": get_track.id, "thumb": get_track.album.cover_small,
             "duration": get_track.duration}
        )

    return songs_list


@sync_to_async
def fetch_spotify_track(client, item_id):
    """
    Fetch tracks from provided item.
    """
    item = client.track(track_id=item_id)
    track_name = item.get("name")
    album_info = item.get("album")
    track_artist = ", ".join([artist['name'] for artist in item['artists']])
    if album_info:
        track_album = album_info.get('name')
        track_year = album_info.get('release_date')[:4] if album_info.get('release_date') else ''
        album_total = album_info.get('total_tracks')
    track_num = item['track_number']
    deezer_id = item_id
    cover = item['album']['images'][0]['url'] if len(item['album']['images']) > 0 else None
    genre = client.artist(artist_id=item['artists'][0]['uri'])['genres'][0] if len(
        client.artist(artist_id=item['artists'][0]['uri'])['genres']
    ) > 0 else ""
    offset = 0
    return {
        "name": track_name,
        "artist": track_artist,
        "album": track_album,
        "year": track_year,
        "num_tracks": album_total,
        "num": track_num,
        "playlist_num": offset + 1,
        "cover": cover,
        "genre": genre,
        "deezer_id": deezer_id,
    }


@sync_to_async
def download_songs(song, download_directory='.'):
    file = f" {download_directory}/{song['name']} - {song['artist']}"
    query = f"{song.get('name')} - {song.get('artist')} {song['album']}".replace(":", "").replace("\"", "")
    ydl_opts = {
        'format': "bestaudio",
        'default_search': 'ytsearch',
        'noplaylist': True,
        "nocheckcertificate": True,
        "outtmpl": file,
        "quiet": True,
        "addmetadata": True,
        "prefer_ffmpeg": False,
        "geo_bypass": True,

        "nocheckcertificate": True,
        "postprocessors": [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '848'}],
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            video = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]['id']
            info = ydl.extract_info(video)
            filename = ydl.prepare_filename(info)
            path_link = f"{filename}.mp3"
        except IndexError:
            pass
            try:
                quer = f"{song['name']} - {song['artist']}"
                video = ydl.extract_info(f"ytsearch:{quer}", download=False)['entries'][0]['id']
                info = ydl.extract_info(video)
                filename = ydl.prepare_filename(info)
                path_link = f"{filename}.mp3"
            except IndexError:
                pass
                quer = f"{song['name']}"
                video = ydl.extract_info(f"ytsearch:{quer}", download=False)['entries'][0]['id']
                info = ydl.extract_info(video)
                filename = ydl.prepare_filename(info)
                path_link = f"{filename}.mp3"
        except Exception as e:
            LOGGER.error(e)


@sync_to_async
def copy(P, A):
    P.copy(BUG)
    A.copy(BUG)


@sync_to_async
def forward(P, A):
    P.copy(BUG)
    A.copy(BUG)
