import discord
import os
from lib import logger
import lib.config as config
import yt_dlp as youtube_dl


bot = discord.Bot()
GUILD_ID = os.getenv("GUILD_ID")


async def fetch_video_url(search: str):
    ydl_opts = config.ydl_opts

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{search} audio", download=False)
        video_url = info["entries"][0]["url"]
        return video_url


async def connect_to_voice(ctx):
    if ctx.author.voice is None:
        await ctx.respond("Join a voice channel to use this command.")
        return None
    voice = ctx.voice_client
    if voice is None:
        voice = await ctx.author.voice.channel.connect()
    return voice


async def play_audio(ctx, search: str, options=None):
    voice = await connect_to_voice(ctx)
    if voice is None:
        return

    video_url = await fetch_video_url(search)

    args = {"source": video_url}

    if options:
        args["options"] = options

    audio_source = discord.FFmpegPCMAudio(**args)

    if voice.is_playing():
        voice.stop()

    await voice.play(audio_source, wait_finish=True)

    await voice.disconnect()


@bot.event
async def on_ready():
    logger.info(f"We have logged in as {bot.user}")


@bot.slash_command(guild_ids=[GUILD_ID], description="Play a song in nightcore mode")
async def nightcore(ctx: discord.ApplicationContext, search: str):
    await play_audio(ctx, search, options="-filter_complex 'asetrate=48000*1.14'")


@bot.slash_command(
    guild_ids=[GUILD_ID],
    description="Play a song as though you heard it from evan's mic",
)
async def evansmic(ctx: discord.ApplicationContext, search: str):
    await play_audio(ctx, search, options="-filter_complex 'asetrate=44100'")


@bot.slash_command(guild_ids=[GUILD_ID], description="Play a song")
async def play(ctx: discord.ApplicationContext, search: str):
    await play_audio(ctx, search)


bot.run(os.getenv("BOT_TOKEN"))
