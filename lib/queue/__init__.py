from enum import Enum
import yt_dlp as yt
from lib import config


Status = Enum(
    "Statuses",
    ["playing", "paused", "stopped", "pending", "played", "skipped", "error"],
)

queue = []


# TODO - implement the queue system
def add_to_queue(search: str):
    with yt.YoutubeDL(config.ydl_ops) as ydl:
        info = ydl.extract_info(f"ytsearch:{search}", download=False)
        video_url = info["entries"][0]["url"]

    queue.append(
        {
            "search": search,
            "video_url": video_url,
            "title": info["entries"][0]["title"],
            "status": Status.pending,
        }
    )
