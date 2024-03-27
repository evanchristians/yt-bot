import yt_dlp
from bot.logger import logger
from bot import config


def is_valid_yt_url(search: str) -> bool:
  extractors = yt_dlp.extractor.gen_extractors()

  for extractor in [ext for ext in extractors if ext.IE_NAME == "Youtube"]:
    if extractor.suitable(search):
      return True
    
  return False


async def fetch_video_url_and_title(search: str):
    ydl_opts = config.ydl_opts

    search_term = f"ytsearch:{search} audio"

    is_url = is_valid_yt_url(search)

    if is_url:  
        search_term = search

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_term, download=False)

        if is_url:
            url, title = info["url"], info["title"]
            logger.info(f"Found video url: {url} {title}")
            return url, title

        if ("entries" not in info) or (len(info["entries"]) == 0):
            return None, None

        url, title = info["entries"][0]["url"], info["entries"][0]["title"]
        logger.info(f"Found video url: {url} {info['entries'][0]['title']}")

        return url, title
