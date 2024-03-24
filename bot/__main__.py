import asyncio
import discord
import os


bot = discord.Bot()
GUILD_ID = os.getenv("GUILD_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.slash_command(guild_ids=GUILD_ID)
async def speak(ctx):
    await ctx.respond("Join a voice channel to use this command")
    if ctx.author.voice is None:
        return
    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()
    voice_client.play(discord.FFmpegOpusAudio("audio.mp3"))
    while voice_client.is_playing():
        await asyncio.sleep(1)
    await voice_client.disconnect()


bot.run(BOT_TOKEN)
