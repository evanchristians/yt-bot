from dotenv import load_dotenv

load_dotenv()


ydl_opts = {
    'format': 'm4a/bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
        'preferredquality': '312',
    }],
    'noplaylist': True,
    'cookiefile' : 'cookies.txt',
    'ignoreerrors': True,
    'quiet': True,
}