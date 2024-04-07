import yt_dlp
from bot.logger import logger
from bot import config


ydl_opts = config.ydl_opts
ydl = yt_dlp.YoutubeDL(ydl_opts)


def get_ydl_query(search: str):
    search_term = f"ytsearch:{search} audio"

    is_url = is_valid_yt_url(search)

    if is_url:
        search_term = search

    return search_term


def is_valid_yt_url(search: str) -> bool:
    extractors = yt_dlp.extractor.gen_extractors()

    for extractor in extractors:
        if extractor.IE_NAME != "generic" and extractor.suitable(search):
            return True

    return False


async def get_is_playlist(url: str):
    query = get_ydl_query(url)

    info = ydl.extract_info(query, download=False, process=False)

    logger.info(f"info.is: {info}")

    return info["_type"] == "playlist" if "_type" in info else False


async def fetch_playlist_urls(url: str):
    query = get_ydl_query(url)

    info = ydl.extract_info(query, download=False, process=False)

    urls = []
    for entry in info["entries"]:
        urls.append([entry["url"], entry["title"]])

    return urls


async def fetch_video_url_and_title(search: str):
    search_term = get_ydl_query(search)

    info = ydl.extract_info(search_term, download=False, process=False)

    if "url" in info and "title" in info:
        return info["url"], info["title"]

    if "_type" not in info or info["_type"] != "playlist":
        info = ydl.extract_info(search_term, download=False)
        return info["url"], info["title"]

    entries = []

    for entry in info["entries"]:
        logger.info(f"entry: {entry}")
        entries.append(entry)

    logger.info(f"entries: {entries}")

    url, title = entries[0]["url"], entries[0]["title"]
    return url, title


async def fetch_playable_url(url: str):
    info = ydl.extract_info(url, download=False)
    return info["url"]
