from dotenv import load_dotenv

load_dotenv()


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '312',
    }],
    'noplaylist': True,
}