import discord
import os
from bot.core.queue import Queue
from bot.logger import logger


bot = discord.Bot()
GUILD_ID = os.getenv("GUILD_ID")

_queue = Queue()

@bot.event
async def on_ready():
    logger.info(f"We have logged in as {bot.user}")


@bot.slash_command(guild_ids=[GUILD_ID], description="Play a song in nightcore mode")
async def nightcore(ctx: discord.ApplicationContext, search: str):
    await _queue.play_next(ctx, search, options="-af asetrate=48000*1.15")


@bot.slash_command(
    guild_ids=[GUILD_ID],
    description="Play a song as though you heard it from evan's mic",
)
async def evansmic(ctx: discord.ApplicationContext, search: str):
    await _queue.play_next(ctx, search, options="-af asetrate=44100")

@bot.slash_command(
    guild_ids=[GUILD_ID],
    description="Play a song sloow",
)
async def sloow(ctx: discord.ApplicationContext, search: str):
    await _queue.play_next(ctx, search, options="-af asetrate=48000*0.85")

@bot.slash_command(guild_ids=[GUILD_ID], description="Play a song")
async def play(ctx: discord.ApplicationContext, search: str):
    await _queue.play_next(ctx, search)

@bot.slash_command(guild_ids=[GUILD_ID], description="Show the queue")
async def queue(ctx: discord.ApplicationContext):
    await _queue.show_queue(ctx)

@bot.slash_command(guild_ids=[GUILD_ID], description="Skip the current song")
async def skip(ctx: discord.ApplicationContext):
    await _queue.skip(ctx)

@bot.slash_command(guild_ids=[GUILD_ID], description="Leave the server and clear the queue")
async def die(ctx: discord.ApplicationContext):
    await _queue.die(ctx)

bot.run(os.getenv("BOT_TOKEN"))
