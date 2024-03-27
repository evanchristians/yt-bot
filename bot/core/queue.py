from enum import Enum
import discord
from bot.core import youtube

Status = Enum(
    "Statuses",
    ["playing", "paused", "stopped", "pending", "played", "skipped", "error"],
)


class Queue:
    def __init__(self):
        self

    queue = []

    def add_to_queue(self, title: str, video_url: str, options=None):
        song = {
            "video_url": video_url,
            "title": title,
            "status": Status.pending,
        }

        if options is not None:
            song["options"] = options

        self.queue.append(song)

    def get_next_pending_index(self):
        return next(
            (
                index
                for index, song in enumerate(self.queue)
                if song["status"] == Status.pending
            ),
            None,
        )
    
    def get_current_playing_index(self):
        return next(
            (
                index
                for index, song in enumerate(self.queue)
                if song["status"] == Status.playing
            ),
            None,
        )
    
    async def show_queue(self, ctx):
        if len(self.queue) == 0:
            await ctx.respond("Queue is empty.")
            return

        queue = "\n".join(
            [
                f"{index + 1}. {song['title']}"
                for index, song in enumerate(self.queue)
            ]
        )

        await ctx.respond(f"Queue:\n{queue}")
    
    async def skip(self, ctx):
        await ctx.response.defer()
        if ctx.voice_client is None:
            await ctx.respond("I'm not in a voice channel.")
            return

        if not ctx.voice_client.is_playing():
            await ctx.respond("I'm not playing anything.")
            return
        
        current_playing = self.get_current_playing_index()

        await ctx.respond(f"Skipping - 🎵 {self.queue[current_playing]['title']} 🎵")

        ctx.voice_client.stop()



    async def connect_to_voice(self, ctx):
        if ctx.author.voice is None:
            await ctx.respond("Join a voice channel to use this command.")
            return None
        voice = ctx.voice_client
        if voice is None:
            voice = await ctx.author.voice.channel.connect()
        return voice

    async def queue_loop(self, ctx):
        next_pending = self.get_next_pending_index()

        # if nothing is pending, return
        if next_pending == None:
            return

        voice = await self.connect_to_voice(ctx)

        if voice is None:
            return

        # am i still playing?
        if ctx.voice_client.is_playing():
            return

        # if not, play the next pending song
        self.queue[next_pending]["status"] = Status.playing

        await ctx.respond(f"Playing - 🎵 {self.queue[next_pending]['title']} 🎵")

        args = {"source": self.queue[next_pending]["video_url"]}

        if "options" in self.queue[next_pending]:
            args["options"] = self.queue[next_pending]["options"]

        audio_source = discord.FFmpegPCMAudio(**args)

        await voice.play(audio_source, wait_finish=True)

        self.queue[next_pending]["status"] = Status.played

        if self.get_next_pending_index() is None:
            await voice.disconnect()
            return

        await self.queue_loop(ctx)

    async def play_next(
        self, ctx: discord.ApplicationContext, search: str, options=None
    ):
        await ctx.response.defer()

        url, title = await youtube.fetch_video_url_and_title(search)

        if url is None:
            await ctx.respond("No video found.")
            return

        self.add_to_queue(title, url, options)

        if (len(self.queue) > 1) and (self.queue[0]["status"] == Status.playing):
            await ctx.respond(f"Added to queue - 🎵 {title} 🎵")
            return

        await self.queue_loop(ctx)

        return None
